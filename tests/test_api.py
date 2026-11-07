import io
import numpy as np
import soundfile as sf
import pytest
from fastapi.testclient import TestClient
from localvoice.server import app
from localvoice.server import matrix_status as read_job_status

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_background_jobs(monkeypatch):
    monkeypatch.setattr('localvoice.server.matrix_status', lambda: None)


def test_frontend_and_status():
    assert client.get('/').status_code == 200
    assert 'LocalVoice' in client.get('/').text
    result = client.get('/api/status').json()
    assert {'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E23'} == {e['id'] for e in result['experiments']}
    assert result['project']['language'] == 'spanish'
    assert client.get('/assets/app.js').status_code == 200
    assert client.get('/api/report').status_code == 200
    assert client.get('/api/export').headers['content-disposition'].endswith('"localvoice-results.json"')


def test_invalid_audio_and_unknown_model():
    assert client.post('/api/transcribe', files={'audio': ('bad.wav', b'not audio')}).status_code == 400
    assert client.post('/api/transcribe', data={'experiment': 'E99'}, files={'audio': ('bad.wav', b'x')}).status_code == 400
    assert client.post('/api/transcribe', data={'reference': '!!!'}, files={'audio': ('bad.wav', b'x')}).status_code == 400


def test_transcription_scores_real_api_contract(monkeypatch):
    import localvoice.inference
    monkeypatch.setattr(localvoice.inference, 'transcribe', lambda audio, experiment: {'transcript': 'hablamos español', 'experiment': experiment, 'latency_seconds': .1, 'load_seconds': 0, 'total_seconds': .1, 'device': 'cpu'})
    buffer = io.BytesIO()
    sf.write(buffer, np.zeros(16000), 16000, format='WAV')
    response = client.post('/api/transcribe', files={'audio': ('clip.wav', buffer.getvalue())}, data={'reference': 'hablamos español'})
    assert response.status_code == 200
    assert response.json()['metrics']['wer'] == 0
    assert response.json()['duration_seconds'] == 1


def test_playground_sample_uses_training_split_only(monkeypatch, tmp_path):
    import localvoice.server
    path = tmp_path / 'sample.wav'
    sf.write(path, np.zeros(1600), 16000)
    monkeypatch.setattr(localvoice.server, 'read_manifest', lambda: [
        {'split': 'test', 'transcript': 'held out'},
        {'split': 'train', 'transcript': 'training sample', 'duration_seconds': .1, 'audio_path': str(path)},
    ])
    assert client.get('/api/sample').json()['transcript'] == 'training sample'
    assert client.get('/api/sample/audio').content == path.read_bytes()


def test_transcription_does_not_compete_with_training(monkeypatch):
    monkeypatch.setattr('localvoice.server.matrix_status', lambda: {'status': 'running'})
    response = client.post('/api/transcribe', files={'audio': ('clip.wav', b'unused')})
    assert response.status_code == 409
    assert 'GPU' in response.json()['detail']
    monkeypatch.setattr('localvoice.server.matrix_status', lambda: {'status': 'queued'})
    assert client.post('/api/transcribe', files={'audio': ('clip.wav', b'unused')}).status_code == 409


def test_job_status_prioritizes_active_work_and_keeps_failures_visible(monkeypatch, tmp_path):
    import json
    import localvoice.server
    monkeypatch.setattr(localvoice.server, 'ROOT', tmp_path)
    folder = tmp_path / 'runs'
    folder.mkdir()
    (folder / 'matrix.json').write_text(json.dumps({'status': 'running', 'started_at': '2026-01-01'}))
    (folder / 'improvement.json').write_text(json.dumps({'status': 'failed', 'started_at': '2026-02-01'}))
    assert read_job_status()['status'] == 'running'
    (folder / 'matrix.json').write_text(json.dumps({'status': 'completed', 'started_at': '2026-01-01'}))
    assert read_job_status()['status'] == 'failed'
    (folder / 'followup.json').write_text(json.dumps({'status': 'queued', 'started_at': '2026-03-01'}))
    assert read_job_status()['status'] == 'queued'
    (folder / 'matrix.json').write_text(json.dumps({'status': 'running', 'started_at': '2026-01-01'}))
    assert read_job_status()['status'] == 'running'
