#!/usr/bin/env python3
"""Verify/restore Drive model parts offline; preserves files with local changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def destination(root, name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError('Unsafe relative path: ' + name)
    out = root.joinpath(*p.parts)
    if not out.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path/symlink escapes root')
    return out


def matches(path, row):
    return path.is_file() and path.stat().st_size == row['size_bytes'] and digest(path) == row['sha256']


def process(manifest, parts_dir, root, action, selected):
    if manifest.get('schema') != 'gemini-vo-model-parts-v1':
        raise ValueError('Unsupported model manifest')
    unknown = set(selected) - {r['key'] for r in manifest['models']}
    if unknown:
        raise ValueError('Unknown model keys: ' + ', '.join(sorted(unknown)))
    rows = [r for r in manifest['models'] if r['key'] in selected]
    files = [(m['key'], f) for m in rows for f in m['files']]
    # Check all selected parts and conflicts before writing any restored file.
    for key, row in files:
        target = destination(root, row['path'])
        if matches(target, row):
            continue
        if action == 'verify':
            raise ValueError('Missing/invalid restored file: ' + row['path'])
        if target.exists():
            raise ValueError('Existing different file preserved; use a fresh root: ' + row['path'])
        if sum(p['size_bytes'] for p in row['parts']) != row['size_bytes']:
            raise ValueError('Parts total size mismatch')
        for part in row['parts']:
            if part['size_bytes'] >= 10000000 or Path(part['name']).name != part['name']:
                raise ValueError('Unsafe or oversized model part')
            if not matches(parts_dir / part['name'], part):
                raise ValueError('Download/repair exact part: ' + part['name'])
    for key, row in files:
        target = destination(root, row['path'])
        if matches(target, row):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix='.model-', dir=target.parent)
        h = hashlib.sha256()
        try:
            with os.fdopen(fd, 'wb') as out:
                for part in row['parts']:
                    with (parts_dir / part['name']).open('rb') as src:
                        for block in iter(lambda: src.read(1048576), b''):
                            out.write(block)
                            h.update(block)
            if Path(name).stat().st_size != row['size_bytes'] or h.hexdigest() != row['sha256']:
                raise ValueError('Full file checksum mismatch: ' + row['path'])
            os.replace(name, target)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    return {'models_verified': selected, 'files_verified': len(files), 'root': str(root.resolve()),
            'model_files_ready': True, 'inference_test_required': True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['restore', 'verify'])
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--manifest-sha256')
    p.add_argument('--parts-dir', type=Path, default=Path('.'))
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--need', required=True, nargs='+')
    a = p.parse_args()
    if a.manifest_sha256 and digest(a.manifest) != a.manifest_sha256:
        p.error('Manifest checksum mismatch')
    print(json.dumps(process(json.loads(a.manifest.read_text()), a.parts_dir, a.root, a.action, a.need), indent=2))


if __name__ == '__main__':
    main()
