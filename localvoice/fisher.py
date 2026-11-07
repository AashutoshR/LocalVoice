"""Estimate and verify a diagonal empirical Fisher from training speech only."""
import hashlib
import json
from pathlib import Path
from .core import ROOT, dataset_fingerprint, experiment_config, read_manifest, write_json


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_verified_fisher(hp, cfg, fingerprint, ancestry):
    from safetensors.torch import load_file
    path = ROOT / hp["ewc_fisher"]
    metadata = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    if metadata["project"] != cfg or metadata["dataset_fingerprint"] != fingerprint:
        raise ValueError("Fisher model or dataset identity differs")
    if metadata["anchor_experiment"] != ancestry.get("initial_experiment") or metadata["anchor_sha256"] != ancestry.get("initial_weights_sha256"):
        raise ValueError("Fisher anchor differs from initial checkpoint")
    if metadata["split"] != "train" or metadata["fisher_sha256"] != digest(path):
        raise ValueError("Fisher provenance or contents changed")
    train = [r for r in read_manifest() if r["split"] == "train"]
    by_path = {r["audio_path"]: r for r in train}
    selected = metadata["training_audio_paths"]
    if not selected or len(selected) != len(set(selected)) or any(p not in by_path for p in selected):
        raise ValueError("Fisher samples must be unique members of the training split")
    if dataset_fingerprint([by_path[p] for p in selected]) != metadata["sample_fingerprint"]:
        raise ValueError("Fisher training sample changed")
    return load_file(str(path), device="cpu"), {**metadata, "lambda": hp["ewc_lambda"],
        "normalization": "global unit trace", "anchor": ancestry["initial_experiment"]}


def prepare(count=128, seed=42):
    import gc
    import time
    import numpy as np
    import torch
    from safetensors.torch import save_file
    from .inference import load_model
    from .training import checked_rows, training_targets
    from .audio import decode_audio
    folder = ROOT / "runs/fisher-E11"
    path = folder / "fisher.safetensors"
    if path.exists() or path.with_suffix(".json").exists():
        raise FileExistsError("Preserve the original Fisher estimate")
    rows, audit = checked_rows()
    train = [r for r in rows if r["split"] == "train"]
    if not 0 < count <= len(train):
        raise ValueError("Invalid Fisher sample size")
    selected = [train[int(i)] for i in np.random.default_rng(seed).choice(len(train), count, replace=False)]
    targets = training_targets(selected, "punctuated")
    processor, model, device = load_model("E11")
    model.config.apply_spec_augment = False
    model.config.use_cache = False
    model.eval()
    parameters = {n:p for n,p in model.named_parameters() if p.requires_grad}
    fisher = {n:torch.zeros_like(p, dtype=torch.float32) for n,p in parameters.items()}
    started = time.perf_counter()
    folder.mkdir(parents=True, exist_ok=True)
    for index, row in enumerate(selected):
        inputs = processor(decode_audio(row["audio_path"]), sampling_rate=16000, return_tensors="pt")
        labels = processor.tokenizer(targets[row["audio_path"]], return_tensors="pt").input_ids.to(device)
        if labels[0,0] == model.config.decoder_start_token_id:
            labels = labels[:,1:]
        model.zero_grad(set_to_none=True)
        output = model(input_features=inputs.input_features.to(device), labels=labels, use_cache=False)
        if not torch.isfinite(output.loss):
            raise ValueError("Nonfinite Fisher example loss")
        output.loss.backward()
        for name, parameter in parameters.items():
            if parameter.grad is not None:
                fisher[name].add_(parameter.grad.detach().float().square() / count)
        if (index + 1) % 16 == 0:
            write_json(folder / "progress.json", dict(phase="training-only Fisher", samples_done=index+1,
                samples_total=count, elapsed_seconds=time.perf_counter()-started))
    if any(not torch.isfinite(f).all() for f in fisher.values()):
        raise ValueError("Nonfinite Fisher estimate")
    tensors = {n:f.cpu().contiguous() for n,f in fisher.items()}
    save_file(tensors, str(path))
    metadata = dict(anchor_experiment="E11", project=experiment_config("E11"), split="train", samples=count,
        seed=seed, training_audio_paths=[r["audio_path"] for r in selected], sample_fingerprint=dataset_fingerprint(selected),
        dataset_fingerprint=dataset_fingerprint(rows), anchor_sha256=digest(ROOT / "runs/E11/checkpoint/model.safetensors"),
        fisher_sha256=digest(path), method="mean squared per-utterance gradient of token-mean supervised cross-entropy; diagonal empirical Fisher",
        seconds=time.perf_counter()-started, evaluation_data_used=False)
    write_json(path.with_suffix(".json"), metadata)
    model.cpu()
    del model, parameters, fisher, tensors, output
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return metadata


if __name__ == "__main__":
    prepare()
