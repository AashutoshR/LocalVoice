"""Prepare additional official MLS TRAIN audio; never consume test references."""
import csv
import hashlib
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .core import ROOT, dataset_fingerprint, normalize, read_manifest, write_json
from .independent import REVISION


def prepare():
    import pyarrow.parquet as pq
    import soundfile as sf
    from huggingface_hub import HfApi, hf_hub_download
    from .audio import decode_audio
    folder = ROOT / "data/additional-spanish"
    if (folder / "source.json").exists():
        raise FileExistsError("Additional training sample already frozen")
    paths = [f"spanish/train-{index:05d}-of-00030.parquet" for index in (0, 15, 29)]
    info = HfApi().dataset_info("facebook/multilingual_librispeech", revision=REVISION, files_metadata=True)
    source_info = {s.rfilename: s for s in info.siblings}
    def download(name):
        from .prepare import download_shard
        destination = folder / "source" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            download_shard(f"https://huggingface.co/datasets/facebook/multilingual_librispeech/resolve/{REVISION}/{name}",
                           destination, source_info[name].size)
        return destination
    with ThreadPoolExecutor(max_workers=3) as executor:
        downloaded = list(executor.map(download, paths))
    base = read_manifest()
    forbidden_text = {normalize(r["transcript"]) for r in base if r["split"] != "train"}
    test_speakers = set(json.loads((ROOT / "data/independent-mls/sample.json").read_text(encoding="utf-8"))["speakers"])
    rows, sources = [], []
    audio_dir = folder / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    for name, path in zip(paths, downloaded):
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        expected = source_info[name].lfs.sha256
        if digest != expected:
            raise ValueError("Training shard SHA-256 mismatch")
        metadata = pq.read_table(path, columns=["id", "transcript", "audio_duration", "speaker_id"]).to_pylist()
        eligible = sorted((r for r in metadata if 0 < r["audio_duration"] <= 30 and
                           normalize(r["transcript"]) and normalize(r["transcript"]) not in forbidden_text), key=lambda r: r["id"])
        chosen = {r["id"] for r in random.Random(42).sample(eligible, 1000)}
        for batch in pq.ParquetFile(path).iter_batches(batch_size=64):
            for item in batch.to_pylist():
                if item["id"] not in chosen:
                    continue
                if item["speaker_id"] in test_speakers:
                    raise ValueError("Official train speaker overlaps reserved MLS test speakers")
                wave = decode_audio(item["audio"]["bytes"])
                output = audio_dir / f'{item["id"]}.wav'
                sf.write(output, wave, 16000, subtype="PCM_16")
                rows.append(dict(id=item["id"], audio_path=str(output.resolve()), transcript=item["transcript"],
                    speaker_id=item["speaker_id"], split="train", duration_seconds=len(wave) / 16000, condition="audiobook"))
        sources.append(dict(path=name, sha256=digest, source_rows=len(metadata), eligible_rows=len(eligible), selected=1000))
        print(json.dumps(sources[-1]), flush=True)
    rows.sort(key=lambda r: r["id"])
    with (folder / "manifest.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_json(folder / "source.json", dict(dataset="facebook/multilingual_librispeech", revision=REVISION,
        source_split="train", language="spanish", license="CC-BY-4.0", seed=42, sources=sources,
        selected_ids=[r["id"] for r in rows], samples=len(rows), hours=sum(r["duration_seconds"] for r in rows) / 3600,
        speakers=len({r["speaker_id"] for r in rows}), dataset_fingerprint=dataset_fingerprint(read_manifest(folder / "manifest.csv")),
        policy="Training only. Excludes exact normalized FLEURS evaluation references; MLS train speakers disjoint from reserved test speakers."))
    print(f"Prepared {len(rows)} additional Spanish training clips", flush=True)


if __name__ == "__main__":
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    prepare()
