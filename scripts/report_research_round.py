"""Publish measured controlled-ablation results after all GPU jobs complete."""
from localvoice.public_evidence import write_public_snapshot
import json
from datetime import datetime, timezone
from localvoice.core import ROOT, experiments, write_json, experiment_config
from localvoice.reporting import compatible_metrics, write_results
from localvoice.diagnostics import compare_predictions


def errors(m):
    return sum(m[k] for k in ('substitutions', 'deletions', 'insertions'))


def main():
    state = json.loads((ROOT / 'runs/research-round.json').read_text(encoding='utf-8'))
    if state['status'] != 'completed':
        raise ValueError('Finish all prespecified experiments before publishing conclusions')
    followup_path = ROOT / 'runs/ewc-followup.json'
    if followup_path.exists() and json.loads(followup_path.read_text(encoding='utf-8'))['status'] != 'completed':
        raise ValueError('Finish the frozen stronger-EWC follow-up first')
    runs = {r['id']:r for r in experiments()}
    extra = ['E23'] if runs.get('E23',{}).get('metrics') else []
    identity_keys = ['initial_weights_sha256', 'training_target_sha256', 'dataset_fingerprint',
        'training_dataset_fingerprint', 'generation_config_sha256', 'decoder_prefix_tokens', 'learning_rates']
    identity_proof = {}
    for name, ids in (('small', ['E18','E19','E20']), ('tiny', ['E21','E22']+extra)):
        for key in identity_keys:
            if any(runs[i]['training'][key] != runs[ids[0]]['training'][key] for i in ids):
                raise ValueError(f'Controlled inputs differ: {name} {key}')
        identity_proof[name] = dict(runs=ids, identical_fields=identity_keys)
    write_json(ROOT / 'runs/research-input-audit.json', identity_proof)
    selection_path = ROOT / ('runs/selection-research-strong.json' if extra else 'runs/selection-research.json')
    selected = json.loads(selection_path.read_text(encoding='utf-8'))
    lines = ['# Research methods: controlled fine-tuning results', '',
        'Updated ' + datetime.now(timezone.utc).strftime('%d %B %Y') + '. Same existing Tiny and Small backbones; original FLEURS validation only. '
        'These are observed development results, not a fresh blind test or a multi-seed confirmation.', '',
        '## Small: lower-encoder freezing', '',
        '| Recipe | WER | CER | Word errors | Trainable weights | Stage time | Peak allocated GPU memory |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for identifier in ('E7', 'E8', 'E10', 'E18', 'E19', 'E20'):
        run, m = runs[identifier], runs[identifier]['metrics']
        tr = run.get('training') or {}
        ram = f"{tr['peak_gpu_memory_mb']:.0f} MB" if tr.get('peak_gpu_memory_mb') else '—'
        lines.append(f"| {identifier} · {run['name']} | {m['wer']:.4f}% | {m['cer']:.4f}% | {errors(m):,} | "
            f"{m['trainable_parameters']:,} | {tr.get('training_seconds',0)/60:.1f} min | {ram} |")
    for identifier, control in [('E19','E18'), ('E20','E18'), ('E22','E21')]+[('E23','E21') for _ in extra]:
        a, b = runs[control]['metrics'], runs[identifier]['metrics']
        if not compatible_metrics(a,b):
            raise ValueError('Controlled comparison protocol differs')
        p = compare_predictions(identifier, baseline_id=control, primary=False)
        low, high = p['wer_reduction_95_interval_pp']
        if identifier == 'E22':
            lines += ['', '## Tiny: training-only Fisher EWC', '',
                '| Recipe | WER | CER | Word errors | Stage time |', '| --- | --- | --- | --- | --- |']
            for i in ['E0', 'E11', 'E17', 'E21', 'E22']+extra:
                m, tr = runs[i]['metrics'], runs[i].get('training') or {}
                lines.append(f"| {i} · {runs[i]['name']} | {m['wer']:.4f}% | {m['cer']:.4f}% | {errors(m):,} | {tr.get('training_seconds',0)/60:.1f} min |")
        lines += ['', f"**{identifier} versus matched {control}:** {a['wer']:.4f}% → {b['wer']:.4f}% WER; "
            f"{abs(errors(a)-errors(b)):,} {'fewer' if errors(a)>=errors(b) else 'more'} word error{'s' if abs(errors(a)-errors(b))!=1 else ''} ({100*(a['wer']-b['wer'])/a['wer']:+.2f}% relative reduction). "
            f"Paired utterance-bootstrap interval for WER reduction: {low:.3f} to {high:.3f} pp; "
            f"{p['utterances_improved']} clips improve, {p['utterances_worsened']} worsen. Negative reduction means regression. "
            'Intervals are exploratory after validation selection; speaker IDs are unavailable.']
    lines += ['', '## Which checkpoint is retained?', '']
    for backbone, old in (('small','E10'), ('tiny','E11')):
        choice = selected['selected'][backbone]['experiment']
        a, b = runs[old]['metrics'], runs[choice]['metrics']
        delta = a['wer'] - b['wer']
        lines += [f"- {backbone.capitalize()}: **{choice}**, {b['wer']:.4f}% WER. "
            f"Compared with previous {old}: {delta:+.4f} pp WER reduction, {errors(a)-errors(b):+,} fewer word errors. "
            + ('The earlier checkpoint remains selected; the new methods did not beat it.' if choice == old else
               'This is an observed validation gain; independent generalization remains unverified.')]
        write_json(ROOT / f'runs/selection-{backbone}-research.json', dict(selected_experiment=choice,
            validation_wer=b['wer'], project=experiment_config(choice), policy=selected['policy'],
            frozen_at=selected['frozen_at']))
        if choice != old:
            compare_predictions(choice, baseline_id=old, primary=False)
    lines += ['', '## Implementation and limits', '',
        '- Small arms share E8 initialization, source clips, seed, learning-rate schedule and augmentation. E19/E20 additionally freeze the acoustic front end plus the specified lower blocks. Actual stopping times can differ.',
        '- Tiny arms share E11 initialization and replay data. E22 adds a unit-trace diagonal empirical Fisher penalty with lambda 10000, estimated from 128 original training clips. Its preparation time is recorded separately.',
        '- Saved-weight audits verify protected layers stayed unchanged. Fisher hashes and training-only sample membership are verified before adaptation.',
        '- `runs/research-input-audit.json` verifies identical initial weights, actual training text/audio, prefix, generation settings and learning rates within both controlled comparisons.',
        '- No existing FLEURS/MLS test or Latin holdout was used for coefficient/layer/checkpoint selection. No new holdout evaluation is claimed in this round.',
        '- A smaller training-memory footprint is a separate outcome from recognition accuracy. Inference architecture size stays the same within each backbone.',
        '- E23 is a separately preserved follow-up at lambda 1e7, chosen from E22 training penalty scale before reading its validation scores. The original five recipes and first selection are unchanged.',
        '- Method details and source papers: `docs/RESEARCH_METHODS_IMPLEMENTATION.md`; configs: `configs/research-e18.json` through `research-e23.json`.', '']
    content = '\n'.join(lines)
    (ROOT / 'docs/RESEARCH_METHOD_RESULTS.md').write_text(content,encoding='utf-8')
    write_public_snapshot(ROOT / 'docs/evidence/research-methods-round.json', dict(selection=selected,
        runs={i:{k:runs[i].get(k) for k in ('id','name','metrics','training','weight_audit')}
              for i in ['E18','E19','E20','E21','E22']+extra}))
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    if '## Research-method experiments in progress' in text:
        before, rest = text.split('## Research-method experiments in progress',1)
        _, after = rest.split('## Fine-tuning results',1)
        text = before + '## Fine-tuning results' + after
    marker = '## Research-method implementation results'
    insertion = '## Latest research-method results\n\nThe controlled E18–E23 round tested partial encoder freezing and Fisher-weighted elastic weight consolidation (EWC) on the existing backbones.\n\n'
    control, frozen = runs['E18'], runs['E20']
    ram_a, ram_b = control['training']['peak_gpu_memory_mb'], frozen['training']['peak_gpu_memory_mb']
    a, b = control['metrics'], frozen['metrics']
    insertion += (f"**Partial freezing:** nine frozen lower blocks reduce peak allocated training memory "
        f"{ram_a:,.0f} → {ram_b:,.0f} MB (**{100*(ram_a-ram_b)/ram_a:.1f}% lower**). "
        f"CER improves {a['cer']:.4f}% → {b['cer']:.4f}%, while WER worsens {a['wer']:.4f}% → {b['wer']:.4f}%. "
        "Inference size is unchanged; this is a training-resource tradeoff.\n\n")
    a, b = runs['E21']['metrics'], runs['E22']['metrics']
    insertion += (f"**Fisher EWC:** {a['wer']:.4f}% → {b['wer']:.4f}% WER versus matched replay "
        f"({errors(a)-errors(b)} fewer word errors), but it does not beat retained Tiny E11. "
        "The stronger penalty regresses. These are single-seed development comparisons; no fresh blind test is claimed.\n\n")
    small_choice = selected['selected']['small']['experiment']
    tiny_choice = selected['selected']['tiny']['experiment']
    small_errors_removed = errors(runs['E10']['metrics']) - errors(runs[small_choice]['metrics'])
    insertion += (f"**Retained checkpoints:** Small **{small_choice}** ({runs[small_choice]['metrics']['wer']:.4f}% WER), "
        f"Tiny **{tiny_choice}** ({runs[tiny_choice]['metrics']['wer']:.4f}% WER). "
        f"The Small choice removes {small_errors_removed} word errors versus previous E10. "
        + ("The newer methods did not produce a new Tiny WER record.\n\n" if tiny_choice == 'E11' else "Independent confirmation remains outstanding.\n\n"))
    insertion += '[Controlled comparisons, exact error counts and limitations](docs/RESEARCH_METHOD_RESULTS.md) · [Implementation and paper references](docs/RESEARCH_METHODS_IMPLEMENTATION.md) · [Workbench preview](docs/research-method-results-20261101.png).\n\n'
    if '<!-- RESEARCH_RESULTS_START -->' in text and '<!-- RESEARCH_RESULTS_END -->' in text:
        before, rest = text.split('<!-- RESEARCH_RESULTS_START -->', 1)
        _, after = rest.split('<!-- RESEARCH_RESULTS_END -->', 1)
        text = before + '<!-- RESEARCH_RESULTS_START -->\n' + insertion + '<!-- RESEARCH_RESULTS_END -->' + after
    elif marker in text:
        before, rest = text.split(marker, 1)
        _, after = rest.split('## Earlier fine-tuning results', 1)
        text = before + insertion + '## Earlier fine-tuning results' + after
    else:
        text = text.replace('## Fine-tuning results', insertion + '## Earlier fine-tuning results', 1)
    readme.write_text(text, encoding='utf-8')
    methods = ROOT / 'docs/RESEARCH_METHODS_IMPLEMENTATION.md'
    method_text = methods.read_text(encoding='utf-8').replace(
        'Results are pending until saved checkpoints are reloaded and evaluated. No accuracy gain is assumed.',
        'The original five checkpoints and stronger-EWC follow-up have completed saved-model validation. See [the measured comparisons](RESEARCH_METHOD_RESULTS.md); no broad accuracy gain is assumed.')
    methods.write_text(method_text, encoding='utf-8')
    write_results()
    print('Wrote docs/RESEARCH_METHOD_RESULTS.md, README comparisons, selections and evidence.')


if __name__ == '__main__':
    main()
