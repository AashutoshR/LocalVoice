"""Exploratory follow-up on new MLS dev clips after the earlier test was read."""
import argparse
import csv
import hashlib
import json
import os
import random
import time
from datetime import datetime, timezone
from .core import ROOT, dataset_fingerprint, experiment_config, normalize, read_manifest, write_json
from .independent import REVISION

FOLDER = ROOT / "data/spanish-mls-dev"


def prepare():
    import pyarrow.parquet as pq
    import soundfile as sf
    from huggingface_hub import HfApi
    from .audio import decode_audio
    from .prepare import download_shard
    if (FOLDER / "sample.json").exists():
        raise FileExistsError("Follow-up sample already frozen")
    name = "spanish/dev-00000-of-00001.parquet"
    meta = next(s for s in HfApi().dataset_info("facebook/multilingual_librispeech", revision=REVISION,
                files_metadata=True).siblings if s.rfilename == name)
    FOLDER.mkdir(parents=True, exist_ok=True)
    source = FOLDER / "source.parquet"
    if not source.exists():
        download_shard(f"https://huggingface.co/datasets/facebook/multilingual_librispeech/resolve/{REVISION}/{name}", source, meta.size)
    with source.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != meta.lfs.sha256:
        raise ValueError("Follow-up source checksum mismatch")
    records = pq.read_table(source).to_pylist()
    eligible = sorted((r for r in records if normalize(r["transcript"]) and 0 < r["audio_duration"] <= 30), key=lambda r: r["id"])
    chosen = sorted(random.Random(43).sample(eligible, 300), key=lambda r: r["id"])
    (FOLDER / "audio").mkdir(exist_ok=True)
    rows = []
    for item in chosen:
        wave = decode_audio(item["audio"]["bytes"])
        output = FOLDER / "audio" / f'{item["id"]}.wav'
        sf.write(output, wave, 16000, subtype="PCM_16")
        rows.append(dict(id=item["id"], audio_path=str(output.resolve()), transcript=item["transcript"],
                         speaker_id=item["speaker_id"], split="test", duration_seconds=len(wave) / 16000))
    with (FOLDER / "manifest.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_json(FOLDER / "sample.json", dict(dataset="facebook/multilingual_librispeech", revision=REVISION,
        source_split="dev", source_sha256=digest, samples=len(rows), seed=43,
        eligible_rows=len(eligible), selected_ids=[r["id"] for r in rows],
        dataset_fingerprint=dataset_fingerprint(read_manifest(FOLDER / "manifest.csv")), speakers=sorted({r["speaker_id"] for r in rows}),
        frozen_at=datetime.now(timezone.utc).isoformat(),
        interpretation="New held-out clips; exploratory follow-up because the earlier MLS test informed the domain choice. No further tuning after these scores."))


def evaluate_one(experiment, selection):
    if experiment not in selection["evaluation_order"]:
        raise ValueError("Experiment is not in the frozen follow-up comparison")
    import numpy as np
    from .inference import load_model
    from .training import evaluate_rows
    folder = ROOT / "runs" / experiment
    if (folder / "metrics-mls-dev.json").exists():
        raise FileExistsError("Preserve the first follow-up result")
    rows = read_manifest(FOLDER / "manifest.csv")
    sample = json.loads((FOLDER / "sample.json").read_text(encoding="utf-8"))
    if dataset_fingerprint(rows) != sample["dataset_fingerprint"]:
        raise ValueError("Follow-up sample changed")
    if experiment in selection["checkpoint_sha256"]:
        with (folder / "checkpoint/model.safetensors").open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != selection["checkpoint_sha256"][experiment]:
                raise ValueError("Frozen checkpoint changed")
    processor, model, device = load_model(experiment)
    evaluate_rows(model, processor, rows[:1], device)
    metrics, predictions = evaluate_rows(model, processor, rows, device,
        progress_path=folder / "followup-progress.json", context=dict(split="mls-dev", evaluation_batch_size=4))
    cfg = experiment_config(experiment)
    metrics.update(split="mls-dev", dataset=sample["dataset"], dataset_revision=REVISION,
        dataset_fingerprint=sample["dataset_fingerprint"], model=cfg["model"], model_revision=cfg["model_revision"],
        language="spanish", normalization=cfg["normalization"],
        evaluation_protocol=dict(batch_size=4, precision="float32", num_beams=1, max_new_tokens=225),
        generation_config_sha256=getattr(model, "_localvoice_generation_sha256", None),
        mean_latency_seconds=float(np.mean([r["latency_seconds"] for r in predictions])),
        interpretation=sample["interpretation"], evaluated_at=datetime.now(timezone.utc).isoformat())
    write_json(folder / "metrics-mls-dev.json", metrics)
    write_json(folder / "predictions-mls-dev.json", predictions)


