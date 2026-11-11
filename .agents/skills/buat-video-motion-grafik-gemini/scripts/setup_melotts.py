#!/usr/bin/env python3
"""Prepare isolated MeloTTS-MS dependencies and require a real Malay inference proof."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model-root', required=True, type=Path)
    p.add_argument('--venv', type=Path)
    p.add_argument('--dependency-root', type=Path, help='Prefix created by install_vo_dependencies.py')
    p.add_argument('--install', action='store_true')
    p.add_argument('--offline', action='store_true')
    p.add_argument('--wheelhouse', type=Path)
    p.add_argument('--source-archive', type=Path)
    p.add_argument('--report', required=True, type=Path)
    a = p.parse_args()
    root = a.model_root.resolve()
    env = os.environ.copy()
    if a.dependency_root:
        from install_vo_dependencies import apply_environment
        settings = json.loads((a.dependency_root / 'runtime-env.json').read_text())
        env = apply_environment(settings)
        if not a.venv:
            a.venv = Path(settings['venv'])
    if not a.venv:
        p.error('--venv or --dependency-root is required')
    python = a.venv.resolve() / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    report = {'ready': False, 'model_root': str(root), 'python': str(python),
              'offline': a.offline, 'checks': {}}
    try:
        for name in ['melotts-ms/model.pth', 'melotts-ms/config.json', 'malay-bert/config.json',
                     'malay-bert/pytorch_model.bin', 'malay-bert/vocab.txt',
                     'malay-bert/tokenizer_config.json', 'malay-bert/special_tokens_map.json']:
            report['checks'][name] = (root / name).is_file()
        if not all(report['checks'].values()):
            raise RuntimeError('Restore/verify all model parts with model_bundle.py first')
        espeak = shutil.which('espeak-ng', path=env.get('PATH')) or shutil.which('espeak', path=env.get('PATH'))
        if not espeak:
            raise RuntimeError('Install OS espeak-ng + libespeak-ng1 (or espeak + libespeak1), then retry')
        report['espeak'] = espeak
        if a.install and not a.dependency_root:
            if not a.wheelhouse or not a.wheelhouse.is_dir():
                raise RuntimeError('Use the verified Drive dependency bundle or provide its complete --wheelhouse; raw source installation is not the offline profile')
            lock = a.wheelhouse.parent / 'requirements.lock.txt'
            if not lock.is_file():
                raise RuntimeError('The verified requirements.lock.txt must accompany --wheelhouse')
            if not python.is_file():
                subprocess.run([sys.executable, '-m', 'venv', str(a.venv.resolve())], check=True)
            subprocess.run([str(python), '-m', 'pip', 'install', '--no-index', '--find-links',
                            str(a.wheelhouse.resolve()), '--require-hashes', '-r', str(lock)], env=env, check=True)
        if not python.is_file():
            raise RuntimeError('Isolated Python environment missing; use --install during setup')
        if a.install:
            subprocess.run([str(python), str(Path(__file__).with_name('prepare_malay_runtime.py'))], env=env, check=True)
        env['MODEL_ID'] = str(root / 'malay-bert')
        # Even an online installation must pass inference using restored local models.
        env['HF_HUB_OFFLINE'] = '1'
        env['TRANSFORMERS_OFFLINE'] = '1'
        proof = a.report.resolve().with_suffix('.proof.wav')
        code = '''import json, sys
from melo.api import TTS
import soundfile as sf
import numpy as np
root, out = sys.argv[1:]
model = TTS(language='MS', device='cpu', config_path=root+'/melotts-ms/config.json', ckpt_path=root+'/melotts-ms/model.pth')
model.tts_to_file('Korang pernah rasa macam ini? Jom kita faham sama-sama.', 0, output_path=out, split=True, sdp_ratio=0, noise_scale=0.667, speed=1.0)
x,sr=sf.read(out)
assert sr>0 and len(x)>sr and np.isfinite(x).all() and np.max(np.abs(x))>0.001
print(json.dumps({'sample_rate':sr,'duration':len(x)/sr,'peak':float(np.max(np.abs(x)))}))
'''
        proof.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run([str(python), '-c', code, str(root), str(proof)],
                                env=env, capture_output=True, text=True, timeout=600)
        report['inference_returncode'] = result.returncode
        report['inference_log'] = (result.stdout + result.stderr)[-6000:]
        report['proof'] = str(proof)
        report['ready'] = result.returncode == 0 and proof.is_file()
        if not report['ready']:
            raise RuntimeError('Local Malay inference failed; inspect inference_log. Do not switch model/language silently')
        frozen = subprocess.run([str(python), '-m', 'pip', 'freeze'], env=env, capture_output=True, text=True, check=True)
        a.report.with_suffix('.requirements.txt').write_text(frozen.stdout)
    except Exception as exc:
        report['error'] = str(exc)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if not report['ready']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
