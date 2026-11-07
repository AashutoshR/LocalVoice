"""Sequential real experiment execution, isolated processes and durable progress."""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from .core import ROOT, config, write_json


def run_matrix():
    path = ROOT / "runs/matrix.json"
    steps = [("E0", "evaluate"), ("E2", "train"), ("E2", "evaluate"),
             ("E1", "train"), ("E1", "evaluate"), ("E4", "train"),
             ("E4", "evaluate"), ("E3", "train"), ("E3", "evaluate")]
    state = {"status": "running", "project": config(), "pid": os.getpid(), "started_at": datetime.now(timezone.utc).isoformat(), "steps": []}
    write_json(path, state)
    env = {**os.environ, "PYTHONUTF8": "1", "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4"}
    try:
        for experiment, action in steps:
            folder = ROOT / "runs" / experiment
            if action == "evaluate" and (folder / "metrics-validation.json").exists():
                continue
            if action == "train" and (folder / "training.json").exists():
                existing = json.loads((folder / "training.json").read_text(encoding="utf-8"))
                if existing.get("status") == "completed":
                    continue
                raise RuntimeError(f"{experiment} has an unfinished prior run. Inspect and archive it before retrying.")
            state.update(experiment=experiment, action=action)
            write_json(path, state)
            log = ROOT / "runs" / f"{experiment}-{action}.log"
            with log.open("w", encoding="utf-8") as output:
                result = subprocess.run([sys.executable, "-m", "localvoice.cli", action, experiment], cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT)
            state["steps"].append({"experiment": experiment, "action": action, "exit_code": result.returncode})
            if result.returncode:
                raise RuntimeError(f"{experiment} {action} failed. See {log.name}.")
        state["status"] = "completed"
    except BaseException as exc:
        state["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        state["error"] = str(exc)
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run_matrix()
