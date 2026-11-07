"""Measure actual saved encoder/decoder changes against the initial weights."""
import math
import json
from .core import ROOT, write_json


def audit_adapter(experiment):
    import torch
    from safetensors import safe_open
    folder = ROOT / "runs" / experiment
    training = json.loads((folder / "training.json").read_text(encoding="utf-8"))
    names = training.get("trainable_parameter_names") or []
    if not training.get("base_parameters_frozen") or not names or any("lora_" not in n for n in names):
        raise ValueError("Adapter audit requires verified frozen base parameters")
    tensors, updated_b = 0, 0
    with safe_open(folder / "checkpoint/adapter_model.safetensors", framework="pt", device="cpu") as weights:
        for name in weights.keys():
            if "lora_" not in name:
                raise ValueError("Unexpected non-adapter tensor in saved checkpoint")
            value = weights.get_tensor(name)
            if not torch.isfinite(value).all():
                raise ValueError("Nonfinite adapter weights")
            tensors += 1
            if "lora_B" in name and torch.count_nonzero(value).item():
                updated_b += 1
    if not updated_b:
        raise ValueError("No saved LoRA B tensor differs from its zero initialization")
    result = dict(experiment=experiment, base_parameters_frozen=True, adapter_tensors=tensors,
        updated_b_tensors=updated_b, trainable_parameters=training["trainable_parameters"],
        interpretation="Saved nonzero B tensors establish adapter updates. Quality is measured separately after reloading and merging.")
    write_json(folder / "adapter-audit.json", result)
    return result


def audit(experiment, parent):
    import torch
    from safetensors import safe_open
    torch.set_num_threads(4)
    before = ROOT / 'runs' / parent / 'checkpoint/model.safetensors'
    after = ROOT / 'runs' / experiment / 'checkpoint/model.safetensors'
    groups = {key: dict(parameters=0, changed_parameters=0, tensors=0, changed_tensors=0,
                         squared_change=0., squared_initial=0.) for key in ('encoder', 'decoder')}
    training = json.loads((ROOT / 'runs' / experiment / 'training.json').read_text(encoding='utf-8'))
    frozen = training.get('encoder_freezing', {}).get('frozen_lower_blocks', 0)
    protected_tensors, changed_protected = 0, 0
    with safe_open(before, framework='pt', device='cpu') as initial, safe_open(after, framework='pt', device='cpu') as trained:
        if set(initial.keys()) != set(trained.keys()):
            raise ValueError('Weight audit requires the same architecture')
        for name in trained.keys():
            key = 'encoder' if name.startswith('model.encoder.') else 'decoder'
            a, b = initial.get_tensor(name), trained.get_tensor(name)
            if a.shape != b.shape:
                raise ValueError('Weight shape changed')
            changed = int(torch.count_nonzero(a != b).item())
            protected = frozen and (name.startswith(('model.encoder.conv1.', 'model.encoder.conv2.')) or
                any(name.startswith(f'model.encoder.layers.{i}.') for i in range(frozen)))
            if protected:
                protected_tensors += 1
                changed_protected += int(changed > 0)
            g = groups[key]
            g['parameters'] += a.numel()
            g['changed_parameters'] += changed
            g['tensors'] += 1
            g['changed_tensors'] += int(changed > 0)
            g['squared_change'] += (b.float() - a.float()).square().sum(dtype=torch.float64).item()
            g['squared_initial'] += a.float().square().sum(dtype=torch.float64).item()
    for g in groups.values():
        g['relative_l2_change'] = math.sqrt(g.pop('squared_change') / max(g.pop('squared_initial'), 1e-30))
    result = dict(experiment=experiment, initial_experiment=parent, groups=groups,
                  interpretation='Parameter changes verify training; recognition quality is measured separately by validation WER/CER.')
    if frozen:
        result['partial_freezing'] = dict(frozen_lower_blocks=frozen, protected_tensors=protected_tensors,
            changed_protected_tensors=changed_protected)
        if changed_protected or not protected_tensors:
            raise ValueError('Saved checkpoint violated partial encoder freezing')
    write_json(ROOT / 'runs' / experiment / 'weight-audit.json', result)
    return result
