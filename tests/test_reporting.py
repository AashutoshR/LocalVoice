from localvoice import reporting


def test_report_preserves_regressions_and_rejects_mismatched_comparisons(monkeypatch):
    common = dict(split='validation', dataset_fingerprint='a', model='whisper',
                  model_revision='fixed', language='spanish', normalization='nfc',
                  cer=5, samples=10, trainable_parameters=100, training_seconds=60)
    runs = [
        dict(id='E0', name='Baseline', metrics={**common, 'wer': 20}),
        dict(id='E1', name='Regressed', metrics={**common, 'wer': 25}),
        dict(id='E2', name='Different data', metrics={**common, 'wer': 1, 'dataset_fingerprint': 'b'}),
    ]
    monkeypatch.setattr(reporting, 'experiments', lambda: runs)
    monkeypatch.setattr(reporting, 'config', lambda: {'model': 'whisper'})
    report = reporting.comparison_markdown()
    assert '-5.00 pp' in report
    different = next(line for line in report.splitlines() if 'Different data' in line)
    assert '+19.00 pp' not in different
    assert 'regressions' in report


def test_final_selection_uses_validation_and_ignores_test_scores():
    from localvoice.finalize import choose
    common = dict(split='validation', dataset_fingerprint='a', model='whisper',
                  model_revision='fixed', language='spanish', normalization='nfc')
    runs = [dict(id='E0', metrics={**common, 'wer': 20}),
            dict(id='E1', metrics={**common, 'wer': 19}, test_metrics={'wer': 1}),
            dict(id='E5', metrics={**common, 'wer': 18}, test_metrics={'wer': 99}),
            dict(id='E6', metrics={**common, 'wer': 2, 'dataset_fingerprint': 'different'})]
    assert choose(runs)['id'] == 'E5'


def test_small_gains_use_small_baseline_and_matching_decode_protocol(monkeypatch):
    from localvoice.reporting import compatible_metrics
    common = dict(split='validation', dataset_fingerprint='a', model='small',
                  model_revision='small-fixed', language='spanish', normalization='nfc',
                  cer=3, samples=10, trainable_parameters=100, training_seconds=60,
                  evaluation_protocol=dict(batch_size=4, precision='float32', num_beams=1, max_new_tokens=225))
    runs = [dict(id='E0', name='Tiny baseline', metrics={**common, 'model': 'tiny', 'wer': 20}),
            dict(id='E7', name='Small baseline', baseline_id='E7', metrics={**common, 'wer': 7}),
            dict(id='E8', name='Small tuned', baseline_id='E7', metrics={**common, 'wer': 6})]
    monkeypatch.setattr(reporting, 'experiments', lambda: runs)
    monkeypatch.setattr(reporting, 'config', lambda: {'model': 'tiny'})
    report = reporting.comparison_markdown()
    assert '+1.00 pp vs E7' in report
    assert '+14.00 pp' not in report
    assert not compatible_metrics(common, {**common, 'evaluation_protocol': {'batch_size': 1}})
    assert not compatible_metrics({**common, 'generation_config_sha256': 'a'},
                                  {**common, 'generation_config_sha256': 'b'})
