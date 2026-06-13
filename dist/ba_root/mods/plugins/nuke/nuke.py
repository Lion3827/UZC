# ba_meta require api 9

from __future__ import annotations
import weakref
import bascenev1 as bs
from bascenev1lib.actor.bomb import Bomb, BombFactory
from bascenev1lib.gameutils import SharedObjects

try:
    from plugins.perms import perms as _perms
    _PERMS_AVAILABLE = True
except Exception:
    _PERMS_AVAILABLE = False

_state: dict = {
    'nuke':               None,
    'timer':              None,
    'light':              None,
    'countdown':          None,
    'holder':             None,
    'seconds':            15,
    'ice':                False,
    'countdown_started':  False,
    'activity':           None,
    'tick_id':            0,
}


class NukeBomb:

    def __init__(self, position: tuple, seconds: int, ice: bool) -> None:
        self._exploded  = False
        self._held_by   = 0
        self._seconds   = seconds
        self._ice       = ice
        self._nodes: list = []
        self._timers: list = []

        act = bs.get_foreground_host_activity()
        if not act:
            return

        with act.context:
            factory = BombFactory.get()
            shared  = SharedObjects.get()

            materials = (
                factory.bomb_material,
                shared.footing_material,
                shared.object_material,
                factory.normal_sound_material,
            )

            if ice:
                mesh      = factory.bomb_mesh
                light_mesh = factory.bomb_mesh
                tex       = factory.ice_tex
            else:
                mesh      = factory.impact_bomb_mesh
                light_mesh = factory.impact_bomb_mesh
                tex       = factory.impact_tex

            self.node = bs.newnode('prop', delegate=self, attrs={
                'position':        position,
                'velocity':        (0.0, 0.0, 0.0),
                'mesh':            mesh,
                'light_mesh':      light_mesh,
                'body':            'crate',
                'shadow_size':     0.5,
                'color_texture':   tex,
                'reflection':      'powerup',
                'reflection_scale':[1.5],
                'materials':       materials,
            })

            self.node.mesh_scale = 1.0

            color = (0.4, 0.8, 1.0) if ice else (1.0, 0.5, 0.1)
            self._light = bs.newnode('light', owner=self.node, attrs={
                'color':     color,
                'radius':    0.5,
                'intensity': 0.4,
            })
            self.node.connectattr('position', self._light, 'position')

            self._timer_text_math = bs.newnode('math', owner=self.node, attrs={
                'input1': (0, 1.5, 0),
                'operation': 'add',
            })
            self.node.connectattr('position', self._timer_text_math, 'input2')
            self._timer_text = bs.newnode('text', owner=self.node, attrs={
                'text':     str(seconds),
                'in_world': True,
                'scale':    0.02,
                'shadow':   1.0,
                'flatness': 1.0,
                'color':    (1.0, 1.0, 1.0),
                'h_align':  'center',
            })
            self._timer_text_math.connectattr('output', self._timer_text, 'position')

            self._nodes = [self._light, self._timer_text_math, self._timer_text]

    def handlemessage(self, msg) -> None:
        if isinstance(msg, bs.PickedUpMessage):
            self._held_by += 1
            self._update_floatyness()
            if self._held_by == 1 and not _state.get('countdown_started'):
                _state['countdown_started'] = True
                tid = _state['tick_id']
                _state['timer'] = bs.Timer(1.0, lambda: _tick(tid))
                self.start_growth(_state.get('seconds', 15))
        elif isinstance(msg, bs.DroppedMessage):
            self._held_by = max(0, self._held_by - 1)
            try:
                holder_node = self.node.hold_node if self.node and self.node.exists() else None
                if holder_node and holder_node.exists():
                    holder_node.extra_acceleration = (0, 0, 0)
                    holder_node.jump_height_scale  = 1.0
            except Exception:
                pass
            self._update_floatyness()
            _state['holder'] = None
            if self._held_by == 0:
                _state['timer'] = None
        elif isinstance(msg, bs.HitMessage):
            if not self._exploded:
                self._explode()
        elif isinstance(msg, bs.DieMessage):
            if not self._exploded:
                self._explode()

    def _update_floatyness(self) -> None:
        if not self.node or not self.node.exists():
            return
        try:
            old_y = self.node.extra_acceleration[1]
        except Exception:
            old_y = 0
        new_y = {0: 0, 1: 39, 2: 19 + 20 * 2, 3: 19 + 20 * 3}.get(self._held_by, 0)
        time = 0.3 if (old_y >= new_y) else 1.0
        keys = {0: (0, old_y, 0), time: (0, new_y, 0)}
        bs.timer(0.0, lambda: bs.animate_array(self.node, 'extra_acceleration', 3, keys) if self.node and self.node.exists() else None)

        try:
            holder_node = self.node.hold_node
            if holder_node and holder_node.exists():
                if self._held_by > 0:
                    old_hy = holder_node.extra_acceleration[1]
                    keys_h = {0: (0, old_hy, 0), time: (0, 18, 0)}
                    hn1 = holder_node
                    bs.timer(0.0, lambda h=hn1, k=keys_h: bs.animate_array(h, 'extra_acceleration', 3, k) if h and h.exists() else None)
                    holder_node.jump_height_scale = 1.8
                else:
                    old_hy = holder_node.extra_acceleration[1]
                    keys_h = {0: (0, old_hy, 0), 0.3: (0, 0, 0)}
                    hn2 = holder_node
                    bs.timer(0.0, lambda h=hn2, k=keys_h: bs.animate_array(h, 'extra_acceleration', 3, k) if h and h.exists() else None)
                    holder_node.jump_height_scale = 1.0
        except Exception:
            pass

    def start_growth(self, seconds: int) -> None:
        """Activa el crecimiento y animaciones — llamado al agarrar por primera vez."""
        try:
            if not self.node or not self.node.exists():
                return
            bs.animate(self.node, 'mesh_scale', {
                0:             1.0,
                seconds * 0.3: 2.0,
                seconds * 0.7: 4.0,
                seconds:       6.0,
            })
            bs.animate(self._light, 'intensity', {0.0: 0.4, 0.5: 1.2, 1.0: 0.4}, loop=True)
            bs.animate(self._light, 'radius', {
                0:               0.5,
                seconds * 0.5:   1.5,
                seconds:         3.5,
            })
        except Exception as e:
            print(f'[nuke] start_growth error: {e}')

    def update_text(self, seconds: int) -> None:
        try:
            if self._timer_text and self._timer_text.exists():
                self._timer_text.text = str(seconds)
                if seconds <= 5:
                    self._timer_text.color = (1.0, 0.3, 0.3)
                elif seconds <= 10:
                    self._timer_text.color = (1.0, 0.8, 0.2)
                else:
                    self._timer_text.color = (1.0, 1.0, 1.0)
        except Exception:
            pass

    def _explode(self) -> None:
        if self._exploded:
            return
        self._exploded = True

        try:
            act = bs.get_foreground_host_activity()
            if act:
                with act.context:
                    try:
                        pos = self.node.position if self.node.exists() else (0, 1, 0)
                    except Exception:
                        pos = (0, 1, 0)

                    if self._ice:
                        _do_ice_blast(pos)
                    else:
                        _do_nuke_blast(pos)

                    try:
                        if self.node and self.node.exists():
                            self.node.delete()
                    except Exception:
                        pass
        except Exception as e:
            print(f'[nuke] explode error: {e}')
        finally:
            _cleanup_nuke()

    def destroy(self) -> None:
        try:
            if self.node and self.node.exists():
                self.node.delete()
        except Exception:
            pass


