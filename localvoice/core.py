"""Shared data contracts and evaluation. No model imports required by the UI."""
import csv
import hashlib
import json
import math
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = [
    {"id": "E0", "name": "Pretrained baseline", "strategy": "baseline", "augmentation": False},
    {"id": "E1", "name": "Full fine-tuning", "strategy": "full", "augmentation": False},
    {"id": "E2", "name": "LoRA fine-tuning", "strategy": "lora", "augmentation": False},
    {"id": "E3", "name": "Full + augmentation", "strategy": "full", "augmentation": True},
    {"id": "E4", "name": "LoRA + augmentation", "strategy": "lora", "augmentation": True},
    {"id": "E5", "name": "Conservative full tuning", "strategy": "full", "augmentation": False},
    {"id": "E6", "name": "Stable LoRA tuning", "strategy": "lora", "augmentation": False},
    {"id": "E7", "name": "Whisper Small pretrained", "strategy": "baseline", "augmentation": False, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E8", "name": "Whisper Small decoder tuning", "strategy": "decoder", "augmentation": False, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E9", "name": "Prompt-aligned Tiny tuning", "strategy": "full", "augmentation": False, "baseline_id": "E0"},
    {"id": "E10", "name": "Small encoder + decoder adaptation", "strategy": "full", "augmentation": True, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E11", "name": "Tiny stronger acoustic adaptation", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E12", "name": "Tiny teacher-regularized fine-tuning", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E13", "name": "Tiny diverse-data fine-tuning", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E14", "name": "Tiny final domain refinement", "strategy": "full", "augmentation": False, "baseline_id": "E0"},
    {"id": "E15", "name": "Small higher-rate decoder refinement", "strategy": "decoder", "augmentation": False, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E16", "name": "Small regularized decoder LoRA", "strategy": "lora", "augmentation": False, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E17", "name": "Tiny Latin American replay tuning", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E18", "name": "Small matched full-tuning control", "strategy": "full", "augmentation": True, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E19", "name": "Small lower-six encoder blocks frozen", "strategy": "full", "augmentation": True, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E20", "name": "Small lower-nine encoder blocks frozen", "strategy": "full", "augmentation": True, "baseline_id": "E7", "model_config": "configs/whisper-small.json"},
    {"id": "E21", "name": "Tiny matched replay control", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E22", "name": "Tiny Fisher-protected replay", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
    {"id": "E23", "name": "Tiny stronger Fisher-protected replay", "strategy": "full", "augmentation": True, "baseline_id": "E0"},
]


def config():
    return json.loads((ROOT / "configs/project.json").read_text(encoding="utf-8"))


def experiment_config(experiment):
    spec = next(s for s in EXPERIMENTS if s["id"] == experiment)
    settings = config()
    if spec.get("model_config"):
        settings.update(json.loads((ROOT / spec["model_config"]).read_text(encoding="utf-8")))
    return settings


def normalize(text):
    text = unicodedata.normalize("NFC", text).lower()
    return " ".join("".join(" " if unicodedata.category(c).startswith("P") else c for c in text).split())


def score(references, hypotheses):
    from jiwer import process_words, cer
    refs, hyps = [normalize(t) for t in references], [normalize(t) for t in hypotheses]
    if not refs or len(refs) != len(hyps) or any(not r for r in refs):
        raise ValueError("Scoring needs equally sized lists and nonempty normalized references.")
    words = process_words(refs, hyps)
    common = {"substitutions": Counter(), "deletions": Counter(), "insertions": Counter()}
    for i, alignment in enumerate(words.alignments):
        for chunk in alignment:
            reference = " ".join(words.references[i][chunk.ref_start_idx:chunk.ref_end_idx])
            hypothesis = " ".join(words.hypotheses[i][chunk.hyp_start_idx:chunk.hyp_end_idx])
            if chunk.type == "substitute":
                common["substitutions"][f"{reference} → {hypothesis}"] += 1
            elif chunk.type == "delete":
                common["deletions"][reference] += 1
            elif chunk.type == "insert":
                common["insertions"][hypothesis] += 1
    return {"wer": words.wer * 100, "cer": cer(refs, hyps) * 100,
            "substitutions": words.substitutions, "deletions": words.deletions,
            "insertions": words.insertions, "reference_words": words.hits + words.substitutions + words.deletions,
            "samples": len(refs), "common_errors": {kind: [{"text": text, "count": count} for text, count in counter.most_common(10)] for kind, counter in common.items()}}


def read_manifest(path=None):
    path = Path(path or ROOT / config()["manifest"]).resolve()
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"audio_path", "transcript", "speaker_id", "split", "duration_seconds"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Manifest needs columns: {', '.join(sorted(required))}")
        rows = list(reader)
    for row in rows:
        p = Path(row["audio_path"])
        row["audio_path"] = str((path.parent / p).resolve() if not p.is_absolute() else p)
    return rows


def validate_manifest(path=None, inspect_audio=True, required_splits=("train", "validation", "test")):
    import soundfile as sf
    rows = read_manifest(path)
    errors, warnings, speakers, seen = [], [], {}, set()
    summary = {s: {"samples": 0, "hours": 0} for s in ("train", "validation", "test")}
    for index, row in enumerate(rows, 2):
        prefix = f"Row {index}"
        split = row["split"]
        if split not in summary:
            errors.append(f"{prefix}: invalid split {split}")
            continue
        if not normalize(row["transcript"]):
            errors.append(f"{prefix}: empty transcript")
        try:
            duration = float(row["duration_seconds"])
            if not math.isfinite(duration) or not 0 < duration <= 30:
                raise ValueError()
        except ValueError:
            errors.append(f"{prefix}: duration must be between 0 and 30 seconds")
            continue
        audio = Path(row["audio_path"])
        if not audio.is_file():
            errors.append(f"{prefix}: missing audio {audio.name}")
        elif inspect_audio:
            try:
                info = sf.info(audio)
                if info.channels != 1 or info.samplerate != 16000:
                    errors.append(f"{prefix}: audio must be mono 16 kHz")
                if abs(info.duration - duration) > 0.1:
                    errors.append(f"{prefix}: duration does not match audio")
                digest = hashlib.sha256(audio.read_bytes()).hexdigest()
                if digest in seen:
                    errors.append(f"{prefix}: duplicate audio content")
                seen.add(digest)
            except (RuntimeError, ValueError) as exc:
                errors.append(f"{prefix}: unreadable audio ({exc})")
        speaker = row["speaker_id"].strip()
        if speaker:
            speakers.setdefault(speaker, set()).add(split)
        summary[split]["samples"] += 1
        summary[split]["hours"] += duration / 3600
    for speaker, splits in speakers.items():
        if len(splits) > 1:
            errors.append(f"Speaker {speaker} occurs across splits: {', '.join(sorted(splits))}")
    if any(not r["speaker_id"].strip() for r in rows):
        warnings.append("Speaker IDs are missing: speaker independence cannot be verified.")
    for split in required_splits:
        if split not in summary:
            raise ValueError("Unknown required split")
        if not summary[split]["samples"]:
            errors.append(f"Missing {split} split")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "splits": summary, "samples": len(rows)}


def dataset_fingerprint(rows):
    # Includes audio content, labels, split membership, and grouping metadata.
    digest = hashlib.sha256()
    for row in rows:
        digest.update(json.dumps(row, sort_keys=True, ensure_ascii=False).encode())
        digest.update(Path(row["audio_path"]).read_bytes())
    return digest.hexdigest()


def experiments():
    result = []
    for spec in EXPERIMENTS:
        folder = ROOT / "runs" / spec["id"]
        metrics = None
        training = None
        if (folder / "metrics.json").exists():
            metrics = json.loads((folder / "metrics.json").read_text(encoding="utf-8"))
        if (folder / "training.json").exists():
            training = json.loads((folder / "training.json").read_text(encoding="utf-8"))
        checkpoint_ready = spec["strategy"] == "baseline" or (folder / "checkpoint/config.json").is_file() or (folder / "checkpoint/adapter_config.json").is_file()
        status = "evaluated" if metrics else "checkpoint ready" if checkpoint_ready else "planned"
        if training and training.get("status") in {"running", "failed", "interrupted"}:
            status = training["status"]
        history = json.loads((folder / "history.json").read_text(encoding="utf-8")) if (folder / "history.json").exists() else []
        progress = json.loads((folder / "progress.json").read_text(encoding="utf-8")) if (folder / "progress.json").exists() else None
        paired_path = folder / f"paired-{metrics.get('split', 'validation') if metrics else 'validation'}.json"
        paired = json.loads(paired_path.read_text(encoding="utf-8")) if paired_path.exists() else None
        test_path = folder / "metrics-test.json"
        test_metrics = json.loads(test_path.read_text(encoding="utf-8")) if test_path.exists() else None
        independent_path = folder / "metrics-mls-test.json"
        independent_metrics = json.loads(independent_path.read_text(encoding="utf-8")) if independent_path.exists() else None
        followup_path = folder / "metrics-mls-dev.json"
        followup_metrics = json.loads(followup_path.read_text(encoding="utf-8")) if followup_path.exists() else None
        latin_path = folder / "metrics-latin-holdout.json"
        latin_metrics = json.loads(latin_path.read_text(encoding="utf-8")) if latin_path.exists() else None
        weight_path = folder / "weight-audit.json"
        weight_audit = json.loads(weight_path.read_text(encoding="utf-8")) if weight_path.exists() else None
        adapter_path = folder / "adapter-audit.json"
        adapter_audit = json.loads(adapter_path.read_text(encoding="utf-8")) if adapter_path.exists() else None
        known_issues = (["Superseded training prompt: encoded labels omitted Spanish/task tokens; corrected in E9."]
                        if spec["id"] in {"E1", "E2", "E3", "E4", "E5", "E6"} and training
                        and not training.get("tokenizer_prefix_verified") else [])
        result.append({**spec, "model": metrics["model"] if metrics else experiment_config(spec["id"])["model"], "status": status, "checkpoint_ready": checkpoint_ready, "metrics": metrics,
                       "training": training, "history": history, "progress": progress, "paired": paired,
                       "test_metrics": test_metrics, "independent_metrics": independent_metrics,
                       "followup_metrics": followup_metrics, "latin_metrics": latin_metrics, "weight_audit": weight_audit,
                       "adapter_audit": adapter_audit, "known_issues": known_issues})
    return result


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    import time
    import uuid
    temp = path.with_name(f"{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    for attempt in range(8):
        try:
            temp.replace(path)
            return
        except PermissionError:
            if attempt == 7:
                raise
            time.sleep(0.05 * (attempt + 1))
