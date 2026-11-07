"""Matched Whisper Small baseline and decoder adaptation, validation only."""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from .core import ROOT, experiment_config, write_json


def run():
    path = ROOT / "runs/accuracy.json"
    state = {"status": "running", "pid": os.getpid(), "project": experiment_config("E7"),
             "started_at": datetime.now(timezone.utc).isoformat(), "steps": []}
    try:
        for experiment, action in [("E7", "evaluate"), ("E9", "train"), ("E9", "evaluate"), ("E8", "train"), ("E8", "evaluate")]:
            folder = ROOT / "runs" / experiment
            if action == "evaluate" and (folder / "metrics-validation.json").exists():
                continue
            if action == "train" and (folder / "training.json").exists():
                previous = json.loads((folder / "training.json").read_text(encoding="utf-8"))
                if previous.get("status") == "completed":
                    continue
                raise RuntimeError(f"{experiment} already has an unfinished run; inspect before retrying")
            state.update(experiment=experiment, action=action)
            write_json(path, state)
            command = [sys.executable, "-u", "-m", "localvoice.cli", action, experiment]
            if action == "train":
                command += ["--config", "configs/conservative.json" if experiment == "E9" else "configs/small-decoder.json"]
            with (ROOT / "runs" / f"{experiment}-{action}.log").open("w", encoding="utf-8") as output:
                result = subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"},
                                        stdout=output, stderr=subprocess.STDOUT)
            state["steps"].append({"experiment": experiment, "action": action, "exit_code": result.returncode})
            if result.returncode:
                raise RuntimeError(f"{experiment} {action} failed; inspect its log")
        from .diagnostics import compare_predictions
        compare_predictions("E9")
        compare_predictions("E8", baseline_id="E7")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
