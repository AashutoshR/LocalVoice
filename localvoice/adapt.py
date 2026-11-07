"""Further acoustic adaptation; validation-only development round."""
import os
import subprocess
import sys
from datetime import datetime, timezone
from .core import ROOT, experiment_config, write_json


def run():
    path = ROOT / 'runs/adaptation.json'
    state = dict(status='running', pid=os.getpid(), project=experiment_config('E10'),
        started_at=datetime.now(timezone.utc).isoformat(), experiment='E10', action='train',
        selection_split='validation', target_validation_wer=5.0, steps=[])
    try:
        for action in ('train', 'evaluate'):
            state['action'] = action
            write_json(path, state)
            command = [sys.executable, '-u', '-m', 'localvoice.cli', action, 'E10']
            if action == 'train':
                command += ['--config', 'configs/small-acoustic.json']
            with (ROOT / 'runs' / f'E10-{action}.log').open('w', encoding='utf-8') as log:
                result = subprocess.run(command, cwd=ROOT, env={**os.environ, 'PYTHONUTF8': '1'}, stdout=log, stderr=subprocess.STDOUT)
            state['steps'].append(dict(action=action, exit_code=result.returncode))
            if result.returncode:
                raise RuntimeError(f'E10 {action} failed; inspect its log')
        from .diagnostics import compare_predictions
        compare_predictions('E10', baseline_id='E7')
        from .weight_audit import audit
        audit('E10', 'E8')
        state['status'] = 'completed'
    except BaseException as exc:
        state.update(status='failed', error=str(exc))
        raise
    finally:
        state['updated_at'] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == '__main__':
    run()
