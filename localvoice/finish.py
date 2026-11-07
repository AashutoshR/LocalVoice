"""Complete frozen Small and corrected Tiny test comparisons sequentially."""
import os
from datetime import datetime, timezone
from .core import ROOT, experiment_config, write_json
from .finalize import run as finalize


def run():
    path = ROOT / "runs/finish.json"
    state = {"status": "running", "pid": os.getpid(), "project": experiment_config("E7"),
             "started_at": datetime.now(timezone.utc).isoformat(),
             "experiment": "E8", "action": "training, validation, then frozen test comparison"}
    write_json(path, state)
    try:
        finalize(wait=True, baseline_id="E7")
        state.update(experiment="E9", action="corrected Tiny held-out test comparison")
        write_json(path, state)
        finalize(baseline_id="E0", tag="aligned-tiny")
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
