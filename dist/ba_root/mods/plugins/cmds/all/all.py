from __future__ import annotations

import datetime
import json
import os
import shutil
import threading
import time

import bascenev1 as bs

try:
    from plugins.stats import stats as _stats
    _STATS_AVAILABLE = True
except Exception:
    _STATS_AVAILABLE = False

try:
    from plugins.perms import perms as _perms
    _PERMS_AVAILABLE = True
except Exception:
    _PERMS_AVAILABLE = False

try:
    from plugins.chatlog import chatlog as _chatlog
    _CHATLOG_AVAILABLE = True
except Exception:
    _CHATLOG_AVAILABLE = False

_BASE_DIR     = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'nexus_data')
_REPORTS_FILE = os.path.join(_BASE_DIR, 'reports.json')
_COOLDOWNS: dict = {}
_COOLDOWN_SECS  = 120
_report_lock    = threading.Lock()

def _reply(msg: str, color: tuple = (1.0, 1.0, 1.0)) -> None:
    try:
        import _bascenev1
        _bascenev1.chatmessage(msg)
    except Exception:
        try:
            bs.broadcastmessage(msg, color=color)
        except Exception:
            pass

def _atomic_write(path: str, data: list) -> None:
    tmp = path + '.tmp'
    bak = path + '.backup'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if os.path.exists(path):
            shutil.copyfile(path, bak)
        os.replace(tmp, path)
    except Exception as e:
        print(f'[report] atomic_write error: {e}')

