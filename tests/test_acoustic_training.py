import hashlib
import json
from types import SimpleNamespace
import pytest
from localvoice import training


def test_encoder_decoder_groups_cover_all_trainable_weights():
    torch = pytest.importorskip("torch")
    model = torch.nn.Module()
    model.model = torch.nn.Module()
    model.model.encoder = torch.nn.Linear(2, 3)
    model.decoder = torch.nn.Linear(3, 2)
    groups, rates = training.optimizer_groups(model, dict(learning_rate_encoder=2e-6, learning_rate_decoder=5e-7), 2e-6)
    ids = [id(p) for g in groups for p in g['params']]
    assert len(ids) == len(set(ids))
    assert set(ids) == {id(p) for p in model.parameters() if p.requires_grad}
    assert rates == {'encoder': 2e-6, 'decoder': 5e-7}
    model.model.encoder.requires_grad_(False)
    groups, rates = training.optimizer_groups(model, dict(learning_rate_encoder=2e-6, learning_rate_decoder=5e-7), 2e-6)
    assert list(rates) == ['decoder']


def test_specaugment_mask_excludes_padding():
    torch = pytest.importorskip("torch")
    mask = training.speech_mask(torch.zeros(80, 3000), 5.76)
    assert mask.shape == (3000,) and mask.sum().item() == 576
    assert mask[:576].all() and not mask[576:].any()
    assert training.speech_mask(torch.zeros(80, 3000), 31).sum().item() == 3000
    with pytest.raises(ValueError):
        training.speech_mask(torch.zeros(80, 3000), 0)


def test_warm_start_requires_matching_data_and_records_weight_hash(tmp_path, monkeypatch):
    monkeypatch.setattr(training, 'ROOT', tmp_path)
    folder = tmp_path / 'runs/E8'
    (folder / 'checkpoint').mkdir(parents=True)
    (folder / 'checkpoint/model.safetensors').write_bytes(b'weights')
    (folder / 'checkpoint/config.json').write_text('{}')
    cfg = {'model': 'small', 'language': 'spanish'}
    (folder / 'training.json').write_text(json.dumps(dict(status='completed', project=cfg, dataset_fingerprint='same', training_seconds=12)))
    (folder / 'metrics-test.json').write_bytes(b'corrupt and must not be read')
    source, record = training.initial_checkpoint({'initialize_from': 'E8'}, cfg, 'same')
    assert source == folder / 'checkpoint'
    assert record['initial_weights_sha256'] == hashlib.sha256(b'weights').hexdigest()
    assert record['parent_training_seconds'] == 12
    with pytest.raises(ValueError, match='matching'):
        training.initial_checkpoint({'initialize_from': 'E8'}, cfg, 'changed')


def test_additional_training_rejects_eval_rows_and_duplicate_eval_text(monkeypatch):
    monkeypatch.setattr(training, 'validate_manifest', lambda _, **kwargs: {'valid': True})
    extra = [dict(split='test', transcript='hola')]
    monkeypatch.setattr(training, 'read_manifest', lambda _: extra)
    hp = {'additional_training_manifest': 'extra.csv'}
    with pytest.raises(ValueError, match='train-only'):
        training.additional_training_rows(hp, [])
    extra[0]['split'] = 'train'
    with pytest.raises(ValueError, match='duplicates'):
        training.additional_training_rows(hp, [dict(split='validation', transcript='HOLA!')])
    assert training.additional_training_rows(hp, [dict(split='validation', transcript='adios')]) == extra
