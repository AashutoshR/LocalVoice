import copy
import json
import pytest


def test_decoder_adapters_update_while_base_stays_fixed_and_merge_preserves_logits(tmp_path, monkeypatch):
    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")
    pytest.importorskip("peft")
    from localvoice.training import configure_lora
    from localvoice import weight_audit
    torch.manual_seed(42)
    cfg = transformers.WhisperConfig(vocab_size=32, d_model=16, encoder_layers=1,
        decoder_layers=1, encoder_attention_heads=2, decoder_attention_heads=2,
        encoder_ffn_dim=32, decoder_ffn_dim=32, max_source_positions=5,
        max_target_positions=16, decoder_start_token_id=1, pad_token_id=0, eos_token_id=2)
    base = transformers.WhisperForConditionalGeneration(cfg)
    original = [(parameter, parameter.detach().clone()) for parameter in base.parameters()]
    hp = dict(lora_rank=2, lora_alpha=4, lora_dropout=0., freeze_encoder=True,
              lora_targets=r"model\.decoder\.layers\.\d+\.(self_attn|encoder_attn)\.(q_proj|v_proj)")
    model = configure_lora(base, hp).eval()
    names = [name for name, p in model.named_parameters() if p.requires_grad]
    assert len(names) == 8
    assert all(".model.decoder." in name for name in names)
    inputs = dict(input_features=torch.randn(1, 80, 10), labels=torch.tensor([[3, 4, 2]]))
    optimizer = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=.1)
    model(**inputs).loss.backward()
    optimizer.step()
    assert all(not parameter.requires_grad and torch.equal(parameter, before) for parameter, before in original)
    with torch.no_grad():
        expected = model(**inputs).logits
    folder = tmp_path / "runs/E16"
    model.save_pretrained(folder / "checkpoint", save_embedding_layers=False)
    (folder / "training.json").write_text(json.dumps(dict(base_parameters_frozen=True,
        trainable_parameter_names=names, trainable_parameters=sum(p.numel() for p in model.parameters() if p.requires_grad))))
    monkeypatch.setattr(weight_audit, "ROOT", tmp_path)
    proof = weight_audit.audit_adapter("E16")
    assert proof["updated_b_tensors"] == 4
    merged = model.merge_and_unload().eval()
    with torch.no_grad():
        assert torch.allclose(expected, merged(**inputs).logits, atol=1e-5)
