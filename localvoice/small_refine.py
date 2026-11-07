"""Higher-rate fine-tuning of the existing Small decoder, after Tiny jobs finish."""
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
    path = ROOT / "runs/small-final.json"
    state = dict(status="queued", experiment="E15", action="waiting for Tiny follow-up",
                 project=experiment_config("E15"), pid=os.getpid(),
                 started_at=datetime.now(timezone.utc).isoformat())
    write_json(path, state)
    try:
        while True:
            previous = json.loads((ROOT / "runs/followup.json").read_text(encoding="utf-8"))
            if previous["status"] == "completed":
                break
            if previous["status"] in {"failed", "interrupted"}:
                raise ValueError("Resolve the Tiny workflow before starting Small")
            time.sleep(10)
        state.update(status="running", action="decoder refinement")
        write_json(path, state)
        from .train_stage import run as train_stage
        train_stage("E15", "configs/small-refinement.json")
        runs = experiments()
        baseline = next(r for r in runs if r["id"] == "E7")
        candidates = [r for r in runs if r["id"] in {"E8", "E10", "E15"} and
                      compatible_metrics(r["metrics"], baseline["metrics"])]
        if len(candidates) != 3:
            raise ValueError("Every planned Small candidate must complete compatible validation")
        chosen = min(candidates, key=lambda r: r["metrics"]["wer"])
        checkpoint = ROOT / "runs" / chosen["id"] / "checkpoint/model.safetensors"
        with checkpoint.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        selection = dict(selected_experiment=chosen["id"], validation_wer=chosen["metrics"]["wer"],
                         candidates={r["id"]: r["metrics"]["wer"] for r in candidates},
                         checkpoint_sha256=digest, project=experiment_config(chosen["id"]),
                         frozen_at=datetime.now(timezone.utc).isoformat(),
                         policy="Validation-only selection. The original FLEURS test was already read in earlier rounds; this is a reused-test diagnostic, not a new blind study.")
        selection_path = ROOT / "runs/selection-small-refined.json"
        if selection_path.exists():
            raise FileExistsError("Preserve the frozen Small selection")
        write_json(selection_path, selection)
        if not (ROOT / "runs" / chosen["id"] / "metrics-test.json").exists():
            state.update(experiment=chosen["id"], action="reused FLEURS test diagnostic")
            write_json(path, state)
            with (ROOT / "runs" / f"{chosen['id']}-test-diagnostic.log").open("w", encoding="utf-8") as log:
                result = subprocess.run([sys.executable, "-u", "-m", "localvoice.cli", "evaluate", chosen["id"],
                                         "--split", "test", "--final-test"], cwd=ROOT,
                                        env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError("Small reused-test diagnostic failed")
        from .diagnostics import compare_predictions
        compare_predictions(chosen["id"], split="test", baseline_id="E7")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
