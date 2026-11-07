"""Export derived public evidence without machine-specific project paths."""
from .core import ROOT, write_json


def portable_paths(value):
    if isinstance(value, dict):
        return {key: portable_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [portable_paths(item) for item in value]
    if isinstance(value, str):
        for prefix in (str(ROOT), ROOT.as_posix()):
            if value.startswith(prefix + '/') or value.startswith(prefix + '\\'):
                return value[len(prefix):].lstrip('/\\').replace('\\', '/')
    return value


def write_public_snapshot(path, data):
    exported = portable_paths(data)
    exported['_export'] = {
        'paths': 'Project-relative; original machine-local records are preserved in runs/.',
        'metrics_modified': False,
        'fingerprints': 'Historical fingerprints are preserved, not recalculated after path redaction.',
    }
    write_json(path, exported)
