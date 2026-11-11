"""API pembangunan loopback sahaja; auth/storage produksi ialah fasa seterusnya."""
import argparse
import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from .worker import Worker, MAX_BYTES


def make_server(worker, port=8787):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # Jangan log dokumen/prompt.

        def respond(self, status, body):
            data = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status); self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)

        def do_POST(self):
            try:
                parts = urlsplit(self.path)
                if parts.path != '/jobs':
                    return self.respond(404, {'error': 'Laluan tidak dijumpai.'})
                if self.headers.get('Content-Type') != 'application/pdf':
                    return self.respond(415, {'error': 'Hantar application/pdf.'})
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= MAX_BYTES:
                    return self.respond(413, {'error': 'Had PDF 20 MiB.'})
                self.connection.settimeout(20)
                data = self.rfile.read(size)
                if len(data) != size:
                    raise ValueError('Upload tidak lengkap.')
                prompt = parse_qs(parts.query).get('prompt', [''])[0]
                ident = worker.enqueue(data, prompt)
                self.respond(202, {'id': ident, 'status': 'PENDING'})
            except (ValueError, OSError) as exc:
                self.respond(400, {'error': str(exc)})
            except Exception:
                self.respond(400, {'error': 'PDF tidak dapat diproses.'})

        def do_GET(self):
            parts = urlsplit(self.path).path.strip('/').split('/')
            if len(parts) not in (2, 3) or parts[0] != 'jobs':
                return self.respond(404, {'error': 'Laluan tidak dijumpai.'})
            try:
                ident = uuid.UUID(parts[1]).hex
                job = worker.status(ident)
                if len(parts) == 2:
                    return self.respond(200, job)
                if parts[2] not in ['video.mp4', 'captions.srt', 'manifest.json', 'coverage.json'] or job['status'] != 'SUCCEEDED':
                    raise KeyError()
                path = worker.root / ident / parts[2]
                self.send_response(200)
                self.send_header('Content-Type', 'video/mp4' if path.suffix == '.mp4' else 'application/octet-stream')
                self.send_header('Content-Length', str(path.stat().st_size)); self.end_headers()
                with path.open('rb') as source:
                    import shutil
                    shutil.copyfileobj(source, self.wfile)
            except (KeyError, ValueError):
                self.respond(404, {'error': 'Job/fail tidak dijumpai.'})
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8787)
    parser.add_argument('--storage', default='.data/jobs')
    args = parser.parse_args(); worker = Worker(args.storage); stop = threading.Event()
    def consume():
        while not stop.is_set():
            worker.run_next()
            stop.wait(.5)
    threading.Thread(target=consume, daemon=True).start()
    server = make_server(worker, args.port)
    try:
        server.serve_forever()
    finally:
        stop.set(); server.server_close()


if __name__ == '__main__':
    main()
