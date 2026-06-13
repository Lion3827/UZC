# ba_meta require api 9

from __future__ import annotations

import collections
import datetime
import importlib
import importlib.util
import json
import logging
import os
import sys
import warnings

import babase
import bascenev1 as bs
from baclassic._appmode import ClassicAppMode

_PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "plugins")
_loaded_plugins: list = []


# === CONFIG MAESTRA DEL SERVIDOR ===
_SERVER_CFG_PATH = os.path.join(os.path.dirname(__file__), "plugins", "server_config.json")
_SERVER_CFG: dict = {}

try:
    with open(_SERVER_CFG_PATH, encoding="utf-8") as _f:
        _SERVER_CFG = json.load(_f)
    print("[hooks] server_config.json cargado OK")
except Exception as _e:
    print(f"[hooks] server_config.json no encontrado o invalido: {_e}")

def get_server_cfg() -> dict:
    """Retorna la seccion server del config maestro."""
    return _SERVER_CFG.get("server", {})

def get_plugin_cfg(name: str) -> dict:
    """Retorna el bloque config de un plugin especifico. Uso: get_plugin_cfg("hud_ladder")"""
    return _SERVER_CFG.get("plugins", {}).get(name, {}).get("config", {})

def get_plugin_enabled(name: str) -> bool:
    """Retorna si un plugin esta habilitado segun server_config.json."""
    return _SERVER_CFG.get("plugins", {}).get(name, {}).get("enabled", True)
# === FIN CONFIG MAESTRA ===


# === PARCHE MAESTRO: deduplicación de DieMessage ===
# Evita que cualquier mod registre muertes múltiples por el mismo evento.
# Funciona a nivel de Spaz antes de que cualquier plugin lo vea.
def _install_die_dedup() -> None:
    from bascenev1lib.actor.spaz import Spaz
    import time as _time

    _orig_spaz_hm = Spaz.handlemessage
    _die_times: dict = {}  # id(node) -> timestamp ultima muerte
    _COOLDOWN = 0.5  # segundos

    def _dedup_hm(self, msg):
        if isinstance(msg, bs.DieMessage):
            try:
                node_id = id(self.node)
                now = _time.monotonic()
                last = _die_times.get(node_id, 0)
                if now - last < _COOLDOWN:
                    return  # duplicado, ignorar
                _die_times[node_id] = now
                # limpiar nodos viejos cada 100 muertes
                if len(_die_times) > 100:
                    cutoff = now - 10.0
                    for k in [k for k, v in _die_times.items() if v < cutoff]:
                        del _die_times[k]
            except Exception:
                pass
        return _orig_spaz_hm(self, msg)

    Spaz.handlemessage = _dedup_hm
    print('[hooks] parche anti-DieMessage duplicado instalado')
# === FIN PARCHE MAESTRO ===