def run():
    path = ROOT / "runs/followup.json"
    state = dict(status="queued", experiment="E14", action="waiting for training", pid=os.getpid(),
                 started_at=datetime.now(timezone.utc).isoformat())
    write_json(path, state)
    try:
        while True:
            current = json.loads((ROOT / "runs/current-training.json").read_text(encoding="utf-8"))
            if current["experiment"] == "E14" and current["status"] == "completed":
                break
            if current["status"] in {"failed", "interrupted"}:
                raise ValueError("Resolve failed training first")
            time.sleep(10)
        rows = read_manifest(ROOT / "data/additional-spanish/manifest.csv")
        sample = json.loads((FOLDER / "sample.json").read_text(encoding="utf-8"))
        if set(sample["speakers"]) & {r["speaker_id"] for r in rows}:
            raise ValueError("Follow-up speakers overlap additional training speakers")
        selection = dict(evaluation_order=["E0", "E11", "E13", "E14"], checkpoint_sha256={}, validation_wer={},
                         frozen_at=datetime.now(timezone.utc).isoformat(), policy="No tuning on follow-up scores")
        for experiment in ("E11", "E13", "E14"):
            folder = ROOT / "runs" / experiment
            with (folder / "checkpoint/model.safetensors").open("rb") as stream:
                selection["checkpoint_sha256"][experiment] = hashlib.file_digest(stream, "sha256").hexdigest()
            selection["validation_wer"][experiment] = json.loads((folder / "metrics.json").read_text(encoding="utf-8"))["wer"]
        selection["selected_experiment"] = min(selection["validation_wer"], key=selection["validation_wer"].get)
        if (ROOT / "runs/selection-diverse.json").exists():
            raise FileExistsError("Selection already frozen")
        write_json(ROOT / "runs/selection-diverse.json", selection)
        chosen = selection["selected_experiment"]
        write_json(ROOT / "runs/selection-tiny-final.json", dict(selected_experiment=chosen,
            validation_wer=selection["validation_wer"][chosen], project=experiment_config(chosen),
            frozen_at=selection["frozen_at"], source_selection="runs/selection-diverse.json"))
        import subprocess
        import sys
        for experiment in selection["evaluation_order"]:
            state.update(status="running", experiment=experiment, action="new MLS dev clips")
            write_json(path, state)
            with (ROOT / "runs" / f"{experiment}-followup.log").open("w", encoding="utf-8") as log:
                result = subprocess.run([sys.executable, "-u", "-m", "localvoice.followup", "evaluate", experiment],
                    cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env={**os.environ, "PYTHONUTF8": "1"})
            if result.returncode:
                raise RuntimeError(f"Follow-up evaluation failed for {experiment}")
        from .diagnostics import compare_predictions
        for experiment in ("E11", "E13", "E14"):
            compare_predictions(experiment, split="mls-dev", baseline_id="E0", cluster_field="speaker_id")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run", "evaluate"])
    parser.add_argument("experiment", nargs="?")
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    elif args.action == "evaluate":
        evaluate_one(args.experiment, json.loads((ROOT / "runs/selection-diverse.json").read_text(encoding="utf-8")))
    else:
        run()
