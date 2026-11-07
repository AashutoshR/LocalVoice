"""Freeze the decoder-LoRA result, then check the known MLS sample diagnostically."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, experiment_config, experiments, write_json
from .reporting import compatible_metrics


def run():
    path = ROOT / "runs/regularized-round.json"
    state = dict(status="queued", experiment="E16", action="waiting for LoRA training",
                 project=experiment_config("E16"), pid=os.getpid(),
                 started_at=datetime.now(timezone.utc).isoformat())
    write_json(path, state)
    try:
        while True:
            current = json.loads((ROOT / "runs/current-training.json").read_text(encoding="utf-8"))
            if current["experiment"] != "E16" or current["status"] in {"failed", "interrupted"}:
                raise ValueError("Resolve the expected LoRA training stage before testing")
            if current["status"] == "completed":
                break
            time.sleep(10)
        runs = {r["id"]: r for r in experiments()}
        candidates = [runs[i] for i in ("E8", "E10", "E15", "E16")]
        if any(not compatible_metrics(r["metrics"], runs["E7"]["metrics"]) for r in candidates):
            raise ValueError("Validation comparisons must match the Small baseline")
        chosen = min(candidates, key=lambda r: r["metrics"]["wer"])
        files = {}
        for checkpoint_file in (ROOT / "runs/E16/checkpoint").iterdir():
            if checkpoint_file.is_file():
                with checkpoint_file.open("rb") as stream:
                    files[checkpoint_file.name] = hashlib.file_digest(stream, "sha256").hexdigest()
        selection = dict(selected_experiments=[chosen["id"]], selected_experiment=chosen["id"],
            validation_wer=chosen["metrics"]["wer"], project=experiment_config(chosen["id"]),
            candidates={r["id"]: r["metrics"]["wer"] for r in candidates},
            checkpoint_files={"E16": files}, checkpoint_sha256={}, evaluation_order=["E16"],
            independent_sample=json.loads((ROOT / "data/independent-mls/sample.json").read_text(encoding="utf-8"))["dataset_fingerprint"],
            frozen_at=datetime.now(timezone.utc).isoformat(),
            policy="Validation-only selection. The known MLS sample is reused only as an exploratory diagnostic; no tuning follows its score in this round.")
        selection_file = "runs/selection-regularized.json"
        if (ROOT / selection_file).exists():
            raise FileExistsError("Preserve the original frozen selection")
        write_json(ROOT / selection_file, selection)
        state.update(status="running", action="reused MLS diagnostic")
        write_json(path, state)
        with (ROOT / "runs/E16-reused-mls.log").open("w", encoding="utf-8") as log:
            result = subprocess.run([sys.executable, "-u", "-m", "localvoice.independent", "evaluate", "E16",
                "--selection", selection_file], cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError("LoRA reused-MLS diagnostic failed; inspect its log")
        from .diagnostics import compare_predictions
        compare_predictions("E16", baseline_id="E10", primary=False)
        compare_predictions("E16", split="mls-test", baseline_id="E7", cluster_field="speaker_id")
        compare_predictions("E16", split="mls-test", baseline_id="E10", cluster_field="speaker_id", primary=False)
        from .reporting import write_results
        write_results()
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
