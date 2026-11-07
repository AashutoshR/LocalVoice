r"""Opt-in integration smoke: real pretrained weights, isolated three-clip fixture.

This tests full and LoRA updates, augmentation, save/reload, and evaluation.
It is an engineering check and never writes research results into runs/.
Run after dataset preparation: .venv\Scripts\python scripts/verify_ml.py
"""
import csv
import json
import tempfile
from pathlib import Path
import torch
from localvoice import core, training, inference


def main():
    settings = core.config()
    original_rows = core.read_manifest()
    clips = [r for r in original_rows if r["split"] == "train"][:3]
    if len(clips) < 3:
        raise ValueError("Prepare at least three training clips first.")
    with tempfile.TemporaryDirectory(prefix="localvoice-smoke-") as temporary:
        root = Path(temporary).resolve()
        core.ROOT = training.ROOT = inference.ROOT = root
        cfg = {**settings, "manifest": "manifest.csv"}
        core.config = training.config = inference.config = lambda: cfg
        fields = ["audio_path", "transcript", "speaker_id", "split", "duration_seconds"]
        with (root / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fields, extrasaction="ignore")
            writer.writeheader()
            for row, split in zip(clips, ["train", "validation", "test"]):
                writer.writerow({**row, "split": split, "speaker_id": ""})
        hp = json.loads((Path(__file__).resolve().parent.parent / "configs/training.json").read_text())
        hp.update({"epochs": 1, "batch_size": 1, "gradient_accumulation_steps": 1})
        core.write_json(root / "smoke-settings.json", hp)
        for experiment in ("E1", "E4"):
            print(f"INTEGRATION SMOKE {experiment}", flush=True)
            training.train(experiment, root / "smoke-settings.json")
            training.evaluate(experiment)
            inference._loaded = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        print("PASS: full and augmented LoRA training, checkpoint reload, and validation evaluation. Smoke artifacts isolated from research runs.", flush=True)


if __name__ == "__main__":
    main()
