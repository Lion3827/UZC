# ba_meta require api 9
from __future__ import annotations

import importlib.util
import os
import sys

_PACKS_DIR = os.path.join(os.path.dirname(__file__), 'powerups')


def _load_pack(filepath: str) -> None:
    name = os.path.splitext(os.path.basename(filepath))[0]
    unique_name = f'_powerups__{name}'
    try:
        spec = importlib.util.spec_from_file_location(unique_name, filepath)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = mod
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        if hasattr(mod, 'enable'):
            mod.enable()
        print(f'[powerups] loaded: {name}')
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f'[powerups] failed to load {name}: {e}')


def _load_third_party() -> None:
    third = os.path.join(_PACKS_DIR, 'third_party')
    if not os.path.isdir(third):
        return
    for fname in sorted(os.listdir(third)):
        if fname.endswith('.py') and not fname.startswith('_'):
            _load_pack(os.path.join(third, fname))


def enable() -> None:
    if not os.path.isdir(_PACKS_DIR):
        os.makedirs(_PACKS_DIR)
        print('[powerups] powerups dir created')
        return

    for fname in sorted(os.listdir(_PACKS_DIR)):
        if fname == 'third_party':
            continue
        if fname.endswith('.py') and not fname.startswith('_'):
            _load_pack(os.path.join(_PACKS_DIR, fname))

    _load_third_party()
    