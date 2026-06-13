# ba_meta require api 9
from __future__ import annotations

import json
import os
import time
import threading
import uuid

import bascenev1 as bs

_BASE_DIR  = os.path.join(os.path.dirname(__file__), '..', '..', 'nexus_data')
_CHAT_FILE  = os.path.join(_BASE_DIR, 'chat.json')
_DC_TO_BS   = os.path.join(_BASE_DIR, 'dc_to_bs.txt')
_MAX_MSGS  = 50

_chat_lock = threading.Lock()


def _texture_to_character(texture: str) -> str:
    _MAP = {
        'neoSpaz':  'neoSpaz',  'kronk':    'kronk',    'zoe':      'zoe',
        'jack':     'jackMcFlail', 'ninja':  'ninja',    'pixel':    'pixel',
        'frosty':   'frosty',   'santa':    'santa',     'cyborg':   'cyborg',
        'agent':    'agent',    'wizard':   'wizard',    'pirate':   'pirate',
        'robot':    'robot',    'toon':     'toon',      'mel':      'mel',
        'bear':     'bear',     'penguin':  'penguin',   'ali':      'ali',
        'bunny':    'bunny',    'octopus':  'octopus',   'cat':      'cat',
        'enforcer': 'enforcer', 'exploder': 'exploder',  'magicMan': 'magicMan',
        'assassin': 'assassin', 'bones':    'bones',     'helmet':   'helmet',
        'demoMan':  'demoMan',  'holiday':  'holiday',   'powerups': 'powerups',
    }
    tl = texture.lower()
    for key, char in _MAP.items():
        if key.lower() in tl:
            return char
    return 'neoSpaz'


def _parse_tag(tag: dict) -> dict:
    text  = tag.get('text', '')
    color = tag.get('color_stops', [[1.0, 1.0, 1.0]])[0]
    icon  = ''
    if text and ord(text[0]) > 0xe000:
        icon = text[0]
    elif text and ord(text[-1]) > 0xe000:
        icon = text[-1]
    clean = text.lstrip(icon).rstrip(icon).strip() if icon else text
    return {
        'tag_text':  clean,
        'tag_icon':  icon,
        'tag_color': color if isinstance(color, list) else [1.0, 1.0, 1.0],
    }


def _get_tag_info(account_id: str, name: str = '') -> dict:
    try:
        perms_path = os.path.join(
            os.path.dirname(__file__), '..', 'perms', 'perms_data.json'
        )
        if os.path.exists(perms_path):
            with open(perms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            tags = data.get('tags', {})
            for key, tag in tags.items():
                if account_id.startswith(key) or key.startswith(account_id):
                    return _parse_tag(tag)
            if name:
                name_clean = ''.join(c for c in name if not (0xe000 <= ord(c) <= 0xf8ff)).strip()
                for key, tag in tags.items():
                    if key == name_clean:
                        return _parse_tag(tag)
    except Exception:
        pass
    return {'tag_text': '', 'tag_icon': '', 'tag_color': [1.0, 1.0, 1.0]}


def _extract_icon_from_name(raw_name: str) -> str:
    """Extrae el unicode BS del nombre si lo tiene (inicio o final)."""
    if raw_name and ord(raw_name[0]) >= 0xe000:
        return raw_name[0]
    if raw_name and ord(raw_name[-1]) >= 0xe000:
        return raw_name[-1]
    return ''


def _write_message(account_id: str, name: str, message: str, player_info: dict, profile_name: str = '', raw_name: str = '') -> None:
    os.makedirs(_BASE_DIR, exist_ok=True)
    tag_icon = _extract_icon_from_name(raw_name)
    tag_color = player_info.get('color', [1.0, 1.0, 1.0])
    tag_info = {
        'tag_text':  '',
        'tag_icon':  tag_icon,
        'tag_color': tag_color,
    }
    entry = {
        'id':           str(uuid.uuid4()),
        'account_id':   account_id,
        'profile_name': profile_name,
        'name':         name,
        'message':      message,
        'timestamp':    time.time(),
        **player_info,
        **tag_info,
    }
    with _chat_lock:
        try:
            if os.path.exists(_CHAT_FILE):
                with open(_CHAT_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'messages': []}
            data['messages'].append(entry)
            data['messages'] = data['messages'][-_MAX_MSGS:]
            tmp = _CHAT_FILE + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            os.replace(tmp, _CHAT_FILE)
        except Exception as e:
            print(f'[live_chat] error escribiendo mensaje: {e}')


def on_chat(message: str, client_id: int) -> None:
    """Llamado por _hooks.py para cada mensaje de chat."""
    try:
        if message.startswith('/') or message.startswith('@'):
            return
        if client_id == -1:
            return

        roster = bs.get_game_roster()
        entry  = next((e for e in roster if e.get('client_id') == client_id), None)
        if entry is None:
            return

        account_id = entry.get('account_id', '')
        if not account_id:
            return

        profile_name = ''
        try:
            spec = json.loads(entry.get('spec_string', '{}'))
            profile_name = spec.get('n', '')
        except Exception:
            pass

        try:
            raw_name = entry['players'][0]['name_full']
        except Exception:
            raw_name = entry.get('display_string', account_id)
        name = ''.join(c for c in raw_name if not (0xe000 <= ord(c) <= 0xf8ff)).strip()

        player_info = {'character': 'neoSpaz', 'color': [1.0, 1.0, 1.0], 'highlight': [1.0, 1.0, 1.0]}
        try:
            sess = bs.get_foreground_host_session()
            if sess:
                for sp in sess.sessionplayers:
                    try:
                        if sp.get_account_id() == account_id:
                            info = sp.get_icon_info()
                            player_info = {
                                'character': _texture_to_character(info.get('texture', '')),
                                'color':     list(info.get('tint_color',  [1.0, 1.0, 1.0]))[:3],
                                'highlight': list(info.get('tint2_color', [1.0, 1.0, 1.0]))[:3],
                            }
                            break
                    except Exception:
                        continue
                else:
                    try:
                        colors = bs.get_player_profile_colors(entry.get('spec_string', '{}'))
                        if colors and len(colors) >= 2:
                            player_info['color']     = list(colors[0])[:3]
                            player_info['highlight'] = list(colors[1])[:3]
                    except Exception:
                        pass
        except Exception:
            pass

        threading.Thread(
            target=_write_message,
            args=(account_id, name, message, player_info, profile_name, raw_name),
            daemon=True,
        ).start()

    except Exception as e:
        print(f'[live_chat] on_chat error: {e}')


_dc_thread_started = False


def _dc_reader_thread() -> None:
    """Thread permanente que lee dc_to_bs.txt y pushea mensajes al hilo de BS."""
    import babase
    while True:
        time.sleep(1)
        if not os.path.exists(_DC_TO_BS):
            continue
        try:
            with open(_DC_TO_BS, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if not lines:
                continue
            with open(_DC_TO_BS, 'w', encoding='utf-8') as f:
                f.write('')
            for line in lines:
                line = line.strip()
                if line:
                    babase.pushcall(lambda l=line: bs.chatmessage(l), from_other_thread=True)
        except Exception as e:
            print(f'[live_chat] dc_reader error: {e}')


def enable() -> None:
    global _dc_thread_started
    os.makedirs(_BASE_DIR, exist_ok=True)
    if not os.path.exists(_CHAT_FILE):
        with open(_CHAT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'messages': []}, f)
    if not _dc_thread_started:
        _dc_thread_started = True
        threading.Thread(target=_dc_reader_thread, daemon=True).start()
    print('[live_chat] cargado')


def disable() -> None:
    print('[live_chat] desactivado')
