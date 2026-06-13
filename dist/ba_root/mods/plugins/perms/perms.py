# ba_meta require api 9

from __future__ import annotations
import json
import os

_DATA_PATH   = os.path.join(os.path.dirname(__file__), 'perms_data.json')
_RELOAD_FLAG = os.path.join(os.path.dirname(__file__), '.reload')

_data: dict = {
    'accounts':   {},
    'role_defs':  {},
    'role_perms': {},
    'tags':       {},
    'hierarchy':  {'owner': [], 'admin': [], 'staff': []},
}

# IDs de cuentas que tenían tag antes del reload, para detectar cambios
_prev_tags: dict = {}


def _load() -> None:
    global _data
    try:
        if os.path.exists(_DATA_PATH):
            with open(_DATA_PATH, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                _data.update(loaded)
                print(f'[perms] _load OK: {len(_data.get("tags", {}))} tags, id(_data)={id(_data)}')
    except Exception as e:
        print(f'[perms] load error: {e}')


def _save() -> None:
    tmp = _DATA_PATH + '.tmp'
    bak = _DATA_PATH + '.backup'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(_data, f, indent=2, ensure_ascii=False)
        if os.path.exists(_DATA_PATH):
            import shutil
            shutil.copyfile(_DATA_PATH, bak)
        os.replace(tmp, _DATA_PATH)
    except Exception as e:
        print(f'[perms] save error: {e}')


def _apply_live_if_online(changed_accs: list) -> None:
    """Llama tag.apply_live() en el thread principal de BS."""
    print(f'[perms] apply_live_if_online: {changed_accs}')
    try:
        import babase
        from plugins.tag import tag as _tag
        for acc in changed_accs:
            def _do(a=acc):
                try:
                    _tag.apply_live(a)
                    print(f'[perms] apply_live -> {a}')
                except Exception as e:
                    print(f'[perms] apply_live error {a}: {e}')
            babase.pushcall(_do, from_other_thread=True)
    except Exception as e:
        print(f'[perms] apply_live import error: {e}')
def _check_reload() -> None:
    """Loop en thread separado — detecta .reload y recarga _data."""
    import time
    while True:
        time.sleep(0.5)
        try:
            if os.path.exists(_RELOAD_FLAG):
                os.remove(_RELOAD_FLAG)
                old_tags = dict(_data.get('tags', {}))
                _load()
                print('[perms] recargado desde disco')
                new_tags = _data.get('tags', {})
                changed = [acc for acc, cfg in new_tags.items() if old_tags.get(acc) != cfg]
                changed += [acc for acc in old_tags if acc not in new_tags]
                if changed:
                    _apply_live_if_online(changed)
        except Exception as e:
            print(f'[perms] reload error: {e}')


def get_role(acc: str) -> str | None:
    for role, cfg in _data.get('role_defs', {}).items():
        if acc in cfg.get('ids', []):
            return role
    return None


def get_role_level(role: str | None) -> int:
    if not role:
        return 0
    return _data.get('role_defs', {}).get(role, {}).get('level', 0)


def has_perm(acc: str, cmd: str) -> bool:
    role = get_role(acc)
    if not role:
        return False
    cmds = _data.get('role_defs', {}).get(role, {}).get('commands', [])
    return 'all' in cmds or cmd in cmds


def get_role_cfg(role: str) -> dict | None:
    return _data.get('role_defs', {}).get(role)


def get_all_roles() -> list:
    return list(_data.get('role_defs', {}).keys())


def set_account_role(acc: str, role: str) -> None:
    for cfg in _data.get('role_defs', {}).values():
        ids = cfg.get('ids', [])
        if acc in ids:
            ids.remove(acc)
    _data['role_defs'][role].setdefault('ids', []).append(acc)
    _save()


def remove_account_role(acc: str) -> None:
    for cfg in _data.get('role_defs', {}).values():
        ids = cfg.get('ids', [])
        if acc in ids:
            ids.remove(acc)
    _save()


def create_role(name: str, cfg: dict) -> None:
    _data.setdefault('role_defs', {})[name] = cfg
    _save()


def add_role_perm(role: str, cmd: str) -> None:
    role_def = _data.get('role_defs', {}).get(role)
    if not role_def:
        return
    cmds = role_def.setdefault('commands', [])
    if cmd not in cmds:
        cmds.append(cmd)
    _save()


def get_tag(acc: str) -> dict | None:
    result = _data.get('tags', {}).get(acc)
    if result is not None:
        return result
    role = get_role(acc)
    if role:
        role_cfg = _data.get('role_defs', {}).get(role)
        if role_cfg:
            return role_cfg
    return None


def get_effects(acc: str) -> list:
    return _data.get('effects', {}).get(acc, [])


def set_effect(acc: str, effect: str) -> None:
    effects = _data.setdefault('effects', {})
    if acc not in effects:
        effects[acc] = []
    if effect not in effects[acc]:
        effects[acc].append(effect)
    _save()


def remove_effect(acc: str, effect: str) -> None:
    effects = _data.get('effects', {})
    if acc in effects and effect in effects[acc]:
        effects[acc].remove(effect)
        if not effects[acc]:
            del effects[acc]
    _save()


def clear_effects(acc: str) -> None:
    _data.get('effects', {}).pop(acc, None)
    _save()


def set_tag(acc: str, tag_cfg: dict) -> None:
    _data.setdefault('tags', {})[acc] = tag_cfg
    _save()


def remove_tag(acc: str) -> None:
    _data.get('tags', {}).pop(acc, None)
    _save()


def get_acc_from_client_id(client_id: int) -> str | None:
    try:
        import bascenev1 as bs
        roster = bs.get_game_roster()
        for entry in roster:
            if entry.get('client_id') == client_id:
                return entry.get('account_id')
    except Exception as e:
        print(f'[perms] get_acc_from_client_id error: {e}')
    return None


_reload_thread: 'threading.Thread | None' = None

_PENDING_ROLES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'nexus_data', 'pending_bs_roles.json')

