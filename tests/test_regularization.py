import pytest
torch = pytest.importorskip("torch")
from localvoice.regularization import FisherPenalty, freeze_lower_encoder


def test_lower_freezing_preserves_upper_gradients():
    transformers = pytest.importorskip("transformers")
    WhisperConfig, WhisperForConditionalGeneration = transformers.WhisperConfig, transformers.WhisperForConditionalGeneration
    model = WhisperForConditionalGeneration(WhisperConfig(vocab_size=32, d_model=8, encoder_layers=3,
        decoder_layers=1, encoder_attention_heads=2, decoder_attention_heads=2, encoder_ffn_dim=16,
        decoder_ffn_dim=16, pad_token_id=0, bos_token_id=1, eos_token_id=2, decoder_start_token_id=1))
    before = model.model.encoder.layers[0].self_attn.q_proj.weight.detach().clone()
    record = freeze_lower_encoder(model, 2)
    assert record['frozen_lower_blocks'] == 2
    assert not model.model.encoder.conv1.weight.requires_grad
    assert not model.model.encoder.layers[1].self_attn.q_proj.weight.requires_grad
    assert model.model.encoder.layers[2].self_attn.q_proj.weight.requires_grad
    optimizer = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=.1)
    sum(p.square().sum() for p in model.parameters() if p.requires_grad).backward()
    optimizer.step()
    assert torch.equal(before, model.model.encoder.layers[0].self_attn.q_proj.weight)
    assert model.model.encoder.layers[2].self_attn.q_proj.weight.grad is not None
    with pytest.raises(ValueError):
        freeze_lower_encoder(model, 4)


def test_fisher_penalty_protects_important_weights_and_normalizes_trace():
    model = torch.nn.Linear(2, 1, bias=False)
    penalty = FisherPenalty(model, {'weight': torch.tensor([[9., 1.]])})
    assert penalty().item() == 0
    with torch.no_grad():
        model.weight.add_(1)
    penalty().backward()
    assert penalty().item() == pytest.approx(1.)
    assert model.weight.grad[0, 0] / model.weight.grad[0, 1] == pytest.approx(9.)
    with pytest.raises(ValueError):
        FisherPenalty(model, {'weight': torch.zeros(1, 2)})
    with pytest.raises(ValueError):
        FisherPenalty(model, {'weight': torch.tensor([[float('nan'), 1.]])})


def test_fisher_loader_rejects_tampering_and_wrong_anchor(tmp_path, monkeypatch):
    save_file = pytest.importorskip("safetensors.torch").save_file
    from localvoice import fisher
    from localvoice.core import write_json, dataset_fingerprint
    monkeypatch.setattr(fisher, 'ROOT', tmp_path)
    audio = tmp_path / 'train.wav'
    audio.write_bytes(b'fixture audio')
    row = {'audio_path': str(audio), 'transcript': 'hola', 'split': 'train', 'duration_seconds': 1.0}
    monkeypatch.setattr(fisher, 'read_manifest', lambda: [row])
    path = tmp_path / 'fisher.safetensors'
    save_file({'weight': torch.ones(1, 2)}, str(path))
    cfg = {'model': 'tiny', 'language': 'spanish'}
    metadata = dict(project=cfg, dataset_fingerprint='base', anchor_experiment='E11', anchor_sha256='anchor',
        split='train', fisher_sha256=fisher.digest(path), training_audio_paths=[str(audio)], sample_fingerprint=dataset_fingerprint([row]))
    write_json(path.with_suffix('.json'), metadata)
    hp = {'ewc_fisher':'fisher.safetensors','ewc_lambda':10000.}
    ancestry = {'initial_experiment':'E11','initial_weights_sha256':'anchor'}
    values, proof = fisher.load_verified_fisher(hp, cfg, 'base', ancestry)
    assert values['weight'].shape == (1, 2) and proof['anchor'] == 'E11'
    del values
    import gc
    gc.collect()
    with pytest.raises(ValueError, match='anchor'):
        fisher.load_verified_fisher(hp, cfg, 'base', dict(initial_experiment='E11', initial_weights_sha256='changed'))
    metadata['training_audio_paths'] = ['test.wav']
    write_json(path.with_suffix('.json'), metadata)
    with pytest.raises(ValueError, match='training split'):
        fisher.load_verified_fisher(hp, cfg, 'base', ancestry)
    metadata['training_audio_paths'] = [str(audio)]
    write_json(path.with_suffix('.json'), metadata)
    path.write_bytes(b'tampered')
    with pytest.raises(ValueError, match='changed'):
        fisher.load_verified_fisher(hp, cfg, 'base', ancestry)
