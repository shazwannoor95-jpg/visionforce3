"""CI mesti menolak versi yang tidak diperuntukkan ledger remote."""
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
subprocess.run(['git','fetch','--quiet','origin','refs/heads/vf-version-ledger'],cwd=root,check=True)
ledger=json.loads(subprocess.check_output(['git','show','FETCH_HEAD:ledger.json'],cwd=root,text=True))
v=json.loads((root/'version.json').read_text());reserved=ledger['tasks'][v['task']]
for key in ['build','display','semver','fileVersion','baseCommit']:
 if reserved[key]!=v[key]:raise SystemExit('Versi tidak sepadan ledger: '+key)
print('PASS ledger reservation '+v['display'])
