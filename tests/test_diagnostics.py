import json
import pytest
from localvoice import diagnostics


def test_paired_errors_and_interval_use_the_same_clips(tmp_path, monkeypatch):
    base = [{"audio_path": f"{i}.wav", "transcript": "uno dos", "hypothesis": "uno tres"} for i in range(3)]
    tuned = [{**r, "hypothesis": "uno dos"} for r in base]
    for name, rows in [("E0", base), ("E5", tuned)]:
        folder = tmp_path / "runs" / name
        folder.mkdir(parents=True)
        (folder / "predictions-validation.json").write_text(json.dumps(rows))
    monkeypatch.setattr(diagnostics, "ROOT", tmp_path)
    result = diagnostics.compare_predictions("E5", repetitions=100)
    assert result["errors_removed"] == 3
    assert result["wer_reduction_pp"] == 50
    assert result["wer_reduction_95_interval_pp"] == [50, 50]
    assert result["utterances_improved"] == 3
    tuned[0]["audio_path"] = "different.wav"
    (tmp_path / "runs/E5/predictions-validation.json").write_text(json.dumps(tuned))
    with pytest.raises(ValueError, match="identical ordered"):
        diagnostics.compare_predictions("E5", repetitions=100)


def test_cluster_bootstrap_resamples_speakers_not_individual_clips(tmp_path, monkeypatch):
    base = [dict(audio_path=f"{i}.wav", transcript="uno dos", hypothesis="uno tres",
                 speaker_id="a" if i < 3 else "b") for i in range(4)]
    tuned = [{**r, "hypothesis": "uno dos"} for r in base]
    for name, rows in (("E0", base), ("E11", tuned)):
        folder = tmp_path / "runs" / name
        folder.mkdir(parents=True)
        (folder / "predictions-mls-test.json").write_text(json.dumps(rows))
    monkeypatch.setattr(diagnostics, "ROOT", tmp_path)
    result = diagnostics.compare_predictions("E11", split="mls-test", repetitions=100, cluster_field="speaker_id")
    assert result["sampling_units"] == 2
    assert result["samples"] == 4
    assert result["wer_reduction_95_interval_pp"] == [50, 50]
