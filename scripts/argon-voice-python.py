#!/usr/bin/env python3
"""Run isolated voice Python with the local non-secret runtime selectors."""
import json,os,pathlib,subprocess,sys
root=pathlib.Path('/workspace/argon-runtime')
settings=root/'vo-env.json'
if not settings.is_file():raise SystemExit('Voice runtime not installed on this machine; see docs/ARGON-VOICE-MS.md')
env=dict(os.environ,**json.loads(settings.read_text()))
raise SystemExit(subprocess.call([str(root/'vo-venv/bin/python'),*sys.argv[1:]],env=env))
