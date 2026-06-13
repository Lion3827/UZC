# ba_meta require api 9

from __future__ import annotations
import bascenev1 as bs

try:
    from plugins.perms import perms as _perms
    _PERMS_AVAILABLE = True
except Exception:
    _PERMS_AVAILABLE = False

_MODULES = [
    'plugins.cmds.all.all',
    'plugins.cmds.admin.admin',
    'plugins.cmds.trolls.trolls',
]

_CMDS: dict = {}


def _load_cmds() -> None:
    for mod_path in _MODULES:
        try:
            parts  = mod_path.split('.')
            module = __import__(mod_path, fromlist=[parts[-1]])
            for name, entry in module.CMDS.items():
                _CMDS[name] = entry
        except Exception as e:
            print(f'[cmds] error loading {mod_path}: {e}')


def _reply(msg: str, color: tuple = (1.0, 1.0, 1.0)) -> None:
    try:
        import _bascenev1
        _bascenev1.chatmessage(msg)
    except Exception:
        try:
            bs.broadcastmessage(msg, color=color)
        except Exception:
            pass


def _find_sp_by_client_id(client_id: int) -> object | None:
    try:
        roster     = bs.get_game_roster()
        account_id = None
        for entry in roster:
            if entry.get('client_id') == client_id:
                account_id = entry.get('account_id')
                break
        if account_id is None:
            return None
        session = bs.get_foreground_host_session()
        if not session:
            return None
        for sp in session.sessionplayers:
            try:
                if sp.get_account_id() == account_id:
                    return sp
            except Exception:
                pass
    except Exception as e:
        print(f'[cmds] find_sp error: {e}')
    return None


def _handle_chat(msg: str, sp: object) -> bool:
    if not msg.startswith('/'):
        return False
    parts = msg[1:].strip().split()
    if not parts:
        return False
    cmd  = parts[0].lower()
    args = parts[1:]

    if cmd not in _CMDS:
        return False

    perm, func = _CMDS[cmd]
    _PUBLIC = {'stats','rank','top','list','report','help','ns','ping','pb','discord','v'}
    if cmd not in _PUBLIC:
        try:
            acc = sp.get_account_id()
        except Exception:
            return True
        if not (_PERMS_AVAILABLE and _perms.has_perm(acc, cmd)):
            _reply('Sin permisos.')
            return True

    func(sp, args)
    return True


def _filter_chat_hook(msg: str, client_id: int) -> str | None:
    try:
        if not msg.startswith('/'):
            return msg
        sp = _find_sp_by_client_id(client_id)
        if sp and _handle_chat(msg, sp):
            return None
    except Exception as e:
        print(f'[cmds] filter_chat_hook error: {e}')
    return msg


def enable() -> None:
    try:
        from baclassic._appmode import ClassicAppMode
        _orig = ClassicAppMode.handle_remote_chat_message
        def _patched(self, msg, client_id):
            if _filter_chat_hook(msg, client_id) is None:
                return
            _orig(self, msg, client_id)
        ClassicAppMode.handle_remote_chat_message = _patched
        print("[cmds] chat hook registrado")
    except Exception as e:
        print(f"[cmds] error registrando chat hook: {e}")
    _load_cmds()
    print(f'[cmds] loaded — {len(_CMDS)} cmds: {", ".join(_CMDS.keys())}')
