#!/usr/bin/env python3
"""Use lazy language imports in the pinned isolated fork; retain original backups."""
import argparse
import ast
import hashlib
import importlib.util
from pathlib import Path
import json

EXPECTED = {
    'text/__init__.py': '3e6eda12d143d0dcf39747849db6b99309d5b4a31ec69ae3888e5da757e4379f',
    'text/cleaner.py': 'f735926cb88c55c46c94172b483fc21b3a4ed080e40a8933b15643de9639f02b',
    'text/malay.py': '442af7b0bd353f38bae4d15d602c2aaf2316ef37fc4ce30122097af6366f5293',
}
MARKER = '# Gemini Malay lazy imports v2\n'


def patch(root):
    writes = []
    for name, sha in EXPECTED.items():
        p = root / name
        raw = p.read_bytes()
        if raw.startswith(MARKER.encode()):
            continue
        if raw.startswith(b'# Gemini Malay lazy imports v1\n'):
            raw = p.with_suffix(p.suffix + '.upstream').read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError('Unrecognized upstream code; preserve it and inspect: ' + name)
        s = raw.decode()
        if name == 'text/malay.py':
            s = s.replace('from .japanese import distribute_phone', 'from .malay_phone import distribute_phone')
            s = s.replace('    return normalizer\n', '''    asset = os.environ.get('GEMINI_MALAYA_DEMOJI')
    if asset:
        import json
        from malaya.preprocessing import Demoji
        with open(asset, encoding='utf-8') as f:
            normalizer.normalizer._demoji = Demoji(dictionary=json.load(f)).demoji
    return normalizer
''', 1)
        elif name == 'text/cleaner.py':
            start = s.index('from . import chinese,')
            end = s.index('\n\n\ndef clean_text', start)
            s = s[:start] + '''from . import cleaned_text_to_sequence
import copy
import importlib

class _LanguageModules(dict):
    def __getitem__(self, key):
        name = {'ZH':'chinese','JP':'japanese','EN':'english','ZH_MIX_EN':'chinese_mix',
                'KR':'korean','FR':'french','SP':'spanish','ES':'spanish','MS':'malay'}[key]
        return importlib.import_module('.' + name, __package__)

language_module_map = _LanguageModules()
''' + s[end:]
        else:
            node = next(n for n in ast.parse(s).body if isinstance(n, ast.FunctionDef) and n.name == 'get_bert')
            lines = s.splitlines(keepends=True)
            replacement = '''def get_bert(norm_text, word2ph, language, device):
    import importlib
    name = {'ZH':'chinese_bert','EN':'english_bert','JP':'japanese_bert','ZH_MIX_EN':'chinese_mix',
            'FR':'french_bert','SP':'spanish_bert','ES':'spanish_bert','KR':'korean','MS':'malay_bert'}[language]
    return importlib.import_module('.' + name, __package__).get_bert_feature(norm_text, word2ph, device)
'''
            s = ''.join(lines[:node.lineno-1]) + replacement + ''.join(lines[node.end_lineno:])
        s = MARKER + s
        ast.parse(s)
        backup = p.with_suffix(p.suffix + '.upstream')
        if backup.exists() and backup.read_bytes() != raw:
            raise ValueError('Backup conflict: ' + str(backup))
        writes.append((p, raw, s, backup))
    helper = MARKER + '''def distribute_phone(n_phone, n_word):
    phones_per_word = [0] * n_word
    for task in range(n_phone):
        min_tasks = min(phones_per_word)
        min_index = phones_per_word.index(min_tasks)
        phones_per_word[min_index] += 1
    return phones_per_word
'''
    helper_path = root / 'text/malay_phone.py'
    if helper_path.exists() and helper_path.read_text() != helper and not helper_path.read_text().startswith('# Gemini Malay lazy imports v1\n'):
        raise ValueError('Existing helper preserved')
    for p, raw, s, backup in writes:
        if not backup.exists():
            backup.write_bytes(raw)
        p.write_text(s)
    helper_path.write_text(helper)
    return {'patched': len(writes), 'root': str(root), 'models_modified': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package-root', type=Path)
    a = p.parse_args()
    if a.package_root:
        root = a.package_root
    else:
        spec = importlib.util.find_spec('melo')
        if spec is None or not spec.submodule_search_locations:
            p.error('MeloTTS-MS is not installed in this Python environment')
        root = Path(next(iter(spec.submodule_search_locations)))
    print(json.dumps(patch(root), indent=2))


if __name__ == '__main__':
    main()
