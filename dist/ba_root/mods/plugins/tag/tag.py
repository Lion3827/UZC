# ba_meta require api 9

from __future__ import annotations
import weakref
import random
import bascenev1 as bs
import babase as ba
from bascenev1lib.actor.playerspaz import PlayerSpaz

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

_ACTIVE:      dict = {}
_ACTIVE_INFO: dict = {}
_ACTIVE_RANK: dict = {}
_calls:       dict = {}

_CHAR_WIDTHS = {
    'A':16.758,'B':15.898,'C':15.555,'D':16.156,'E':14.352,'F':13.148,
    'G':15.898,'H':17.102,'I':7.906,'J':9.625,'K':15.727,'L':13.234,
    'M':20.883,'N':17.102,'O':17.102,'P':15.039,'Q':17.359,'R':15.984,
    'S':15.555,'T':15.039,'U':16.156,'V':15.469,'W':20.453,'X':15.297,
    'Y':15.469,'Z':14.953,'a':12.547,'b':12.891,'c':11.773,'d':13.062,
    'e':12.633,'f':8.594,'g':13.406,'h':13.062,'i':6.359,'j':7.305,
    'k':12.375,'l':6.188,'m':20.367,'n':13.32,'o':13.062,'p':12.633,
    'q':12.633,'r':10.227,'s':12.461,'t':8.766,'u':13.406,'v':12.375,
    'w':17.359,'x':12.289,'y':12.375,'z':11.258,'0':13.922,'1':13.922,
    '2':13.922,'3':13.922,'4':13.922,'5':13.922,'6':13.922,'7':13.922,
    '8':13.922,'9':13.922,'!':7.82,'@':20.969,'#':14.867,'$':13.922,
    '%':19.078,'^':14.094,'&':23.031,'*':15.555,'(':11.086,')':11.086,
    '-':6.016,'_':12.031,'=':13.922,'+':13.922,'[':9.625,']':9.625,
    '{':9.625,'}':9.625,'|':8.164,';':6.961,':':6.961,',':6.961,
    '.':6.961,'<':13.922,'>':13.922,'?':11.516,'/':12.719,'~':13.922,
    '`':9.281,' ':6.961,
}

_SPECIAL_WIDTHS = {
    '\ue001':29.12,'\ue002':29.12,'\ue003':19.52,'\ue004':19.52,
    '\ue005':29.12,'\ue006':29.12,'\ue007':29.12,'\ue008':29.12,
    '\ue009':29.12,'\ue00a':29.12,'\ue00b':29.12,'\ue00c':29.12,
    '\ue00d':29.12,'\ue00e':29.12,'\ue00f':29.12,'\ue010':29.12,
    '\ue011':29.12,'\ue012':29.12,'\ue013':29.12,'\ue014':29.12,
    '\ue015':29.12,'\ue016':29.12,'\ue017':29.12,'\ue019':29.12,
    '\ue01a':29.12,'\ue01b':29.12,'\ue01c':29.12,'\ue01d':32.96,
    '\ue01e':17.28,'\ue01f':29.12,'\ue020':17.28,'\ue021':17.28,
    '\ue022':29.12,'\ue023':29.12,'\ue024':29.12,'\ue025':29.12,
    '\ue026':17.28,'\ue027':29.12,'\ue028':17.28,'\ue029':29.12,
    '\ue02a':43.68,'\ue02b':43.68,'\ue02c':43.68,'\ue02d':43.68,
    '\ue02e':43.68,'\ue02f':43.68,'\ue030':17.28,'\ue031':17.28,
    '\ue032':17.28,'\ue033':17.28,'\ue034':17.28,'\ue035':17.28,
    '\ue036':17.28,'\ue037':17.28,'\ue038':17.28,'\ue039':17.28,
    '\ue03a':17.28,'\ue03b':17.28,'\ue03c':17.28,'\ue03d':17.28,
    '\ue03e':17.28,'\ue03f':17.28,'\ue040':17.28,'\ue041':22.4,
    '\ue042':17.28,'\ue043':22.4,'\ue044':17.28,'\ue045':17.28,
    '\ue046':22.4,'\ue047':17.28,'\ue048':22.4,'\ue049':22.4,
    '\ue04a':17.28,'\ue04b':22.4,'\ue04c':22.4,'\ue04d':17.28,
    '\ue04e':22.4,'\ue04f':22.4,'\ue050':17.28,'\ue051':17.28,
    '\ue052':17.28,'\ue053':17.28,'\ue054':17.28,'\ue055':17.28,
    '\ue056':17.28,'\ue057':17.28,'\ue058':17.28,'\ue059':17.28,
    '\ue05a':17.28,'\ue05b':17.28,'\ue05c':17.28,'\ue05d':17.28,
    '\ue05e':17.28,'\ue05f':17.28,'\ue060':17.28,'\ue061':17.28,
    '\ue062':17.28,'\ue063':24.96,'\ue064':22.4,'\ue065':28.8,
    '\ue066':22.4,'\ue067':24.96,
}

