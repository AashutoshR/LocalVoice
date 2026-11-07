"""Use official parquet exports so no remote dataset scripts are executed."""
import csv
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import soundfile as sf
from .audio import decode_audio
from .core import ROOT, config, write_json


def download_shard(url, destination, size):
    """Bounded HTTP ranges avoid buffering multi-GB responses in desktop proxies."""
    partial = destination.with_suffix(".partial")
    offset = partial.stat().st_size if partial.exists() else 0
    chunk_size = 8 * 1024 * 1024

    def fetch(start):
        end = min(start + chunk_size, size) - 1
        request = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
        with urllib.request.urlopen(request, timeout=90) as response:
            if response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/"):
                raise ValueError("Server did not honor the requested download range.")
            content = response.read(chunk_size + 1)
            if len(content) != end - start + 1:
                raise ValueError("Incomplete parquet download range; rerun to resume.")
            return content

    with partial.open("ab") as output, ThreadPoolExecutor(max_workers=4) as pool:
        while offset < size:
            starts = list(range(offset, min(offset + chunk_size * 4, size), chunk_size))
            for content in pool.map(fetch, starts):
                output.write(content)
                offset += len(content)
            output.flush()
            print(f"  {offset / size:.0%} ({offset // 1048576}/{size // 1048576} MB)", flush=True)
    if partial.stat().st_size != size:
        raise ValueError("Parquet size mismatch.")
    partial.replace(destination)


def prepare():
    from datasets import Audio, load_dataset
    cfg = config()
    target = ROOT / cfg["manifest"]
    if target.exists():
        raise FileExistsError("Manifest already exists; keep the current splits or move data/ to an archive first.")
    url = f"https://huggingface.co/api/datasets/{cfg['dataset']}/tree/refs%2Fconvert%2Fparquet/{cfg['dataset_config']}?recursive=true"
    with urllib.request.urlopen(url, timeout=60) as response:
        tree = json.load(response)
    files = {split: [f"https://huggingface.co/datasets/{cfg['dataset']}/resolve/refs%2Fconvert%2Fparquet/{item['path']}"
                     for item in tree if item['type'] == 'file' and item['path'].startswith(f"{cfg['dataset_config']}/{split}/") and item['path'].endswith('.parquet')]
             for split in ("train", "validation", "test")}
    if any(not shards for shards in files.values()):
        raise ValueError("Official parquet export is missing one or more required splits.")
    sizes = {item['path']: item['size'] for item in tree if item['type'] == 'file'}
    records, skipped = [], []
    for split in ("train", "validation", "test"):
        # datasets interprets huggingface.co/api URLs as repository paths. Download
        # through HTTP first, then let datasets consume the local parquet shards.
        cache = target.parent / "parquet"
        cache.mkdir(parents=True, exist_ok=True)
        shards = []
        for number, remote in enumerate(files[split]):
            local = cache / f"{split}-{number}.parquet"
            if not local.exists():
                print(f"Downloading {split} shard {number}...", flush=True)
                remote_path = remote.split("/refs%2Fconvert%2Fparquet/", 1)[1]
                download_shard(remote, local, sizes[remote_path])
            shards.append(str(local))
        dataset = load_dataset("parquet", data_files={split: shards}, split=split)
        dataset = dataset.cast_column("audio", Audio(decode=False))
        folder = target.parent / "audio" / split
        folder.mkdir(parents=True, exist_ok=True)
        for index, row in enumerate(dataset):
            audio = row["audio"]
            raw = audio.get("bytes")
            source = raw if raw is not None else audio["path"]
            try:
                wave = decode_audio(source)
            except (ValueError, RuntimeError) as exc:
                skipped.append({"split": split, "index": index, "reason": str(exc)})
                continue
            path = folder / f"{index:05d}.wav"
            sf.write(path, wave, 16000, subtype="PCM_16")
            records.append({"audio_path": path.relative_to(target.parent).as_posix(), "transcript": row["transcription"],
                            "speaker_id": str(row["speaker_id"]) if row.get("speaker_id") is not None else "", "split": split,
                            "duration_seconds": round(len(wave) / 16000, 6), "dialect": "", "condition": "read speech"})
    with target.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["audio_path", "transcript", "speaker_id", "split", "duration_seconds", "dialect", "condition"])
        writer.writeheader()
        writer.writerows(records)
    write_json(target.parent / "provenance.json", {"source": url, "files": files, "license": "CC-BY-4.0", "attribution": "FLEURS: Few-shot Learning Evaluation of Universal Representations of Speech (Google, 2022)", "skipped": skipped,
               "speaker_limitation": "FLEURS may not expose speaker IDs. Official splits retained; speaker independence cannot then be audited."})
    print(f"Prepared {len(records)} clips; excluded {len(skipped)} clips. Run localvoice validate next.")