def _load_reports() -> list:
    if not os.path.exists(_REPORTS_FILE):
        return []
    try:
        with open(_REPORTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        bak = _REPORTS_FILE + '.backup'
        if os.path.exists(bak):
            try:
                with open(bak, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
    return []

def _save_report(entry: dict) -> None:
    os.makedirs(_BASE_DIR, exist_ok=True)
    reports = _load_reports()
    reports.append(entry)
    if len(reports) > 500:
        reports = reports[-500:]
    _atomic_write(_REPORTS_FILE, reports)

def _find_by_client_id(client_id: int) -> dict | None:
    try:
        for entry in bs.get_game_roster():
            if entry.get('client_id') == client_id:
                return entry
    except Exception:
        pass
    return None

def _get_context() -> dict:
    ctx: dict = {}
    try:
        session = bs.get_foreground_host_session()
        if session:
            ctx['players_online'] = len(session.sessionplayers)
        act = bs.get_foreground_host_activity()
        if act:
            ctx['activity'] = type(act).__name__
    except Exception:
        pass
    return ctx

def cmd_stats(sp: object, args: list) -> None:
    if not _STATS_AVAILABLE:
        _reply('Stats no disponible.')
        return
    try:
        acc = sp.get_v1_account_id()
        p   = _stats.get_player(acc)
        if not p:
            _reply('No tenes stats registradas aun.')
            return
        kd = _stats.calc_kd(p)
        wr = _stats.calc_win_ratio(p)
        _reply(f"Stats de {p['name']}", (0.6, 0.9, 1.0))
        _reply(f"Kills: {p['kills']}  Muertes: {p['deaths']}  K/D: {kd}", (0.6, 0.9, 1.0))
        _reply(f"Partidas: {p['games']}  Victorias: {p['wins']}  WR: {wr}%", (0.6, 0.9, 1.0))
        _reply(f"NS: {p['ns']}  Division: {p['division']}", (0.6, 0.9, 1.0))
    except Exception as e:
        print(f'[cmds.all] stats error: {e}')

def cmd_rank(sp: object, args: list) -> None:
    if not _STATS_AVAILABLE:
        _reply('Stats no disponible.')
        return
    try:
        acc            = sp.get_v1_account_id()
        data           = _stats.get_stats()
        if not data:
            _reply('No hay datos de ranking aun.')
            return
        sorted_players = sorted(data.values(), key=lambda p: p.get('kills', 0), reverse=True)
        rank = 0
        for i, p in enumerate(sorted_players):
            if p.get('aid') == acc:
                rank = i + 1
                break
        if not rank:
            _reply('No estas en el ranking aun.')
            return
        total = len(sorted_players)
        p     = data.get(acc, {})
        _reply(f"#{rank} de {total} | {sp.getname()} | Kills: {p.get('kills', 0)}", (1.0, 0.85, 0.2))
    except Exception as e:
        print(f'[cmds.all] rank error: {e}')

def cmd_top(sp: object, args: list) -> None:
    if not _STATS_AVAILABLE:
        _reply('Stats no disponible.')
        return
    try:
        data = _stats.get_stats()
        if not data:
            _reply('No hay datos aun.')
            return
        sorted_players = sorted(data.values(), key=lambda p: p.get('kills', 0), reverse=True)
        _reply('--- Top 5 ---', (1.0, 0.85, 0.2))
        for i, p in enumerate(sorted_players[:5]):
            _reply(f"#{i+1} {p['name']} | Kills: {p.get('kills', 0)} | NS: {p.get('ns', 500)}", (1.0, 0.85, 0.2))
    except Exception as e:
        print(f'[cmds.all] top error: {e}')

def cmd_list(sp: object, args: list) -> None:
    try:
        roster = bs.get_game_roster()
        if not roster:
            _reply('No hay jugadores conectados.')
            return
        _reply('--- Jugadores ---')
        for entry in roster:
            cid  = entry.get('client_id', '?')
            aid  = entry.get('account_id', '?')
            name = '?'
            try:
                name = entry['players'][0]['name_full']
            except Exception:
                name = entry.get('display_string', '?')
            role = (_perms.get_role(aid) if _PERMS_AVAILABLE else None) or 'user'
            _reply(f'[{cid}] {name} | {role}')
    except Exception as e:
        print(f'[cmds.all] list error: {e}')

def cmd_report(sp: object, args: list) -> None:
    if len(args) < 2:
        _reply('/report [clientID] [razon]', (1.0, 0.6, 0.2))
        return
    try:
        target_cid = int(args[0])
    except ValueError:
        _reply('clientID debe ser un numero. Usa /list para verlos.', (1.0, 0.4, 0.4))
        return

    reporter_aid  = sp.get_v1_account_id()
    reporter_name = sp.getname(full=True)

    with _report_lock:
        last = _COOLDOWNS.get(reporter_aid, 0)
        if time.time() - last < _COOLDOWN_SECS:
            remaining = int(_COOLDOWN_SECS - (time.time() - last))
            _reply(f'Espera {remaining}s antes de reportar de nuevo.', (1.0, 0.4, 0.4))
            return
        _COOLDOWNS[reporter_aid] = time.time()

    target_entry = _find_by_client_id(target_cid)
    if not target_entry:
        _reply('Jugador no encontrado. Usa /list para ver los IDs.', (1.0, 0.4, 0.4))
        return

    target_aid  = target_entry.get('account_id', '?')
    target_name = target_entry.get('display_string', '?')
    try:
        target_name = target_entry['players'][0]['name_full']
    except Exception:
        pass

    if target_aid == reporter_aid:
        _reply('No podes reportarte a vos mismo.', (1.0, 0.4, 0.4))
        return

    reason      = ' '.join(args[1:])
    target_role = _perms.get_role(target_aid) if _PERMS_AVAILABLE else None

    reporter_character = 'neoSpaz'
    reporter_color     = [1.0, 1.0, 1.0]
    reporter_highlight = [1.0, 1.0, 1.0]
    try:
        act = bs.get_foreground_host_activity()
        if act:
            for player in act.players:
                try:
                    if player.sessionplayer.get_v1_account_id() == reporter_aid:
                        node = player.actor.node
                        reporter_character = getattr(node, 'style', 'neoSpaz')
                        reporter_color     = list(getattr(node, 'color', (1.0, 1.0, 1.0)))
                        reporter_highlight = list(getattr(node, 'highlight', (1.0, 1.0, 1.0)))
                        break
                except Exception:
                    pass
    except Exception:
        pass
    if reporter_character == 'neoSpaz':
        try:
            session = bs.get_foreground_host_session()
            for sp in session.sessionplayers:
                try:
                    if sp.get_v1_account_id() == reporter_aid:
                        reporter_character = sp.character
                        reporter_color     = list(sp.color)
                        reporter_highlight = list(sp.highlight)
                        break
                except Exception:
                    pass
        except Exception:
            pass

    entry = {
        'ts':                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ts_unix':            time.time(),
        'reporter_aid':       reporter_aid,
        'reporter_name':      reporter_name,
        'reporter_character': reporter_character,
        'reporter_color':     reporter_color,
        'reporter_highlight': reporter_highlight,
        'target_aid':         target_aid,
        'target_name':        target_name,
        'target_role':        target_role,
        'reason':             reason,
        'chat_snapshot':      _chatlog.snapshot() if _CHATLOG_AVAILABLE else [],
        'context':            _get_context(),
    }

    threading.Thread(target=_save_report, args=(entry,), daemon=True).start()
    _reply(f'Reporte enviado contra {target_name}.', (0.4, 1.0, 0.5))
    print(f'[report] {reporter_name} reporto a {target_name} — {reason}')

def cmd_help(sp: object, args: list) -> None:
    _reply('=== Comandos del servidor ===', (0.6, 0.9, 1.0))
    _reply('-- Generales --', (1.0, 0.85, 0.2))
    _reply('/stats — tus estadisticas de juego', (0.8, 0.8, 0.8))
    _reply('/rank — tu posicion en el ranking', (0.8, 0.8, 0.8))
    _reply('/top — top 5 jugadores del ladder', (0.8, 0.8, 0.8))
    _reply('/ns — como funciona el sistema de puntos NS', (0.8, 0.8, 0.8))
    _reply('/list — jugadores conectados con su ID', (0.8, 0.8, 0.8))
    _reply('/pb [cid] — ver account ID propio o de otro', (0.8, 0.8, 0.8))
    _reply('/ping [cid|all] — ver ping propio o de todos', (0.8, 0.8, 0.8))
    _reply('/report [cid] [razon] — reportar un jugador', (0.8, 0.8, 0.8))
    _reply('/help — esta lista de comandos', (0.8, 0.8, 0.8))
    _reply('-- Sistema NS --', (0.4, 0.8, 1.0))
    _reply('NS = Nivel de Skill. Sube matando y baja al morir.', (0.8, 0.8, 0.8))
    _reply('Cuanto mas alto el NS del rival, mas ganas al matarlo.', (0.8, 0.8, 0.8))
    _reply('Divisiones: Madera > Piedra > Hierro > Bronce > Plata > Oro > Diamante > Leyenda', (0.8, 0.8, 0.8))
    _reply('-- Admin/Moderacion (requiere permisos) --', (1.0, 0.5, 0.2))
    _reply('/kick /ban /mute /unmute /end /remove', (0.8, 0.8, 0.8))
    _reply('/nv /dv /sm /pause /tint /camera', (0.8, 0.8, 0.8))
    _reply('/role /tag /ef /lm /gp /info /pb', (0.8, 0.8, 0.8))
    _reply('/party /maxplayers /playlist /kickvote /quit', (0.8, 0.8, 0.8))
    _reply('-- Trolleo (requiere permisos) --', (1.0, 0.3, 0.3))
    _reply('/kill /heal /curse /shield /gloves /freeze /unfreeze', (0.8, 0.8, 0.8))
    _reply('/sleep /fly /inv /head /creep /celebrate', (0.8, 0.8, 0.8))
    _reply('/gm /sp /speed /nuke /bunny', (0.8, 0.8, 0.8))

def cmd_ns(sp: object, args: list) -> None:
    _reply('=== Sistema de NS (Nivel de Skill) ===', (0.4, 0.8, 1.0))
    _reply('El NS mide tu habilidad en el servidor.', (0.8, 0.8, 0.8))
    _reply('Ganas NS al matar y pierdes NS al morir.', (0.8, 0.8, 0.8))
    _reply('Matar a alguien con mas NS que tu da mas puntos.', (0.8, 0.8, 0.8))
    _reply('Matar a alguien con mucho menos NS da pocos puntos.', (0.8, 0.8, 0.8))
    _reply('Divisiones por NS:', (1.0, 0.85, 0.2))
    _reply('Madera: 0  |  Piedra: 500  |  Hierro: 1000', (0.8, 0.8, 0.8))
    _reply('Bronce: 1500  |  Plata: 2000  |  Oro: 2500', (0.8, 0.8, 0.8))
    _reply('Diamante: 3000  |  Leyenda: 3500+', (0.8, 0.8, 0.8))
    _reply('El NS se reinicia parcialmente cada 21 dias.', (0.7, 0.7, 0.7))
    _reply('En Leyenda el NS no baja tanto al reinicio.', (0.7, 0.7, 0.7))

def cmd_ping(sp: object, args: list) -> None:
    try:
        import _bascenev1
        session = bs.get_foreground_host_session()
        if not session:
            _reply('No hay sesion activa.', (1.0, 0.4, 0.4))
            return
        if args and args[0].lower() == 'all':
            _reply('--- Ping de jugadores ---', (0.6, 0.9, 1.0))
            for player in session.sessionplayers:
                try:
                    cid  = player.inputdevice.client_id
                    name = player.getname(full=True, icon=False)
                    ping = _bascenev1.get_client_ping(cid)
                    _reply(f'{name}: {ping}ms', (0.8, 0.8, 0.8))
                except Exception:
                    pass
        else:
            cid  = sp.inputdevice.client_id
            ping = _bascenev1.get_client_ping(cid)
            _reply(f'Tu ping: {ping}ms', (0.6, 0.9, 1.0))
    except Exception as e:
        print(f'[cmds.all] ping error: {e}')

def cmd_pb(sp: object, args: list) -> None:
    try:
        if not args:
            acc = sp.get_v1_account_id()
            _reply(f'Tu account ID: {acc}', (0.6, 0.9, 1.0))
        else:
            cid = int(args[0])
            session = bs.get_foreground_host_session()
            if not session:
                _reply('No hay sesion activa.')
                return
            for p in session.sessionplayers:
                try:
                    if p.inputdevice.client_id == cid:
                        acc  = p.get_v1_account_id()
                        name = p.getname(full=True, icon=False)
                        _reply(f'{name}: {acc}', (0.6, 0.9, 1.0))
                        return
                except Exception:
                    pass
            _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.all] pb error: {e}')

def cmd_discord(sp: object, args: list) -> None:
    import uuid, time
    try:
        acc = sp.get_v1_account_id()

        if os.path.exists(_VERIFIED_PATH):
            with open(_VERIFIED_PATH, 'r', encoding='utf-8') as f:
                verified = json.load(f)
            if acc in verified:
                bs.chatmessage(
                    '\u2705 Ya estas verificado en Discord.',
                    clients=[sp.inputdevice.client_id])
                return

        token = uuid.uuid4().hex[:12].upper()
        expires = time.time() + 7200  # 2 horas

        pending = {}
        if os.path.exists(_VERIFY_PATH):
            try:
                with open(_VERIFY_PATH, 'r', encoding='utf-8') as f:
                    pending = json.load(f)
            except Exception:
                pass

        pending = {k: v for k, v in pending.items() if v.get('acc') != acc and v.get('expires', 0) > time.time()}
        pending[token] = {
            'acc': acc,
            'expires': expires
        }

        act = bs.get_foreground_host_activity()
        character = 'neoSpaz'
        color     = [1.0, 1.0, 1.0]
        highlight = [1.0, 1.0, 1.0]
        name      = sp.getname()
        try:
            roster_path = os.path.join(_BASE_DIR, 'roster.json')
            if os.path.exists(roster_path):
                with open(roster_path, 'r', encoding='utf-8') as f:
                    roster = json.load(f)
                for p in roster.get('players', []):
                    if p.get('aid') == acc:
                        character = p.get('character', character)
                        color     = p.get('color', color)
                        highlight = p.get('highlight', highlight)
                        name      = p.get('name', name)
                        break
        except Exception:
            pass

        account_name = ''
        try:
            stats_path = os.path.join(_BASE_DIR, 'stats.json')
            if os.path.exists(stats_path):
                with open(stats_path, 'r', encoding='utf-8') as f:
                    sdata = json.load(f)
                account_name = sdata.get('stats', {}).get(acc, {}).get('account_name', '')
        except Exception:
            pass
        if not account_name:
            try:
                import _bascenev1
                roster = _bascenev1.get_game_roster()
                for entry in roster:
                    if entry.get('account_id') == acc:
                        display = entry.get('display_string', '')
                        print(f'[debug] display_string: {repr(display)}')
                        account_name = display.split('•')[0].strip() if '•' in display else display.strip()
                        break
            except Exception:
                pass

        pending[token] = {
            'acc':          acc,
            'expires':      expires,
            'name':         name,
            'account_name': account_name,
            'character':    character,
            'color':        color,
            'highlight':    highlight,
        }

        with open(_VERIFY_PATH, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)

        notify_path = os.path.join(_BASE_DIR, 'verify_notify.json')
        with open(notify_path, 'w', encoding='utf-8') as f:
            json.dump({'token': token, 'acc': acc}, f)

        client_id = sp.inputdevice.client_id
        display_name = account_name if account_name else name

        bs.chatmessage('💬 Verificacion generada.', clients=[client_id])
        bs.chatmessage('Ve a #verificacion en Discord.', clients=[client_id])
        bs.chatmessage('Haz clic en el boton del bot.', clients=[client_id])
        bs.chatmessage('discord.gg/9HbHhKrW3V', clients=[client_id])

        bs.chatmessage(f'⚠️ Verificacion de {display_name} generada.')
        bs.chatmessage('Este proceso es solo para ellx.')
        bs.chatmessage('Para verificarte ejecuta /discord vos mismo.')
    except Exception as e:
        print(f'[cmds.all] discord error: {e}')

def cmd_v(sp: object, args: list) -> None:
    import json, os, time
    try:
        client_id = sp.inputdevice.client_id
        if not args:
            bs.chatmessage('❌ Uso: /v TOKEN', clients=[client_id])
            return
        token = args[0].strip().upper()
        if not os.path.exists(_VERIFY_PATH):
            bs.chatmessage('❌ Token inválido.', clients=[client_id])
            return
        with open(_VERIFY_PATH, 'r', encoding='utf-8') as f:
            pending = json.load(f)
        entry = pending.get(token)
        if not entry:
            bs.chatmessage('❌ Token no encontrado.', clients=[client_id])
            return
        if entry.get('expires', 0) < time.time():
            bs.chatmessage('❌ Token expirado. Generá uno nuevo en Discord.', clients=[client_id])
            return
        acc = sp.get_v1_account_id()
        if os.path.exists(_VERIFIED_PATH):
            with open(_VERIFIED_PATH, 'r', encoding='utf-8') as f:
                verified = json.load(f)
            if acc in verified:
                bs.chatmessage('✅ Ya estás verificado.', clients=[client_id])
                return
        account_name = ''
        character = 'neoSpaz'
        color     = [1.0, 1.0, 1.0]
        highlight = [1.0, 1.0, 1.0]
        name      = sp.getname()
        try:
            import _bascenev1
            roster = _bascenev1.get_game_roster()
            for e in roster:
                if e.get('account_id') == acc:
                    display = e.get('display_string', '')
                    account_name = display.split('•')[0].strip() if '•' in display else display.strip()
                    print(f'[debug] display_string raw: {repr(display)}')
                    account_name = ''.join(c for c in account_name if ord(c) < 0xe000 or ord(c) > 0xf8ff)
                    break
        except Exception:
            pass
        try:
            stats_path = os.path.join(_BASE_DIR, 'stats.json')
            if os.path.exists(stats_path):
                with open(stats_path, 'r', encoding='utf-8') as f:
                    sdata = json.load(f)
                p = sdata.get('stats', {}).get(acc, {})
                character = p.get('character', character)
                color     = p.get('color', color)
                highlight = p.get('highlight', highlight)
                name      = p.get('name', name)
                if not account_name:
                    account_name = p.get('account_name', '')
        except Exception:
            pass
        entry['name']         = name
        entry['account_name'] = account_name
        entry['character']    = character
        entry['color']        = color
        entry['highlight']    = highlight
        pending[token] = entry
        with open(_VERIFY_PATH, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)
        notify_path = os.path.join(_BASE_DIR, 'verify_notify.json')
        with open(notify_path, 'w', encoding='utf-8') as f:
            json.dump({'token': token, 'acc': acc}, f)
        bs.chatmessage('✅ Token válido. Confirmá en Discord.', clients=[client_id])
    except Exception as e:
        print(f'[cmds.all] cmd_v error: {e}')

CMDS: dict = {
    'stats':   (None, cmd_stats),
    'rank':    (None, cmd_rank),
    'top':     (None, cmd_top),
    'list':    (None, cmd_list),
    'report':  (None, cmd_report),
    'help':    (None, cmd_help),
    'ns':      (None, cmd_ns),
    'ping':    (None, cmd_ping),
    'pb':      (None, cmd_pb),
    'discord': (None, cmd_discord),
    'v':       (None, cmd_v),
}

_VERIFY_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'nexus_data', 'pending_verify.json'))
_VERIFIED_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'nexus_data', 'verified.json'))
