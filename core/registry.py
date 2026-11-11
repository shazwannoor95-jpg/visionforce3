"""Registry tempatan; pemasangan hanya daripada lockfile yang disemak."""
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryManager:
    def list(self):
        return json.loads((ROOT / 'docs/repository-registry.json').read_text())


class SkillRegistry:
    def list(self):
        rows = []
        for path in sorted((ROOT / '.agents/skills').glob('*/SKILL.md')):
            text = path.read_text()
            rows.append({'id': path.parent.name, 'source': str(path.relative_to(ROOT)),
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'status': 'VERIFIED' if text.startswith('---\n') and '\ndescription:' in text else 'FAILED',
                         'scope': 'Fail arahan sahaja; runtime mesti diuji untuk job.'})
        return rows


class DependencyProvisioningEngine:
    def inspect(self):
        package = ROOT / 'video/node_modules/remotion/package.json'
        expected = json.loads((ROOT / 'video/package.json').read_text())['dependencies']['remotion']
        return {'node': bool(shutil.which('node')), 'ffmpeg': bool(shutil.which('ffmpeg')),
                'ffprobe': bool(shutil.which('ffprobe')), 'chromium': Path('/usr/bin/chromium').is_file(),
                'remotion': package.is_file() and json.loads(package.read_text())['version'] == expected,
                'lockfile': (ROOT / 'video/package-lock.json').is_file()}

    def ensure(self, allow_install=False):
        checks = self.inspect()
        if not checks['remotion'] and allow_install:
            # Tiada shell/remote script atau pemasangan GPU. npm ci mengekalkan lockfile.
            subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'],
                           cwd=ROOT / 'video', check=True, timeout=600,
                           env=dict(os.environ, npm_config_cache=str(ROOT.parent / '.npm-cache')))
            checks = self.inspect()
        if not all(checks.values()):
            raise RuntimeError('BLOCKED: dependency worker belum lengkap: ' + json.dumps(checks))
        return {'status': 'INSTALLED', 'checks': checks, 'note': 'READY hanya selepas render dan verifikasi output.'}
