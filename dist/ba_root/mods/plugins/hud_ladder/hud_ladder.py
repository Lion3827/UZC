from __future__ import annotations

try:
    import custom_hooks as _hooks
    _CFG = _hooks.get_plugin_cfg('hud_ladder')
except Exception:
    _CFG = {}

def _cfg(key, default):
    entry = _CFG.get(key, {})
    return entry.get('value', default) if isinstance(entry, dict) else default

import datetime
import importlib
import traceback
import weakref
from typing import Optional

import bascenev1 as bs

TIPS = _cfg('tips', [
    '\ue049 Usa /help para ver todos los comandos disponibles',
    '\ue043 Escribe /stats para ver tus estadisticas de juego',
    '\ue048 Sube de division acumulando NS en cada partida',
    '\ue047 El KD y win ratio determinan tu posicion en el ladder',
    '\ue026 Usa /report para reportar jugadores que hagan trampa',
    '\ue043 Escribe /top para ver el top 5 del servidor',
    '\ue048 El ladder se reinicia cada 15 dias. El NS cada 21',
    '\ue026 Unete a nuestro Discord desde el menu Estadisticas',
    '\ue049 Mata mas y muere menos para subir en el ladder',
    '\ue043 Tu division depende de tu NS acumulado',
    '\ue047 Ganar partidas mejora tu win ratio y tu ranking',
    '\ue048 En Leyenda el NS no baja tanto al reinicio de temporada',
    '\ue026 Anuncios y recompensas exclusivas en nuestro Discord',
    '\ue049 Usa /ping para ver tu latencia actual',
    '\ue043 Escribe /rank para saber tu posicion exacta en el ranking',
    '\ue047 El streak mas alto te da bonificacion de NS',
    '\ue049 Escribe /ns para entender como funciona el sistema de puntos',
    '\ue043 Usa /report solo cuando sea necesario. El abuso tiene sancion',
    '\ue048 Cada fin de temporada los mejores jugadores reciben premios',
    '\ue047 Reportar sin razon puede resultar en sancion',
])

BASE_Y  = -100
ROW_H   = 17
NAME_X  = -170
STAT_X  = 5

RAINBOW = [
    (1.0, 0.0, 0.0),
    (1.0, 0.5, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 1.7, 0.0),
    (0.0, 1.7, 1.0),
    (0.0, 0.5, 1.7),
    (0.8, 0.0, 1.7),
    (1.7, 0.0, 1.7),
    (0.9, 0.9, 0.9),
    (0.6, 0.6, 0.6),
]

def _row_y(i: int) -> float:
    return BASE_Y - i * ROW_H

def _days_until_reset() -> int:
    try:
        stats = importlib.import_module('plugins.stats.stats')
        season = stats._load_season()
        last = datetime.datetime.strptime(season['last_ladder_reset'], '%Y-%m-%d')
        reset_days = getattr(stats, '_LADDER_RESET_DAYS', 15)
        elapsed = (datetime.datetime.now() - last).days
        remaining = max(0, reset_days - elapsed)
        return remaining
    except Exception:
        return -1

def _get_top10() -> list[dict]:
    try:
        stats = importlib.import_module('plugins.stats.stats')
        data = stats.get_stats()
        players = list(data.values())
        players.sort(key=lambda p: (
            -p.get('kills', 0),
            -round(p.get('kills', 0) / max(p.get('deaths', 1), 1), 2),
            -round((p.get('wins', 0) / max(p.get('games', 1), 1)) * 100, 1),
        ))
        result = []
        for i, p in enumerate(players[:10]):
            kd = round(p.get('kills', 0) / max(p.get('deaths', 1), 1), 2)
            wr = round((p.get('wins', 0) / max(p.get('games', 1), 1)) * 100, 1)
            result.append({
                'rank':      i + 1,
                'name':      p.get('name', '?'),
                'kills':     p.get('kills', 0),
                'kd':        kd,
                'win_ratio': wr,
            })
        return result
    except Exception:
        return []

