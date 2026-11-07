"""One training-scale-calibrated EWC follow-up; preserve the original round."""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from .core import ROOT, experiment_config, experiments, write_json


def run():
    path = ROOT / 'runs/ewc-followup.json'
    recipe = ROOT / 'configs/research-e23.json'
    if path.exists():
        raise FileExistsError('Preserve the first follow-up execution')
    state = dict(status='queued', experiment='E23', action='waiting for original research round',
        project=experiment_config('E23'), pid=os.getpid(), started_at=datetime.now(timezone.utc).isoformat(),
        recipe_sha256=hashlib.sha256(recipe.read_bytes()).hexdigest(),
        reason='E22 training logs show weighted EWC penalty around 4e-5 versus CE 0.7–1.1; test stronger lambda 1e7, chosen before inspecting E22 validation scores. No test data used.')
    write_json(path, state)
    try:
        while True:
            prior=json.loads((ROOT/'runs/research-round.json').read_text(encoding='utf-8'))
            if prior['status'] in ('failed','interrupted'):
                raise RuntimeError('Resolve the original round first')
            if prior['status']=='completed':
                break
            time.sleep(10)
        if hashlib.sha256(recipe.read_bytes()).hexdigest()!=state['recipe_sha256']:
            raise ValueError('Follow-up recipe changed after freezing')
        state.update(status='running', action='stronger Fisher EWC training and validation')
        write_json(path,state)
        from .train_stage import run as stage
        stage('E23','configs/research-e23.json')
        runs={r['id']:r for r in experiments()}
        from .reporting import compatible_metrics,write_results
        original=json.loads((ROOT/'runs/selection-research.json').read_text(encoding='utf-8'))
        candidates=list(original['selected']['tiny']['candidates'])+['E23']
        if any(not compatible_metrics(runs[i]['metrics'],runs['E0']['metrics']) for i in candidates):
            raise ValueError('Tiny validation protocols differ')
        winner=min(candidates,key=lambda i:runs[i]['metrics']['wer'])
        selected={**original['selected'],'tiny':dict(experiment=winner,validation_wer=runs[winner]['metrics']['wer'],
            candidates={i:runs[i]['metrics']['wer'] for i in candidates})}
        files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'runs/E23/checkpoint').iterdir() if p.is_file()}
        write_json(ROOT/'runs/selection-research-strong.json',dict(selected=selected,
            checkpoint_files={**original['checkpoint_files'],'E23':files},
            frozen_at=datetime.now(timezone.utc).isoformat(),policy=original['policy'],
            original_selection='runs/selection-research.json',followup_recipe_sha256=state['recipe_sha256']))
        from .diagnostics import compare_predictions
        compare_predictions('E23',baseline_id='E21',primary=False)
        compare_predictions('E23',baseline_id='E22',primary=False)
        write_results()
        state.update(status='completed',selected_tiny=winner)
    except BaseException as error:
        state.update(status='failed',error=str(error))
        raise
    finally:
        state['updated_at']=datetime.now(timezone.utc).isoformat()
        write_json(path,state)


if __name__=='__main__':
    run()
