#!/usr/bin/env python3
"""Restore checksum-verified offline VO dependency archives from small Drive parts."""
import argparse
import json
from pathlib import Path
from model_bundle import digest, process


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['restore', 'verify'])
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--manifest-sha256')
    p.add_argument('--parts-dir', type=Path, default=Path('.'))
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--need', nargs='+', default=['python_cp311', 'espeak_linux', 'wheelhouse_cp311_cpu'])
    a = p.parse_args()
    if a.manifest_sha256 and digest(a.manifest) != a.manifest_sha256:
        p.error('Dependency manifest checksum mismatch')
    m = json.loads(a.manifest.read_text())
    if m.get('schema') != 'gemini-vo-dependency-parts-v1':
        p.error('Unsupported dependency manifest')
    adapted = {'schema': 'gemini-vo-model-parts-v1', 'models': m['components']}
    r = process(adapted, a.parts_dir, a.root, a.action, a.need)
    r['components_verified'] = r.pop('models_verified')
    r['dependency_archives_ready'] = r.pop('model_files_ready')
    r.pop('inference_test_required', None)
    r['runtime_install_required'] = True
    print(json.dumps(r, indent=2))


if __name__ == '__main__':
    main()
