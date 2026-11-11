"""Queue SQLite dan render Remotion. PDF sebagai data, bukan kod atau arahan."""
import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
import sqlite3
import subprocess
import uuid
from pathlib import Path
from pypdf import PdfReader
from .registry import ROOT, DependencyProvisioningEngine

MAX_BYTES = 20 * 1024 * 1024


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def analyse_pdf(data, prompt):
    if not data.startswith(b'%PDF-') or len(data) > MAX_BYTES:
        raise ValueError('PDF diperlukan, maksimum 20 MiB.')
    if not isinstance(prompt, str) or not 1 <= len(prompt.strip()) <= 2000:
        raise ValueError('Prompt diperlukan, maksimum 2000 aksara.')
    reader = PdfReader(io.BytesIO(data))
    if reader.is_encrypted or not 1 <= len(reader.pages) <= 50:
        raise ValueError('PDF mesti tidak berkunci dan mempunyai 1–50 halaman.')
    pages = [{'page': i + 1, 'text': (page.extract_text() or '').strip()} for i, page in enumerate(reader.pages)]
    if sum(len(p['text']) for p in pages) > 100000:
        raise ValueError('PDF melebihi had teks worker pembangunan.')
    scenes = []
    for page in pages:
        # Petikan tepat, bukan ringkasan AI: angka/istilah asal tidak diubah.
        for line in page['text'].splitlines():
            if line.strip() and len(scenes) < 8:
                scenes.append({'text': line.strip()[:180], 'page': page['page']})
    if not scenes:
        raise ValueError('PDF tiada teks boleh baca; OCR belum disediakan.')
    for scene in scenes:
        assert scene['text'] in pages[scene['page'] - 1]['text']
    return {'sha256': hashlib.sha256(data).hexdigest(), 'pages': pages, 'scenes': scenes,
            'prompt': prompt, 'source_lock': True, 'planner': 'Petikan deterministik; tiada panggilan LLM.'}


class Worker:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, status TEXT, error TEXT)')

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.root / 'queue.sqlite', timeout=30)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def enqueue(self, data, prompt):
        manifest = analyse_pdf(data, prompt)
        ident = uuid.uuid4().hex
        folder = self.root / ident
        folder.mkdir()
        (folder / 'source.pdf').write_bytes(data)
        write_json(folder / 'source.json', manifest)
        with self.db() as db:
            db.execute('INSERT INTO jobs VALUES (?, ?, NULL)', (ident, 'PENDING'))
        return ident

    def status(self, ident):
        with self.db() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (ident,)).fetchone()
        if row is None:
            raise KeyError('Job tidak dijumpai.')
        return dict(row)

    def retry(self, ident):
        with self.db() as db:
            # Operator mesti memastikan tiada worker lama hidup sebelum recover RUNNING.
            db.execute("UPDATE jobs SET status='PENDING', error=NULL WHERE id=? AND status IN ('FAILED','RUNNING')", (ident,))
        return self.status(ident)

    def run_next(self):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT id FROM jobs WHERE status='PENDING' ORDER BY rowid LIMIT 1").fetchone()
            if row is None:
                return None
            ident = row['id']
            db.execute("UPDATE jobs SET status='RUNNING' WHERE id=?", (ident,))
        try:
            self.render(ident)
        except Exception as exc:
            with self.db() as db:
                db.execute("UPDATE jobs SET status='FAILED', error=? WHERE id=?", (str(exc)[:2000], ident))
        else:
            with self.db() as db:
                db.execute("UPDATE jobs SET status='SUCCEEDED' WHERE id=?", (ident,))
        return self.status(ident)

    def render(self, ident):
        folder = self.root / ident
        source = json.loads((folder / 'source.json').read_text())
        checks = DependencyProvisioningEngine().ensure(allow_install=False)
        frames = 90 * len(source['scenes'])
        props = folder / 'props.json'
        write_json(props, {'scenes': source['scenes']})
        env = dict(os.environ, npm_config_cache=str(ROOT.parent / '.npm-cache'))
        with (folder / 'render.log').open('w') as log:
            def run(args, timeout=600):
                subprocess.run(args, cwd=ROOT / 'video', env=env, stdout=log,
                               stderr=subprocess.STDOUT, check=True, timeout=timeout)
            run(['node', str(ROOT / 'video/node_modules/@remotion/cli/remotion-cli.js'),
                 'render', 'src/document.tsx', 'Document', str(folder / 'silent.mp4'),
                 '--props=' + str(props), '--concurrency=2', '--codec=h264',
                 '--browser-executable=/usr/bin/chromium'])
            # Bed audio sintetik tempatan; tiada VO/servis AI yang dipalsukan.
            run(['ffmpeg', '-y', '-v', 'error', '-i', str(folder / 'silent.mp4'), '-f', 'lavfi',
                 '-i', 'sine=frequency=160:sample_rate=48000', '-af', 'volume=0.025',
                 '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', str(folder / 'video.mp4')])
            run(['ffmpeg', '-v', 'error', '-i', str(folder / 'video.mp4'), '-f', 'null', '-'])
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames',
            '-show_streams', '-show_format', '-of', 'json', str(folder / 'video.mp4')], text=True, timeout=60))
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
        if (video['width'], video['height'], video['r_frame_rate'], int(video['nb_read_frames']), video['codec_name'], audio['codec_name']) != (1920, 1080, '30/1', frames, 'h264', 'aac'):
            raise ValueError('Verifikasi output gagal.')
        srt = []
        for i, scene in enumerate(source['scenes']):
            def stamp(seconds):
                return f'{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02},000'
            srt.append(f"{i+1}\n{stamp(i*3)} --> {stamp((i+1)*3)}\n{scene['text']}\n")
        (folder / 'captions.srt').write_text('\n'.join(srt))
        coverage = []
        for page in source['pages']:
            remaining = page['text']
            used = [s['text'] for s in source['scenes'] if s['page'] == page['page']]
            for text in used:
                remaining = remaining.replace(text, '', 1)
            coverage.append({'page': page['page'], 'used': used, 'not_used': remaining.strip()})
        write_json(folder / 'coverage.json', {'source_sha256': source['sha256'], 'pages': coverage,
                   'all_scene_quotes_verified': True, 'claims_outside_source': [], 'complete_document': all(not p['not_used'] for p in coverage)})
        write_json(folder / 'manifest.json', {'id': ident, 'engine': 'remotion', 'engine_version': '4.0.542',
            'skill': 'remotion-markup', 'source_lock': True, 'scenes': source['scenes'],
            'planner': source['planner'], 'audio': 'Bed nada sintetik; tiada voice-over.',
            'provisioning': checks, 'status': 'TESTED', 'probe': probe})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--storage', type=Path, default=ROOT / '.data/jobs')
    sub = parser.add_subparsers(dest='command', required=True)
    submit = sub.add_parser('submit'); submit.add_argument('pdf', type=Path); submit.add_argument('--prompt', required=True)
    sub.add_parser('run-next')
    for name in ['status', 'retry']:
        sub.add_parser(name).add_argument('id')
    args = parser.parse_args(); worker = Worker(args.storage)
    if args.command == 'submit':
        print(worker.enqueue(args.pdf.read_bytes(), args.prompt))
    elif args.command == 'run-next':
        result = worker.run_next(); print(json.dumps(result)); return int(result is not None and result['status'] == 'FAILED')
    else:
        print(json.dumps(getattr(worker, args.command)(args.id)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
