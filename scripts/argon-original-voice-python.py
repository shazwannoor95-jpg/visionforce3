#!/usr/bin/env python3
"""Run the verified original CPython 3.11.18 voice bundle, isolated from system tools."""
import json,os,pathlib,subprocess,sys
root=pathlib.Path('/workspace/argon-runtime/vo-original-cp31118')
settings=root/'runtime-env.json'
if not settings.is_file():raise SystemExit('Original voice bundle missing; see docs/ARGON-CP31118-MS.md')
env=os.environ.copy()
cache=pathlib.Path('/workspace/argon-runtime/cache')
for name,folder in [('MALAYA_CACHE','malaya'),('MALAYA-SPEECH_CACHE','malaya-speech'),('HF_HOME','huggingface')]:env[name]=str(cache/folder)
env.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','MODEL_ID':'/workspace/argon-runtime/vo-models/malay-bert'})
s=json.loads(settings.read_text())
for k,v in s.items():
 if k.endswith('_prepend'):
  name=k[:-8];env[name]=v+(os.pathsep+env[name] if env.get(name) else '')
 elif k not in ('python','venv'):env[k]=v
raise SystemExit(subprocess.call([str(root/'venv/bin/python'),*sys.argv[1:]],env=env))
