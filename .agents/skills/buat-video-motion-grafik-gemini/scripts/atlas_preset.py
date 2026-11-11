#!/usr/bin/env python3
"""Route to the verified Atlas implementation installed from atlas_locked."""
import importlib.util
import os
from pathlib import Path
import sys

root = Path(os.environ.get('GEMINI_ATLAS_ROOT', Path(__file__).resolve().parents[1] / 'atlas_locked'))
entry = root / 'scripts/atlas_preset.py'
if not entry.is_file():
    raise SystemExit('Install selected core + atlas_locked packs from the current Drive manifest; or set GEMINI_ATLAS_ROOT to the verified locked toolkit root.')
sys.path.insert(0, str(entry.parent))
spec = importlib.util.spec_from_file_location('_gemini_locked_atlas', entry)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
AtlasLibrary = module.AtlasLibrary
AtlasPreset = module.AtlasPreset
main = module.main
if __name__ == '__main__':
    main()
