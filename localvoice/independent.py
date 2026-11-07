"""Frozen, independent Spanish MLS sample. Never used for training or selection."""
import argparse
import csv
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from .core import ROOT, dataset_fingerprint, experiment_config, normalize, read_manifest, write_json

REVISION = "2e83e61823b4c47dcbcb1980bb88601274127609"
FOLDER = ROOT / "data/independent-mls"


def prepare():
    import pyarrow.parquet as pq
    import soundfile as sf
    from .audio import decode_audio
    manifest = FOLDER / "manifest.csv"
    if (FOLDER / "sample.json").exists():
        raise FileExistsError("Independent sample is already frozen; do not resample it")
    source = FOLDER / "source/spanish/test-00000-of-00001.parquet"
    table = pq.read_table(source)
    records = table.to_pylist()
    eligible = sorted((r for r in records if normalize(r["transcript"]) and
                       0 < r["audio_duration"] <= 30), key=lambda r: r["id"])
    chosen = sorted(random.Random(42).sample(eligible, 300), key=lambda r: r["id"])
    audio_dir = FOLDER / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in chosen:
        audio = decode_audio(item["audio"]["bytes"])
        path = audio_dir / f'{item["id"]}.wav'
        sf.write(path, audio, 16000, subtype="PCM_16")
        rows.append(dict(id=item["id"], audio_path=str(path.resolve()),
                         transcript=item["transcript"], speaker_id=item["speaker_id"],
                         split="test", duration_seconds=len(audio) / 16000, condition="audiobook"))
    with manifest.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    frozen = dict(dataset="facebook/multilingual_librispeech", revision=REVISION,
                  language="spanish", source_split="test", source_rows=len(records),
                  eligible_rows=len(eligible), samples=len(rows), seed=42,
                  sampling="uniform sample without replacement from ID-sorted eligible test clips",
                  exclusions="empty normalized reference or duration outside (0, 30] seconds only",
                  source_sha256=hashlib.file_digest(source.open("rb"), "sha256").hexdigest(),
                  dataset_fingerprint=dataset_fingerprint(read_manifest(manifest)),
                  selected_ids=[r["id"] for r in rows], speakers=sorted({r["speaker_id"] for r in rows}),
                  hours=sum(r["duration_seconds"] for r in rows) / 3600,
                  license="CC-BY-4.0", frozen_at=datetime.now(timezone.utc).isoformat(),
                  policy="No training, checkpoint selection, or hyperparameter tuning on this sample. Pretraining overlap is unknown.")
    write_json(FOLDER / "sample.json", frozen)
    print(json.dumps({k: v for k, v in frozen.items() if k != "selected_ids"}, indent=2))


def evaluate(experiment, selection_file="runs/selection-acoustic.json"):
    import numpy as np
    from .inference import load_model
    from .training import evaluate_rows
    selection = json.loads((ROOT / selection_file).read_text(encoding="utf-8"))
    if experiment not in {"E0", "E7", "E8", "E9", *selection["selected_experiments"], *selection.get("evaluation_order", [])}:
        raise ValueError("Only the frozen candidate and its two prespecified controls may be evaluated")
    if experiment in selection.get("checkpoint_files", {}):
        for name, expected in selection["checkpoint_files"][experiment].items():
            if Path(name).name != name:
                raise ValueError("Invalid frozen checkpoint filename")
            with (ROOT / "runs" / experiment / "checkpoint" / name).open("rb") as stream:
                if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
                    raise ValueError("Checkpoint changed after the diagnostic was frozen")
    elif experiment in selection.get("checkpoint_sha256", {}):
        weights = ROOT / "runs" / experiment / "checkpoint/model.safetensors"
        with weights.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != selection["checkpoint_sha256"][experiment]:
                raise ValueError("Checkpoint changed after independent selection was frozen")
    sample = json.loads((FOLDER / "sample.json").read_text(encoding="utf-8"))
    rows = read_manifest(FOLDER / "manifest.csv")
    if dataset_fingerprint(rows) != sample["dataset_fingerprint"]:
        raise ValueError("Independent holdout changed after freezing")
    if selection.get("independent_sample", sample["dataset_fingerprint"]) != sample["dataset_fingerprint"]:
        raise ValueError("Selection identifies a different diagnostic sample")
    folder = ROOT / "runs" / experiment
    if (folder / "metrics-mls-test.json").exists():
        raise FileExistsError("Independent test results already exist; preserve the first evaluation")
    cfg = experiment_config(experiment)
    processor, model, device = load_model(experiment)
    evaluate_rows(model, processor, rows[:1], device)
    metrics, predictions = evaluate_rows(model, processor, rows, device,
        progress_path=folder / "independent-progress.json",
        context={"split": "mls-test", "evaluation_batch_size": 4})
    metrics.update(split="mls-test", dataset=sample["dataset"], dataset_revision=REVISION,
                   dataset_fingerprint=sample["dataset_fingerprint"], language="spanish",
                   model=cfg["model"], model_revision=cfg["model_revision"],
                   normalization=cfg["normalization"], device=device,
                   evaluation_protocol=dict(batch_size=4, precision="float32", num_beams=1, max_new_tokens=225),
                   generation_config_sha256=getattr(model, "_localvoice_generation_sha256", None),
                   mean_latency_seconds=float(np.mean([r["latency_seconds"] for r in predictions])),
                   selection_file=selection_file,
                   evaluated_at=datetime.now(timezone.utc).isoformat())
    if selection_file != "runs/selection-acoustic.json":
        metrics["evaluation_context"] = "Reused MLS test corpus; earlier project scores were already read. Exploratory diagnostic after frozen validation selection, not a new blind evaluation."
    write_json(folder / "predictions-mls-test.json", predictions)
    write_json(folder / "metrics-mls-test.json", metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "evaluate"])
    parser.add_argument("experiment", nargs="?")
    parser.add_argument("--selection", default="runs/selection-acoustic.json")
    args = parser.parse_args()
    prepare() if args.action == "prepare" else evaluate(args.experiment, args.selection)
