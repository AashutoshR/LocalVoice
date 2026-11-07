import csv
import io
import numpy as np
import pytest
import soundfile as sf
from localvoice.audio import augment, decode_audio
from localvoice.core import normalize, score, validate_manifest


def test_atomic_json_retries_temporary_windows_lock(tmp_path, monkeypatch):
    import json
    from pathlib import Path
    from localvoice.core import write_json
    original = Path.replace
    calls = []
    def transient_lock(source, target):
        calls.append(source)
        if len(calls) == 1:
            raise PermissionError("temporary reader lock")
        return original(source, target)
    monkeypatch.setattr(Path, "replace", transient_lock)
    target = tmp_path / "training.json"
    target.write_text('{"status":"running"}', encoding="utf-8")
    write_json(target, {"status": "completed"})
    assert json.loads(target.read_text()) == {"status": "completed"}
    assert len(calls) == 2
    assert not list(tmp_path.glob("*.tmp"))


def test_scoring_counts_and_normalization():
    assert normalize('  ¡Hola, MUNDO! ') == 'hola mundo'
    assert normalize('¿Qué tal? ¡Español!') == 'qué tal español'
    result = score(['one two three'], ['one four'])
    assert result['substitutions'] == 1
    assert result['deletions'] == 1
    assert result['insertions'] == 0
    assert result['common_errors']['substitutions'][0]['count'] == 1
    assert result['wer'] == pytest.approx(200 / 3)
    assert score(['hello world'], ['HELLO, world!'])['wer'] == 0
    with pytest.raises(ValueError):
        score(['!!!'], ['hello'])


def test_audio_resampling_and_limits():
    buffer = io.BytesIO()
    sf.write(buffer, np.zeros((8000, 2)), 8000, format='WAV')
    wave = decode_audio(buffer.getvalue())
    assert wave.shape == (16000,)
    with pytest.raises(ValueError):
        decode_audio(buffer.getvalue(), max_seconds=.5)


def test_augmentation_is_reproducible_bounded_and_finite():
    wave = np.sin(np.arange(16000) * .04).astype(np.float32)
    a = augment(wave, np.random.default_rng(42))
    b = augment(wave, np.random.default_rng(42))
    assert np.array_equal(a, b)
    assert np.max(np.abs(a)) <= 1
    assert np.isfinite(a).all()
    assert abs(len(a) - len(wave)) < 1000
    long_wave = np.ones(480000, dtype=np.float32) * .2
    for seed in range(5):
        assert len(augment(long_wave, np.random.default_rng(seed))) <= 480000


def test_manifest_detects_speaker_leak_and_duplicate_content(tmp_path):
    path = tmp_path / 'manifest.csv'
    rows = []
    for i, split in enumerate(['train', 'validation', 'test']):
        audio = tmp_path / f'{i}.wav'
        sf.write(audio, np.ones(1600) * i / 10, 16000)
        rows.append([audio.name, 'hablamos español', 'same-speaker', split, .1])
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['audio_path', 'transcript', 'speaker_id', 'split', 'duration_seconds'])
        writer.writerows(rows)
    result = validate_manifest(path)
    assert not result['valid']
    assert any('across splits' in e for e in result['errors'])
    for row in rows:
        row[2] = ''
    (tmp_path / '1.wav').write_bytes((tmp_path / '0.wav').read_bytes())
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['audio_path', 'transcript', 'speaker_id', 'split', 'duration_seconds'])
        writer.writerows(rows)
    result = validate_manifest(path)
    assert any('duplicate' in e for e in result['errors'])
    assert result['warnings']


def test_training_only_supplement_is_valid_without_weakening_default_split_checks(tmp_path):
    audio = tmp_path / 'train.wav'
    sf.write(audio, np.zeros(1600), 16000)
    manifest = tmp_path / 'extra.csv'
    with manifest.open('w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(['audio_path', 'transcript', 'speaker_id', 'split', 'duration_seconds'])
        writer.writerow([audio.name, 'hablamos español', 'speaker', 'train', .1])
    assert validate_manifest(manifest, required_splits=('train',))['valid']
    assert not validate_manifest(manifest)['valid']
    sf.write(audio, np.zeros(1600), 8000)
    assert not validate_manifest(manifest, required_splits=('train',))['valid']
