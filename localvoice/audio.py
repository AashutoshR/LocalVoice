import io
from math import gcd
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


def decode_audio(source, max_seconds=30):
    """Decode bounded WAV/FLAC/OGG; browser recordings are converted to WAV."""
    stream = io.BytesIO(source) if isinstance(source, bytes) else source
    with sf.SoundFile(stream) as f:
        if f.frames / f.samplerate > max_seconds or f.frames == 0:
            raise ValueError(f"Audio must contain 0–{max_seconds} seconds of speech.")
        rate = f.samplerate
        audio = f.read(dtype="float32", always_2d=True).mean(axis=1)
    if not np.isfinite(audio).all():
        raise ValueError("Audio contains non-finite samples.")
    if rate != 16000:
        factor = gcd(rate, 16000)
        audio = resample_poly(audio, 16000 // factor, rate // factor).astype(np.float32)
    return audio


def augment(audio, rng):
    """Conservative train-only speed perturbation and randomized 20–35 dB noise."""
    # Avoid truncating a slowed clip: its transcript must remain intact.
    speed = float(rng.uniform(max(0.95, len(audio) / 480000), 1.05))
    length = round(len(audio) / speed)
    shifted = np.interp(np.linspace(0, len(audio) - 1, length), np.arange(len(audio)), audio)
    rms = float(np.sqrt(np.mean(shifted ** 2)))
    noise = rng.normal(0, max(rms, 1e-6) / 10 ** (rng.uniform(20, 35) / 20), length)
    return np.clip(shifted + noise, -1, 1).astype(np.float32)
