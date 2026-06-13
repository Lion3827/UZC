# ba_meta require api 9

from __future__ import annotations

try:
    import custom_hooks as _hooks
    _CFG = _hooks.get_plugin_cfg('stats')
except Exception:
    _CFG = {}

def _cfg(key, default):
    entry = _CFG.get(key, {})
    return entry.get('value', default) if isinstance(entry, dict) else default

import datetime
import json
import os
import queue
import shutil
import threading
import weakref
from typing import Optional

import babase as ba
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz

_BASE_DIR   = os.path.join(os.path.dirname(__file__), '..', '..', 'nexus_data')
_STATS_FILE = os.path.join(_BASE_DIR, 'stats.json')
_CLANS_FILE = os.path.join(_BASE_DIR, 'clans.json')

DIVISIONES: list[tuple[str, int]] = [
    ('Madera',    0),
    ('Piedra',    500),
    ('Hierro',    1000),
    ('Bronce',    1500),
    ('Plata',     2000),
    ('Oro',       2500),
    ('Diamante',  3000),
    ('Leyenda',   3500),
]

def get_division(ns: int) -> str:
    div = DIVISIONES[0][0]
    for name, minimo in DIVISIONES:
        if ns >= minimo:
            div = name
    return div

def _get_division_index(ns: int) -> int:
    idx = 0
    for i, (name, minimo) in enumerate(DIVISIONES):
        if ns >= minimo:
            idx = i
    return idx


_NS_TABLE: list[tuple[int, int]] = [
    (20, 10),
    (15, 10),
    (10, 10),
    (10, 10),
    (8,  16),
    (8,  20),
    (8,  20),
    (8,  25),
]

def calc_ns_change(ns_killer: int, ns_victim: int) -> tuple[int, int]:
    killer_div = _get_division_index(ns_killer)
    victim_div = _get_division_index(ns_victim)
    diff = killer_div - victim_div

    base_gain, base_loss = _NS_TABLE[victim_div]

    if diff >= 3:
        adjusted_loss = max(1, round(base_loss * (1 - diff * 0.05)))
        return 1, adjusted_loss

    factor = 1.0 - diff * 0.05
    gain = max(1, round(base_gain * factor))
    loss = max(1, round(base_loss * factor))
    return gain, loss

_LEYENDA_NS = 3500

def _get_division_floor(ns: int) -> int:
    floor = 0
    for name, minimo in DIVISIONES:
        if name in ('Diamante', 'Leyenda'):
            continue
        if ns >= minimo:
            floor = minimo
    return floor

def _default_player(aid: str, name: str) -> dict:
    return {
        'aid':          aid,
        'name':         name,
        'kills':        0,
        'deaths':       0,
        'scores':       0,
        'games':        0,
        'wins':         0,
        'losses':       0,
        'streak':       0,
        'best_streak':  0,
        'ns':           500,
        'ns_floor':     500,
        'division':     'Piedra',
        'clan':         None,
        'last_seen':    str(datetime.datetime.now()),
        'first_seen':   str(datetime.datetime.now()),
        'device_ids':   [],
    }

def calc_kd(entry: dict) -> float:
    return round(entry['kills'] / max(entry['deaths'], 1), 2)

def calc_win_ratio(entry: dict) -> float:
    if entry['games'] == 0:
        return 0.0
    return round((entry['wins'] / entry['games']) * 100, 1)

_stats_cache: dict = {}
_clans_cache: dict = {}
_stats_lock  = threading.RLock()
_clans_lock  = threading.RLock()

_stats_queue: queue.Queue = queue.Queue(maxsize=100)
_clans_queue: queue.Queue = queue.Queue(maxsize=50)
_SEASON_FILE      = os.path.join(_BASE_DIR, 'season.json')
_NS_RESET_DAYS    = _cfg("ns_reset_days", 21)
_LADDER_RESET_DAYS = _cfg("ladder_reset_days", 15)
_scheduler_thread: threading.Thread | None = None
_stop_event = threading.Event()
_write_thread: threading.Thread | None = None

