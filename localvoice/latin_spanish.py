"""Prepare licensed Latin American read speech; reserve text-disjoint clips first."""
import csv
import hashlib
import io
import json
import random
import re
import urllib.request
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from .core import ROOT, dataset_fingerprint, normalize, read_manifest, write_json

FOLDER = ROOT / "data/latin-spanish"
BASE = "https://www.openslr.org/resources/61/"


def audit_partition():
    source=json.loads((FOLDER/"source.json").read_text(encoding="utf-8"))
    base=read_manifest()
    train=read_manifest(FOLDER/"manifest.csv")
    holdout=read_manifest(FOLDER/"holdout.csv")
    if dataset_fingerprint(train)!=source["train"]["dataset_fingerprint"] or dataset_fingerprint(holdout)!=source["holdout"]["dataset_fingerprint"]:
        raise ValueError("Prepared Latin American partition changed")
    known={normalize(r["transcript"]) for r in base+train}
    if known & {normalize(r["transcript"]) for r in holdout}:
        raise ValueError("Held-out transcript overlaps training or FLEURS")
    training_file=ROOT/"runs/E17/training.json"
    if training_file.exists():
        training=json.loads(training_file.read_text(encoding="utf-8"))
        expected=dataset_fingerprint([r for r in base if r["split"]=="train"]+train)
        if training["training_dataset_fingerprint"]!=expected:
            raise ValueError("E17 trained on a different partition")
    proof=dict(train_samples=len(train),holdout_samples=len(holdout),exact_text_overlap=0,
        train_fingerprint=source["train"]["dataset_fingerprint"],holdout_fingerprint=source["holdout"]["dataset_fingerprint"],
        speaker_independence="unverified; source speaker IDs unavailable")
    write_json(ROOT/"runs/E17/data-audit.json",proof)
    return proof


def prepare():
    from .prepare import download_shard
    from .audio import decode_audio
    import soundfile as sf
    if (FOLDER / "source.json").exists():
        raise FileExistsError("Latin American sample is already frozen")
    source_dir = FOLDER / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    state_path = ROOT / "runs/latin-data.json"
    state = dict(status="running", started_at=datetime.now(timezone.utc).isoformat())
    write_json(state_path, state)
    try:
        sources = []
        def download(part):
            index_name = f"line_index_{part}.tsv"
            index = source_dir / index_name
            if not index.exists():
                with urllib.request.urlopen(BASE + index_name, timeout=30) as response:
                    index.write_bytes(response.read())
            archive_name = f"es_ar_{part}.zip"
            archive = source_dir / archive_name
            if not archive.exists():
                with urllib.request.urlopen(urllib.request.Request(BASE + archive_name,
                        headers={"Range": "bytes=0-0"}), timeout=30) as response:
                    if response.status != 206:
                        raise ValueError("Archive server must honor byte ranges")
                    size = int(response.headers["Content-Range"].split("/")[-1])
                download_shard(BASE + archive_name, archive, size)
            with archive.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            return index, archive, dict(url=BASE+archive_name, sha256=digest,
                index_sha256=hashlib.sha256(index.read_bytes()).hexdigest())
        with ThreadPoolExecutor(max_workers=2) as pool:
            parts = list(pool.map(download, ("female", "male")))
        base = read_manifest()
        forbidden_eval = {normalize(r["transcript"]) for r in base if r["split"] != "train"}
        previously_seen_text = {normalize(r["transcript"]) for r in base}
        audio_dir = FOLDER / "audio"
        audio_dir.mkdir(exist_ok=True)
        rows, exclusions, seen_audio = [], Counter(), set()
        for index, archive, source in parts:
            sources.append(source)
            entries = [line.split("\t", 1) for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
            with zipfile.ZipFile(archive) as zipped:
                members = {Path(m.filename).stem: m for m in zipped.infolist() if Path(m.filename).suffix.lower() == ".wav"}
                for identifier, transcript in entries:
                    if not re.fullmatch(r"ar[fm]_\d+_\d+", identifier):
                        raise ValueError("Unexpected public file ID")
                    if not normalize(transcript) or "\ufffd" in transcript or normalize(transcript) in forbidden_eval:
                        exclusions["empty, corrupt text or FLEURS evaluation text"] += 1
                        continue
                    if identifier not in members:
                        raise ValueError("Published transcript has no matching archive audio")
                    try:
                        wave = decode_audio(zipped.read(members[identifier]))
                    except (ValueError, RuntimeError):
                        exclusions["invalid audio or duration outside (0,30] seconds"] += 1
                        continue
                    buffer = io.BytesIO()
                    sf.write(buffer, wave, 16000, format="WAV", subtype="PCM_16")
                    raw = buffer.getvalue()
                    audio_hash = hashlib.sha256(raw).hexdigest()
                    if audio_hash in seen_audio:
                        exclusions["duplicate audio"] += 1
                        continue
                    seen_audio.add(audio_hash)
                    output = audio_dir / f"{identifier}.wav"
                    output.write_bytes(raw)
                    rows.append(dict(id=identifier, audio_path=str(output.resolve()), transcript=transcript,
                        training_text=transcript, speaker_id="", split="train", duration_seconds=len(wave)/16000,
                        dialect="es-AR", condition="read sentences"))
            print(f"Decoded {len(rows)} eligible Latin American clips", flush=True)
        grouped = defaultdict(list)
        for row in rows:
            if normalize(row["transcript"]) not in previously_seen_text:
                grouped[normalize(row["transcript"])].append(row)
        rng = random.Random(43)
        heldout_texts = set(rng.sample(sorted(grouped), 300))
        heldout = [dict(rng.choice(grouped[text]), split="test") for text in sorted(heldout_texts)]
        available = sorted((r for r in rows if normalize(r["transcript"]) not in heldout_texts), key=lambda r:r["id"])
        train = sorted(random.Random(42).sample(available, min(3000,len(available))), key=lambda r:r["id"])
        for name, selected in (("manifest.csv",train),("holdout.csv",heldout)):
            with (FOLDER/name).open("w",encoding="utf-8",newline="") as output:
                writer=csv.DictWriter(output,fieldnames=list(selected[0]))
                writer.writeheader(); writer.writerows(selected)
        def describe(name):
            selected=read_manifest(FOLDER/name)
            return dict(samples=len(selected),hours=sum(float(r["duration_seconds"]) for r in selected)/3600,
                        ids=[r["id"] for r in selected],dataset_fingerprint=dataset_fingerprint(selected))
        write_json(FOLDER/"source.json",dict(dataset="OpenSLR 61",url="https://www.openslr.org/61/",
            language="Spanish",locale="Argentina",license="CC-BY-SA-4.0",sources=sources,
            train=describe("manifest.csv"),holdout=describe("holdout.csv"),exclusions=dict(exclusions),
            train_seed=42,holdout_seed=43,eligible_clips=len(rows),speaker_ids_available=False,
            split_policy="Holdout references are text-disjoint from all FLEURS and all added training clips; no speaker-independence claim. Weather-message data excluded.",
            frozen_at=datetime.now(timezone.utc).isoformat()))
        state["status"]="completed"
    except BaseException as error:
        state.update(status="failed",error=str(error))
        raise
    finally:
        write_json(state_path,state)


if __name__ == "__main__":
    prepare()
