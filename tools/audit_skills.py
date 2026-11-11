"""Audit statik 18 sumber asal tanpa mengubahnya atau melaksanakan skripnya."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED=['remotion-best-practices','remotion-captions','remotion-create','remotion-docs','remotion-interactivity','remotion-license','remotion-maps','remotion-markup','remotion-multimedia','remotion-render','remotion-saas','remotion-studio','remotion-upgrade','playwright-cli','playwright-component-testing','playwright-trace','buat-video-motion-grafik','buat-video-motion-grafik-gemini']
def audit():
 root=ROOT/'.agents/skills';actual={p.name for p in root.iterdir() if p.is_dir()};rows=[]
 if actual!=set(EXPECTED):raise ValueError('Folder skill tidak sepadan 18 ID yang dijangka')
 for ident in EXPECTED:
  p=root/ident;skill=p/'SKILL.md';text=skill.read_text();name=re.search(r'^name:\s*(.+)$',text,re.M);description=re.search(r'^description:\s*(.+)$',text,re.M)
  if not text.startswith('---\n') or not name or name[1]!=ident or not description:raise ValueError('SKILL.md tidak sah: '+ident)
  files=[f for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts and not f.name.startswith('.bundle')]
  local_links=[]
  for target in re.findall(r'\]\(([^)]+)\)',text):
   target=target.split('#')[0]
   if target and not re.match(r'[a-z]+:',target) and not (p/target).exists():local_links.append(target)
  rows.append({'id':ident,'sha256':hashlib.sha256(skill.read_bytes()).hexdigest(),'description':description[1], 'files':len(files),'references':(p/'references').is_dir(),'scripts':(p/'scripts').is_dir(),'assets':(p/'assets').is_dir(),'missing_direct_links':local_links,'status':'VERIFIED_INSTRUCTIONS','windows_runtime':'NOT_TESTED','linux_runtime':'SELECTED_CAPABILITIES_TESTED_SEE_REPORTS' if ident.startswith('buat-video') else 'NOT_ALL_CAPABILITIES_TESTED','security_review':'STATIC_ONLY; no automatic execution of skill scripts','license_review':'PER_ASSET_REVIEW_REQUIRED','catalog_namespace':'argon-original-842' if ident=='buat-video-motion-grafik' else 'gemini-locked-922' if ident=='buat-video-motion-grafik-gemini' else None})
 return rows
if __name__=='__main__':
 rows=audit();(ROOT/'docs/v41-skill-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 manifest=json.loads((ROOT/'docs/skill-install-manifest.json').read_text());lookup={r['name']:r for r in manifest}
 for row in rows:
  old=lookup.get(row['id'],{'name':row['id'],'source':'User supplied Skill Argon multipart archive; not a public Git repo'})
  old.update({'instruction_sha256':row['sha256'],'current_files':row['files'],'status':row['status'],'windows_runtime':row['windows_runtime']});lookup[row['id']]=old
 (ROOT/'docs/skill-install-manifest.json').write_text(json.dumps(list(lookup.values()),ensure_ascii=False,indent=2)+'\n')
 print('PASS 18 skills; missing links:',sum(len(r['missing_direct_links']) for r in rows))
