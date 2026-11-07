import pytest


def test_acoustic_selection_uses_matched_validation_not_test_or_changed_weights():
    from localvoice.assess import choose
    common = dict(split="validation", dataset_fingerprint="fixed", model="small",
                  model_revision="pinned", language="spanish", normalization="nfc")
    runs = [dict(id="E7", metrics={**common, "wer": 6}),
            dict(id="E8", metrics={**common, "wer": 5.5}, independent_metrics={"wer": 99}),
            dict(id="E10", metrics={**common, "wer": 5.6}, independent_metrics={"wer": 0})]
    assert choose(runs, "E7", {"E8", "E10"})["id"] == "E8"
    runs[-1]["metrics"]["dataset_fingerprint"] = "different"
    with pytest.raises(ValueError, match="compatible"):
        choose(runs, "E7", {"E8", "E10"})


def test_saved_weight_audit_distinguishes_encoder_and_decoder(tmp_path, monkeypatch):
    torch = pytest.importorskip("torch")
    from safetensors.torch import save_file
    from localvoice import weight_audit
    monkeypatch.setattr(weight_audit, "ROOT", tmp_path)
    before = {"model.encoder.weight": torch.ones(3), "model.decoder.weight": torch.ones(2)}
    after = {"model.encoder.weight": torch.tensor([1., 2., 1.]), "model.decoder.weight": torch.ones(2)}
    for name, data in (("parent", before), ("child", after)):
        folder = tmp_path / "runs" / name / "checkpoint"
        folder.mkdir(parents=True)
        save_file(data, folder / "model.safetensors")
    (tmp_path / "runs/child/training.json").write_text('{}')
    result = weight_audit.audit("child", "parent")
    assert result["groups"]["encoder"]["changed_parameters"] == 1
    assert result["groups"]["decoder"]["changed_parameters"] == 0
    assert result["groups"]["encoder"]["relative_l2_change"] > 0
