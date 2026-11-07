import hashlib
import json
import pytest


def test_a_later_run_cannot_silently_enter_the_original_frozen_test(tmp_path, monkeypatch):
    from localvoice import independent
    monkeypatch.setattr(independent, "ROOT", tmp_path)
    folder = tmp_path / "runs"
    folder.mkdir()
    (folder / "selection-acoustic.json").write_text(json.dumps(dict(selected_experiments=["E8"], checkpoint_sha256={})))
    with pytest.raises(ValueError, match="frozen candidate"):
        independent.evaluate("E16")


def test_explicit_later_round_rejects_changed_adapter_before_inference(tmp_path, monkeypatch):
    from localvoice import independent, inference
    monkeypatch.setattr(independent, "ROOT", tmp_path)
    monkeypatch.setattr(inference, "load_model", lambda _: pytest.fail("Changed checkpoint reached inference"))
    folder = tmp_path / "runs/E16/checkpoint"
    folder.mkdir(parents=True)
    (folder / "adapter_model.safetensors").write_bytes(b"changed")
    selection = dict(selected_experiments=["E10"], evaluation_order=["E16"],
        checkpoint_files={"E16": {"adapter_model.safetensors": hashlib.sha256(b"original").hexdigest()}})
    (tmp_path / "runs/selection-regularized.json").write_text(json.dumps(selection))
    with pytest.raises(ValueError, match="Checkpoint changed"):
        independent.evaluate("E16", "runs/selection-regularized.json")
