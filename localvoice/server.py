import importlib.util
import json
import threading
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from .core import ROOT, config, experiments, normalize, read_manifest, score, validate_manifest
from .audio import decode_audio

app = FastAPI(title="LocalVoice", version="0.1.0")
app.mount("/assets", StaticFiles(directory=ROOT / "frontend"), name="assets")
_inference_gate = threading.Lock()


def matrix_status():
    states = [json.loads(path.read_text(encoding="utf-8"))
              for path in (ROOT / "runs/matrix.json", ROOT / "runs/improvement.json", ROOT / "runs/finalization.json", ROOT / "runs/accuracy.json", ROOT / "runs/finalization-small.json", ROOT / "runs/finalization-aligned-tiny.json", ROOT / "runs/finish.json", ROOT / "runs/adaptation.json") if path.exists()]
    for path in (ROOT / "runs/refinement.json", ROOT / "runs/independent-evaluation.json", ROOT / "runs/current-training.json", ROOT / "runs/followup.json", ROOT / "runs/small-final.json", ROOT / "runs/regularized-round.json", ROOT / "runs/latin-round.json", ROOT / "runs/research-round.json", ROOT / "runs/ewc-followup.json"):
        if path.exists():
            states.append(json.loads(path.read_text(encoding="utf-8")))
    active = [state for state in states if state.get("status") == "running"]
    queued = [state for state in states if state.get("status") == "queued"]
    return max(active or queued or states, key=lambda state: state.get("started_at", "")) if states else None


@app.get("/")
def index():
    return FileResponse(ROOT / "frontend/index.html")


@app.get("/api/status")
def status():
    cfg = config()
    manifest = ROOT / cfg["manifest"]
    data = {"available": False, "samples": 0, "splits": {}, "warnings": []}
    if manifest.exists():
        try:
            data = {"available": True, **validate_manifest(manifest, inspect_audio=False)}
        except (ValueError, OSError) as exc:
            data["error"] = str(exc)
    job = matrix_status()
    selections = [json.loads(path.read_text(encoding="utf-8")) for path in
                  (ROOT / "runs/selection.json", ROOT / "runs/selection-aligned-tiny.json", ROOT / "runs/selection-small.json",
                   ROOT / "runs/selection-tiny-final.json", ROOT / "runs/selection-small-refined.json",
                   ROOT / "runs/selection-regularized.json", ROOT / "runs/selection-latin.json",
                     ROOT / "runs/selection-small-research.json", ROOT / "runs/selection-tiny-research.json") if path.exists()]
    if job and job.get("status") == "running" and job.get("project", {}).get("model"):
        selections = [s for s in selections if s.get("project", {}).get("model") == job["project"]["model"]]
    selection = min(selections, key=lambda s: s["validation_wer"]) if selections else None
    run_data = experiments()
    ready = [e for e in run_data if e["metrics"] and e["metrics"].get("split") == "validation" and e["checkpoint_ready"]]
    recommended = min(ready, key=lambda e: e["metrics"]["wer"])["id"] if ready else "E0"
    return {"project": cfg, "experiments": run_data, "dataset": data, "selection": selection,
            "recommended_experiment": recommended,
            "matrix": job,
            "ml_installed": all(importlib.util.find_spec(m) is not None for m in ("torch", "transformers", "peft"))}


@app.get("/api/report")
def report():
    content = (ROOT / "docs/RESEARCH_REPORT.md").read_text(encoding="utf-8")
    latest = ROOT / "docs/FINE_TUNING_COMPARISON.md"
    if latest.exists():
        content = latest.read_text(encoding="utf-8") + "\n\n" + content
    measured = [e for e in experiments() if e["metrics"]]
    live = "\n\n## Current local results\n\n"
    if not measured:
        live += "No research experiments have completed evaluation yet."
    else:
        live += "\n".join(f"- {e['id']} · {e['name']}: WER {e['metrics']['wer']:.2f}%, CER {e['metrics']['cer']:.2f}%, {e['metrics']['samples']} clips on the {e['metrics']['split']} split." for e in measured)
    tested = [e for e in experiments() if e.get("test_metrics")]
    if tested:
        live += "\n\n## Held-out test results\n\nSelection was frozen using validation results before this evaluation.\n\n"
        live += "\n".join(f"- {e['id']} · {e['name']}: WER {e['test_metrics']['wer']:.2f}%, CER {e['test_metrics']['cer']:.2f}%, {e['test_metrics']['samples']} test clips." for e in tested)
    research = ROOT / "docs/RESEARCH_METHOD_RESULTS.md"
    if research.exists():
        content = research.read_text(encoding="utf-8") + "\n\n---\n\n" + content
    return {"content": content + live}


def sample_row():
    try:
        return next(r for r in read_manifest() if r["split"] == "train")
    except (OSError, ValueError, StopIteration) as exc:
        raise HTTPException(404, "Prepare the dataset first to try a sample clip.") from exc


@app.get("/api/sample")
def sample():
    row = sample_row()
    return {"transcript": row["transcript"], "duration_seconds": row["duration_seconds"], "split": "train", "audio_url": "/api/sample/audio"}


@app.get("/api/sample/audio")
def sample_audio():
    row = sample_row()
    return FileResponse(row["audio_path"], media_type="audio/wav", filename="spanish-training-sample.wav")


@app.get("/api/export")
def export():
    return Response(json.dumps({"project": config(), "experiments": experiments()}, indent=2, ensure_ascii=False),
                    media_type="application/json", headers={"Content-Disposition": 'attachment; filename="localvoice-results.json"'})


@app.post("/api/transcribe")
def transcription(audio: UploadFile = File(...), experiment: str = Form("E0"), reference: str = Form("")):
    if experiment not in {e["id"] for e in experiments()}:
        raise HTTPException(400, "Unknown experiment.")
    if reference.strip() and not normalize(reference):
        raise HTTPException(400, "The reference transcript must contain words, not only punctuation.")
    active = matrix_status()
    if active and active.get("status") in {"running", "queued"}:
        raise HTTPException(409, "The experiment series is using the GPU. Transcription resumes after fine-tuning and evaluation finish.")
    content = audio.file.read(12 * 1024 * 1024 + 1)
    if len(content) > 12 * 1024 * 1024:
        raise HTTPException(413, "Audio must be smaller than 12 MB.")
    try:
        waveform = decode_audio(content)
    except Exception as exc:
        raise HTTPException(400, "Cannot read audio. Use a WAV, FLAC, or OGG file, up to 30 seconds.") from exc
    if not _inference_gate.acquire(blocking=False):
        raise HTTPException(409, "Another transcription is running. Try again shortly.")
    try:
        from .inference import transcribe
        result = transcribe(waveform, experiment)
        result["duration_seconds"] = len(waveform) / 16000
        result["metrics"] = score([reference], [result["transcript"]]) if reference.strip() else None
        return result
    except ImportError as exc:
        raise HTTPException(503, "Speech dependencies are not installed. Run: python -m pip install -e .[ml]") from exc
    except FileNotFoundError as exc:
        raise HTTPException(409, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(503, f"Model could not transcribe: {exc}") from exc
    finally:
        _inference_gate.release()
