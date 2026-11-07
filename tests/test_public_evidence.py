import json
from localvoice import public_evidence


def test_public_export_redacts_nested_paths_without_changing_metrics_or_source(tmp_path, monkeypatch):
    monkeypatch.setattr(public_evidence, 'ROOT', tmp_path)
    original = {'wer': 5.565493937586961, 'fingerprint': 'original-hash',
                'samples': [str(tmp_path / 'data' / 'example.wav')],
                'source': 'https://www.openslr.org/61/'}
    destination = tmp_path / 'snapshot.json'
    public_evidence.write_public_snapshot(destination, original)
    saved = json.loads(destination.read_text(encoding='utf-8'))
    assert saved['wer'] == original['wer'] and saved['fingerprint'] == 'original-hash'
    assert saved['samples'] == ['data/example.wav']
    assert original['samples'][0].startswith(str(tmp_path))
    assert saved['source'] == original['source']
    assert saved['_export']['metrics_modified'] is False
