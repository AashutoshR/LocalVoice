"""Queue the compact model's stronger adaptation without concurrent GPU jobs."""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, experiment_config, write_json


def run():
    state = dict(status="queued", experiment="E11", action="waiting for E10",
                 project=experiment_config("E11"), pid=os.getpid(),
                 started_at=datetime.now(timezone.utc).isoformat(), steps=[])
    path = ROOT / "runs/refinement.json"
    write_json(path, state)
    try:
        while json.loads((ROOT / "runs/adaptation.json").read_text(encoding="utf-8"))["status"] == "running":
            time.sleep(10)
        state["status"] = "running"
        for action in ("train", "evaluate"):
            state["action"] = action
            write_json(path, state)
            command = [sys.executable, "-u", "-m", "localvoice.cli", action, "E11"]
            if action == "train":
                command += ["--config", "configs/tiny-acoustic.json"]
            with (ROOT / "runs" / f"E11-{action}.log").open("w", encoding="utf-8") as log:
                result = subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
            state["steps"].append(dict(action=action, exit_code=result.returncode))
            if result.returncode:
                raise RuntimeError(f"E11 {action} failed; inspect its log")
        from .diagnostics import compare_predictions
        compare_predictions("E11", baseline_id="E0")
        from .weight_audit import audit
        audit("E11", "E9")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