def _do_nuke_blast(pos: tuple) -> None:
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        shared = SharedObjects.get()
        factory = BombFactory.get()

        for i in range(5):
            bs.timer(i * 0.08, lambda p=pos: bs.newnode('explosion', attrs={
                'position': p,
                'radius':   10.0,
            }))

        light = bs.newnode('light', attrs={
            'position': pos,
            'color':    (1.0, 0.5, 0.1),
            'radius':   8.0,
        })
        bs.animate(light, 'intensity', {0.0: 5.0, 0.5: 8.0, 2.5: 0.0})
        bs.animate(light, 'radius',    {0.0: 8.0, 0.5: 18.0, 2.5: 0.0})
        bs.timer(2.5, light.delete)
        bs.camerashake(25.0)

        offsets = [
            (0, 0, 0),
            (2, 0, 0), (-2, 0, 0),
            (0, 0, 2), (0, 0, -2),
            (3, 0, 3), (-3, 0, 3),
            (3, 0, -3), (-3, 0, -3),
        ]
        for ox, oy, oz in offsets:
            bpos = (pos[0] + ox, pos[1] + oy + 0.5, pos[2] + oz)
            try:
                b = Bomb(position=bpos, bomb_type='impact')
                b.blast_radius = 3.5
                b.autoretain()
            except Exception:
                pass

        try:
            factory.hiss_sound.play(4.0, position=pos)
        except Exception:
            pass


