# ba_meta require api 9

from __future__ import annotations
import weakref
import bascenev1 as bs
import babase as ba
from bascenev1lib.actor.playerspaz import PlayerSpaz

_ACTIVE: dict = {}
_calls:  dict = {}

_REGISTRY: dict = {
    'cube':  None,
    'tesla': None,
}


def _load_effect(name: str):
    if name == 'cube':
        from plugins.effects.ancestral.cube import CubeAura
        return CubeAura
    if name == 'tesla':
        from plugins.effects.ancestral.tesla import TeslaAura
        return TeslaAura
    return None


def apply(acc: str, effect: str, spaz: PlayerSpaz) -> bool:
    cls = _load_effect(effect)
    if not cls:
        return False
    act = bs.get_foreground_host_activity()
    if not act:
        return False
    old = _ACTIVE.get(f'{acc}_{effect}')
    if old:
        try:
            old.destroy()
        except Exception:
            pass
    with act.context:
        _ACTIVE[f'{acc}_{effect}'] = cls(spaz)
    _ACTIVE[f'{acc}_{effect}_on'] = True
    return True


def remove(acc: str, effect: str) -> bool:
    old = _ACTIVE.pop(f'{acc}_{effect}', None)
    if old:
        try:
            old.destroy()
        except Exception:
            pass
    _ACTIVE[f'{acc}_{effect}_on'] = False
    return True


def is_active(acc: str, effect: str) -> bool:
    return bool(_ACTIVE.get(f'{acc}_{effect}_on'))


def find_spaz(act, acc: str) -> PlayerSpaz | None:
    for pl in act.players:
        try:
            if pl.sessionplayer.get_account_id() == acc:
                if hasattr(pl, 'actor') and pl.actor and pl.actor.node:
                    return pl.actor
        except Exception:
            pass
    return None


def apply_live(acc: str, effect: str) -> bool:
    act = bs.get_foreground_host_activity()
    if not act:
        return False
    spaz = find_spaz(act, acc)
    if not spaz:
        return False
    return apply(acc, effect, spaz)


def _new_spaz_init(self: PlayerSpaz, *a, **k) -> None:
    _calls['init'](self, *a, **k)
    try:
        acc = self._player.sessionplayer.get_account_id()
    except Exception:
        return
    try:
        from plugins.perms import perms as _p
        saved = _p.get_effects(acc)
        for effect in saved:
            _ACTIVE[f'{acc}_{effect}_on'] = True
    except Exception:
        pass
    for effect in _REGISTRY:
        if _ACTIVE.get(f'{acc}_{effect}_on'):
            ref = weakref.ref(self)
            def _do(ref=ref, acc=acc, effect=effect):
                spaz = ref()
                if not spaz or not spaz.node or not spaz.node.exists():
                    return
                act = bs.get_foreground_host_activity()
                if not act:
                    return
                apply(acc, effect, spaz)
            bs.timer(0.15, _do)


def _setup() -> None:
    _calls['init'] = PlayerSpaz.__init__
    PlayerSpaz.__init__ = _new_spaz_init

    def _flush_all() -> None:
        for key in list(_ACTIVE.keys()):
            if not key.endswith('_on'):
                val = _ACTIVE.get(key)
                if val is not None:
                    try:
                        val.destroy()
                    except Exception:
                        pass
                    _ACTIVE[key] = None

    orig_transition = bs.GameActivity.on_transition_in
    def _patched_transition(self, *a, **k) -> None:
        _flush_all()
        orig_transition(self, *a, **k)
    bs.GameActivity.on_transition_in = _patched_transition

    orig_begin = bs.GameActivity.on_begin
    def _patched_begin(self, *a, **k) -> None:
        _flush_all()
        orig_begin(self, *a, **k)
    bs.GameActivity.on_begin = _patched_begin

    orig_end = bs.GameActivity.end_game
    def _patched_end(self, *a, **k) -> None:
        _flush_all()
        orig_end(self, *a, **k)
    bs.GameActivity.end_game = _patched_end


def enable() -> None:
    _setup()
    print('[effects] loaded')
