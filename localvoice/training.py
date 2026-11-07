"""A transparent Whisper training loop with validation-only checkpoint selection."""
import csv
import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from .audio import augment, decode_audio
from .prompts import align_spanish_processor, canonical_generation
from .core import ROOT, EXPERIMENTS, config, experiment_config, dataset_fingerprint, normalize, read_manifest, score, validate_manifest, write_json


def checked_rows():
    audit = validate_manifest()
    if not audit["valid"]:
        raise ValueError("Dataset validation failed: " + "; ".join(audit["errors"][:8]))
    return read_manifest(), audit


def training_targets(rows, mode):
    """Train-only text formatting; evaluation references and splits never change."""
    if any(row["split"] != "train" for row in rows):
        raise ValueError("Training targets must only use the training split")
    if mode == "normalized":
        return {r["audio_path"]: normalize(r["transcript"]) for r in rows}
    if mode != "punctuated":
        raise ValueError("Unknown target_text mode")
    import pyarrow.parquet as pq
    raw = {}
    for shard in sorted((ROOT / "data/parquet").glob("train-*.parquet")):
        table = pq.read_table(shard, columns=["transcription", "raw_transcription"])
        for item in table.to_pylist():
            # Retain number-word and lexical conventions used by this benchmark.
            if normalize(item["raw_transcription"]) == normalize(item["transcription"]):
                raw[normalize(item["transcription"])] = item["raw_transcription"]
    targets = {r["audio_path"]: raw.get(normalize(r["transcript"]), r["transcript"][:1].upper() + r["transcript"][1:] + ".") for r in rows}
    for row in rows:
        if row.get("training_text"):
            if normalize(row["training_text"]) != normalize(row["transcript"]):
                raise ValueError("Natural training text must preserve the exact transcript words")
            targets[row["audio_path"]] = row["training_text"]
    return targets


def initial_checkpoint(hp, cfg, fingerprint):
    """Validate stage ancestry without reading test outcomes."""
    import hashlib
    parent = hp.get("initialize_from")
    if not parent:
        return None, {}
    if parent not in {e["id"] for e in EXPERIMENTS}:
        raise ValueError("Unknown initial experiment")
    folder = ROOT / "runs" / parent
    previous = json.loads((folder / "training.json").read_text(encoding="utf-8"))
    if previous.get("status") != "completed" or previous.get("project") != cfg or previous.get("dataset_fingerprint") != fingerprint:
        raise ValueError("Initial checkpoint must be completed with matching model, language and dataset")
    weights = folder / "checkpoint/model.safetensors"
    if not weights.is_file() or not (folder / "checkpoint/config.json").is_file():
        raise ValueError("Initial checkpoint must be a full saved model")
    digest = hashlib.sha256()
    with weights.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return folder / "checkpoint", {"initial_experiment": parent, "initial_weights_sha256": digest.hexdigest(),
        "parent_training_seconds": previous.get("cumulative_training_seconds", previous.get("training_seconds", 0)),
        "parent_training_data": previous.get("training_data")}


def optimizer_groups(model, hp, default_lr):
    """Assign every trainable tensor once; retain the encoder/decoder LR ratio."""
    params = [p for p in model.parameters() if p.requires_grad]
    if "learning_rate_encoder" not in hp:
        return params, {"all": default_lr}
    encoder_ids = {id(p) for p in model.model.encoder.parameters()}
    encoder = [p for p in params if id(p) in encoder_ids]
    decoder = [p for p in params if id(p) not in encoder_ids]
    groups = [{"params": p, "lr": hp["learning_rate_" + name], "name": name}
              for name, p in (("encoder", encoder), ("decoder", decoder)) if p]
    if any(group["lr"] <= 0 for group in groups):
        raise ValueError("Learning rates must be positive")
    return groups, {g["name"]: g["lr"] for g in groups}


def configure_lora(model, hp):
    from peft import LoraConfig, get_peft_model
    adapted = get_peft_model(model, LoraConfig(r=hp["lora_rank"], lora_alpha=hp["lora_alpha"],
        lora_dropout=hp["lora_dropout"], target_modules=hp["lora_targets"], bias="none"))
    names = [name for name, value in adapted.named_parameters() if value.requires_grad]
    if not names or any("lora_" not in name for name in names):
        raise ValueError("LoRA must update adapter tensors only")
    if hp.get("freeze_encoder") and any(".model.encoder." in name for name in names):
        raise ValueError("Encoder adapters conflict with the frozen-encoder recipe")
    return adapted


