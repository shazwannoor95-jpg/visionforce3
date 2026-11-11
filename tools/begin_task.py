"""Permulaan tugasan kod baharu: checkpoint + peruntukan versi remote."""
import argparse,json,subprocess
from pathlib import Path
from versioning.manager import VersionManager
p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--title',required=True);p.add_argument('--branch',required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];manager=VersionManager(root)
if manager.git('status','--porcelain').stdout:raise SystemExit('Working tree belum bersih. Simpan checkpoint perubahan pengguna dahulu; tiada reset dilakukan.')
if not a.branch.startswith('feat/'):raise SystemExit('Gunakan branch feat/ khusus, bukan main.')
manager.checkpoint('checkpoint/'+a.task)
manager.git('switch','-c',a.branch)
record=manager.reserve(a.task,a.title)
(root/'version.json').write_text(json.dumps(record,indent=2)+'\n')
print(record['display']);print('Jalankan node desktop/scripts/sync-version.cjs sebelum build.')