class LadderHUD:

    def __init__(self, activity: bs.Activity) -> None:
        self._act = weakref.ref(activity)
        self._nodes_rows: list[tuple] = []
        self._tip_node: Optional[bs.Node] = None
        self._reset_node: Optional[bs.Node] = None
        self._tip_index: int = 0
        self._tip_chars: int = 0
        self._tip_target: str = ''
        self._update_timer: Optional[bs.Timer] = None
        self._tip_timer: Optional[bs.Timer] = None
        self._typewriter_timer: Optional[bs.Timer] = None
        self._rainbow_timer: Optional[bs.Timer] = None
        self._rainbow_index: int = 0
        self._build()

    def _build(self) -> None:
        act = self._act()
        if act is None:
            return
        print(f'[hud_ladder] _build() act={type(act).__name__}')
        with act.context:
            titulo = bs.newnode('text', attrs={
                'text': '\ue04e  TOP LADDER  \ue04e',
                'position': (-120, -70),
                'scale': 0.5,
                'h_align': 'center',
                'v_attach': 'top',
                'h_attach': 'right',
                'color': (0.0, 1.5, 0.0),
                'shadow': 0.3,
                'opacity': 0.0,
                'flatness': 0.0,
            })
            bs.animate(titulo, 'opacity', {0.0: 0.0, 1.35: 0.85})

            top = _get_top10()
            for i in range(10):
                y = _row_y(i)
                col = RAINBOW[i]
                delay = i * 0.08

                if i < len(top):
                    p = top[i]
                    name_txt = f'#{str(i+1).rjust(2)}  {p["name"][:9]}'
                    stat_txt = f'{p["kills"]:,}k  {p["kd"]}kd  {p["win_ratio"]}%'
                else:
                    name_txt = f'#{str(i+1).rjust(2)}  ---'
                    stat_txt = '0k  0kd  0%'

                n = bs.newnode('text', attrs={
                    'text': name_txt,
                    'position': (NAME_X, y),
                    'scale': 0.45,
                    'h_align': 'left',
                    'v_attach': 'top',
                    'h_attach': 'right',
                    'color': col,
                    'shadow': 0.3,
                    'opacity': 0.0,
                    'flatness': 0.0,
                })
                s = bs.newnode('text', attrs={
                    'text': stat_txt,
                    'position': (STAT_X, y),
                    'scale': 0.40,
                    'h_align': 'right',
                    'v_attach': 'top',
                    'h_attach': 'right',
                    'color': (1.3, 1.3, 0.0),
                    'shadow': 0.3,
                    'opacity': 0.0,
                    'flatness': 0.0,
                })
                bs.animate(n, 'opacity', {delay: 0.0, delay + 0.3: 0.9})
                bs.animate(s, 'opacity', {delay: 0.0, delay + 0.3: 0.75})
                self._nodes_rows.append((n, s))

            days = _days_until_reset()
            reset_txt = f'\ue043 Reset en: {days} dias' if days >= 0 else '\ue043 Reset en: -- dias'
            self._reset_node = bs.newnode('text', attrs={
                'text': reset_txt,
                'position': (-120, -280),
                'scale': 0.45,
                'h_align': 'center',
                'v_attach': 'top',
                'h_attach': 'right',
                'color': (1.0, 1.5, 0.0),
                'shadow': 0.3,
                'opacity': 0.0,
                'flatness': 0.0,
            })
            bs.animate(self._reset_node, 'opacity', {0.0: 0.0, 1.35: 0.65})

            bs.newnode('image', attrs={
                'texture': bs.gettexture('flagColor'),
                'position': (90, 35),
                'scale': (170, 58),
                'opacity': 0.6,
                'color': (0.05, 0.05, 0.05),
                'attach': 'bottomLeft',
            })
            bs.newnode('image', attrs={
                'texture': bs.gettexture('bunnyIcon'),
                'tint_texture': bs.gettexture('bunnyIconColorMask'),
                'tint_color': (0.1, 0.1, 1.0),
                'tint2_color': (1.0, 0.15, 0.15),
                'position': (35, 35),
                'scale': (60, 60),
                'opacity': 1.0,
                'attach': 'bottomLeft',
            })
            bs.newnode('text', attrs={
                'text': '\ue043 Lion3827',
                'position': (75, 30),
                'scale': 0.6,
                'h_align': 'left',
                'v_attach': 'bottom',
                'h_attach': 'left',
                'color': (0.1, 0.1, 1.0),
                'shadow': 1.0,
                'opacity': 1.0,
                'flatness': 1.0,
            })
            bs.newnode('text', attrs={
                'text': 'Owner',
                'position': (95, 12),
                'scale': 0.55,
                'h_align': 'left',
                'v_attach': 'bottom',
                'h_attach': 'left',
                'color': (1.0, 0.84, 0.0),
                'shadow': 1.0,
                'opacity': 1.0,
                'flatness': 1.0,
            })

            self._tip_node = bs.newnode('text', attrs={
                'text': '',
                'position': (0, 55),
                'scale': 0.90,
                'h_align': 'center',
                'v_attach': 'bottom',
                'color': (0.9, 0.9, 0.9),
                'shadow': 1.0,
                'opacity': 1.0,
                'flatness': 1.0,
            })

            self._update_timer = bs.Timer(float(_cfg("update_interval", 30)), bs.WeakCall(self._update_top), repeat=True)
            self._tip_timer = bs.Timer(float(_cfg("tip_interval", 8)), bs.WeakCall(self._next_tip), repeat=True)
            self._rainbow_timer = bs.Timer(0.18, bs.WeakCall(self._cycle_rainbow), repeat=True)

        print('[hud_ladder] _build() completo')
        self._start_tip(TIPS[0])

    def _cycle_rainbow(self) -> None:
        act = self._act()
        if act is None:
            return
        with act.context:
            self._rainbow_index = (self._rainbow_index + 1) % len(RAINBOW)
            for i, (n, s) in enumerate(self._nodes_rows):
                col = RAINBOW[(i + self._rainbow_index) % len(RAINBOW)]
                n.color = col

    def _update_top(self) -> None:
        act = self._act()
        if act is None:
            return
        with act.context:
            top = _get_top10()
            for i, (n, s) in enumerate(self._nodes_rows):
                y = _row_y(i)
                if i < len(top):
                    p = top[i]
                    n.text = f'#{str(i+1).rjust(2)}  {p["name"][:9]}'
                    s.text = f'{p["kills"]:,}k  {p["kd"]}kd  {p["win_ratio"]}%'
                else:
                    n.text = f'#{str(i+1).rjust(2)}  ---'
                    s.text = '0k  0kd  0%'
                n.position = (NAME_X, y)
                s.position = (STAT_X, y)

            if self._reset_node is not None:
                days = _days_until_reset()
                self._reset_node.text = f'\ue043 Reset en: {days} dias' if days >= 0 else '\ue043 Reset en: -- dias'

    def _next_tip(self) -> None:
        self._tip_index = (self._tip_index + 1) % len(TIPS)
        self._start_tip(TIPS[self._tip_index])

    def _start_tip(self, text: str) -> None:
        self._tip_target = text
        self._tip_chars = 0
        if self._typewriter_timer is not None:
            self._typewriter_timer = None
        act = self._act()
        if act is None:
            return
        if self._tip_node is not None:
            with act.context:
                self._tip_node.text = ''
        with act.context:
            self._typewriter_timer = bs.Timer(0.04, bs.WeakCall(self._typewriter_tick), repeat=True)

    def _typewriter_tick(self) -> None:
        if self._tip_node is None:
            self._typewriter_timer = None
            return
        self._tip_chars += 1
        act = self._act()
        if act is None:
            self._typewriter_timer = None
            return
        with act.context:
            self._tip_node.text = self._tip_target[:self._tip_chars]
        if self._tip_chars >= len(self._tip_target):
            self._typewriter_timer = None