_SYMBOL_NAMES: dict | None = None

def _get_symbols() -> dict:
    global _SYMBOL_NAMES
    if _SYMBOL_NAMES is not None:
        return _SYMBOL_NAMES
    S = ba.SpecialChar
    _SYMBOL_NAMES = {
        'crown':    ba.charstr(S.CROWN),
        'skull':    ba.charstr(S.SKULL),
        'heart':    ba.charstr(S.HEART),
        'moon':     ba.charstr(S.MOON),
        'eye':      ba.charstr(S.EYE_BALL),
        'yin':      ba.charstr(S.YIN_YANG),
        'spider':   ba.charstr(S.SPIDER),
        'helmet':   ba.charstr(S.HELMET),
        'mushroom': ba.charstr(S.MUSHROOM),
        'dragon':   ba.charstr(S.DRAGON),
        'ninja':    ba.charstr(S.NINJA_STAR),
        'fire':     ba.charstr(S.FIREBALL),
        'hal':      ba.charstr(S.HAL),
        'fedora':   ba.charstr(S.FEDORA),
        'viking':   ba.charstr(S.VIKING_HELMET),
        'santa':    ba.charstr(S.SANTA_HAT),
        'palm':     ba.charstr(S.PALM_TREE),
        'glove':    ba.charstr(S.BOXING_GLOVE),
        'potato':   ba.charstr(S.POTATO),
        'party':    ba.charstr(S.PARTY_ICON),
        'ticket':   ba.charstr(S.TICKET),
        'token':    ba.charstr(S.TOKEN),
        'trophy':   ba.charstr(S.TROPHY1),
        'trophy2':  ba.charstr(S.TROPHY2),
        'trophy3':  ba.charstr(S.TROPHY3),
        'trophy4':  ba.charstr(S.TROPHY4),
        'logo':     ba.charstr(S.LOGO),
        'discord':  ba.charstr(S.DISCORD_LOGO),
        'steam':    ba.charstr(S.STEAM_LOGO),
        'flag_us':  ba.charstr(S.FLAG_UNITED_STATES),
        'flag_uk':  ba.charstr(S.FLAG_UNITED_KINGDOM),
        'flag_bo':  ba.charstr(S.FLAG_BRAZIL),
        'flag_ar':  ba.charstr(S.FLAG_ARGENTINA),
        'flag_mx':  ba.charstr(S.FLAG_MEXICO),
        'flag_jp':  ba.charstr(S.FLAG_JAPAN),
        'flag_cn':  ba.charstr(S.FLAG_CHINA),
        'flag_de':  ba.charstr(S.FLAG_GERMANY),
        'flag_fr':  ba.charstr(S.FLAG_FRANCE),
        'flag_br':  ba.charstr(S.FLAG_BRAZIL),
        'flag_ru':  ba.charstr(S.FLAG_RUSSIA),
    }
    return _SYMBOL_NAMES

_RAINBOW_COLORS = [
    (1.0, 0.0, 0.0),
    (1.0, 0.5, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.5, 1.0),
    (0.5, 0.0, 1.0),
    (1.0, 0.0, 0.5),
]

_VALID_ANIMS  = ('wave_bright', 'color_travel', 'rainbow', 'pulse', 'static', 'wave', 'silver_wave', 'umbr_wave')
_VALID_ENTERS = ('wave_in', 'drop_in', 'explode_in', 'spin_in', 'random_in', 'fade_in')

_DEFAULT_WIDTH = 14.0
_SCALE_FACTOR  = 0.01075

_DIV_COLORS = {
    'Madera':   (0.5,  0.35, 0.15),
    'Piedra':   (0.7,  0.7,  0.7),
    'Hierro':   (0.55, 0.55, 0.6),
    'Bronce':   (0.8,  0.5,  0.2),
    'Plata':    (0.75, 0.75, 0.75),
    'Oro':      (1.0,  0.84, 0.0),
    'Diamante': (0.4,  0.8,  1.0),
    'Leyenda':  (1.0,  0.55, 0.0),
}

_DIV_EMOJI = {
    'Madera':   '\ue02e',
    'Piedra':   '\ue02d',
    'Hierro':   '\ue02a',
    'Bronce':   '\ue02b',
    'Plata':    '\ue02c',
    'Oro':      '\ue02f',
    'Diamante': '\ue02f\ue02f',
}

_TOP_EMOJI = {1: '\ue02f', 2: '\ue02c', 3: '\ue02b'}
_TOP_EMOJI_DEFAULT = '\ue02d'