def _write_worker() -> None:
    while not _stop_event.is_set():
        try:
            data = _stats_queue.get(timeout=3.0)
            if data is None:
                break
            while True:
                try:
                    data = _stats_queue.get_nowait()
                    if data is None:
                        break
                except queue.Empty:
                    break
            if data is not None:
                _atomic_write(_STATS_FILE, {'stats': data})
        except queue.Empty:
            pass
        except Exception as e:
            print(f'[stats] error escribiendo stats: {e}')
        try:
            clans = _clans_queue.get_nowait()
            while True:
                try:
                    clans = _clans_queue.get_nowait()
                except queue.Empty:
                    break
            _atomic_write(_CLANS_FILE, clans)
        except queue.Empty:
            pass
        except Exception as e:
            print(f'[stats] error escribiendo clanes: {e}')
    print('[stats] write thread detenido')

def _atomic_write(path: str, data: dict) -> None:
    tmp = path + '.tmp'
    bak = path + '.backup'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if os.path.exists(path):
            shutil.copyfile(path, bak)
        os.replace(tmp, path)
    except Exception as e:
        print(f'[stats] error atomic_write {path}: {e}')

def _enqueue_stats(s: dict) -> None:
    try:
        _stats_queue.put_nowait(s)
    except queue.Full:
        print('[stats] cola llena, escritura descartada')

def _enqueue_clans(c: dict) -> None:
    try:
        _clans_queue.put_nowait(c)
    except queue.Full:
        print('[stats] cola clanes llena, escritura descartada')

