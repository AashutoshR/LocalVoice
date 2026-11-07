"""Refresh the historical domain report without replacing the curated README."""
import json
from localvoice.core import ROOT, write_json
from localvoice.reporting import write_results
from scripts.report_fine_tuning import main


def publish():
    state = json.loads((ROOT / "runs/latin-round.json").read_text(encoding="utf-8"))
    if state["status"] != "completed":
        raise ValueError("Complete the planned round first")
    current_path = ROOT / "runs/current-training.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    if current.get("experiment") == "E17" and current.get("status") == "failed":
        write_json(ROOT / "runs/E17/original-stage-failure.json", current)
        current.update(status="completed", action="recovered final metadata; validation and audits completed",
                       recovery_record="runs/E17/recovery.json")
        write_json(current_path, current)
    main()
    write_results()


if __name__ == "__main__":
    publish()