_hud_instance: Optional[LadderHUD] = None

def _inject_hud(activity: bs.Activity) -> None:
    global _hud_instance
    print(f'[hud_ladder] _inject_hud: {type(activity).__name__}')
    try:
        if _hud_instance is not None:
            _hud_instance._update_timer = None
            _hud_instance._tip_timer = None
            _hud_instance._typewriter_timer = None
            _hud_instance._rainbow_timer = None
            _hud_instance._nodes_rows = []
            _hud_instance._tip_node = None
            _hud_instance._reset_node = None
            _hud_instance._act = lambda: None
        _hud_instance = None
        _hud_instance = LadderHUD(activity)
        print('[hud_ladder] HUD iniciado')
    except Exception as e:
        print(f'[hud_ladder] error: {e}')
        traceback.print_exc()

_orig_on_begin = None

def _on_begin_hook(self: bs.Activity) -> None:
    print(f'[hud_ladder] hook: {type(self).__name__}')
    _orig_on_begin(self)
    from bascenev1 import GameActivity
    if not isinstance(self, GameActivity):
        return
    with self.context:
        bs.timer(0.0, lambda: _inject_hud(self))

def enable() -> None:
    global _orig_on_begin
    from bascenev1._activity import Activity
    _orig_on_begin = Activity.on_begin
    Activity.on_begin = _on_begin_hook
    print('[hud_ladder] plugin cargado')

def disable() -> None:
    global _orig_on_begin
    from bascenev1._activity import Activity
    if _orig_on_begin is not None:
        Activity.on_begin = _orig_on_begin
        _orig_on_begin = None
    print('[hud_ladder] plugin descargado')
