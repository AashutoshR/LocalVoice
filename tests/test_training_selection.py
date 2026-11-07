"""Exercise real optimizer updates and checkpoint selection on a tiny CPU model."""
import json
from pathlib import Path
from types import SimpleNamespace
import pytest


def test_mid_epoch_validation_saves_best_checkpoint_and_stops(tmp_path, monkeypatch):
    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")
    pytest.importorskip("peft")
    from localvoice import training
    source = Path(__file__).resolve().parents[1] / "data/models/whisper-small"
    if not (source / "tokenizer.json").exists():
        pytest.skip("Optional local tokenizer assets not downloaded")
    tokenizer = transformers.WhisperTokenizerFast.from_pretrained(source, local_files_only=True)

    class Processor:
        def __init__(self):
            self.tokenizer = tokenizer

        def __call__(self, *args, **kwargs):
            return SimpleNamespace(input_features=torch.zeros(1, 80, 10))

        def save_pretrained(self, folder):
            self.tokenizer.save_pretrained(folder)

    cfg = transformers.WhisperConfig(vocab_size=51865, d_model=16, encoder_layers=1,
        decoder_layers=1, encoder_attention_heads=2, decoder_attention_heads=2,
        encoder_ffn_dim=32, decoder_ffn_dim=32, max_source_positions=5,
        max_target_positions=64, decoder_start_token_id=50258, pad_token_id=50257,
        eos_token_id=50257)
    model = transformers.WhisperForConditionalGeneration(cfg)
    model.config.apply_spec_augment = True  # Inherited from an augmented parent stage.
    monkeypatch.setattr(transformers.WhisperProcessor, "from_pretrained", lambda *a, **k: Processor())
    monkeypatch.setattr(transformers.WhisperForConditionalGeneration, "from_pretrained", lambda *a, **k: model)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(training, "ROOT", tmp_path)
    project = dict(model="toy", model_revision="fixed", language="spanish")
    monkeypatch.setattr(training, "experiment_config", lambda _: project)
    monkeypatch.setattr(training, "canonical_generation", lambda *a: "toy-decoding")
    rows = []
    for i in range(10):
        audio = tmp_path / f"{i}.wav"
        audio.write_bytes(str(i).encode())
        rows.append(dict(audio_path=str(audio), transcript="hola mundo", split="train" if i < 8 else "validation"))
    monkeypatch.setattr(training, "checked_rows", lambda: (rows, {"valid": True}))
    monkeypatch.setattr(training, "dataset_fingerprint", lambda _: "fixed-data")
    monkeypatch.setattr(training, "decode_audio", lambda _: torch.zeros(100).numpy())
    scores = iter([20, 19, 21, 22])
    monkeypatch.setattr(training, "evaluate_rows", lambda *a, **k: ({"wer": next(scores), "cer": 5}, []))
    settings = dict(seed=42, batch_size=2, gradient_accumulation_steps=1, epochs=3,
        learning_rate_full=.0001, learning_rate_lora=.0001, weight_decay=0,
        warmup_ratio=0, early_stopping_patience=2, validation_interval_updates=1,
        freeze_encoder=True)
    hp = tmp_path / "training.json"
    hp.write_text(json.dumps(settings))
    training.train("E8", hp)
    result = json.loads((tmp_path / "runs/E8/training.json").read_text())
    history = json.loads((tmp_path / "runs/E8/history.json").read_text())
    progress = json.loads((tmp_path / "runs/E8/progress.json").read_text())
    assert result["status"] == "completed"
    assert result["best_epoch"] == .5 and result["best_optimizer_step"] == 2
    assert result["optimizer_steps"] == 4 and result["best_validation_wer"] == 19
    assert [h["epoch"] for h in history] == [.25, .5, .75, 1]
    assert progress["epochs_completed"] == 1 and progress["validation_checks"] == 4
    assert result["tokenizer_prefix_verified"] is True
    assert all(not p.requires_grad for p in model.model.encoder.parameters())
    assert model.config.apply_spec_augment is False