def _load_plugins() -> None:
    if not os.path.isdir(_PLUGINS_DIR):
        os.makedirs(_PLUGINS_DIR)
        print("[hooks] plugins dir created")
        return

    entries = sorted(os.listdir(_PLUGINS_DIR))
    candidates = []

    for entry in entries:
        full = os.path.join(_PLUGINS_DIR, entry)
        if not os.path.isdir(full):
            continue
        meta_path = os.path.join(full, "plugin.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception as e:
                print(f"[hooks] {entry}: plugin.json invalid: {e}")
                continue
        else:
            meta = {"enabled": True, "priority": 50}

        if not meta.get("enabled", True):
            print(f"[hooks] {entry}: desactivado por plugin.json")
            continue
        if not get_plugin_enabled(entry):
            print(f"[hooks] {entry}: desactivado por server_config.json")
            continue

        candidates.append((meta.get("priority", 50), entry, meta))

    candidates.sort(key=lambda x: x[0])

    if not candidates:
        print("[hooks] no plugins found")
        return

    for _, name, meta in candidates:
        try:
            mod = importlib.import_module(f"plugins.{name}.{name}")
            _loaded_plugins.append(mod)
            if hasattr(mod, "enable"):
                mod.enable()
            print(f"[hooks] loaded: {name} v{meta.get('version', '?')}")
        except Exception as e:
            print(f"[hooks] failed to load {name}: {e}")


_original_classic_activate = ClassicAppMode.on_activate


def _new_classic_activate(*args, **kwargs):
    result = _original_classic_activate(*args, **kwargs)
    _on_classic_app_mode_active()
    return result


ClassicAppMode.on_activate = _new_classic_activate


def _on_classic_app_mode_active() -> None:
    try:
        import salsadiamond
        salsadiamond.set_server_name("Patata")
        print("[hooks] salsadiamond: server name set")
    except Exception as e:
        print(f"[hooks] salsadiamond failed: {e}")
    def _set_name() -> None:
        try:
            bs.set_public_party_name("/ue043Build")
            print("[hooks] party name set")
        except Exception as e:
            print(f"[hooks] set_public_party_name failed: {e}")
    babase.pushcall(_set_name)


_LOG_BUFFER: collections.deque = collections.deque(maxlen=300)
_CRASH_SIGNALS = (
    'Killing app due to stuck activity',
    'ERROR: Activity is not dying when expected',
)
_SILENCE = ('not dying when expected', 'WeakCallStrict', 'out-of-bounds messages', 'efro.debug', 'Icon not dying')
_LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')


def _dump_crash_log(trigger_msg: str) -> None:
    os.makedirs(_LOGS_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join(_LOGS_DIR, f'crash_{ts}.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'=== CRASH DUMP {ts} ===\n')
        f.write(f'Trigger: {trigger_msg}\n')
        f.write('=== LAST 300 LINES ===\n')
        f.write('\n'.join(_LOG_BUFFER))
    print(f'[hooks] crash log saved: {path}')


class _CrashHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = record.getMessage()
        except Exception:
            return
        if any(s in msg for s in _SILENCE):
            return
        _LOG_BUFFER.append(f'[{record.levelname}] {msg}')
        for signal in _CRASH_SIGNALS:
            if signal in msg:
                _dump_crash_log(msg)
                break


# ba_meta export babase.Plugin
class HooksPlugin(babase.Plugin):
    def on_app_running(self) -> None:
        try:
            _ml_path = os.path.join(os.path.dirname(__file__), 'plugins', 'maps_loader', 'maps_loader.py')
            _spec = importlib.util.spec_from_file_location('_maps_loader_early', _ml_path)
            _mod = importlib.util.module_from_spec(_spec)
            sys.modules['_maps_loader_early'] = _mod
            _spec.loader.exec_module(_mod)
            _mod.scan()
        except Exception as e:
            print(f'[hooks] maps early load failed: {e}')
        warnings.filterwarnings('ignore', message='.*WeakCallStrict.*')
        handler = _CrashHandler()
        handler.setLevel(logging.WARNING)
        root = logging.getLogger()
        root.addHandler(handler)
        _SILENCED = ('not dying when expected', 'WeakCallStrict', 'out-of-bounds messages', 'efro.debug', 'Icon not dying')
        for _h in root.handlers:
            if isinstance(_h, _CrashHandler):
                continue
            _orig_emit = _h.emit
            def _patched_emit(record, _orig=_orig_emit):
                try:
                    if any(s in record.getMessage() for s in _SILENCED):
                        return
                except Exception:
                    pass
                _orig(record)
            _h.emit = _patched_emit
        print("[hooks] initializing...")
        _install_die_dedup()
        _load_plugins()

import threading as _roster_threading
import time as _roster_time

_ROSTER_JSON = os.path.join(os.path.dirname(__file__), 'nexus_data', 'roster.json')

_texture_to_char_map = {
    'neoSpaz': 'neoSpaz', 'kronk': 'kronk', 'zoe': 'zoe',
    'jack': 'jackMcFlail', 'ninja': 'ninja', 'pixel': 'pixel',
    'frosty': 'frosty', 'santa': 'santa', 'cyborg': 'cyborg',
    'agent': 'agent', 'wizard': 'wizard', 'pirate': 'pirate',
    'robot': 'robot', 'toon': 'toon', 'mel': 'mel',
    'bear': 'bear', 'penguin': 'penguin', 'ali': 'ali',
    'bunny': 'bunny', 'octopus': 'octopus', 'cat': 'cat',
    'enforcer': 'enforcer', 'exploder': 'exploder', 'magicMan': 'magicMan',
    'assassin': 'assassin', 'bones': 'bones', 'helmet': 'helmet',
    'demoMan': 'demoMan', 'holiday': 'holiday', 'powerups': 'powerups',
}

def _tex_to_char(texture: str) -> str:
    tl = texture.lower()
    for key, char in _texture_to_char_map.items():
        if key.lower() in tl:
            return char
    return 'neoSpaz'

def _do_roster_write() -> None:
    import json as _json
    import bascenev1 as _bs
    try:
        from plugins.perms import perms as _perms
        import _bascenev1
        roster_check = _bs.get_game_roster() or []
        for entry in roster_check:
            acc = entry.get('account_id', '')
            cid = entry.get('client_id', -1)
            if acc and cid >= 0 and _perms.is_banned(acc):
                reason = _perms.get_ban_reason(acc)
                msg = '🚫 Has sido BANEADO de este servidor.'
                if reason:
                    msg += f' Razon: {reason}.'
                msg += ' Para apelar contacta a un Owner en Discord.'
                try:
                    _bascenev1.chatmessage(msg, clients=[cid])
                except Exception:
                    _bascenev1.chatmessage(msg)
                _bascenev1.disconnect_client(cid, ban_time=600)
                print(f'[hooks] roster ban kick: {acc}')
    except Exception as e:
        print(f'[hooks] roster ban check error: {e}')
    try:
        roster = _bs.get_game_roster() or []
        aid_to_entry = {}
        for p in roster:
            aid = p.get('account_id', '')
            if aid and aid != '-1':
                aid_to_entry[aid] = p
        players = []
        try:
            session = _bs.get_foreground_host_session()
            sps = session.sessionplayers if session else []
        except Exception:
            sps = []
        for sp in sps:
            try:
                aid = sp.get_account_id()
                if not aid or aid == '-1':
                    continue
                rp = aid_to_entry.get(aid, {})
                raw_name = '<lobby>'
                try:
                    raw_name = rp['players'][0]['name_full']
                except Exception:
                    raw_name = rp.get('display_string', '<lobby>')
                name = ''.join(c for c in raw_name if not (0xe000 <= ord(c) <= 0xf8ff)).strip()
                tag_icon = ''
                if raw_name and ord(raw_name[0]) >= 0xe000:
                    tag_icon = raw_name[0]
                elif raw_name and ord(raw_name[-1]) >= 0xe000:
                    tag_icon = raw_name[-1]
                character = 'neoSpaz'
                color     = [1.0, 1.0, 1.0]
                highlight = [1.0, 1.0, 1.0]
                try:
                    info = sp.get_icon_info()
                    character = _tex_to_char(info.get('texture', ''))
                    color     = list(info.get('tint_color',  [1.0, 1.0, 1.0]))[:3]
                    highlight = list(info.get('tint2_color', [1.0, 1.0, 1.0]))[:3]
                except Exception:
                    pass
                ping = -1
                try:
                    cid = rp.get('client_id', -1)
                    if cid >= 0:
                        import _bascenev1
                        ping = _bascenev1.get_client_ping(cid)
                except Exception:
                    pass
                players.append({
                    'aid':       aid,
                    'name':      name,
                    'tag_icon':  tag_icon,
                    'character': character,
                    'color':     color,
                    'highlight': highlight,
                    'ping':      ping,
                })
            except Exception:
                pass
        with open(_ROSTER_JSON, 'w', encoding='utf-8') as _f:
            _json.dump({'players': players}, _f)
        _flag = _ROSTER_JSON + '.flag'
        with open(_flag, 'w') as _f:
            _f.write('1')
    except Exception:
        pass

def _roster_writer() -> None:
    import babase as _babase
    while True:
        _babase.pushcall(_do_roster_write, from_other_thread=True)
        _roster_time.sleep(5)

_roster_threading.Thread(target=_roster_writer, daemon=True).start()

_roster_hooks_installed = False

def _install_roster_hooks():
    global _roster_hooks_installed
    if _roster_hooks_installed:
        return
    _roster_hooks_installed = True

    from bascenev1._activity import Activity

    _orig_a_join  = Activity.on_player_join
    _orig_a_leave = Activity.on_player_leave

    def _hooked_a_join(self, player):
        try:
            acc = player.sessionplayer.get_account_id()
            from plugins.perms import perms as _perms
            if _perms.is_banned(acc):
                import _bascenev1
                reason = _perms.get_ban_reason(acc)
                _bascenev1.disconnect_client(player.sessionplayer.inputdevice.client_id, ban_time=0)
                print(f'[hooks] ban bloqueado: {acc}')
                return
        except Exception as e:
            print(f'[hooks] ban check error: {e}')
        _orig_a_join(self, player)
        _do_roster_write()
        try:
            import json, os
            pending_path = os.path.join(os.path.dirname(__file__), 'nexus_data', 'pending_bs_roles.json')
            if os.path.exists(pending_path):
                with open(pending_path, 'r', encoding='utf-8') as f:
                    pending = json.load(f)
                acc = player.sessionplayer.get_account_id()
                if acc in pending:
                    role = pending.pop(acc)
                    from plugins.perms import perms as _perms
                    if role is None:
                        _perms.remove_account_role(acc)
                        print(f'[hooks] rol removido de {acc} desde Discord')
                    else:
                        _perms.set_account_role(acc, role)
                        print(f'[hooks] rol {role} asignado a {acc} desde verificacion Discord')
                    with open(pending_path, 'w', encoding='utf-8') as f:
                        json.dump(pending, f, indent=2)
        except Exception as e:
            print(f'[hooks] pending_bs_role error: {e}')

    def _hooked_a_leave(self, player):
        _orig_a_leave(self, player)
        _do_roster_write()

    Activity.on_player_join  = _hooked_a_join

    from bascenev1._session import Session
    _orig_s_request = Session.on_player_request

    def _hooked_s_request(self, player):
        try:
            import _bascenev1
            acc = player.get_account_id()
            from plugins.perms import perms as _perms
            if _perms.is_banned(acc):
                reason = _perms.get_ban_reason(acc)
                msg = '🚫 Has sido BANEADO de este servidor.'
                if reason:
                    msg += f' Razon: {reason}.'
                msg += ' Para apelar contacta a un Owner en Discord.'
                cid = player.inputdevice.client_id
                try:
                    _bascenev1.chatmessage(msg, clients=[cid])
                except Exception:
                    _bascenev1.chatmessage(msg)
                _bascenev1.disconnect_client(cid, ban_time=600)
                print(f'[hooks] ban lobby bloqueado: {acc}')
                return False
        except Exception as e:
            print(f'[hooks] ban request error: {e}')
        return _orig_s_request(self, player)

    Session.on_player_request = _hooked_s_request
    Activity.on_player_leave = _hooked_a_leave

import babase as _babase2
_babase2.pushcall(_install_roster_hooks, from_other_thread=False)
