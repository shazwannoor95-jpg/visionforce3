"""Preserve all 600 assets while serving duplicate individual ZIPs on demand."""
import json,re
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'dist'
p=D/'vlog-assets.json';data=json.loads(p.read_text())
removed=0
for r in data['items']:
 if r['type']=='lut':
  n=int(r['id'][2:]);pack=f'vlog/packs/luts-{(n-1)//25+1}.zip'
  r['download_pack']=pack;r['download_entry']=f"assets/vlog_montage/luts/{r['id']}.cube"
  r['file']=pack;r['files']=[pack];r['download']=pack
  f=D/f"vlog/luts/{r['id']}.zip"
  if f.exists():removed+=f.stat().st_size;f.unlink()
 elif r['type'] in ('transition','overlay'):
  f=D/r['download']
  if f.exists():removed+=f.stat().st_size;f.unlink()
  r['download_files']=r['files'];r['download']=r['files'][0]
p.write_text(json.dumps(data,ensure_ascii=False))
p=D/'vlog-gallery.js';s=p.read_text()
s=s.replace("dl.textContent=`Muat turun ${x.download.endsWith('.zip')?'pek':x.format.toUpperCase()} ↓`;","dl.textContent=`Muat turun ${x.download_pack?'LUT':x.download_files?'pek':x.format.toUpperCase()} ↓`;\n  dl.onclick=async e=>{if(!x.download_pack&&!x.download_files)return;e.preventDefault();dl.textContent='Memuatkan fail…';try{const z=new JSZip();if(x.download_pack){z.file(x.id+'.cube',await AtlasZip.entry(x.download_pack,x.download_entry,'uint8array'));}else{for(const name of x.download_files){const rr=await fetch(name);if(!rr.ok)throw Error('Fail tidak dapat dimuatkan');z.file(name.replace(/^vlog\\//,''),await rr.arrayBuffer());}z.file('asset.json',JSON.stringify(x,null,2));}z.file('LICENSE.txt','Original Motion Atlas VL assets. You may use, edit and render these original assets in personal or commercial video projects. No Motion Array or Envato source files are included.');AtlasZip.download(await z.generateAsync({type:'blob',compression:'DEFLATE'}),x.id+'.zip');}catch(err){dl.textContent=err.message;return;}dl.textContent='Muat turun ↓';};")
p.write_text(s)
print(json.dumps({'bytes_removed':removed,'items_preserved':len(data['items'])}))
