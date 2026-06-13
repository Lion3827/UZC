from __future__ import annotations
import weakref
import math
import random
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.gameutils import SharedObjects

_PUNCH_TEXTS = ['THUNDER', 'SURGE', 'VOLT', 'ZAP', 'SHOCK', 'BURST']

_SLOT_COLS = [
    [(0.2,0.0,1.0),(0.4,0.0,1.0),(0.6,0.1,1.0),(0.9,0.2,1.0)],
    [(0.3,0.0,0.9),(0.5,0.0,1.0),(0.7,0.0,1.0),(1.0,0.3,1.0)],
    [(0.4,0.1,1.0),(0.6,0.0,0.9),(0.8,0.0,1.0),(1.0,0.4,0.9)],
]
_SEP     = 0.9
_FIXED_R = 0.30


class TargetHead:

    def __init__(self, owner_spaz: PlayerSpaz, rival_spaz: PlayerSpaz,
                 act, shared) -> None:
        self._rival_ref = weakref.ref(rival_spaz)
        self._timers: list = []
        self._act = act
        self._shared = shared
        self._alive = [True]
        self._slots: list = [[], [], []]
        self._lights: list = []
        self._px = [0.0, 0.0, 0.0]
        self._py = [0.0, 0.0, 0.0]
        self._pz = [0.0, 0.0, 0.0]
        self._vx = [0.0, 0.0, 0.0]
        self._vy = [0.0, 0.0, 0.0]
        self._vz = [0.0, 0.0, 0.0]
        self._phases = [0.0, 2.094, 4.188]
        self._cur_height = [1.5, 1.5, 1.5]
        self._spark_interval = [1.2]
        self._state = 0
        self._hook_rival_die(rival_spaz)
        with act.context:
            self._add_slot(0, rival_spaz.node.position)
        self._timers.append(bs.Timer(0.06, bs.WeakCallStrict(self._tick), repeat=True))
        self._timers.append(bs.Timer(1.2, bs.WeakCallStrict(self._do_spark)))

    def _add_slot(self, idx: int, pos: tuple) -> None:
        self._px[idx] = pos[0]
        self._py[idx] = pos[1] + self._cur_height[idx]
        self._pz[idx] = pos[2]
        p = (self._px[idx], self._py[idx], self._pz[idx])
        for c in _SLOT_COLS[idx]:
            s = bs.newnode('shield', attrs={'color': c, 'radius': _FIXED_R, 'position': p})
            self._slots[idx].append(s)
        l = bs.newnode('light', attrs={
            'color': (0.6, 0.0, 1.0), 'radius': 0.18, 'intensity': 0.5, 'position': p})
        self._lights.append(l)

    def _do_spark(self) -> None:
        if not self._alive[0]:
            return
        rival = self._rival_ref()
        if not rival or not rival.node or not rival.node.exists():
            return
        with self._act.context:
            for l in self._lights:
                if l.exists():
                    sp = l.position
                    bs.emitfx(position=sp,
                              velocity=(random.uniform(-0.8, 0.8),
                                        random.uniform(0.2, 1.2),
                                        random.uniform(-0.8, 0.8)),
                              count=2, scale=0.6, spread=0.15,
                              chunk_type='spark', emit_type='chunks')
        self._timers.append(bs.Timer(self._spark_interval[0], bs.WeakCallStrict(self._do_spark)))

    def _tick(self) -> None:
        if not self._alive[0]:
            return
        rival = self._rival_ref()
        if not rival or not rival.node or not rival.node.exists():
            if self._state < 1:
                self._state = 1
                self._trigger_lightning()
            return
        p = rival.node.position
        ratio = rival.hitpoints / max(rival.hitpoints_max, 1)
        dmg = 1.0 - ratio
        self._spark_interval[0] = max(0.08, 1.2 - dmg * 1.12)
        if dmg > 0.4 and len(self._lights) < 2:
            with self._act.context:
                self._add_slot(1, p)
        if dmg > 0.7 and len(self._lights) < 3:
            with self._act.context:
                self._add_slot(2, p)
        chaos = dmg * dmg
        sep = dmg * _SEP
        t = bs.time()
        for idx in range(len(self._lights)):
            th = 1.5 + dmg * 2.8
            self._cur_height[idx] += (th - self._cur_height[idx]) * 0.05
            wave = (math.sin(t * 1.2 + self._phases[idx]) * 0.18 +
                    math.sin(t * 2.3 + self._phases[idx] * 1.7) * 0.10)
            tx = p[0] + math.cos(self._phases[idx]) * sep + math.sin(t * 1.1 + self._phases[idx]) * 0.10
            ty = p[1] + self._cur_height[idx] + wave
            tz = p[2] + math.sin(self._phases[idx]) * sep + math.cos(t * 1.3 + self._phases[idx]) * 0.10
            kick = 0.018 + chaos * 0.06
            self._vx[idx] += (tx - self._px[idx]) * 0.14 + random.uniform(-kick, kick)
            self._vy[idx] += (ty - self._py[idx]) * 0.14 + random.uniform(-kick * 0.3, kick * 0.3)
            self._vz[idx] += (tz - self._pz[idx]) * 0.14 + random.uniform(-kick, kick)
            damp = 0.86 - chaos * 0.24
            self._vx[idx] *= damp
            self._vy[idx] *= damp
            self._vz[idx] *= damp
            self._px[idx] += self._vx[idx]
            self._py[idx] += self._vy[idx]
            self._pz[idx] += self._vz[idx]
            np2 = (self._px[idx], self._py[idx], self._pz[idx])
            for s in self._slots[idx]:
                if s.exists():
                    s.position = np2
            if idx < len(self._lights) and self._lights[idx].exists():
                self._lights[idx].position = np2
                self._lights[idx].intensity = (0.4 + math.sin(t * 4 + idx * 1.3) * 0.3 + chaos * 0.5)

    def _hook_rival_die(self, rival: PlayerSpaz) -> None:
        orig = rival.handlemessage
        ref = weakref.ref(self)

        def _hm(msg, orig=orig, ref=ref):
            th = ref()
            if th and isinstance(msg, bs.DieMessage) and th._alive[0]:
                th._alive[0] = False
                th._trigger_lightning()
            return orig(msg)

        rival.handlemessage = _hm

    def _trigger_lightning(self) -> None:
        rival = self._rival_ref()
        if not rival or not rival.node:
            self._cleanup_slots()
            return
        p = rival.node.position
        sky = (p[0], p[1] + 9.0, p[2])
        with self._act.context:
            bolt = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (0.8, 0.3, 1.0), 'opacity': 0.0,
                'size': [0.14], 'additive': True, 'draw_beauty': True,
                'position': (sky[0], sky[1] - j * 0.45, sky[2]),
            }) for j in range(20)]
            [bs.animate(bolt[j], 'opacity', {
                j * 0.016: 0.0, j * 0.016 + 0.05: 1.0,
                j * 0.016 + 0.14: 1.0, j * 0.016 + 0.25: 0.0,
            }) for j in range(20)]
            lray = bs.newnode('light', attrs={
                'color': (0.7, 0.1, 1.0), 'radius': 0.0,
                'intensity': 0.0, 'position': sky,
            })
            bs.animate(lray, 'radius',    {0.0: 0.0, 0.2: 5.0, 0.7: 0.0})
            bs.animate(lray, 'intensity', {0.0: 0.0, 0.2: 12.0, 0.7: 0.0})
            from bascenev1lib.actor.spazfactory import SpazFactory
            sf = SpazFactory.get()
            snd = sf.impact_sounds_harder[random.randrange(len(sf.impact_sounds_harder))]
            snd.play(4.0, position=p)
            sf.shield_down_sound.play(1.5, position=p)
        bs.camerashake(8.0)
        self._timers.append(bs.Timer(0.08, lambda: bs.camerashake(5.0)))
        self._timers.append(bs.Timer(0.18, lambda: bs.camerashake(3.0)))
        self._timers.append(bs.Timer(0.18, bs.WeakCallStrict(self._explode, p)))
        self._timers.append(bs.Timer(0.55, lambda nodes=bolt: [
            n.delete() for n in nodes if n.exists()]))
        self._timers.append(bs.Timer(1.8, lambda: lray.delete() if lray.exists() else None))

    def _explode(self, pos: tuple) -> None:
        ep = pos
        rival = self._rival_ref()
        if rival and rival.node and rival.node.exists():
            ep = rival.node.position
        with self._act.context:
            bs.emitfx(position=ep, velocity=(0, 6, 0), count=30,
                      scale=2.2, spread=0.7, chunk_type='spark', emit_type='chunks')
            bs.emitfx(position=ep, velocity=(0, 2, 0), count=12,
                      scale=2.5, spread=1.2, emit_type='tendrils', tendril_type='smoke')
            exsh = [bs.newnode('shield', attrs={'color': c, 'radius': 0.0, 'position': ep})
                    for c in [(0.2,0.0,1.0),(0.4,0.0,1.0),(0.7,0.0,1.0),(1.0,0.2,1.0),(1.0,0.5,0.8)]]
            [bs.animate(exsh[i], 'radius', {
                i * 0.07: 0.0,
                i * 0.07 + 0.18: 3.8 - i * 0.5,
                i * 0.07 + 1.5: 0.0,
            }) for i in range(5)]
            el = bs.newnode('light', attrs={
                'color': (0.6, 0.1, 1.0), 'radius': 0.0,
                'intensity': 0.0, 'position': ep,
            })
            bs.animate(el, 'radius',    {0.0: 0.0, 0.1: 7.0, 1.0: 0.0})
            bs.animate(el, 'intensity', {0.0: 0.0, 0.1: 14.0, 1.0: 0.0})
        bs.camerashake(9.0)
        self._timers.append(bs.Timer(0.08, lambda: bs.camerashake(6.0)))
        self._timers.append(bs.Timer(0.18, lambda: bs.camerashake(4.0)))
        self._timers.append(bs.Timer(0.32, lambda: bs.camerashake(2.0)))
        self._cleanup_slots()
        self._timers.append(bs.Timer(1.8, lambda: [s.delete() for s in exsh if s.exists()]))
        self._timers.append(bs.Timer(1.8, lambda: el.delete() if el.exists() else None))

    def _cleanup_slots(self) -> None:
        for sl in self._slots:
            for s in sl:
                try:
                    if s.exists():
                        bs.animate(s, 'radius', {0.0: s.radius, 0.3: 0.0})
                except Exception:
                    pass
        self._timers.append(bs.Timer(0.35, lambda: [
            s.delete() for sl in self._slots for s in sl if s.exists()]))
        self._timers.append(bs.Timer(0.35, lambda: [
            l.delete() for l in self._lights if l.exists()]))

    def is_dead(self) -> bool:
        return not self._alive[0] and self._state >= 1

    def destroy(self) -> None:
        self._timers.clear()
        for sl in self._slots:
            for s in sl:
                try:
                    if s.exists():
                        s.delete()
                except Exception:
                    pass
        for l in self._lights:
            try:
                if l.exists():
                    l.delete()
            except Exception:
                pass