def _check_pending_roles() -> None:
    import time
    while True:
        time.sleep(3)
        try:
            if not os.path.exists(_PENDING_ROLES_PATH):
                continue
            with open(_PENDING_ROLES_PATH, 'r', encoding='utf-8') as f:
                pending = json.load(f)
            if not pending:
                continue
            import bascenev1 as bs
            try:
                roster = bs.get_game_roster()
            except Exception:
                continue
            online_ids = {e.get('account_id') for e in roster if e.get('account_id')}
            changed = []
            for acc in list(pending.keys()):
                if acc in online_ids:
                    role = pending.pop(acc)
                    if role is None:
                        remove_account_role(acc)
                        print(f'[perms] unverify en vivo: {acc}')
                    else:
                        set_account_role(acc, role)
                        print(f'[perms] rol {role} en vivo: {acc}')
                    changed.append(acc)
            if changed:
                with open(_PENDING_ROLES_PATH, 'w', encoding='utf-8') as f:
                    json.dump(pending, f, indent=2)
                _apply_live_if_online(changed)
        except Exception as e:
            print(f'[perms] pending_roles error: {e}')


def enable() -> None:
    import threading
    global _reload_thread
    _load()
    _reload_thread = threading.Thread(target=_check_reload, daemon=True, name='perms_reload')
    _reload_thread.start()
    threading.Thread(target=_check_pending_roles, daemon=True, name='perms_pending').start()

    print('[perms] loaded')


_BANNED_PATH = os.path.join(os.path.dirname(__file__), 'banned.json')

def _load_banned() -> dict:
    try:
        if os.path.exists(_BANNED_PATH):
            with open(_BANNED_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f'[perms] banned load error: {e}')
    return {}

def _save_banned(data: dict) -> None:
    try:
        with open(_BANNED_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f'[perms] banned save error: {e}')

def ban(acc: str, reason: str = '') -> None:
    data = _load_banned()
    data[acc] = {'reason': reason}
    _save_banned(data)

def unban(acc: str) -> None:
    data = _load_banned()
    data.pop(acc, None)
    _save_banned(data)

def is_banned(acc: str) -> bool:
    return acc in _load_banned()

def get_ban_reason(acc: str) -> str:
    return _load_banned().get(acc, {}).get('reason', '')
