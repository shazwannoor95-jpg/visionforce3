"""Verify published preview samples against the pinned renderer; repair mismatches."""
import concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer'))
import render
from atlas_preset import AtlasLibrary

def check(pid):
    cfg=render.configuration(pid);duration=cfg['duration'];video=ROOT/'dist/media'/f'{pid}.mp4'
    indices=[int(duration*30*f) for f in (.13,.47,.83)]
    def errors():
        filt='+'.join(f'eq(n\\,{n})' for n in indices)
        data=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-i',str(video),'-vf','select='+filt,'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'])
        actual=np.frombuffer(data,dtype=np.uint8).reshape(len(indices),540,960,3)
        expected=[np.asarray(render.frame(pid,n/30,cfg,False).convert('RGB').resize((960,540),Image.Resampling.LANCZOS)) for n in indices]
        return [float(np.abs(a.astype(float)-b.astype(float)).mean()) for a,b in zip(actual,expected)]
    before=errors(); repaired=max(before)>5
    if repaired:
        tmp=video.with_suffix('.refresh.mp4')
        render.render_video(pid,cfg,tmp,fps=30,width=960,labels=False,crf=20)
        tmp.replace(video)
    after=errors() if repaired else before
    if max(after)>5:raise ValueError((pid,after))
    render.frame(pid,duration*.52,cfg,False).resize((640,360)).save(video.with_suffix('.webp'),quality=85)
    return {'id':pid,'repaired':repaired,'mean_errors':after,'sample_indices':indices,
            'sha256':hashlib.sha256(video.read_bytes()).hexdigest()}

if __name__=='__main__':
    lib=AtlasLibrary();ids=list(render.registry()[0]);results=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for row in pool.map(check,ids):
            results.append(row)
            if len(results)%25==0:print(f'{len(results)}/{len(ids)} verified',flush=True)
    (ROOT/'preview-runtime-validation.json').write_text(json.dumps({'count':len(results),'samples_per_preview':3,'results':results},indent=2))
    print('Done',len(results),'repaired',sum(r['repaired'] for r in results),flush=True)
