#!/usr/bin/env python3
"""Install the verified CPU/CPython 3.11 VO bundle offline into a user-owned prefix."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shlex
import shutil
import subprocess
import tarfile
import tempfile
from model_bundle import digest


def run(argv, env=None):
    return subprocess.run([str(x) for x in argv], env=env, check=True,
                          capture_output=True, text=True)


def unpack(archive, destination):
    """Extract only data/relative internal links into a fresh directory."""
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    links = []
    with tarfile.open(archive, 'r:*') as t:
        for m in t:
            name = PurePosixPath(m.name)
            if name.is_absolute() or '..' in name.parts or '\\' in m.name:
                raise ValueError('Unsafe archive member: ' + m.name)
            out = destination.joinpath(*name.parts)
            if not out.resolve().is_relative_to(destination):
                raise ValueError('Archive path escapes prefix')
            if m.isdir():
                out.mkdir(parents=True, exist_ok=True)
            elif m.isfile():
                out.parent.mkdir(parents=True, exist_ok=True)
                with t.extractfile(m) as src, out.open('wb') as dst:
                    shutil.copyfileobj(src, dst)
                out.chmod(m.mode & 0o777)
            elif m.issym() or m.islnk():
                target = Path(m.linkname)
                if target.is_absolute():
                    raise ValueError('Absolute archive link rejected')
                resolved = (out.parent / target if m.issym() else destination / target).resolve()
                if not resolved.is_relative_to(destination):
                    raise ValueError('Archive link escapes prefix')
                links.append((m, out, resolved))
            else:
                raise ValueError('Special archive member rejected')
    for m, out, target in links:
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() or out.is_symlink():
            raise ValueError('Archive link collision')
        if m.issym():
            out.symlink_to(m.linkname)
        else:
            os.link(target, out)


def component(archive, prefix, name, state):
    target = prefix / name
    sha = digest(archive)
    if target.exists():
        if state.get('components', {}).get(name) != sha:
            raise ValueError('Existing unmanaged/different component preserved: ' + str(target))
        return target
    with tempfile.TemporaryDirectory(prefix='.vo-extract-', dir=prefix) as td:
        unpack(archive, Path(td))
        source = Path(td) / 'python' if name == 'python' else Path(td)
        if name == 'python':
            shutil.move(str(source), target)
        else:
            target.mkdir()
            for p in Path(td).iterdir():
                shutil.move(str(p), target / p.name)
    state.setdefault('components', {})[name] = sha
    (prefix / 'install-state.json').write_text(json.dumps(state, indent=2) + '\n')
    return target


def runtime_environment(prefix):
    es = prefix / 'espeak'
    lib = es / 'usr/lib/x86_64-linux-gnu'
    return {
        'python': str(prefix / 'python/bin/python3.11'),
        'venv': str(prefix / 'venv'),
        'PATH_prepend': str(prefix / 'bin'),
        'LD_LIBRARY_PATH_prepend': ':'.join(map(str, [lib, lib / 'pulseaudio', es / 'lib/x86_64-linux-gnu'])),
        'ESPEAK_DATA_PATH': str(lib),
        'PHONEMIZER_ESPEAK_LIBRARY': str(lib / 'libespeak-ng.so.1'),
        'GEMINI_MALAYA_DEMOJI': str(prefix / 'packages/normalizer/demoji.json'),
        'OMP_NUM_THREADS': '2',
        'OPENBLAS_NUM_THREADS': '2',
    }


def apply_environment(settings):
    env = os.environ.copy()
    for key, value in settings.items():
        if key.endswith('_prepend'):
            name = key[:-8]
            env[name] = value + (os.pathsep + env[name] if env.get(name) else '')
        elif key not in ('python', 'venv'):
            env[key] = value
    return env


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--bundle-root', required=True, type=Path)
    p.add_argument('--prefix', required=True, type=Path)
    p.add_argument('--report', required=True, type=Path)
    a = p.parse_args()
    prefix = a.prefix.resolve()
    report = {'ready': False, 'offline': True, 'prefix': str(prefix), 'target': 'Linux x86_64/glibc>=2.35, CPython 3.11, CPU'}
    try:
        libc, version = platform.libc_ver()
        if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'AMD64'):
            raise RuntimeError('This bundle requires Linux x86_64; use a separately built profile for other platforms')
        if libc != 'glibc' or tuple(map(int, version.split('.')[:2])) < (2, 35):
            raise RuntimeError('This bundle requires host glibc >= 2.35; do not replace host libc')
        if not shutil.which('dpkg-deb'):
            raise RuntimeError('dpkg-deb is required to extract the bundled official .deb packages without root')
        m = json.loads(a.manifest.read_text())
        if m.get('schema') != 'gemini-vo-dependency-parts-v1':
            raise ValueError('Unsupported dependency manifest')
        files = {c['key']: c['files'][0] for c in m['components']}
        archives = {}
        for key in ('python_cp311', 'espeak_linux', 'wheelhouse_cp311_cpu'):
            row = files[key]
            path = (a.bundle_root / row['path']).resolve()
            if not path.is_relative_to(a.bundle_root.resolve()) or path.stat().st_size != row['size_bytes'] or digest(path) != row['sha256']:
                raise ValueError('Restore and verify archive first: ' + row['path'])
            archives[key] = path
        state_path = prefix / 'install-state.json'
        if prefix.exists() and any(prefix.iterdir()) and not state_path.is_file():
            raise ValueError('Existing unmanaged prefix preserved; choose a fresh output prefix')
        prefix.mkdir(parents=True, exist_ok=True)
        state = json.loads(state_path.read_text()) if state_path.is_file() else {'schema': 'gemini-vo-install-state-v1', 'components': {}}
        python_root = component(archives['python_cp311'], prefix, 'python', state)
        packages = component(archives['wheelhouse_cp311_cpu'], prefix, 'packages', state)
        deb_root = component(archives['espeak_linux'], prefix, 'espeak-debs', state)
        es = prefix / 'espeak'
        if not es.exists():
            with tempfile.TemporaryDirectory(prefix='.espeak-', dir=prefix) as td:
                for deb in sorted((deb_root / 'debs').glob('*.deb')):
                    run(['dpkg-deb', '-x', deb, td])
                shutil.move(td, es)
        settings = runtime_environment(prefix)
        env = apply_environment(settings)
        bindir = prefix / 'bin'
        bindir.mkdir(exist_ok=True)
        wrapper = bindir / 'espeak-ng'
        wrapper.write_text('#!/bin/sh\nexec ' + shlex.quote(str(es / 'usr/bin/espeak-ng')) + ' --path=' + shlex.quote(settings['ESPEAK_DATA_PATH']) + ' "$@"\n')
        wrapper.chmod(0o755)
        python = python_root / 'bin/python3.11'
        venv = prefix / 'venv'
        if not (venv / 'bin/python').is_file():
            run([python, '-m', 'venv', venv], env)
        vp = venv / 'bin/python'
        run([vp, '-m', 'pip', 'install', '--no-index', '--find-links', packages / 'wheelhouse',
             '--require-hashes', '-r', packages / 'requirements.lock.txt'], env)
        run([vp, '-m', 'pip', 'check'], env)
        run([vp, Path(__file__).with_name('prepare_malay_runtime.py')], env)
        esproof = run([wrapper, '--voices=ms'], env)
        report['espeak_voices'] = esproof.stdout
        imports = run([vp, '-c', "import torch,torchaudio,transformers,phonemizer,malaya,malaya_speech; import importlib.metadata as m; print({n:m.version(n) for n in ['torch','torchaudio','transformers','malaya','malaya-speech','phonemizer','melotts']}); assert not torch.version.cuda"], env)
        report['versions'] = imports.stdout.strip()
        report['ready'] = 'Malay' in esproof.stdout
        report['tts_inference_required'] = True
        (prefix / 'runtime-env.json').write_text(json.dumps(settings, indent=2) + '\n')
        report['runtime_env'] = str(prefix / 'runtime-env.json')
    except Exception as exc:
        report['error'] = str(exc)
        if isinstance(exc, subprocess.CalledProcessError):
            report['command_output'] = (exc.stdout + exc.stderr)[-8000:]
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if not report['ready']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