def speech_mask(features, duration_seconds, sample_rate=16000, hop_length=160):
    import torch
    samples = round(float(duration_seconds) * sample_rate)
    if samples <= 0:
        raise ValueError("Speech duration must be positive")
    valid = min(features.shape[-1], (samples + hop_length - 1) // hop_length)
    return (torch.arange(features.shape[-1]) < valid).long()


def distillation_loss(student_logits, teacher_logits, labels, temperature):
    """Token-mean KL(teacher || student), excluding padding, with T² scaling."""
    import torch.nn.functional as F
    if temperature <= 0 or student_logits.shape != teacher_logits.shape:
        raise ValueError("Distillation needs matching logits and positive temperature")
    valid = labels.ne(-100)
    if not valid.any():
        raise ValueError("Distillation needs nonpadding targets")
    student = student_logits[valid].float() / temperature
    teacher = teacher_logits.detach()[valid].float() / temperature
    return F.kl_div(F.log_softmax(student, dim=-1), F.softmax(teacher, dim=-1),
                    reduction="batchmean") * temperature ** 2


def additional_training_rows(hp, base_rows):
    path = hp.get("additional_training_manifest")
    if not path:
        return []
    path = ROOT / path
    audit = validate_manifest(path, required_splits=("train",))
    extra = read_manifest(path)
    if not audit["valid"] or not extra or any(r["split"] != "train" for r in extra):
        raise ValueError("Additional audio must be a valid nonempty train-only manifest")
    forbidden = {normalize(r["transcript"]) for r in base_rows if r["split"] != "train"}
    if any(normalize(r["transcript"]) in forbidden for r in extra):
        raise ValueError("Additional training text duplicates an evaluation reference")
    return extra


def train(experiment, settings_path):
    import torch
    from torch.utils.data import DataLoader, Dataset
    from transformers import WhisperForConditionalGeneration, WhisperProcessor, get_linear_schedule_with_warmup
    cfg = experiment_config(experiment)
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    hp = json.loads(settings_path.read_text(encoding="utf-8"))
    spec = next(s for s in EXPERIMENTS if s["id"] == experiment)
    folder = ROOT / "runs" / experiment
    if (folder / "training.json").exists() or (folder / "checkpoint").exists():
        raise FileExistsError("Run already exists. Archive it before repeating; never overwrite provenance.")
    rows, audit = checked_rows()
    fingerprint = dataset_fingerprint(rows)
    starting_checkpoint, ancestry = initial_checkpoint(hp, cfg, fingerprint)
    extra_rows = additional_training_rows(hp, rows)
    training_rows = [r for r in rows if r["split"] == "train"] + extra_rows
    seed = hp["seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    rng = np.random.default_rng(seed)
    targets = training_targets(training_rows, hp.get("target_text", "normalized"))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    source = ROOT / cfg["local_model_path"] if cfg.get("local_model_path") else cfg["model"]
    processor = WhisperProcessor.from_pretrained(source, revision=cfg["model_revision"], language=cfg["language"], task="transcribe")
    prefix_tokens = align_spanish_processor(processor, cfg["language"])
    model = WhisperForConditionalGeneration.from_pretrained(starting_checkpoint or source,
                **({} if starting_checkpoint else {"revision": cfg["model_revision"]}))
    generation_digest = canonical_generation(model, cfg, source)
    model.config.use_cache = False
    if hp.get("freeze_encoder"):
        model.model.encoder.requires_grad_(False)
    from .regularization import freeze_lower_encoder
    if hp.get("freeze_encoder") and hp.get("freeze_encoder_layers"):
        raise ValueError("Choose complete encoder freezing or partial freezing, not both")
    freezing = freeze_lower_encoder(model, hp.get("freeze_encoder_layers", 0))
    spec_augment = hp.get("augmentation_method") == "specaugment"
    waveform_augment = spec["augmentation"] and not spec_augment
    model.config.apply_spec_augment = spec_augment
    if spec_augment:
        for name in ("mask_time_prob", "mask_time_length", "mask_time_min_masks", "mask_feature_prob", "mask_feature_length"):
            if name in hp:
                setattr(model.config, name, hp[name])
    if spec["strategy"] == "lora":
        model = configure_lora(model, hp)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.to(device)
    teacher = None
    teacher_record = None
    if hp.get("teacher_experiment"):
        from .inference import load_model
        teacher_processor, teacher, teacher_device = load_model(hp["teacher_experiment"])
        if teacher_device != device or teacher_processor.tokenizer.get_vocab() != processor.tokenizer.get_vocab():
            raise ValueError("Teacher and student need identical token IDs and device")
        teacher.requires_grad_(False).eval()
        teacher.config.use_cache = False
        teacher_record = {"experiment": hp["teacher_experiment"],
                          "project": experiment_config(hp["teacher_experiment"]),
                          "temperature": hp["distillation_temperature"],
                          "kl_weight": hp["distillation_weight"],
                          "inputs": "training split only; clean features before student augmentation",
                          "trainable": False}
        if not 0 < hp["distillation_weight"] < 1:
            raise ValueError("Distillation weight must be between zero and one")

    class SpeechDataset(Dataset):
        def __init__(self, selected):
            self.rows = selected
            # Unaugmented features are invariant across epochs. Cache them on
            # disk instead of repeating FFT/mel extraction every epoch.
            self.feature_cache = ROOT / "data" / "features" / cfg["model"].replace("/", "--")
            if not waveform_augment:
                self.feature_cache.mkdir(parents=True, exist_ok=True)

        def __len__(self):
            return len(self.rows)

        def __getitem__(self, i):
            row = self.rows[i]
            import hashlib
            key = hashlib.sha256(Path(row["audio_path"]).read_bytes() + cfg["model_revision"].encode()).hexdigest()
            cached = self.feature_cache / f"{key}.npy"
            if not waveform_augment and cached.exists():
                features = torch.from_numpy(np.load(cached, allow_pickle=False))
            else:
                audio = decode_audio(row["audio_path"])
                if waveform_augment:
                    audio = augment(audio, rng)
                features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features[0]
                if not waveform_augment:
                    np.save(cached, features.numpy(), allow_pickle=False)
            labels = processor.tokenizer(targets[row["audio_path"]]).input_ids
            if len(labels) > model.config.max_target_positions:
                raise ValueError("Transcript exceeds Whisper target context; shorten the clip.")
            item = {"input_features": features, "input_ids": labels}
            if spec_augment:
                item["attention_mask"] = speech_mask(features, row["duration_seconds"])
            return item

    def collate(batch):
        features = torch.stack([b["input_features"] for b in batch])
        padded = processor.tokenizer.pad([{"input_ids": b["input_ids"]} for b in batch], return_tensors="pt")
        labels = padded.input_ids.masked_fill(padded.attention_mask.ne(1), -100)
        if (labels[:, 0] == model.config.decoder_start_token_id).all():
            labels = labels[:, 1:]
        result = {"input_features": features.to(device), "labels": labels.to(device)}
        if spec_augment:
            result["attention_mask"] = torch.stack([b["attention_mask"] for b in batch]).to(device)
        return result

    validation_rows = [r for r in rows if r["split"] == "validation"]
    loader = DataLoader(SpeechDataset(training_rows), batch_size=hp["batch_size"], shuffle=True, collate_fn=collate, num_workers=0)
    ewc = None
    ewc_record = None
    if hp.get("ewc_fisher"):
        from .fisher import load_verified_fisher
        from .regularization import FisherPenalty
        if teacher or spec["strategy"] == "lora" or hp.get("ewc_lambda", 0) <= 0:
            raise ValueError("This EWC recipe requires full tuning, no teacher, and a positive penalty")
        fisher, ewc_record = load_verified_fisher(hp, cfg, fingerprint, ancestry)
        ewc = FisherPenalty(model, fisher)
        ewc_record["raw_fisher_trace"] = ewc.trace_before_normalization
        del fisher
    params = [p for p in model.parameters() if p.requires_grad]
    lr = hp["learning_rate_lora"] if spec["strategy"] == "lora" else hp["learning_rate_full"]
    groups, learning_rates = optimizer_groups(model, hp, lr)
    optimizer = torch.optim.AdamW(groups, lr=lr, weight_decay=hp["weight_decay"])
    accumulation = hp["gradient_accumulation_steps"]
    steps = int(np.ceil(len(loader) / accumulation)) * hp["epochs"]
    scheduler = get_linear_schedule_with_warmup(optimizer, round(steps * hp["warmup_ratio"]), steps)
    amp_dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=device == "cuda" and amp_dtype == torch.float16, init_scale=1024)
    import hashlib
    target_hash = hashlib.sha256(json.dumps(targets, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    provenance = {"experiment": spec, "project": cfg, "hyperparameters": hp, "effective_learning_rate": lr,
                  **ancestry, "learning_rates": learning_rates, "encoder_freezing": freezing, "ewc": ewc_record,
                  "training_target_sha256": target_hash, "training_target_count": len(targets),
                  "decoder_prefix_tokens": prefix_tokens, "tokenizer_prefix_verified": True,
                  "generation_config_sha256": generation_digest,
                  "checkpoint_evaluation_batch_size": hp.get("validation_batch_size", cfg.get("evaluation_batch_size", 1)),
                  "teacher": teacher_record,
                  "loss_objective": "supervised cross-entropy + diagonal Fisher EWC" if ewc else "weighted supervised cross-entropy + teacher KL" if teacher else "supervised cross-entropy",
                  "dataset_fingerprint": fingerprint, "validation_audit": audit,
                  "training_dataset_fingerprint": dataset_fingerprint(training_rows),
                  "training_data": {"base_training_samples": len(training_rows) - len(extra_rows),
                                    "additional_samples": len(extra_rows),
                                    "additional_manifest": hp.get("additional_training_manifest"),
                                    "additional_license": hp.get("additional_training_license"),
                                    "total_samples": len(training_rows),
                                    "total_hours": sum(float(r.get("duration_seconds", 0)) for r in training_rows) / 3600},
                  "started_at": datetime.now(timezone.utc).isoformat(), "device": device,
                  "gpu": torch.cuda.get_device_name() if device == "cuda" else None,
                  "torch": torch.__version__, "trainable_parameters": sum(p.numel() for p in params),
                  "trainable_parameter_names": [name for name, value in model.named_parameters() if value.requires_grad] if spec["strategy"] == "lora" else None,
                  "base_parameters_frozen": all("lora_" in name for name, value in model.named_parameters() if value.requires_grad) if spec["strategy"] == "lora" else False,
                  "total_parameters": sum(p.numel() for p in model.parameters()), "precision": str(amp_dtype) if device == "cuda" else "float32", "optimizer_steps": 0, "skipped_steps": 0, "status": "running"}
    write_json(folder / "training.json", provenance)
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    started, best, stale, history = time.perf_counter(), float("inf"), 0, []
    progress_path = folder / "progress.json"

    def validate_checkpoint(epoch_value, train_loss):
        nonlocal best, stale
        measured, _ = evaluate_rows(model, processor, validation_rows, device, progress_path=progress_path,
                                    context={"evaluation_batch_size": hp.get("validation_batch_size", cfg.get("evaluation_batch_size", 1)),
                                             "epoch": epoch_value, "epochs": hp["epochs"],
                                             "optimizer_steps": provenance["optimizer_steps"], "train_loss": train_loss})
        entry = {"epoch": epoch_value, "optimizer_steps": provenance["optimizer_steps"], "train_loss": train_loss,
                 "validation_wer": measured["wer"], "validation_cer": measured["cer"],
                 "elapsed_seconds": time.perf_counter() - started}
        history.append(entry)
        write_json(folder / "history.json", history)
        print(json.dumps(entry), flush=True)
        if measured["wer"] < best:
            best, stale = measured["wer"], 0
            model.save_pretrained(folder / "checkpoint", safe_serialization=True)
            processor.save_pretrained(folder / "checkpoint")
            provenance.update(best_epoch=epoch_value, best_optimizer_step=provenance["optimizer_steps"], best_validation_wer=best)
        else:
            stale += 1
        write_json(folder / "training.json", provenance)
        return stale >= hp["early_stopping_patience"]

    stop = False
    try:
        for epoch in range(hp["epochs"]):
            model.train()
            optimizer.zero_grad(set_to_none=True)
            total_loss = 0
            write_json(progress_path, {"phase": "training", "epoch": epoch + 1, "epochs": hp["epochs"], "batches_done": 0, "batches_total": len(loader), "optimizer_steps": provenance["optimizer_steps"]})
            for i, batch in enumerate(loader):
                # The final accumulation group may contain fewer batches.
                group_size = min(accumulation, len(loader) - (i // accumulation) * accumulation)
                with torch.autocast(device_type=device, dtype=amp_dtype, enabled=device == "cuda"):
                    if teacher is not None:
                        with torch.no_grad():
                            teacher_logits = teacher(**batch, use_cache=False).logits.detach()
                    output = model(**batch)
                    loss = output.loss
                    if teacher is not None:
                        kl = distillation_loss(output.logits, teacher_logits, batch["labels"], hp["distillation_temperature"])
                        weight = hp["distillation_weight"]
                        loss = (1 - weight) * loss + weight * kl
                        if i % hp.get("log_every_steps", 20) == 0:
                            print(json.dumps({"objective": "distillation", "epoch": epoch + 1,
                                  "batch": i + 1, "cross_entropy": output.loss.item(), "teacher_kl": kl.item()}), flush=True)
                        del teacher_logits, kl
                total_loss += loss.item()
                if ewc is not None:
                    penalty = ewc()
                    loss = loss + hp["ewc_lambda"] * penalty
                    if i % hp.get("log_every_steps", 20) == 0:
                        print(json.dumps({"objective": "ewc", "cross_entropy": output.loss.item(),
                              "weighted_penalty": hp["ewc_lambda"] * penalty.item()}), flush=True)
                if not np.isfinite(loss.item()):
                    raise ValueError("Non-finite loss; training stopped before saving an invalid checkpoint.")
                scaler.scale(loss / group_size).backward()
                if (i + 1) % accumulation == 0 or i + 1 == len(loader):
                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(params, 1.0)
                    previous_scale = scaler.get_scale()
                    scaler.step(optimizer)
                    scaler.update()
                    if scaler.get_scale() >= previous_scale:
                        scheduler.step()
                        provenance["optimizer_steps"] += 1
                    else:
                        provenance["skipped_steps"] += 1
                    optimizer.zero_grad(set_to_none=True)
                    if provenance["optimizer_steps"] % hp.get("log_every_steps", 20) == 0 or i + 1 == len(loader):
                        progress = {"phase": "training", "epoch": epoch + 1, "epochs": hp["epochs"], "batches_done": i + 1,
                                    "batches_total": len(loader), "optimizer_steps": provenance["optimizer_steps"],
                                    "train_loss": total_loss / (i + 1), "learning_rate": scheduler.get_last_lr()[0],
                                    "elapsed_seconds": time.perf_counter() - started}
                        write_json(progress_path, progress)
                        print(json.dumps(progress), flush=True)
                    interval = hp.get("validation_interval_updates", 0)
                    within_epoch_updates = (i + 1) // accumulation
                    if interval and within_epoch_updates and within_epoch_updates % interval == 0 and i + 1 < len(loader):
                        stop = validate_checkpoint(round(epoch + (i + 1) / len(loader), 3), total_loss / (i + 1))
                        model.train()
                        if stop:
                            break
            if stop:
                break
            if provenance["optimizer_steps"] == 0:
                raise ValueError("No optimizer update completed. Check numerical stability and mixed precision.")
            if validate_checkpoint(epoch + 1, total_loss / len(loader)):
                break
        provenance["status"] = "completed"
        write_json(progress_path, {"phase": "completed", "epochs_completed": history[-1]["epoch"], "validation_checks": len(history), "optimizer_steps": provenance["optimizer_steps"], "best_epoch": provenance["best_epoch"]})
    except BaseException as exc:
        provenance["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        provenance["error"] = str(exc)
        raise
    finally:
        provenance["training_seconds"] = time.perf_counter() - started
        provenance["cumulative_training_seconds"] = ancestry.get("parent_training_seconds", 0) + provenance["training_seconds"]
        provenance["peak_gpu_memory_mb"] = torch.cuda.max_memory_allocated() / 1024 ** 2 if device == "cuda" else None
        write_json(folder / "training.json", provenance)


def evaluate_rows(model, processor, rows, device, progress_path=None, context=None):
    import torch
    refs, hyps, predictions = [], [], []
    model.eval()
    batch_size = (context or {}).get("evaluation_batch_size", 1)
    if batch_size < 1:
        raise ValueError("Evaluation batch size must be positive")
    with torch.inference_mode():
        for index in range(0, len(rows), batch_size):
            selected = rows[index:index + batch_size]
            if progress_path:
                progress = {**(context or {}), "phase": (context or {}).get("split", "validation"), "clips_done": index, "clips_total": len(rows)}
                if index % (25 * batch_size) == 0 or index + batch_size >= len(rows):
                    write_json(progress_path, progress)
                    print(json.dumps(progress), flush=True)
            audio = [decode_audio(row["audio_path"]) for row in selected]
            inputs = processor(audio, sampling_rate=16000, return_tensors="pt", return_attention_mask=True)
            features = inputs.input_features.to(device)
            if device == "cuda":
                torch.cuda.synchronize()
            start = time.perf_counter()
            ids = model.generate(features, attention_mask=inputs.attention_mask.to(device), max_new_tokens=225, use_cache=True)
            if device == "cuda":
                torch.cuda.synchronize()
            latency = (time.perf_counter() - start) / len(selected)
            transcripts = processor.batch_decode(ids, skip_special_tokens=True)
            for row, transcript in zip(selected, transcripts):
                refs.append(row["transcript"])
                hyps.append(transcript)
                predictions.append({**row, "hypothesis": transcript, "latency_seconds": latency})
    return score(refs, hyps), predictions


def evaluate(experiment, split="validation"):
    from .inference import load_model
    rows, audit = checked_rows()
    fingerprint = dataset_fingerprint(rows)
    folder = ROOT / "runs" / experiment
    training_path = folder / "training.json"
    training = json.loads(training_path.read_text(encoding="utf-8")) if training_path.exists() else {}
    if next(s for s in EXPERIMENTS if s["id"] == experiment)["strategy"] != "baseline" and training.get("dataset_fingerprint") != fingerprint:
        raise ValueError("Dataset changed since training; this comparison would be invalid.")
    if next(s for s in EXPERIMENTS if s["id"] == experiment)["strategy"] != "baseline" and training.get("project") != experiment_config(experiment):
        raise ValueError("Project settings changed since training.")
    cfg = experiment_config(experiment)
    processor, model, device = load_model(experiment)
    selected = [r for r in rows if r["split"] == split]
    # Warm up to keep model loading and first CUDA initialization out of latency.
    evaluate_rows(model, processor, selected[:1], device)
    metrics, predictions = evaluate_rows(model, processor, selected, device, progress_path=folder / "evaluation-progress.json", context={"split": split, "evaluation_batch_size": cfg.get("evaluation_batch_size", 1)})
    groups = {}
    for field in ("dialect", "condition"):
        for value in sorted({r.get(field, "") for r in predictions} - {""}):
            group = [r for r in predictions if r.get(field) == value]
            if len(group) >= 10:
                groups[f"{field}:{value}"] = score([r["transcript"] for r in group], [r["hypothesis"] for r in group])
    metrics.update({"split": split, "dataset_fingerprint": fingerprint, "model": cfg["model"], "model_revision": cfg["model_revision"], "language": cfg["language"],
                    "normalization": config()["normalization"], "seed": training.get("hyperparameters", {}).get("seed", config()["seed"]),
                    "mean_latency_seconds": float(np.mean([r["latency_seconds"] for r in predictions])),
                    "trainable_parameters": training.get("trainable_parameters", 0), "training_seconds": training.get("cumulative_training_seconds", training.get("training_seconds", 0)),
                    "inference_parameters": sum(p.numel() for p in model.parameters()),
                    "stage_training_seconds": training.get("training_seconds", 0), "initial_experiment": training.get("initial_experiment"),
                    "peak_gpu_memory_mb": training.get("peak_gpu_memory_mb"), "groups": groups,
                    "evaluation_protocol": {"batch_size": cfg.get("evaluation_batch_size", 1), "precision": "float32", "num_beams": 1, "max_new_tokens": 225},
                    "generation_config_sha256": getattr(model, "_localvoice_generation_sha256", None),
                    "latency_mode": "amortized batch" if cfg.get("evaluation_batch_size", 1) > 1 else "single clip",
                    "audit_warnings": audit["warnings"], "device": device, "evaluated_at": datetime.now(timezone.utc).isoformat()})
    if split == "test" and experiment in {"E10", "E15"}:
        metrics["evaluation_context"] = "Reused FLEURS test corpus: earlier project test results were already read. This is an exploratory diagnostic, not a new blind evaluation."
    write_json(folder / f"metrics-{split}.json", metrics)
    # Keep the tuning comparison on validation when a final test is added.
    if split == "validation" or not (folder / "metrics.json").exists():
        write_json(folder / "metrics.json", metrics)
    write_json(folder / f"predictions-{split}.json", predictions)
    from .reporting import write_results
    write_results()
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
