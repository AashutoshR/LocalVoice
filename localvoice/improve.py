"""Run follow-up experiments without replacing the original comparison series."""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, config, write_json


def run():
    path = ROOT / "runs/improvement.json"
    state = {"status": "running", "project": config(), "pid": os.getpid(),
             "started_at": datetime.now(timezone.utc).isoformat(), "steps": [],
             "selection_split": "validation", "target_wer": 19.0}
    env = {**os.environ, "PYTHONUTF8": "1"}

    def stage(experiment, action, settings=None):
        state.update(experiment=experiment, action=action)
        write_json(path, state)
        folder = ROOT / "runs" / experiment
        if action == "evaluate" and (folder / "metrics-validation.json").exists():
            state["steps"].append({"experiment": experiment, "action": action, "reused": True})
            return
        if action == "train" and (folder / "training.json").exists():
            previous = json.loads((folder / "training.json").read_text(encoding="utf-8"))
            expected = json.loads((ROOT / settings).read_text(encoding="utf-8"))
            if previous.get("status") == "completed" and previous.get("project") == config() and previous.get("hyperparameters") == expected:
                state["steps"].append({"experiment": experiment, "action": action, "reused": True})
                return
            raise RuntimeError(f"{experiment} already exists with unfinished or different settings; inspect it first")
        command = [sys.executable, "-u", "-m", "localvoice.cli", action, experiment]
        if settings:
            command += ["--config", settings]
        with (ROOT / "runs" / f"{experiment}-{action}-followup.log").open("w", encoding="utf-8") as log:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
        state["steps"].append({"experiment": experiment, "action": action, "exit_code": result.returncode})
        if result.returncode:
            raise RuntimeError(f"{experiment} {action} failed; inspect its followup log")

    try:
        # E5 was launched interactively; observe its durable status without
        # starting another process or touching its checkpoint while it trains.
        state.update(experiment="E5", action="train")
        write_json(path, state)
        deadline = time.monotonic() + 7200
        while True:
            training_path = ROOT / "runs/E5/training.json"
            training = json.loads(training_path.read_text(encoding="utf-8")) if training_path.exists() else {}
            if training.get("status") == "completed":
                break
            if training.get("status") in {"failed", "interrupted"}:
                raise RuntimeError("E5 did not complete; inspect its training record")
            if time.monotonic() > deadline:
                raise TimeoutError("E5 exceeded two-hour observation window")
            time.sleep(2)
        stage("E5", "evaluate")
        from .diagnostics import compare_predictions
        compare_predictions("E5")
        metrics = json.loads((ROOT / "runs/E5/metrics-validation.json").read_text(encoding="utf-8"))
        if metrics["wer"] > state["target_wer"]:
            stage("E6", "train", "configs/stable-lora.json")
            stage("E6", "evaluate")
            compare_predictions("E6")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