def _div_emoji(division: str, ns: int) -> str:
    if division == 'Leyenda':
        extra = max(0, (ns - 3500) // 500)
        return '\ue02f' * (3 + extra)
    return _DIV_EMOJI.get(division, '\ue02d')


def _bright(color: tuple) -> tuple:
    return tuple(min(1.0, c + 0.5) for c in color)

def _resolve_symbols(text: str) -> str:
    syms = _get_symbols()
    result = text
    for name, char in syms.items():
        result = result.replace('[' + name + ']', char)
    return result

def _get_char_width(c: str) -> float:
    if c in _SPECIAL_WIDTHS:
        return _SPECIAL_WIDTHS[c]
    return _CHAR_WIDTHS.get(c, _DEFAULT_WIDTH)

def _get_role(acc: str) -> str | None:
    if _PERMS_AVAILABLE:
        return _perms.get_role(acc)
    return None


def _calc_positions(text: str) -> list:
    x = 0.0
    positions = []
    for c in text:
        w = _get_char_width(c)
        positions.append(x + w / 2.0)
        x += w
    offset = x / 2.0
    return [(p - offset) * _SCALE_FACTOR for p in positions]


def _make_gradient(text: str, color_stops: list) -> list:
    visible = [c for c in text if c != ' ']
    n = len(visible)
    if n == 0:
        return [tuple(color_stops[0])] * len(text)
    if len(color_stops) == 1:
        return [tuple(color_stops[0])] * len(text)
    vis_colors = []
    for i in range(n):
        t = i / max(n - 1, 1)
        seg_count = len(color_stops) - 1
        seg = min(int(t * seg_count), seg_count - 1)
        local_t = t * seg_count - seg
        c1 = color_stops[seg]
        c2 = color_stops[seg + 1]
        vis_colors.append((
            c1[0] + (c2[0] - c1[0]) * local_t,
            c1[1] + (c2[1] - c1[1]) * local_t,
            c1[2] + (c2[2] - c1[2]) * local_t,
        ))
    result = []
    vi = 0
    for c in text:
        if c == ' ':
            result.append((1.0, 1.0, 1.0))
        else:
            result.append(vis_colors[vi])
            vi += 1
    return result


def _make_cfg_from_dict(cfg_dict: dict) -> dict:
    raw_text    = cfg_dict.get('text') or cfg_dict.get('tag', '')
    text        = _resolve_symbols(raw_text)
    _tagcolor   = cfg_dict.get('tagcolor', [1.0, 1.0, 1.0])
    cs_raw      = cfg_dict.get('color_stops') or [_tagcolor]
    color_stops = [tuple(c) for c in cs_raw]
    wave_speed  = cfg_dict.get('wave_speed', 1.0)
    light_color = tuple(cfg_dict.get('light_color', color_stops[0]))
    anim        = cfg_dict.get('anim', 'wave_bright')
    if anim not in _VALID_ANIMS:
        anim = 'wave_bright'
    enter = cfg_dict.get('enter', 'wave_in')
    if enter not in _VALID_ENTERS:
        enter = 'wave_in'
    return {
        'text':         text,
        'colors':       _make_gradient(text, color_stops),
        'color_stops':  color_stops,
        'light_color':  light_color,
        'light_radius': 0.18,
        'anim':         anim,
        'enter':        enter,
        'wave_speed':   wave_speed,
    }


def _format_ns(ns: int) -> str:
    if ns >= 1_000_000:
        v = ns / 1_000_000
        return f'{v:.1f}M'.rstrip('0').rstrip('.')
    if ns >= 1000:
        v = ns / 1000
        return f'{v:.1f}k' if ns % 1000 != 0 else f'{int(v)}k'
    return str(ns)


class RoleTag:

    def __init__(self, spaz: PlayerSpaz, role_cfg: dict, use_owner: bool = True) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._ref         = weakref.ref(spaz)
        self._nodes: list = []
        self._timers: list = []
        self._letter_nodes: list = []
        self._math_y_nodes: list = []
        self._use_owner   = use_owner
        self._build(spaz, role_cfg)

    def _build(self, spaz: PlayerSpaz, cfg: dict) -> None:
        node    = spaz.node
        _owner  = node if self._use_owner else None
        text    = cfg['text']
        colors  = cfg.get('colors', [(1.0, 1.0, 1.0)] * len(text))
        positions = _calc_positions(text)
        anim    = cfg.get('anim', 'wave_bright')
        enter   = cfg.get('enter', 'wave_in')

        try:
            m_light = bs.newnode('math', owner=_owner, attrs={
                'input1': (0, 1.45, 0.0), 'operation': 'add',
            })
            node.connectattr('torso_position', m_light, 'input2')
            light = bs.newnode('light', owner=_owner, attrs={
                'color':  tuple(cfg.get('light_color', (1.0, 1.0, 1.0))),
                'radius': cfg.get('light_radius', 0.18),
                'volume_intensity_scale': 1.0,
            })
            m_light.connectattr('output', light, 'position')
            self._nodes += [m_light, light]
            if anim == 'static':
                light.intensity = 0.8
            else:
                bs.animate(light, 'intensity', {0.0: 0.5, 0.9: 1.3, 1.8: 0.5}, loop=True)
        except Exception as e:
            print('[tag] light error: ' + str(e))

        order = list(range(len([c for c in text if c != ' '])))
        if enter == 'random_in':
            random.shuffle(order)

        letter_idx = 0
        for i, char in enumerate(text):
            if char == ' ':
                continue
            color = colors[i] if i < len(colors) else (1.0, 1.0, 1.0)
            x     = positions[i]
            idx   = letter_idx
            letter_idx += 1

            try:
                m = bs.newnode('math', owner=_owner, attrs={
                    'input1': (x, 1.45, 0.0), 'operation': 'add',
                })
                node.connectattr('torso_position', m, 'input2')

                if enter == 'drop_in':
                    mv = bs.newnode('math', owner=_owner, attrs={
                        'input1': (0.0, 0.0, 0.0), 'operation': 'add',
                    })
                    m.connectattr('output', mv, 'input2')
                    self._nodes.append(mv)
                    self._math_y_nodes.append((mv, idx))
                    final_node = mv
                else:
                    final_node = m

                n = bs.newnode('text', owner=_owner, attrs={
                    'text':     char,
                    'in_world': True,
                    'scale':    0.0,
                    'color':    tuple(color) if not isinstance(color, tuple) else color,
                    'flatness': 1.0,
                    'shadow':   1.2,
                    'h_align':  'center',
                    'opacity':  0.0,
                })
                final_node.connectattr('output', n, 'position')
                self._nodes += [m, n]
                self._letter_nodes.append((n, color))

                t = bs.Timer(0.01, bs.WeakCall(
                    self._enter_letter, n, color, idx, enter,
                    mv if enter == 'drop_in' else None
                ))
                self._timers.append(t)

            except Exception as e:
                print('[tag] letter error ' + char + ': ' + str(e))

        enter_duration = self._enter_duration(enter, len(self._letter_nodes))
        t_idle = bs.Timer(enter_duration, bs.WeakCall(self._start_idle, anim, colors))
        self._timers.append(t_idle)

    def _enter_duration(self, enter: str, n: int) -> float:
        durations = {
            'wave_in':    0.15 * n + 0.6,
            'drop_in':    0.12 * n + 0.6,
            'explode_in': 0.12 * n + 0.6,
            'spin_in':    0.12 * n + 0.6,
            'random_in':  0.18 * n + 0.6,
            'fade_in':    0.6,
        }
        return durations.get(enter, 0.8)

    def _enter_letter(self, n: bs.Node, color: tuple, idx: int,
                      enter: str, mv=None) -> None:
        if not n or not n.exists():
            return

        if enter == 'wave_in':
            d = idx * 0.15
            bs.animate(n, 'opacity', {d: 0.0, d + 0.18: 1.0})
            bs.animate(n, 'scale',   {d: 0.0067, d + 0.25: 0.0108,
                                       d + 0.38: 0.0092, d + 0.48: 0.010})

        elif enter == 'drop_in':
            d = idx * 0.12
            bs.animate(n, 'opacity', {d: 0.0, d + 0.05: 1.0})
            if mv and mv.exists():
                bs.animate_array(mv, 'input1', 3, {
                    d:        (0.0,  0.5,  0.0),
                    d + 0.18: (0.0, -0.04, 0.0),
                    d + 0.26: (0.0,  0.02, 0.0),
                    d + 0.32: (0.0, -0.01, 0.0),
                    d + 0.38: (0.0,  0.0,  0.0),
                })
            bs.animate(n, 'scale', {d: 0.010, d + 0.38: 0.010})

        elif enter == 'explode_in':
            d = idx * 0.12
            bs.animate(n, 'opacity', {d: 0.0, d + 0.05: 1.0})
            bs.animate(n, 'scale',   {d: 0.0292, d + 0.15: 0.0075,
                                       d + 0.22: 0.0117, d + 0.28: 0.0092,
                                       d + 0.34: 0.010})

        elif enter == 'spin_in':
            d = idx * 0.12
            bs.animate(n, 'opacity', {d: 0.0, d + 0.08: 1.0})
            bs.animate(n, 'scale',   {d: 0.0, d + 0.25: 0.0117,
                                       d + 0.35: 0.0092, d + 0.42: 0.010})
            bs.animate(n, 'rotate',  {d: 180.0, d + 0.30: 10.0,
                                       d + 0.38: -5.0, d + 0.44: 0.0})

        elif enter == 'random_in':
            d = idx * 0.18
            bs.animate(n, 'opacity', {d: 0.0, d + 0.15: 1.0})
            bs.animate(n, 'scale',   {d: 0.0292, d + 0.15: 0.0075,
                                       d + 0.22: 0.0117, d + 0.28: 0.0092,
                                       d + 0.34: 0.010})

        elif enter == 'fade_in':
            d = idx * 0.06
            bs.animate(n, 'opacity', {d: 0.0, d + 0.25: 1.0})
            bs.animate(n, 'scale',   {0.0: 0.010})

    def _start_idle(self, anim: str, colors: list) -> None:
        nodes     = self._letter_nodes
        n_letters = len(nodes)
        if n_letters == 0:
            return

        if anim in ('wave_bright', 'wave'):
            period = max(0.9, n_letters * 0.09)
            for i, (n, color) in enumerate(nodes):
                if not n or not n.exists():
                    continue
                bright = _bright(color)
                offset = round(i * 0.09, 3)
                keys = {
                    0.0:                    color,
                    offset:                 color,
                    round(offset + 0.10, 3): bright,
                    round(offset + 0.20, 3): color,
                    period:                 color,
                }
                t = bs.Timer(0.01, lambda _n=n, _k=keys: (
                    _n.exists() and
                    bs.animate_array(_n, 'color', 3, _k, loop=True)
                ))
                self._timers.append(t)

        elif anim == 'color_travel':
            period = 1.4
            step   = period / max(n_letters, 1)
            for i, (n, color) in enumerate(nodes):
                if not n or not n.exists():
                    continue
                keys = {}
                for j in range(n_letters + 1):
                    t_key = round(j * step, 3)
                    keys[t_key] = colors[(i + j) % n_letters]
                t = bs.Timer(0.01, lambda _n=n, _k=keys: (
                    _n.exists() and
                    bs.animate_array(_n, 'color', 3, _k, loop=True)
                ))
                self._timers.append(t)

        elif anim == 'rainbow':
            n_colors = len(_RAINBOW_COLORS)
            period   = 2.0
            step     = period / n_colors
            for idx, (n, _) in enumerate(nodes):
                if not n or not n.exists():
                    continue
                offset = idx * 0.15
                keys   = {}
                for j in range(n_colors + 1):
                    t_key = round(j * step + offset, 3) % period
                    keys[t_key] = _RAINBOW_COLORS[j % n_colors]
                try:
                    bs.animate_array(n, 'color', 3, keys, loop=True)
                except Exception:
                    pass

        elif anim == 'pulse':
            for n, color in nodes:
                if not n or not n.exists():
                    continue
                bright = _bright(color)
                bs.animate_array(n, 'color', 3, {
                    0.0: color, 0.5: bright, 1.0: color,
                }, loop=True)
                bs.animate(n, 'scale', {
                    0.0: 0.010, 0.5: 0.0117, 1.0: 0.010,
                }, loop=True)

        elif anim == 'static':
            for n, color in nodes:
                if not n or not n.exists():
                    continue
                n.color = color
                n.scale = 0.010

        elif anim == 'silver_wave':
            base      = (0.5, 0.5, 0.5)
            bright    = (0.95, 0.95, 0.95)
            n_letters = len(nodes)
            period    = max(2.0, n_letters * 0.3 + 0.6)
            for i, (n, _) in enumerate(nodes):
                if not n or not n.exists():
                    continue
                delay = i * 0.3
                keys  = {
                    0.0:          base,
                    delay:        base,
                    delay + 0.15: bright,
                    delay + 0.3:  base,
                    period:       base,
                }
                t = bs.Timer(0.01, lambda _n=n, _k=keys: (
                    _n.exists() and
                    bs.animate_array(_n, 'color', 3, _k, loop=True)
                ))
                self._timers.append(t)

        elif anim == 'umbr_wave':
            base      = (0.16, 0.0, 0.62)
            bright    = (0.6, 0.5, 1.0)
            n_letters = len(nodes)
            period    = max(2.0, n_letters * 0.3 + 0.6)
            for i, (n, _) in enumerate(nodes):
                if not n or not n.exists():
                    continue
                delay = i * 0.3
                keys  = {
                    0.0:          base,
                    delay:        base,
                    delay + 0.15: bright,
                    delay + 0.3:  base,
                    period:       base,
                }
                t = bs.Timer(0.01, lambda _n=n, _k=keys: (
                    _n.exists() and
                    bs.animate_array(_n, 'color', 3, _k, loop=True)
                ))
                self._timers.append(t)

    def destroy(self) -> None:
        self._timers.clear()
        for n in self._nodes:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._nodes.clear()
        self._letter_nodes.clear()
        self._math_y_nodes.clear()


class InfoTag:

    def __init__(self, spaz: PlayerSpaz, acc: str) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._node          = spaz.node
        self._acc           = acc
        self._nodes: list   = []
        self._ns_text       = None
        self._current_ns    = 500
        self._target_ns     = 500
        self._current_color = (1.0, 1.0, 1.0)
        self._timer         = None
        self._build()

    def _build(self) -> None:
        node     = self._node
        ns       = 500
        division = 'Piedra'
        clan     = None
        if _STATS_AVAILABLE:
            try:
                p = _stats.get_player(self._acc)
                if p:
                    ns       = p.get('ns', 500)
                    division = p.get('division', 'Piedra')
                    clan     = p.get('clan')
            except Exception:
                pass

        self._current_ns    = ns
        self._target_ns     = ns
        ns_color            = _DIV_COLORS.get(division, (1.0, 1.0, 1.0))
        self._current_color = ns_color

        role    = _get_role(self._acc)
        tag_len = 6
        if role and _PERMS_AVAILABLE:
            cfg = _perms.get_role_cfg(role)
            if cfg:
                tag_len = len(cfg.get('text', 'STAFF'))
        x_ns = -0.60 - (tag_len * 0.035)
        y    = 1.35

        try:
            m_ns = bs.newnode('math', owner=node,
                              attrs={'input1': (x_ns, y, 0.0), 'operation': 'add'})
            node.connectattr('torso_position', m_ns, 'input2')
            ns_text = bs.newnode('text', owner=node, attrs={
                'text':     f'{_div_emoji(division, ns)} N/S:{_format_ns(ns)}',
                'in_world': True,
                'shadow':   1.0,
                'flatness': 1.0,
                'color':    ns_color,
                'scale':    0.0062,
                'h_align':  'center',
            })
            m_ns.connectattr('output', ns_text, 'position')
            self._ns_text = ns_text
            self._nodes  += [m_ns, ns_text]
            bright = tuple(min(c * 1.35, 1.0) for c in ns_color)
            bs.animate_array(ns_text, 'color', 3,
                             {0.0: ns_color, 0.5: bright, 1.0: ns_color}, loop=True)
        except Exception as e:
            print(f'[tag] InfoTag NS error: {e}')

        if _STATS_AVAILABLE:
            try:
                def _fetch(ref=weakref.ref(self)):
                    obj = ref()
                    if obj is None:
                        return
                    p = _stats.get_player(obj._acc)
                    if p:
                        real_ns = p.get('ns', 500)
                        obj._current_ns = real_ns
                        obj._target_ns  = real_ns
                        div = p.get('division', 'Piedra')
                        if obj._ns_text and obj._ns_text.exists():
                            obj._ns_text.text  = f'{_div_emoji(div, real_ns)} N/S:{_format_ns(real_ns)}'
                            obj._ns_text.color = _DIV_COLORS.get(div, (1.0, 1.0, 1.0))
                bs.timer(0.5, _fetch)
            except Exception:
                pass

        if clan:
            x_clan = abs(x_ns)
            try:
                m_clan = bs.newnode('math', owner=node,
                                    attrs={'input1': (x_clan, y, 0.0), 'operation': 'add'})
                node.connectattr('torso_position', m_clan, 'input2')
                clan_text = bs.newnode('text', owner=node, attrs={
                    'text':     f'{clan}',
                    'in_world': True,
                    'shadow':   1.0,
                    'flatness': 1.0,
                    'color':    (0.6, 0.4, 1.0),
                    'scale':    0.00672,
                    'h_align':  'center',
                })
                m_clan.connectattr('output', clan_text, 'position')
                self._nodes += [m_clan, clan_text]
                bs.animate_array(clan_text, 'color', 3,
                                 {0.0: (0.6, 0.4, 1.0), 0.5: (0.8, 0.6, 1.0), 1.0: (0.6, 0.4, 1.0)},
                                 loop=True)
            except Exception as e:
                print(f'[tag] InfoTag clan error: {e}')

        if _STATS_AVAILABLE:
            self._timer = bs.timer(0.8, bs.WeakCall(self._tick), repeat=True)

    def _tick(self) -> None:
        if not self._ns_text or not self._ns_text.exists():
            return
        try:
            p = _stats.get_player(self._acc)
            if not p:
                return
            self._target_ns = p.get('ns', self._current_ns)
            if self._current_ns == self._target_ns:
                return
            diff     = self._target_ns - self._current_ns
            going_up = diff > 0
            step     = max(1, abs(diff) // 6)
            if going_up:
                self._current_ns = min(self._current_ns + step, self._target_ns)
            else:
                self._current_ns = max(self._current_ns - step, self._target_ns)
            from plugins.stats.stats import get_division as _get_div
            new_div   = _get_div(self._current_ns)
            new_color = _DIV_COLORS.get(new_div, (1.0, 1.0, 1.0))
            self._ns_text.text = f'{_div_emoji(new_div, self._current_ns)} N/S:{_format_ns(self._current_ns)}'
            flash = (0.2, 1.0, 0.4) if going_up else (1.0, 0.3, 0.3)
            self._ns_text.color = flash
            _ref = weakref.ref(self)
            bs.timer(0.18, lambda ref=_ref, c=new_color: ref() and ref()._restore_color(c))
            if new_color != self._current_color:
                self._current_color = new_color
                bright = tuple(min(c * 1.35, 1.0) for c in new_color)
                bs.timer(0.25, lambda ref=_ref, b=new_color, br=bright: ref() and ref()._start_pulse(b, br))
        except Exception:
            pass

    def _restore_color(self, color: tuple) -> None:
        try:
            if self._ns_text and self._ns_text.exists():
                self._ns_text.color = color
        except Exception:
            pass

    def _start_pulse(self, base: tuple, bright: tuple) -> None:
        try:
            if self._ns_text and self._ns_text.exists():
                bs.animate_array(self._ns_text, 'color', 3,
                                 {0.0: base, 0.5: bright, 1.0: base}, loop=True)
        except Exception:
            pass

    def destroy(self) -> None:
        self._timer = None
        for n in self._nodes:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._nodes.clear()
        self._ns_text = None


class RankTag:

    def __init__(self, spaz: PlayerSpaz, acc: str) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._node        = spaz.node
        self._acc         = acc
        self._nodes: list = []
        self._rank_text   = None
        self._timer       = None
        self._current_rank = 0
        self._build()

    def _build(self) -> None:
        rank = self._get_rank()
        self._current_rank = rank
        if not rank:
            return
        text = self._rank_text_for(rank)
        try:
            m = bs.newnode('math', owner=self._node,
                           attrs={'input1': (0.0, 1.2, 0.0), 'operation': 'add'})
            self._node.connectattr('torso_position', m, 'input2')
            n = bs.newnode('text', owner=self._node, attrs={
                'text':     text,
                'in_world': True,
                'shadow':   1.0,
                'flatness': 1.0,
                'color':    (1.0, 1.0, 1.0),
                'scale':    0.0062,
                'h_align':  'center',
            })
            m.connectattr('output', n, 'position')
            self._nodes += [m, n]
            self._rank_text = n
            if _STATS_AVAILABLE:
                self._timer = bs.timer(5.0, bs.WeakCall(self._tick), repeat=True)
        except Exception as e:
            print(f'[tag] RankTag error: {e}')

    def _get_rank(self) -> int:
        if not _STATS_AVAILABLE:
            return 0
        try:
            stats = _stats.get_stats()
            sorted_players = sorted(stats.values(), key=lambda p: p.get('kills', 0), reverse=True)
            for i, p in enumerate(sorted_players):
                if p.get('aid') == self._acc:
                    return i + 1
        except Exception:
            pass
        return 0

    def _rank_text_for(self, rank: int) -> str:
        emoji = _TOP_EMOJI.get(rank, _TOP_EMOJI_DEFAULT)
        return f'{emoji} #{rank}'

    def _tick(self) -> None:
        if not self._rank_text or not self._rank_text.exists():
            return
        try:
            new_rank = self._get_rank()
            if new_rank and new_rank != self._current_rank:
                self._current_rank = new_rank
                self._rank_text.text = self._rank_text_for(new_rank)
        except Exception:
            pass

    def destroy(self) -> None:
        self._timer = None
        for n in self._nodes:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._nodes.clear()
        self._rank_text = None


class CustomTag:

    def __init__(self, spaz: PlayerSpaz, tag_cfg: dict) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._nodes: list = []
        self._build(spaz, tag_cfg)

    def _build(self, spaz: PlayerSpaz, cfg: dict) -> None:
        role_cfg = _make_cfg_from_dict(cfg)
        RoleTag(spaz, role_cfg)

    def destroy(self) -> None:
        for n in self._nodes:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._nodes.clear()


def _new_spaz_init(self: PlayerSpaz, *a, **k) -> None:
    _calls['init'](self, *a, **k)
    try:
        acc = self._player.sessionplayer.get_account_id()
    except Exception:
        return
    ref = weakref.ref(self)
    bs.timer(0.15, lambda: _apply_info(ref, acc))
    bs.timer(0.15, lambda: _apply_rank(ref, acc))

    role = _get_role(acc)
    if role and _PERMS_AVAILABLE:
        raw_cfg = _perms.get_role_cfg(role)
        if raw_cfg:
            cfg = _make_cfg_from_dict(raw_cfg)
            bs.timer(0.15, lambda: _apply_role(ref, acc, cfg))

    if _PERMS_AVAILABLE:
        tag_cfg = _perms.get_tag(acc)
        if tag_cfg:
            built = _make_cfg_from_dict(tag_cfg)
            bs.timer(0.15, lambda: _apply_custom(ref, acc, built))


def _apply_rank(ref: weakref.ref, acc: str) -> None:
    spaz = ref()
    if not spaz or not spaz.node or not spaz.node.exists():
        return
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        old = _ACTIVE_RANK.get(acc)
        if isinstance(old, RankTag):
            try:
                old.destroy()
            except Exception:
                pass
        _ACTIVE_RANK[acc] = RankTag(spaz, acc)


def _apply_info(ref: weakref.ref, acc: str) -> None:
    spaz = ref()
    if not spaz or not spaz.node or not spaz.node.exists():
        return
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        old = _ACTIVE_INFO.get(acc)
        if isinstance(old, InfoTag):
            try:
                old.destroy()
            except Exception:
                pass
        _ACTIVE_INFO[acc] = InfoTag(spaz, acc)


def _apply_role(ref: weakref.ref, acc: str, cfg: dict) -> None:
    spaz = ref()
    if not spaz or not spaz.node or not spaz.node.exists():
        return
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        old = _ACTIVE.get(acc)
        if isinstance(old, RoleTag):
            try:
                old.destroy()
            except Exception:
                pass
        _ACTIVE[acc] = RoleTag(spaz, cfg)


def _apply_custom(ref: weakref.ref, acc: str, cfg: dict) -> None:
    spaz = ref()
    if not spaz or not spaz.node or not spaz.node.exists():
        return
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        old = _ACTIVE.get(acc)
        if isinstance(old, RoleTag):
            try:
                old.destroy()
            except Exception:
                pass
        _ACTIVE[acc] = RoleTag(spaz, cfg)


def _flush_active() -> None:

    for tag in list(_ACTIVE.values()):
        if isinstance(tag, RoleTag):
            try:
                tag.destroy()
            except Exception:
                pass
    _ACTIVE.clear()
    for tag in list(_ACTIVE_INFO.values()):
        if isinstance(tag, InfoTag):
            try:
                tag.destroy()
            except Exception:
                pass
    _ACTIVE_INFO.clear()
    for tag in list(_ACTIVE_RANK.values()):
        if isinstance(tag, RankTag):
            try:
                tag.destroy()
            except Exception:
                pass
    _ACTIVE_RANK.clear()


def _find_spaz_by_acc(act, acc: str):
    for pl in act.players:
        try:
            if pl.sessionplayer.get_account_id() == acc:
                if hasattr(pl, 'actor') and pl.actor and pl.actor.node:
                    return pl.actor
        except Exception:
            pass
    return None


def apply_live(acc: str) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            return
        spaz = _find_spaz_by_acc(act, acc)
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        old = _ACTIVE.get(acc)
        if isinstance(old, RoleTag):
            try:
                old.destroy()
            except Exception:
                pass
        _ACTIVE.pop(acc, None)
        with act.context:
            if _PERMS_AVAILABLE:
                tag_cfg = _perms.get_tag(acc)
                if tag_cfg:
                    built = _make_cfg_from_dict(tag_cfg)
                    _ACTIVE[acc] = RoleTag(spaz, built)
                    return
            role = _get_role(acc)
            if role and _PERMS_AVAILABLE:
                raw_cfg = _perms.get_role_cfg(role)
                if raw_cfg:
                    cfg = _make_cfg_from_dict(raw_cfg)
                    _ACTIVE[acc] = RoleTag(spaz, cfg)
    except Exception as e:
        print(f'[tag] apply_live error: {e}')


def _setup() -> None:
    _calls['init'] = PlayerSpaz.__init__
    PlayerSpaz.__init__ = _new_spaz_init

    orig_in = bs.GameActivity.on_transition_in
    def _patched_in(self, *args, **kwargs) -> None:
        _flush_active()
        orig_in(self, *args, **kwargs)
    bs.GameActivity.on_transition_in = _patched_in

    orig_out = bs.GameActivity.on_transition_out
    def _patched_out(self, *args, **kwargs) -> None:
        _flush_active()
        orig_out(self, *args, **kwargs)
    bs.GameActivity.on_transition_out = _patched_out

    orig_end = bs.GameActivity.end
    def _patched_end(self, *args, **kwargs) -> None:
        _flush_active()
        orig_end(self, *args, **kwargs)
    bs.GameActivity.end = _patched_end


def enable() -> None:
    _setup()
    print('[tag] loaded')