def _load_stats() -> dict:
    if os.path.exists(_STATS_FILE):
        try:
            with open(_STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('stats', {})
        except Exception:
            bak = _STATS_FILE + '.backup'
            if os.path.exists(bak):
                try:
                    with open(bak, 'r', encoding='utf-8') as f:
                        return json.load(f).get('stats', {})
                except Exception:
                    pass
    return {}

def _load_clans() -> dict:
    if os.path.exists(_CLANS_FILE):
        try:
            with open(_CLANS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_stats() -> dict:
    with _stats_lock:
        return dict(_stats_cache)

def get_player(aid: str) -> Optional[dict]:
    with _stats_lock:
        return _stats_cache.get(aid)

def get_or_create_player(aid: str, name: str, device_id: str = None) -> dict:
    with _stats_lock:
        if aid not in _stats_cache:
            _stats_cache[aid] = _default_player(aid, name)
        else:
            _stats_cache[aid]['name'] = name
            for k, v in _default_player(aid, name).items():
                if k == 'first_seen':
                    _stats_cache[aid].setdefault(k, v)
                elif k != 'last_seen':
                    _stats_cache[aid].setdefault(k, v)
        if device_id:
            ids = _stats_cache[aid].setdefault('device_ids', [])
            if device_id not in ids:
                ids.append(device_id)
        return _stats_cache[aid]

def get_ranking() -> list[dict]:
    with _stats_lock:
        sorted_players = sorted(
            _stats_cache.values(),
            key=lambda p: (p['ns'], p['wins']),
            reverse=True,
        )
    result = []
    for i, p in enumerate(sorted_players):
        result.append({
            'rank':       i + 1,
            'aid':        p['aid'],
            'name':       p['name'],
            'ns':         p['ns'],
            'division':   p['division'],
            'kills':      p['kills'],
            'kd':         calc_kd(p),
            'win_ratio':  calc_win_ratio(p),
            'clan':       p.get('clan'),
        })
    return result

def get_rank(aid: str) -> int:
    ranking = get_ranking()
    for entry in ranking:
        if entry['aid'] == aid:
            return entry['rank']
    return 0

def get_clan(tag: str) -> Optional[dict]:
    with _clans_lock:
        return _clans_cache.get(tag)

def get_clan_of_player(aid: str) -> Optional[str]:
    with _clans_lock:
        for tag, clan in _clans_cache.items():
            if aid in clan['miembros']:
                return tag
    return None

def create_clan(tag: str, nombre: str, lider_aid: str) -> tuple[bool, str]:
    tag = tag.upper()[:4]
    with _clans_lock:
        if tag in _clans_cache:
            return False, f'El clan [{tag}] ya existe.'
        if get_clan_of_player(lider_aid):
            return False, 'Ya estás en un clan.'
        _clans_cache[tag] = {
            'tag':          tag,
            'nombre':       nombre,
            'lider':        lider_aid,
            'miembros':     [lider_aid],
            'ns_clan':      0,
            'max_miembros': 12,
            'creado':       datetime.datetime.now().strftime('%Y-%m-%d'),
        }
        _enqueue_clans(dict(_clans_cache))
    with _stats_lock:
        if lider_aid in _stats_cache:
            _stats_cache[lider_aid]['clan'] = tag
            _enqueue_stats(dict(_stats_cache))
    return True, f'Clan [{tag}] creado.'

def join_clan(tag: str, aid: str) -> tuple[bool, str]:
    tag = tag.upper()
    with _clans_lock:
        if tag not in _clans_cache:
            return False, f'Clan [{tag}] no existe.'
        clan = _clans_cache[tag]
        if aid in clan['miembros']:
            return False, 'Ya estás en este clan.'
        existing = get_clan_of_player(aid)
        if existing:
            return False, f'Ya estás en el clan [{existing}].'
        if len(clan['miembros']) >= clan['max_miembros']:
            return False, f'El clan [{tag}] está lleno ({clan["max_miembros"]} miembros).'
        clan['miembros'].append(aid)
        _recalc_clan_ns(tag)
        _enqueue_clans(dict(_clans_cache))
    with _stats_lock:
        if aid in _stats_cache:
            _stats_cache[aid]['clan'] = tag
            _enqueue_stats(dict(_stats_cache))
    return True, f'Te uniste al clan [{tag}].'

def leave_clan(aid: str) -> tuple[bool, str]:
    tag = get_clan_of_player(aid)
    if not tag:
        return False, 'No estás en ningún clan.'
    with _clans_lock:
        clan = _clans_cache.get(tag)
        if not clan:
            return False, 'Clan no encontrado.'
        clan['miembros'].remove(aid)
        if clan['lider'] == aid and clan['miembros']:
            clan['lider'] = clan['miembros'][0]
        if not clan['miembros']:
            del _clans_cache[tag]
        else:
            _recalc_clan_ns(tag)
        _enqueue_clans(dict(_clans_cache))
    with _stats_lock:
        if aid in _stats_cache:
            _stats_cache[aid]['clan'] = None
            _enqueue_stats(dict(_stats_cache))
    return True, f'Saliste del clan [{tag}].'

def _recalc_clan_ns(tag: str) -> None:
    clan = _clans_cache.get(tag)
    if not clan:
        return
    total = 0
    with _stats_lock:
        for aid in clan['miembros']:
            total += _stats_cache.get(aid, {}).get('ns', 500)
    clan['ns_clan'] = total

def get_clan_ranking() -> list[dict]:
    with _clans_lock:
        sorted_clans = sorted(
            _clans_cache.values(),
            key=lambda c: c['ns_clan'],
            reverse=True,
        )
    return [
        {
            'rank':     i + 1,
            'tag':      c['tag'],
            'nombre':   c['nombre'],
            'ns_clan':  c['ns_clan'],
            'miembros': len(c['miembros']),
        }
        for i, c in enumerate(sorted_clans)
    ]

def on_kill(killer_aid: str, victim_aid: str,
            killer_name: str, victim_name: str) -> None:
    with _stats_lock:
        killer = get_or_create_player(killer_aid, killer_name)
        victim = get_or_create_player(victim_aid, victim_name)

        ganancia, perdida = calc_ns_change(killer['ns'], victim['ns'])

        killer['ns'] = max(0, killer['ns'] + ganancia)
        new_victim_ns = max(0, victim['ns'] - perdida)

        if victim['division'] not in ('Diamante', 'Leyenda'):
            floor = victim.get('ns_floor', 0)
            new_victim_ns = max(new_victim_ns, floor)
        victim['ns'] = new_victim_ns

        killer['division'] = get_division(killer['ns'])
        victim['division'] = get_division(victim['ns'])

        if killer['division'] != 'Leyenda':
            new_floor = _get_division_floor(killer['ns'])
            if new_floor > killer.get('ns_floor', 0):
                killer['ns_floor'] = new_floor

        killer['kills'] += 1
        victim['deaths'] += 1

        killer['streak'] += 1
        if killer['streak'] > killer['best_streak']:
            killer['best_streak'] = killer['streak']
        victim['streak'] = 0

        now = str(datetime.datetime.now())
        killer['last_seen'] = now
        victim['last_seen'] = now

        stats_snap = dict(_stats_cache)

    killer_clan = get_clan_of_player(killer_aid)
    victim_clan = get_clan_of_player(victim_aid)
    with _clans_lock:
        if killer_clan:
            _recalc_clan_ns(killer_clan)
        if victim_clan and victim_clan != killer_clan:
            _recalc_clan_ns(victim_clan)
        clans_snap = dict(_clans_cache)

    _enqueue_stats(stats_snap)
    _enqueue_clans(clans_snap)

    print(
        f'[stats] {killer_name} mató a {victim_name} | '
        f'NS: {killer["ns"]} ({killer["division"]}) | '
        f'racha: {killer["streak"]}'
    )

def on_game_end(winners: list[str], losers: list[str],
                scores: dict[str, int]) -> None:
    with _stats_lock:
        for aid in winners + losers:
            if aid not in _stats_cache:
                continue
            p = _stats_cache[aid]
            p['games'] += 1
            p['scores'] += scores.get(aid, 0)
            if aid in winners:
                p['wins'] += 1
            else:
                p['losses'] += 1
            p['last_seen'] = str(datetime.datetime.now())
        stats_snap = dict(_stats_cache)
    _enqueue_stats(stats_snap)


_orig_init: object = None
_orig_team_end: object = None
_write_thread: threading.Thread | None = None


def _make_die_hook(spaz_ref: weakref.ref, orig_hm: object) -> object:
    def _hm(msg: object, orig=orig_hm, ref=spaz_ref) -> None:
        if isinstance(msg, bs.DieMessage):
            spaz = ref()
            if spaz is not None and hasattr(spaz, '_player'):
                try:
                    victim_player = spaz._player
                    victim_aid    = victim_player.sessionplayer.get_account_id()
                    victim_name   = victim_player.getname(full=True)
                    killer_aid    = None
                    killer_name   = None
                    ka = getattr(spaz, 'last_player_attacked_by', None)
                    if ka and ka.exists():
                        try:
                            killer_aid  = ka.sessionplayer.get_account_id()
                            killer_name = ka.getname(full=True)
                        except Exception:
                            pass
                    if victim_aid:
                        if killer_aid and killer_aid != victim_aid:
                            on_kill(killer_aid, victim_aid, killer_name, victim_name)
                        else:
                            with _stats_lock:
                                p = get_or_create_player(victim_aid, victim_name)
                                p['deaths'] += 1
                                p['streak'] = 0
                                snap = dict(_stats_cache)
                            _enqueue_stats(snap)
                except Exception as e:
                    print(f'[stats] die hook error: {e}')
        orig(msg)
    return _hm


def _spaz_init_hook(self: PlayerSpaz, *args, **kwargs) -> None:
    _orig_init(self, *args, **kwargs)
    try:
        player = self._player
        aid    = player.sessionplayer.get_account_id()
        name   = player.getname(full=True)
        device_id = None
        try:
            import _bascenev1
            cid = player.sessionplayer.inputdevice.client_id
            device_id = _bascenev1.get_client_public_device_uuid(cid)
            if not device_id:
                device_id = _bascenev1.get_client_device_uuid(cid)
        except Exception:
            pass
        if aid:
            get_or_create_player(aid, name, device_id)
            try:
                import _bascenev1 as _bsv1
                roster = _bsv1.get_game_roster()
                for entry in roster:
                    if entry.get('account_id') == aid:
                        display = entry.get('display_string', '')
                        account_name = display.split('•')[0].strip() if '•' in display else ''
                        if account_name:
                            with _stats_lock:
                                p = _stats_cache.get(aid)
                                if p is not None:
                                    p['account_name'] = account_name
                        break
            except Exception:
                pass
            try:
                _tex_map = {
                    'neospaz':'neoSpaz','kronk':'kronk','zoe':'zoe',
                    'jack':'jackMcFlail','ninja':'ninja','pixel':'pixel',
                    'frosty':'frosty','santa':'santa','cyborg':'cyborg',
                    'agent':'agent','wizard':'wizard','pirate':'pirate',
                    'robot':'robot','toon':'toon','mel':'mel',
                    'bear':'bear','penguin':'penguin','ali':'ali',
                    'bunny':'bunny','octopus':'octopus','cat':'cat',
                    'enforcer':'enforcer','exploder':'exploder',
                    'magicman':'magicMan','assassin':'assassin',
                    'bones':'bones','helmet':'helmet','demoman':'demoMan',
                    'holiday':'holiday',
                }
                def _t2c(tex):
                    tl = tex.lower()
                    for k,v in _tex_map.items():
                        if k in tl:
                            return v
                    return 'neoSpaz'
                info = player.sessionplayer.get_icon_info()
                char = _t2c(info.get('texture', ''))
                col  = list(info.get('tint_color',  [1.0, 1.0, 1.0]))[:3]
                hi   = list(info.get('tint2_color', [1.0, 1.0, 1.0]))[:3]
                with _stats_lock:
                    p = _stats_cache.get(aid)
                    if p is not None:
                        p['character'] = char
                        p['color']     = col
                        p['highlight'] = hi
            except Exception:
                pass
        orig_hm = self.handlemessage
        self.handlemessage = _make_die_hook(weakref.ref(self), orig_hm)
    except Exception:
        pass


def _team_end_hook(self, results, **kwargs) -> None:
    _orig_team_end(self, results, **kwargs)
    try:
        from bascenev1._gameresults import GameResults
        if isinstance(results, GameResults) and results._game_set:
            total_players = sum(len(st.players) for st in results.sessionteams)
            if total_players < 2:
                return
            winning_st = results.winning_sessionteam
            winners = []
            losers = []
            scores = {}
            for st in results.sessionteams:
                score = results.get_sessionteam_score(st) or 0
                for sp in st.players:
                    try:
                        aid = sp.get_account_id()
                        if not aid:
                            continue
                        scores[aid] = score
                        if winning_st is not None and st is winning_st:
                            winners.append(aid)
                        else:
                            losers.append(aid)
                    except Exception:
                        pass
            if winners or losers:
                on_game_end(winners, losers, scores)
    except Exception as e:
        print(f'[stats] game_end hook error: {e}')


def _load_season() -> dict:
    if os.path.exists(_SEASON_FILE):
        try:
            with open(_SEASON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return {'last_ns_reset': now, 'last_ladder_reset': now}


def _save_season(data: dict) -> None:
    tmp = _SEASON_FILE + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, _SEASON_FILE)
    except Exception as e:
        print(f'[stats] season save error: {e}')



def _award_umbr_alt_tags() -> None:
    try:
        from plugins.perms import perms as _perms
    except Exception as e:
        print(f'[stats] umbr_alt: no se pudo importar perms: {e}')
        return
    try:
        sorted_players = sorted(
            _stats_cache.values(),
            key=lambda p: (p.get('ns', 0), p.get('kills', 0)),
            reverse=True,
        )
        if sorted_players:
            p1 = sorted_players[0]
            _perms._data.setdefault('season_rewards', {})['umbr_top1_pending'] = p1.get('aid')
            _perms._save()
            print(f'[stats] UMBR TOP 1: {p1.get("name","?")} — pendiente tag personalizado')
        for i, p in enumerate(sorted_players[1:10], start=2):
            aid = p.get('aid', '')
            if not aid or aid == '-1':
                continue
            _perms.set_account_role(aid, 'umbr_alt')
            print(f'[stats] Umbr-ALT -> #{i} {p.get("name", aid)}')
    except Exception as e:
        print(f'[stats] umbr_alt error: {e}')


def _award_season_tags() -> None:
    try:
        from plugins.perms import perms as _perms
    except Exception as e:
        print(f'[stats] award_tags: no se pudo importar perms: {e}')
        return
    try:
        tag_cfg = _perms.get_role_cfg('altpha_season')
        if not tag_cfg:
            print('[stats] award_tags: no se encontro altpha_season en tag_defs')
            return
        sorted_players = sorted(
            _stats_cache.values(),
            key=lambda p: (p.get('kills', 0), p.get('wins', 0)),
            reverse=True,
        )
        if sorted_players:
            p1 = sorted_players[0]
            _perms._data.setdefault('season_rewards', {})['top1_pending'] = p1.get('aid')
            _perms._save()
            print(f'[stats] TOP 1: {p1.get("name","?")} ({p1.get("kills",0)} kills) — pendiente tag personalizado')
        for i, p in enumerate(sorted_players[1:10], start=2):
            aid = p.get('aid', '')
            if not aid or aid == '-1':
                continue
            _perms.set_account_role(aid, 'altpha_season')
            print(f'[stats] ALTpha -> #{i} {p.get("name", aid)} ({p.get("kills", 0)} kills)')
    except Exception as e:
        print(f'[stats] award_tags error: {e}')


def ladder_reset() -> int:
    try:
        import json as _json
        top10 = sorted(_stats_cache.values(), key=lambda p: (p.get('kills',0), p.get('wins',0)), reverse=True)[:10]
        snap_path = os.path.join(_BASE_DIR, 'season_snapshot.json')
        with open(snap_path, 'w', encoding='utf-8') as _sf:
            _json.dump(top10, _sf, indent=2)
        print(f'[stats] snapshot guardado — {len(top10)} jugadores')
    except Exception as _se:
        print(f'[stats] snapshot error: {_se}')
    with _stats_lock:
        _award_season_tags()
        count = 0
        for p in _stats_cache.values():
            p['kills']  = 0
            p['deaths'] = 0
            p['scores'] = 0
            p['games']  = 0
            p['wins']   = 0
            p['losses'] = 0
            p['streak'] = 0
            count += 1
        snap = dict(_stats_cache)
    _enqueue_stats(snap)
    print(f'[stats] ladder reseteado — {count} jugadores afectados')
    try:
        import json as _json
        with open(_SEASON_FILE) as _f:
            _s = _json.load(_f)
        _s['season_number'] = _s.get('season_number', 1) + 1
        with open(_SEASON_FILE, 'w') as _f:
            _json.dump(_s, _f, indent=2)
        print(f'[stats] temporada {_s["season_number"]} iniciada')
    except Exception as _e:
        print(f'[stats] season_number error: {_e}')
    return count


def _check_resets() -> None:
    try:
        season = _load_season()
        now    = datetime.datetime.now()
        changed = False

        last_ns = datetime.datetime.strptime(season['last_ns_reset'], '%Y-%m-%d')
        if (now - last_ns).days >= _NS_RESET_DAYS:
            season_reset()
            season['last_ns_reset'] = now.strftime('%Y-%m-%d')
            changed = True
            print('[stats] reset NS de temporada ejecutado automaticamente')

        last_ladder = datetime.datetime.strptime(season['last_ladder_reset'], '%Y-%m-%d')
        if (now - last_ladder).days >= _LADDER_RESET_DAYS:
            ladder_reset()
            season['last_ladder_reset'] = now.strftime('%Y-%m-%d')
            changed = True
            print('[stats] reset Ladder ejecutado automaticamente')

        if changed:
            _save_season(season)
    except Exception as e:
        print(f'[stats] scheduler error: {e}')


def _scheduler_worker() -> None:
    _check_resets()
    while not _stop_event.is_set():
        _stop_event.wait(timeout=300)
        if not _stop_event.is_set():
            _check_resets()


def season_reset() -> int:
    with _stats_lock:
        count = 0
        for aid, p in _stats_cache.items():
            ns = p.get('ns', 500)
            if ns >= _LEYENDA_NS:
                new_ns = 2500
            else:
                new_ns = max(0, ns - 1000)
            p['ns']       = new_ns
            p['ns_floor'] = _get_division_floor(new_ns)
            p['division'] = get_division(new_ns)
            p['kills']    = 0
            p['deaths']   = 0
            p['scores']   = 0
            p['games']    = 0
            p['wins']     = 0
            p['losses']   = 0
            p['streak']   = 0
            count += 1
        snap = dict(_stats_cache)
    _enqueue_stats(snap)
    _award_umbr_alt_tags()
    print(f'[stats] temporada reseteada — {count} jugadores afectados')
    return count


def enable() -> None:
    global _orig_init, _orig_team_end, _write_thread, _scheduler_thread

    os.makedirs(_BASE_DIR, exist_ok=True)

    if not os.path.exists(_STATS_FILE):
        _atomic_write(_STATS_FILE, {'stats': {}})
    if not os.path.exists(_CLANS_FILE):
        _atomic_write(_CLANS_FILE, {})
    if not os.path.exists(_SEASON_FILE):
        _save_season(_load_season())

    with _stats_lock:
        _stats_cache.update(_load_stats())
    with _clans_lock:
        _clans_cache.update(_load_clans())

    _stop_event.clear()
    _write_thread = threading.Thread(target=_write_worker, daemon=True)
    _write_thread.start()

    _check_resets()

    _scheduler_thread = threading.Thread(target=_scheduler_worker, daemon=True)
    _scheduler_thread.start()

    if PlayerSpaz.__init__ is not _spaz_init_hook:
        _orig_init = PlayerSpaz.__init__
        PlayerSpaz.__init__ = _spaz_init_hook

    from bascenev1._gameactivity import GameActivity
    if GameActivity.end is not _team_end_hook:
        _orig_team_end = GameActivity.end
        GameActivity.end = _team_end_hook

    try:
        import babase
        babase.app.add_shutdown_task(_async_disable())
    except Exception:
        pass

    print(f'[stats] cargado — {len(_stats_cache)} jugadores, {len(_clans_cache)} clanes')


async def _async_disable() -> None:
    disable()


def disable() -> None:
    global _orig_init, _orig_team_end, _write_thread, _scheduler_thread

    _stop_event.set()
    try:
        _stats_queue.put_nowait(None)
    except queue.Full:
        pass
    if _write_thread is not None:
        _write_thread.join(timeout=5.0)
        _write_thread = None
    if _scheduler_thread is not None:
        _scheduler_thread.join(timeout=5.0)
        _scheduler_thread = None

    if _orig_init is not None:
        PlayerSpaz.__init__ = _orig_init
        _orig_init = None
    if _orig_team_end is not None:
        from bascenev1._gameactivity import GameActivity
        GameActivity.end = _orig_team_end
        _orig_team_end = None

    print('[stats] desactivado')
