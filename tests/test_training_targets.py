import pytest
pa = pytest.importorskip("pyarrow")
pq = pytest.importorskip("pyarrow.parquet")
from localvoice import training
from localvoice.core import normalize


def test_punctuation_restoration_preserves_words_and_reads_train_only(tmp_path, monkeypatch):
    folder = tmp_path / "data/parquet"
    folder.mkdir(parents=True)
    pq.write_table(pa.table({
        "transcription": ["hola señor", "tengo dos libros"],
        "raw_transcription": ["¡Hola, señor!", "Tengo 2 libros."],
    }), folder / "train-0.parquet")
    # A corrupt held-out shard must never be accessed for target construction.
    (folder / "test-0.parquet").write_bytes(b"not training data")
    monkeypatch.setattr(training, "ROOT", tmp_path)
    rows = [{"audio_path": f"{i}.wav", "transcript": text, "split": "train"}
            for i, text in enumerate(["hola señor", "tengo dos libros"])]
    targets = training.training_targets(rows, "punctuated")
    assert targets["0.wav"] == "¡Hola, señor!"
    assert targets["1.wav"] == "Tengo dos libros."
    assert all(normalize(targets[r["audio_path"]]) == normalize(r["transcript"]) for r in rows)
    with pytest.raises(ValueError, match="training split"):
        training.training_targets([{**rows[0], "split": "validation"}], "punctuated")


def test_published_natural_targets_cannot_change_transcript_words(tmp_path, monkeypatch):
    monkeypatch.setattr(training, "ROOT", tmp_path)
    row=dict(audio_path="clip.wav",transcript="podés venir",training_text="¿Podés venir?",split="train")
    assert training.training_targets([row],"punctuated")["clip.wav"]=="¿Podés venir?"
    with pytest.raises(ValueError,match="exact transcript words"):
        training.training_targets([{**row,"training_text":"¿Podés ir?"}],"punctuated")