def _do_ice_blast(pos: tuple) -> None:
    act = bs.get_foreground_host_activity()
    if not act:
        return
    with act.context:
        shared = SharedObjects.get()
        factory = BombFactory.get()

        light = bs.newnode('light', attrs={
            'position': pos,
            'color':    (0.4, 0.8, 1.0),
            'radius':   6.0,
        })
        bs.animate(light, 'intensity', {0.0: 3.0, 0.5: 5.0, 2.5: 0.0})
        bs.animate(light, 'radius',    {0.0: 6.0, 0.5: 14.0, 2.5: 0.0})
        bs.timer(2.5, light.delete)
        bs.camerashake(10.0)

        for player in act.players:
            try:
                spaz = player.actor
                if spaz and spaz.node and spaz.node.exists():
                    spaz.node.frozen = True
                    bs.timer(5.0, lambda s=weakref.ref(spaz): _unfreeze(s))
            except Exception:
                pass

        try:
            factory.activate_sound.play(2.0, position=pos)
        except Exception:
            pass


def _unfreeze(ref: weakref.ref) -> None:
    try:
        spaz = ref()
        if spaz and spaz.node and spaz.node.exists():
            spaz.node.frozen = False
    except Exception:
        pass


def _cleanup_nuke() -> None:
    _state['nuke']              = None
    _state['timer']             = None
    _state['countdown']         = None
    _state['holder']            = None
    _state['seconds']           = 15
    _state['ice']               = False
    _state['countdown_started'] = False
    _state['activity']          = None
    _state['tick_id']           += 1



def _watchdog(tick_id: int) -> None:
    if tick_id != _state.get('tick_id', 0):
        return
    nuke = _state.get('nuke')
    if not nuke:
        return
    try:
        alive = nuke.node and nuke.node.exists()
    except Exception:
        alive = False
    if not alive:
        _cleanup_nuke()
        return
    try:
        pos = nuke.node.position
        if abs(pos[0]) > 50 or pos[1] > 50 or abs(pos[2]) > 50:
            act = bs.get_foreground_host_activity()
            if act:
                with act.context:
                    nuke.node.delete()
            _cleanup_nuke()
            bs.broadcastmessage('Nuke perdida.', color=(1.0, 0.5, 0.2))
            return
    except Exception:
        pass
    tid = _state['tick_id']
    bs.Timer(0.5, lambda t=tid: _watchdog(t))


