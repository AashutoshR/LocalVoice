"""Fetch the pinned official model into a normal Windows folder and verify it."""
import hashlib
import json
import os
from pathlib import Path


def main():
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    from huggingface_hub import HfApi, snapshot_download
    root = Path(__file__).resolve().parents[1]
    settings = json.loads((root / "configs/whisper-small.json").read_text(encoding="utf-8"))
    repo, revision = settings["model"], settings["model_revision"]
    destination = root / settings["local_model_path"]
    snapshot_download(repo, revision=revision, local_dir=destination,
                      allow_patterns=["*.json", "*.txt", "model.safetensors"], max_workers=2)
    info = HfApi().model_info(repo, revision=revision, files_metadata=True)
    expected = next(f.lfs.sha256 for f in info.siblings if f.rfilename == "model.safetensors")
    digest = hashlib.sha256()
    with (destination / "model.safetensors").open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError("Model weight checksum differs from official repository metadata")
    provenance = {"repo": repo, "revision": info.sha, "file": "model.safetensors",
                  "sha256": digest.hexdigest(), "verified_against_hub_lfs": True}
    (destination / "source.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {repo} at {info.sha}: {destination}")


if __name__ == "__main__":
    main()