class TeslaAura:

    def __init__(self, spaz: PlayerSpaz) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._ref      = weakref.ref(spaz)
        self._nodes: list  = []
        self._timers: list = []
        self._targets: dict = {}
        self._alive    = [True]
        self._last_pos = [spaz.node.position]
        self._my_player = spaz._player
        self._death_timer = None
        self._firefly_timers: list = []
        self._tsh: list = []
        self._tl = None
        self._tcp = [list(spaz.node.position)]
        self._tcv = [0.0, 0.0, 0.0]
        self._tfa = [0.0]
        self._tti = [0.0]
        self._seal: list = []
        self._mat = bs.Material()
        self._mat.add_actions(actions=('modify_part_collision', 'collide', False))
        self._timers.append(bs.Timer(0.2, bs.WeakCallStrict(self._tick_targets), repeat=True))
        self._hook_messages(spaz)
        self._spawn_effect(spaz)

    def _tick_targets(self) -> None:
        spaz = self._ref()
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        act = bs.get_foreground_host_activity()
        if not act:
            return
        shared = SharedObjects.get()
        dead = [k for k, th in self._targets.items() if th.is_dead()]
        for k in dead:
            del self._targets[k]
        for p in act.players:
            try:
                rival = p.actor
                if not rival or not rival.node or not rival.node.exists():
                    continue
                if rival is spaz:
                    continue
                if rival.last_player_attacked_by is not self._my_player:
                    continue
                rid = id(rival)
                if rid not in self._targets:
                    with act.context:
                        self._targets[rid] = TargetHead(spaz, rival, act, shared)
            except Exception:
                pass

    def _hook_messages(self, spaz: PlayerSpaz) -> None:
        from bascenev1lib.actor.spaz import PunchHitMessage
        orig_hm = spaz.handlemessage
        ref = weakref.ref(self)

        def _hm(msg, orig=orig_hm, ref=ref, spaz=spaz):
            aura = ref()
            if aura:
                if isinstance(msg, bs.DieMessage):
                    if aura._alive[0]:
                        aura._alive[0] = False
                        pos = aura._last_pos[0]
                        for th in list(aura._targets.values()):
                            try: th.destroy()
                            except Exception: pass
                        aura._targets.clear()
                        aura._timers.clear()
                        act = bs.get_foreground_host_activity()
                        if act:
                            with act.context:
                                aura._death_effect(pos)
                        else:
                            aura._death_effect(pos)
                elif isinstance(msg, PunchHitMessage):
                    if aura._alive[0]:
                        epos = spaz.node.punch_position if (spaz.node and spaz.node.exists()) else None
                        if epos:
                            act = bs.get_foreground_host_activity()
                            if act:
                                with act.context:
                                    aura._punch_effect(epos)
            return orig(msg)

        spaz.handlemessage = _hm

    def _punch_effect(self, epos: tuple) -> None:
        bs.emitfx(position=epos, velocity=(0, 2, 0),
                  count=4, scale=0.6, spread=0.3,
                  chunk_type='spark', emit_type='chunks')
        bs.emitfx(position=epos, velocity=(0, 1, 0),
                  count=2, scale=0.9, spread=0.4,
                  emit_type='tendrils', tendril_type='smoke')
        txt = random.choice(_PUNCH_TEXTS)
        bs.show_damage_count(txt, epos, (0.6, 0.2, 1.0))

    def _death_effect(self, pos: tuple) -> None:
        p = (pos[0], pos[1] + 0.2, pos[2])
        cols = [(0.05, 0.2, 1.0), (0.3, 0.0, 1.0), (0.6, 0.0, 0.85),
                (0.9, 0.0, 0.6), (1.0, 0.2, 0.1), (1.0, 0.7, 0.0)]
        shields = [bs.newnode('shield', attrs={'color': c, 'radius': 0.0, 'position': p})
                   for c in cols]
        light = bs.newnode('light', attrs={
            'color': (0.5, 0.1, 1.0), 'radius': 0.0, 'intensity': 0.0, 'position': p})
        [bs.animate(shields[i], 'radius',
                    {i * 0.14: 0.0, i * 0.14 + 0.22: 5.5 - i * 0.6, i * 0.14 + 1.8: 0.0})
         for i in range(6)]
        bs.animate(light, 'radius',    {0.0: 0.0, 0.15: 6.0, 0.8: 1.5, 2.2: 0.0})
        bs.animate(light, 'intensity', {0.0: 0.0, 0.15: 12.0, 0.8: 4.0, 2.2: 0.0})
        bs.camerashake(7.0)
        self._timers.append(bs.Timer(0.15, lambda: bs.camerashake(4.0)))
        self._timers.append(bs.Timer(0.3,  lambda: bs.camerashake(2.5)))
        t = [bs.Timer(0.05, lambda: bs.emitfx(
            position=p,
            velocity=(random.uniform(-6, 6), random.uniform(1, 8), random.uniform(-6, 6)),
            count=2, scale=1.8, spread=0.3, chunk_type='spark', emit_type='chunks'),
            repeat=True)]
        self._timers.append(bs.Timer(1.2, lambda: t.clear()))
        self._timers.append(bs.Timer(2.5, lambda: [s.delete() for s in shields if s.exists()]))
        self._timers.append(bs.Timer(2.5, lambda: light.delete() if light.exists() else None))
        if self._tsh:
            for s in self._tsh:
                try:
                    bs.animate(s, 'radius', {0.0: s.radius, 0.4: 0.0})
                except Exception:
                    pass
            self._timers.append(bs.Timer(0.5, lambda: [s.delete() for s in self._tsh if s.exists()]))
        if self._tl:
            try:
                bs.animate(self._tl, 'intensity', {0.0: self._tl.intensity, 0.4: 0.0})
                self._timers.append(bs.Timer(0.45, lambda: self._tl.delete() if self._tl.exists() else None))
            except Exception:
                pass

    def _spawn_effect(self, spaz: PlayerSpaz) -> None:
        pos = spaz.node.position
        self._timers.append(bs.Timer(0.0, bs.WeakCallStrict(self._fase_sello, pos)))
        self._timers.append(bs.Timer(0.0, bs.WeakCallStrict(self._fase_esfera_baja, pos)))
        self._timers.append(bs.Timer(2.2, bs.WeakCallStrict(self._fase_idle)))

    def _fase_sello(self, pos: tuple) -> None:
        act = bs.get_foreground_host_activity()
        if not act:
            return
        ry = pos[1] - 0.88
        nodes = []
        with act.context:
            c1 = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (0.1, 0.3, 1.0), 'opacity': 0.0,
                'size': [0.06], 'additive': True, 'draw_beauty': True,
                'position': (pos[0] + math.cos(i * 2 * math.pi / 120) * 1.5,
                             ry, pos[2] + math.sin(i * 2 * math.pi / 120) * 1.5)
            }) for i in range(120)]
            c2 = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (0.4, 0.1, 1.0), 'opacity': 0.0,
                'size': [0.05], 'additive': True, 'draw_beauty': True,
                'position': (pos[0] + math.cos(i * 2 * math.pi / 80) * 1.0,
                             ry, pos[2] + math.sin(i * 2 * math.pi / 80) * 1.0)
            }) for i in range(80)]
            c3 = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (0.8, 0.2, 1.0), 'opacity': 0.0,
                'size': [0.04], 'additive': True, 'draw_beauty': True,
                'position': (pos[0] + math.cos(i * 2 * math.pi / 40) * 0.5,
                             ry, pos[2] + math.sin(i * 2 * math.pi / 40) * 0.5)
            }) for i in range(40)]
            spokes = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (0.3, 0.5, 1.0), 'opacity': 0.0,
                'size': [0.045], 'additive': True, 'draw_beauty': True,
                'position': (pos[0] + math.cos(s * 2 * math.pi / 6) * (j / 40.0) * 1.5,
                             ry, pos[2] + math.sin(s * 2 * math.pi / 6) * (j / 40.0) * 1.5)
            }) for s in range(6) for j in range(1, 40)]
            runes = [bs.newnode('locator', attrs={
                'shape': 'circle', 'color': (1.0, 0.5, 1.0), 'opacity': 0.0,
                'size': [0.07], 'additive': True, 'draw_beauty': True,
                'position': (pos[0] + math.cos(k * 2 * math.pi / 6) * 1.2,
                             ry, pos[2] + math.sin(k * 2 * math.pi / 6) * 1.2)
            }) for k in range(6)]
            nodes = c1 + c2 + c3 + spokes + runes
        self._seal = nodes
        for i, n in enumerate(c1 + c2 + c3):
            bs.animate(n, 'opacity', {i * 0.002: 0.0, i * 0.002 + 0.08: 0.95})
        for i, n in enumerate(spokes):
            bs.animate(n, 'opacity', {i * 0.004: 0.0, i * 0.004 + 0.06: 1.0})
        for k, n in enumerate(runes):
            bs.animate(n, 'opacity', {k * 0.08: 0.0, k * 0.08 + 0.12: 1.0})
        draw_end = max((len(c1 + c2 + c3) - 1) * 0.002 + 0.08,
                       (len(spokes) - 1) * 0.004 + 0.06)
        hold = 1.2
        fade = 0.8

        def _fade_all(nodes=nodes):
            for n in nodes:
                try:
                    if n.exists():
                        bs.animate(n, 'opacity', {0.0: n.opacity, fade: 0.0})
                except Exception:
                    pass

        def _kill_all(nodes=nodes):
            for n in nodes:
                try:
                    if n.exists():
                        n.delete()
                except Exception:
                    pass
            self._seal.clear()

        self._timers.append(bs.Timer(draw_end + hold, _fade_all))
        self._timers.append(bs.Timer(draw_end + hold + fade + 0.1, _kill_all))
        bs.emitfx(position=(pos[0], pos[1] + 0.1, pos[2]),
                  velocity=(0, 0, 0), count=8, scale=1.5, spread=1.2,
                  chunk_type='spark', emit_type='chunks')

    def _fase_esfera_baja(self, pos: tuple) -> None:
        act = bs.get_foreground_host_activity()
        if not act:
            return
        sky_pos = (pos[0], pos[1] + 8.0, pos[2])
        cols = [(0.8, 0.1, 1.0), (0.55, 0.0, 1.0), (1.0, 0.2, 0.9), (0.4, 0.0, 0.8)]
        with act.context:
            self._tsh = [bs.newnode('shield', attrs={
                'color': c, 'radius': 0.0, 'position': sky_pos
            }) for c in cols]
            self._tl = bs.newnode('light', attrs={
                'color': (0.7, 0.0, 1.0), 'radius': 0.0,
                'intensity': 0.0, 'position': sky_pos
            })
        [bs.animate(s, 'radius', {0.0: 0.0, 0.3: 0.32 + i * 0.09})
         for i, s in enumerate(self._tsh)]
        bs.animate(self._tl, 'radius',    {0.0: 0.0, 0.3: 0.22})
        bs.animate(self._tl, 'intensity', {0.0: 0.0, 0.3: 0.35})
        prog = [0.0]
        idle_started = [False]
        tsh = self._tsh
        tl  = self._tl
        ref = weakref.ref(self)

        def _descend(prog=prog, idle_started=idle_started,
                     tsh=tsh, tl=tl, sky=sky_pos, ref=ref):
            aura = ref()
            if not aura or not aura._alive[0]:
                return
            spaz = aura._ref()
            if not spaz or not spaz.node or not spaz.node.exists():
                return
            prog[0] += 0.04
            t = min(prog[0], 1.0)
            ease = t * t * (3 - 2 * t)
            spos = spaz.node.position
            dst = (spos[0] + 0.55, spos[1] + 0.85, spos[2])
            p = (
                sky[0] + (dst[0] - sky[0]) * ease,
                sky[1] + (dst[1] - sky[1]) * ease,
                sky[2] + (dst[2] - sky[2]) * ease,
            )
            for s in tsh:
                if s.exists():
                    s.position = p
            if tl.exists():
                tl.position = p
            if prog[0] >= 1.0 and not idle_started[0]:
                idle_started[0] = True
                aura._tcp = [list(p)]
                aura._timers.append(bs.Timer(0.06, bs.WeakCallStrict(aura._tick_idle), repeat=True))

        self._timers.append(bs.Timer(0.03, _descend, repeat=True))

    def _fase_idle(self) -> None:
        pass

    def _limpiar_sello(self) -> None:
        for n in self._seal:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._seal.clear()

    def _tick_idle(self) -> None:
        spaz = self._ref()
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        if not self._alive[0]:
            return
        self._last_pos[0] = spaz.node.position
        self._tti[0] += 0.04
        t = self._tti[0]
        bob = math.sin(t * 1.8) * 0.06
        pos = spaz.node.position
        vel = spaz.node.velocity
        spd = (vel[0] ** 2 + vel[2] ** 2) ** 0.5
        if spd > 0.5:
            ta = math.atan2(vel[2], vel[0])
            fa = self._tfa[0]
            diff = math.atan2(math.sin(ta - fa), math.cos(ta - fa))
            self._tfa[0] += diff * 0.04
        fa = self._tfa[0]
        tx = pos[0] + math.cos(fa + 1.57) * 0.55
        ty = pos[1] + 0.85 + bob
        tz = pos[2] + math.sin(fa + 1.57) * 0.55
        cp = self._tcp[0]
        cv = self._tcv
        cv[0] += (tx - cp[0]) * 0.10
        cv[1] += (ty - cp[1]) * 0.10
        cv[2] += (tz - cp[2]) * 0.10
        cv[0] *= 0.80
        cv[1] *= 0.80
        cv[2] *= 0.80
        cp[0] += cv[0]
        cp[1] += cv[1]
        cp[2] += cv[2]
        p2 = (cp[0], cp[1], cp[2])
        for s in self._tsh:
            try:
                if s.exists():
                    s.position = p2
            except Exception:
                pass
        if self._tl and self._tl.exists():
            self._tl.position  = p2
            self._tl.intensity = 0.35 + min(spd / 8.0, 1.0) * 0.9
        sc  = 0.25 + min(spd / 6.0, 1.0) * 0.35
        vsc = 0.6  + min(spd / 5.0, 1.0) * 0.8
        cnt = 2 if spd > 1.5 else 1
        bs.emitfx(
            position=p2,
            velocity=(random.uniform(-vsc, vsc),
                      random.uniform(-vsc, vsc),
                      random.uniform(-vsc, vsc)),
            count=cnt, scale=sc, spread=0.15,
            chunk_type='spark', emit_type='chunks'
        )

    def destroy(self) -> None:
        self._timers.clear()
        self._death_timer = None
        self._firefly_timers.clear()
        self._alive[0] = False
        for th in self._targets.values():
            try:
                th.destroy()
            except Exception:
                pass
        self._targets.clear()
        for n in self._seal:
            try:
                if hasattr(n, 'exists') and n.exists():
                    n.delete()
            except Exception:
                pass
        self._seal.clear()
        for s in self._tsh:
            try:
                if s.exists():
                    s.delete()
            except Exception:
                pass
        self._tsh.clear()
        if self._tl:
            try:
                if self._tl.exists():
                    self._tl.delete()
            except Exception:
                pass
        self._tl = None
        for n in self._nodes:
            try:
                if hasattr(n, 'exists') and n.exists():
                    n.delete()
            except Exception:
                pass
        self._nodes.clear()