def _tick(tick_id: int = 0) -> None:
    if tick_id != _state.get('tick_id', 0):
        return

    nuke = _state.get('nuke')
    if not nuke:
        _cleanup_nuke()
        return

    try:
        node_exists = nuke.node and nuke.node.exists()
    except Exception:
        node_exists = False

    if not node_exists:
        _cleanup_nuke()
        return

    # Si nadie sostiene la bomba, no hacer countdown — solo reschedular chequeo
    try:
        held = nuke._held_by
    except Exception:
        held = 0

    if held == 0:
        tid = _state['tick_id']
        _state['timer'] = bs.Timer(1.0, lambda t=tid: _tick(t))
        return

    secs = _state.get('seconds', 15)
    secs -= 1
    _state['seconds'] = secs
    nuke.update_text(secs)

    if secs <= 0:
        act = bs.get_foreground_host_activity()
        if act:
            with act.context:
                try:
                    pos = nuke.node.position
                except Exception:
                    pos = (0, 1, 0)
                if _state.get('ice'):
                    _do_ice_blast(pos)
                else:
                    _do_nuke_blast(pos)
                try:
                    act.end_game()
                except Exception:
                    pass
        _cleanup_nuke()
        return

    if secs <= 5:
        try:
            from bascenev1lib.actor.bomb import BombFactory
            BombFactory.get().fuse_sound.play(1.0)
        except Exception:
            pass

    tid = _state['tick_id']
    _state['timer'] = bs.Timer(1.0, lambda: _tick(tid))


def spawn_nuke(seconds: int = 15, ice: bool = False) -> None:
    act = bs.get_foreground_host_activity()
    if not act:
        bs.broadcastmessage('No hay partida activa.', color=(1.0, 0.3, 0.3))
        return

    if _state.get('nuke'):
        stored = _state.get('activity')
        stored_act = stored() if stored is not None else None
        if stored_act is not act:
            _cleanup_nuke()
        else:
            bs.broadcastmessage('Ya hay una Nuke activa.', color=(1.0, 0.5, 0.2))
            return

    with act.context:
        try:
            spawn_pos = act.map.get_flag_position(None)
        except Exception:
            spawn_pos = (0.0, 2.0, 0.0)

        nuke_type = 'ICE NUKE' if ice else 'NUKE'
        color     = (0.4, 0.8, 1.0) if ice else (1.0, 0.5, 0.1)
        bs.broadcastmessage(
            f'\u2622 {nuke_type} activada! {seconds}s para sostenerla y ganar!',
            color=color,
        )

        _state['nuke']      = NukeBomb(spawn_pos, seconds, ice)
        _state['seconds']   = seconds
        _state['ice']       = ice
        _state['activity']  = weakref.ref(act)
        tid = _state['tick_id']
        _watchdog(tid)


def filter_chat(msg: str, client_id: int) -> str | None:
    if not msg.startswith('/nuke'):
        return msg

    parts = msg.strip().split()

    try:
        roster = bs.get_game_roster()
        acc    = None
        for entry in roster:
            if entry.get('client_id') == client_id:
                acc = entry.get('account_id')
                break
    except Exception:
        acc = None

    if _PERMS_AVAILABLE and acc:
        role = _perms.get_role(acc)
        if role not in ('owner', 'admin'):
            bs.broadcastmessage('Sin permisos.', clients=[client_id], transient=True)
            return None
    elif not acc:
        return None

    ice     = 'ice' in [p.lower() for p in parts]
    seconds = 15
    for p in parts[1:]:
        if p.isdigit():
            seconds = max(5, min(int(p), 120))
            break

    act = bs.get_foreground_host_activity()
    if act:
        with act.context:
            spawn_nuke(seconds, ice)
    return None


def _flush_nuke() -> None:
    nuke = _state.get('nuke')
    if nuke:
        try:
            act = bs.get_foreground_host_activity()
            if act:
                with act.context:
                    nuke.destroy()
            else:
                nuke.destroy()
        except Exception:
            pass
    _cleanup_nuke()


def enable() -> None:
    from bascenev1._gameactivity import GameActivity
    orig_transition = GameActivity.on_transition_in
    def _patched_transition(self, *a, **k) -> None:
        _flush_nuke()
        orig_transition(self, *a, **k)
    GameActivity.on_transition_in = _patched_transition

    orig_end = GameActivity.end_game
    def _patched_end(self, *a, **k) -> None:
        _flush_nuke()
        orig_end(self, *a, **k)
    GameActivity.end_game = _patched_end

    print('[nuke] loaded')
