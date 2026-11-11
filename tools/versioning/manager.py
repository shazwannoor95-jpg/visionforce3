"""Nombor tugasan melalui ledger Git fast-forward + tag reservation atomik."""
import argparse
import datetime
import json
import re
import subprocess
import uuid
from pathlib import Path

LEDGER = 'refs/heads/vf-version-ledger'


class VersionManager:
    def __init__(self, repo): self.repo = Path(repo)

    def git(self, *args, data=None, check=True):
        return subprocess.run(['git', '-C', str(self.repo), *args], input=data, text=True,
                              capture_output=True, check=check)

    def reserve(self, task, title, remote='origin'):
        if remote not in self.git('remote').stdout.splitlines():raise ValueError('Gunakan remote Git yang dikonfigurasi')
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',task): raise ValueError('ID tugasan tidak sah')
        for attempt in range(20):
            result = self.git('ls-remote',remote,LEDGER,'refs/tags/vf-reservation-*','refs/tags/v0.0.0.*')
            refs = [line.split() for line in result.stdout.splitlines()]
            parent = next((sha for sha,ref in refs if ref==LEDGER),None)
            high = max([int(ref.rsplit('-',1)[1]) for _,ref in refs if re.fullmatch(r'refs/tags/vf-reservation-\d+',ref)]+[int(ref.rsplit('.',1)[1]) for _,ref in refs if re.fullmatch(r'refs/tags/v0\.0\.0\.\d+',ref)]+[0])
            state = {'counter':high,'tasks':{}}
            if parent:
                self.git('fetch','--quiet',remote,parent)
                state=json.loads(self.git('show',parent+':ledger.json').stdout)
            if task in state['tasks']: return state['tasks'][task]
            number=max(high,state['counter'])+1
            if number>=2**32: raise ValueError('Julat FileVersion penuh; nombor tidak direset atau diguna semula')
            record={'task':task,'build':number,'display':f'v0.0.0.{number}', 'semver':f'0.{number//65536}.{number%65536}',
                    'fileVersion':f'0.0.{number//65536}.{number%65536}','title':title,'baseCommit':self.git('rev-parse','HEAD').stdout.strip(),
                    'createdAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DRAFT'}
            state['counter']=number;state['tasks'][task]=record
            blob=self.git('hash-object','-w','--stdin',data=json.dumps(state,sort_keys=True)+'\n').stdout.strip()
            tree=self.git('mktree',data=f'100644 blob {blob}\tledger.json\n').stdout.strip()
            args=['commit-tree',tree]
            if parent: args+=['-p',parent]
            commit=self.git(*args,data=f'Reserve {record["display"]}: {task}\n').stdout.strip()
            tag=f'refs/tags/vf-reservation-{number}'
            push=self.git('push','--atomic',remote,f'{commit}:{LEDGER}',f'{commit}:{tag}',check=False)
            if push.returncode==0:return record
            # Hanya retry jika ledger bergerak (konflik serentak), bukan auth/network failure.
            latest=self.git('ls-remote',remote,LEDGER).stdout.split()
            if (latest[0] if latest else None)==parent:raise RuntimeError('Ledger tidak dapat disimpan: '+push.stderr)
        raise RuntimeError('Konflik ledger berulang; nombor tidak diperuntukkan')

    def checkpoint(self, tag, commit='HEAD'):
        # Git menolak tag yang sedia ada; tiada -f/reset.
        self.git('check-ref-format','refs/tags/'+tag)
        resolved=self.git('rev-parse','--verify','--end-of-options',commit+'^{commit}').stdout.strip()
        self.git('tag','--',tag,resolved)
        return self.git('rev-parse',tag).stdout.strip()

    def compare(self, old, new='HEAD'):
        old_sha=self.git('rev-parse','--verify','--end-of-options',old+'^{commit}').stdout.strip()
        new_sha=self.git('rev-parse','--verify','--end-of-options',new+'^{commit}').stdout.strip()
        return self.git('diff','--stat',old_sha,new_sha,'--').stdout

    def restore_source(self, commit, destination):
        destination=Path(destination).resolve()
        if destination.exists():raise ValueError('Destinasi mesti baharu; sumber semasa tidak ditimpa')
        resolved=self.git('rev-parse','--verify','--end-of-options',commit+'^{commit}').stdout.strip()
        # Clone berasingan, bukan reset/checkout destruktif.
        subprocess.run(['git','clone','--no-hardlinks','--no-checkout',str(self.repo.resolve()),str(destination)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(destination),'checkout','--detach',resolved],check=True,capture_output=True)
        return resolved


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',default='.')
    s=p.add_subparsers(dest='command',required=True)
    r=s.add_parser('reserve');r.add_argument('--task',required=True);r.add_argument('--title',required=True);r.add_argument('--remote',default='origin');r.add_argument('--output')
    c=s.add_parser('checkpoint');c.add_argument('tag');c.add_argument('--commit',default='HEAD')
    h=s.add_parser('history');h.add_argument('--remote',default='origin')
    d=s.add_parser('compare');d.add_argument('old');d.add_argument('--new',default='HEAD')
    r=s.add_parser('restore-source');r.add_argument('commit');r.add_argument('destination');r.add_argument('--approve',action='store_true')
    a=p.parse_args();m=VersionManager(a.repo)
    if a.command=='reserve':
        result=m.reserve(a.task,a.title,a.remote)
        if a.output:
            out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
            if out.exists():raise ValueError('Rekod tempatan sedia ada; jangan overwrite')
            out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    elif a.command=='checkpoint':print(m.checkpoint(a.tag,a.commit))
    elif a.command=='compare':print(m.compare(a.old,a.new))
    elif a.command=='restore-source':
        if not a.approve:raise ValueError('Semak compare dan beri --approve untuk salinan baharu')
        print(m.restore_source(a.commit,a.destination))
    else:
        m.git('fetch','--quiet',a.remote,LEDGER);print(m.git('show','FETCH_HEAD:ledger.json').stdout)

if __name__=='__main__':main()

# Rekod penerimaan tidak memberi kebenaran menerbitkan release dengan sendirinya.
REQUIRED_STABLE_CHECKS=('unit','typecheck','windows_packaged','windows_installer_spaces','windows_installer_plain','windows_portable','video_render','checksums')

def record_result(directory, record, status, checks, source_commit, approved=False):
    if status not in ('DRAFT','BUILDING','FAILED','TESTED','STABLE','ARCHIVED'):raise ValueError('Status versi tidak sah')
    if status=='STABLE' and (not approved or any(checks.get(k)!='PASS' for k in REQUIRED_STABLE_CHECKS)):
        raise ValueError('STABLE memerlukan kelulusan serta semua ujian penerimaan Windows')
    if (status=='TESTED' and not checks) or (any(v=='FAIL' for v in checks.values()) and status in ('TESTED','STABLE')):
        raise ValueError('Ujian gagal/tidak tersedia; gunakan FAILED/DRAFT')
    record={**record,'status':status,'checks':checks,'sourceCommit':source_commit,'eventAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    dest=Path(directory)/record['display']/'events';dest.mkdir(parents=True,exist_ok=True)
    out=dest/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'-'+uuid.uuid4().hex+'.json')
    with out.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    history_file=Path(directory)/'history.json'
    history=json.loads(history_file.read_text()) if history_file.exists() else []
    history=[r for r in history if r.get('display')!=record['display']]+[record]
    history.sort(key=lambda r:r.get('build',0),reverse=True)
    temp=history_file.with_suffix('.'+uuid.uuid4().hex+'.tmp');temp.write_text(json.dumps(history,indent=2)+'\n');temp.replace(history_file)
    return out
