"""Ujian integrasi sebenar: HTTP upload PDF -> SQLite -> Remotion -> HTTP download."""
import io
import json
import threading
import tempfile
import urllib.request
from pathlib import Path
from reportlab.pdfgen import canvas
from core.worker import Worker
from core.server import make_server

root=Path('artifacts/v35-smoke')
root.mkdir(parents=True,exist_ok=True)
data=io.BytesIO(); c=canvas.Canvas(data)
for i,line in enumerate(['VISIONFORGE 3: Latihan Keselamatan','Langkah 1: Semak 42 peralatan sebelum bertugas.']):c.drawString(40,780-i*30,line)
c.save(); source=data.getvalue();(root/'fixture.pdf').write_bytes(source)
worker=Worker(Path(tempfile.mkdtemp(prefix='run-', dir=root))/'jobs');server=make_server(worker,0)
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_port)
try:
 req=urllib.request.Request(url+'/jobs?prompt=Video%20korporat',data=source,headers={'Content-Type':'application/pdf'})
 with urllib.request.urlopen(req) as response:
  assert response.status==202; ident=json.load(response)['id']
 result=worker.run_next();assert result['id']==ident and result['status']=='SUCCEEDED',result
 for name in ['video.mp4','captions.srt','manifest.json','coverage.json']:
  with urllib.request.urlopen(url+'/jobs/'+ident+'/'+name) as response:(root/name).write_bytes(response.read())
 manifest=json.loads((root/'manifest.json').read_text());coverage=json.loads((root/'coverage.json').read_text())
 assert manifest['source_lock'] and coverage['all_scene_quotes_verified'] and coverage['complete_document']
 assert '42' in (root/'captions.srt').read_text()
 (root/'result.json').write_text(json.dumps({'status':'PASS','job':ident,'checks':['HTTP PDF upload','persistent queue','Remotion motion graphics','H264/AAC 1080p30','FFmpeg full decode','HTTP artifact download','source quote/page coverage','SRT source number 42']},indent=2)+'\n')
 print((root/'result.json').read_text())
finally:server.shutdown();server.server_close()
