"""One loaded model at a time, shared by evaluation and browser inference."""
import threading
import time
import json
import os
from pathlib import Path
from .core import ROOT, config, experiment_config, EXPERIMENTS
from .prompts import align_spanish_processor, canonical_generation

_lock = threading.Lock()
_loaded = None


def load_model(experiment="E0"):
    import torch
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    settings = experiment_config(experiment)
    source = ROOT / settings["local_model_path"] if settings.get("local_model_path") else settings["model"]
    baseline = next(s for s in EXPERIMENTS if s["id"] == experiment)["strategy"] == "baseline"
    checkpoint = ROOT / "runs" / experiment / "checkpoint"
    if not baseline and not (checkpoint / "config.json").is_file() and not (checkpoint / "adapter_config.json").is_file():
        raise FileNotFoundError(f"{experiment} has no trained checkpoint. Run training first.")
    if not baseline:
        training = json.loads((checkpoint.parent / "training.json").read_text(encoding="utf-8"))
        if any(training.get("project", {}).get(k) != settings[k] for k in ("language", "model", "model_revision")):
            raise ValueError("Checkpoint belongs to a different language or base model.")
    processor = WhisperProcessor.from_pretrained(source if baseline else checkpoint, language=settings["language"], task="transcribe", **({"revision": settings["model_revision"]} if baseline else {}))
    align_spanish_processor(processor, settings["language"])
    if (checkpoint / "adapter_config.json").is_file() and not baseline:
        from peft import PeftModel
        model = WhisperForConditionalGeneration.from_pretrained(source, revision=settings["model_revision"])
        model = PeftModel.from_pretrained(model, checkpoint).merge_and_unload()
    else:
        model = WhisperForConditionalGeneration.from_pretrained(source if baseline else checkpoint, **({"revision": settings["model_revision"]} if baseline else {}))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    canonical_generation(model, settings, source)
    model.to(device).eval()
    model.config.use_cache = True
    model.generation_config.use_cache = True
    model.generation_config.language = settings["language"]
    model.generation_config.task = "transcribe"
    model.generation_config.forced_decoder_ids = None
    return processor, model, device


def transcribe(audio, experiment="E0"):
    global _loaded
    import torch
    with _lock:
        started = time.perf_counter()
        settings = experiment_config(experiment)
        key = (experiment, settings["language"], settings["model"], settings["model_revision"])
        if _loaded is None or _loaded[0] != key:
            _loaded = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            _loaded = (key, *load_model(experiment))
        _, processor, model, device = _loaded
        ready = time.perf_counter()
        inputs = processor(audio, sampling_rate=16000, return_tensors="pt", return_attention_mask=True)
        features = inputs.input_features.to(device)
        if device == "cuda":
            torch.cuda.synchronize()
        inference_start = time.perf_counter()
        with torch.inference_mode():
            tokens = model.generate(features, attention_mask=inputs.attention_mask.to(device), max_new_tokens=225, use_cache=True)
        if device == "cuda":
            torch.cuda.synchronize()
        latency = time.perf_counter() - inference_start
        return {"transcript": processor.batch_decode(tokens, skip_special_tokens=True)[0],
                "latency_seconds": latency, "load_seconds": ready - started,
                "total_seconds": time.perf_counter() - started, "device": device, "experiment": experiment}
