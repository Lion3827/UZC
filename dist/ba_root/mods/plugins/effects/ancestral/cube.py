from __future__ import annotations
import weakref
import math
import random
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.gameutils import SharedObjects

_CUBE_CONFIGS = (
    (0.75, 0,           0.5,  1),
    (0.75, 2.094395,    0.5,  1),
    (0.75, 4.188790,    0.5,  1),
    (0.65, 1.047197,    1.1,  1),
    (0.65, 3.141592,    1.1,  1),
    (0.65, 5.235987,    1.1,  1),
    (0.50, 0,           1.7, -1),
    (0.50, 2.094395,    1.7, -1),
    (0.50, 4.188790,    1.7, -1),
)


class TargetCube:

    def __init__(self, owner_spaz: PlayerSpaz, rival_spaz: PlayerSpaz,
                 act, shared) -> None:
        self._rival_ref = weakref.ref(rival_spaz)
        self._timers: list = []
        self._firefly_timers: list = []
        self._state = 0
        self._cur_scale = [0.08]
        self._cur_height = [1.5]
        self._prev_vy = [0.0]

        no_col = bs.Material()
        no_col.add_actions(actions=('modify_part_collision', 'collide', False))
        self._no_col = no_col

        src = tuple(owner_spaz.node.position)
        dst_base = rival_spaz.node.position
        self._dst = (dst_base[0], dst_base[1] + 1.5, dst_base[2])
        self._prog = [0.0]

        with act.context:
            self._cube = bs.newnode('prop', attrs={
                'mesh':          bs.getmesh('box'),
                'body':          'box',
                'color_texture': bs.gettexture('black'),
                'position':      src,
                'gravity_scale': 4.0,
                'mesh_scale':    0.08,
                'shadow_size':   0.0,
                'materials':     [no_col],
                'velocity':      (0, 0, 0),
            })
            self._light = bs.newnode('light', attrs={
                'color':     (0.6, 0.0, 1.0),
                'radius':    0.08,
                'position':  src,
            })

        self._shared = shared
        self._act = act
        self._src = src

        self._hook_rival_die(rival_spaz)
        self._timers.append(bs.Timer(0.03, bs.WeakCallStrict(self._tick), repeat=True))

    def _hook_rival_die(self, rival: PlayerSpaz) -> None:
        orig = rival.handlemessage
        ref = weakref.ref(self)

        def _hm(msg, orig=orig, ref=ref):
            tc = ref()
            if tc and isinstance(msg, bs.DieMessage) and tc._state < 2:
                tc._state = 2
            return orig(msg)

        rival.handlemessage = _hm

    def _tick(self) -> None:
        if not self._cube.exists():
            self._state = 4
            return
        if self._state == 4:
            return
        if self._state == 3:
            vy = self._cube.velocity[1]
            if self._prev_vy[0] < -5.0 and vy > -1.0:
                self._state = 4
                self._on_impact()
            self._prev_vy[0] = vy
            if self._light.exists():
                self._light.position = self._cube.position
            return
        if self._state == 2:
            self._state = 3
            with self._act.context:
                if self._light.exists():
                    bs.animate(self._light, 'intensity',
                               {0.0: 0.5, 0.1: 3.0, 0.2: 0.8,
                                0.3: 3.0, 0.4: 0.8, 0.5: 3.0, 0.6: 0.8})
                if self._cube.exists():
                    bs.animate(self._cube, 'mesh_scale', {
                        0.0: self._cur_scale[0],
                        0.15: self._cur_scale[0] * 1.8,
                        0.35: self._cur_scale[0],
                    })
            return
        if self._state == 0:
            self._prog[0] += 0.06
            t = min(self._prog[0], 1.0)
            ease = t * t * (3 - 2 * t)
            p = (
                self._src[0] + (self._dst[0] - self._src[0]) * ease,
                self._src[1] + (self._dst[1] - self._src[1]) * ease,
                self._src[2] + (self._dst[2] - self._src[2]) * ease,
            )
            self._cube.position = p
            self._cube.velocity = (0, 0, 0)
            self._light.position = p
            if self._prog[0] >= 1.0:
                self._state = 1
                self._cube.materials = [self._shared.object_material]
            return
        if self._state == 1:
            rival = self._rival_ref()
            if not rival or not rival.node or not rival.node.exists():
                self._state = 2
                return
            pos = rival.node.position
            ratio = rival.hitpoints / max(rival.hitpoints_max, 1)
            dmg = 1.0 - ratio
            target_scale = 0.08 + dmg * 1.4
            target_height = 1.5 + dmg * 2.5
            self._cur_scale[0] += (target_scale - self._cur_scale[0]) * 0.08
            self._cur_height[0] += (target_height - self._cur_height[0]) * 0.08
            gpos = (pos[0], pos[1] + self._cur_height[0], pos[2])
            self._cube.position = gpos
            self._cube.velocity = (0, 0, 0)
            self._light.position = gpos
            self._cube.mesh_scale = self._cur_scale[0]
            self._light.radius = self._cur_scale[0] * 0.08

    def _on_impact(self) -> None:
        if not self._cube.exists():
            return
        pos = self._cube.position
        with self._act.context:
            from bascenev1lib.actor.spazfactory import SpazFactory
            sf = SpazFactory.get()
            s = sf.impact_sounds_harder[random.randrange(len(sf.impact_sounds_harder))]
            s.play(3.0, position=pos)
            bs.camerashake(6.0)
            self._spawn_fireflies(pos)
            bs.animate(self._cube, 'mesh_scale', {
                0.0: self._cur_scale[0],
                0.2: self._cur_scale[0] * 1.4,
                0.8: 0.0,
            })
            bs.Timer(0.9, lambda: self._cube.delete() if self._cube.exists() else None)
            bs.Timer(0.9, lambda: self._light.delete() if self._light.exists() else None)

    def _spawn_fireflies(self, pos: tuple) -> None:
        timers = []
        for _ in range(35):
            spd = random.uniform(0.2, 0.6)
            dst = (
                pos[0] + random.uniform(-5.0, 5.0),
                pos[1] + random.uniform(0.3, 5.0),
                pos[2] + random.uniform(-5.0, 5.0),
            )
            color = (random.uniform(0.4, 1.0), 0.0, random.uniform(0.6, 1.0))
            n1 = bs.newnode('locator', attrs={
                'shape': 'circle', 'position': pos, 'color': color,
                'opacity': 0.9, 'draw_beauty': True, 'additive': False, 'size': [0.02],
            })
            l = bs.newnode('light', attrs={'color': (0.6, 0.0, 1.0), 'radius': 0.03, 'intensity': 0.8})
            n1.connectattr('position', l, 'position')
            bs.animate_array(n1, 'position', 3, {0.0: pos, spd: dst})
            bs.animate(n1, 'opacity', {0.0: 0.9, spd: 0.9, spd + 0.4: 0.0})
            timers.append(bs.Timer(spd + 0.45, n1.delete))
            timers.append(bs.Timer(spd + 0.45, l.delete))
        self._firefly_timers = timers

    def is_dead(self) -> bool:
        return self._state == 4 or not self._cube.exists()

    def destroy(self) -> None:
        self._timers.clear()
        self._firefly_timers.clear()
        try:
            if self._cube.exists():
                self._cube.delete()
        except Exception:
            pass
        try:
            if self._light.exists():
                self._light.delete()
        except Exception:
            pass


class CubeAura:

    def __init__(self, spaz: PlayerSpaz) -> None:
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._ref    = weakref.ref(spaz)
        self._nodes: list  = []
        self._timers: list = []
        self._cubes: list  = []
        self._lights: list = []
        self._sello: list  = []
        self._angle  = [0.0]
        self._mat    = bs.Material()
        self._mat.add_actions(actions=('modify_part_collision', 'collide', False))
        self._nodes.append(self._mat)
        self._alive = [True]
        self._last_pos = [spaz.node.position]
        self._death_timer = None
        self._firefly_timers: list = []
        self._busy_cubes: set = set()
        self._targets: dict = {}
        self._my_player = spaz._player
        self._timers.append(bs.Timer(0.03, bs.WeakCallStrict(self._tick), repeat=True))
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
        dead = [k for k, tc in self._targets.items() if tc.is_dead()]
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
                        tc = TargetCube(spaz, rival, act, shared)
                    self._targets[rid] = tc
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
                        for tc in list(aura._targets.values()):
                            try: tc.destroy()
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
                    if aura._alive[0] and aura._cubes:
                        epos = spaz.node.punch_position if (spaz.node and spaz.node.exists()) else None
                        if epos:
                            dists = []
                            for i, c in enumerate(aura._cubes):
                                if c.exists() and i not in aura._busy_cubes:
                                    d = ((c.position[0] - epos[0]) ** 2 +
                                         (c.position[2] - epos[2]) ** 2)
                                    dists.append((d, i))
                            if dists:
                                idx = min(dists)[1]
                                act = bs.get_foreground_host_activity()
                                if act:
                                    with act.context:
                                        aura._punch_effect(idx, epos)
            return orig(msg)

        spaz.handlemessage = _hm

    def _punch_effect(self, idx: int, epos: tuple) -> None:
        cube = self._cubes[idx]
        light = self._lights[idx] if idx < len(self._lights) else None
        if not cube.exists():
            return
        self._busy_cubes.add(idx)
        start = tuple(cube.position)
        hit = (
            start[0] + (epos[0] - start[0]) * 0.55,
            start[1] + (epos[1] - start[1]) * 0.55,
            start[2] + (epos[2] - start[2]) * 0.55,
        )
        prog = [0.0]
        done = [False]

        def tick(prog=prog, done=done, cube=cube, light=light,
                 start=start, hit=hit, idx=idx):
            if done[0]:
                return
            if not cube.exists():
                self._busy_cubes.discard(idx)
                done[0] = True
                return
            prog[0] += 0.18
            t = min(prog[0], 1.0)
            ease = t * t
            pos = (
                start[0] + (hit[0] - start[0]) * ease,
                start[1] + (hit[1] - start[1]) * ease,
                start[2] + (hit[2] - start[2]) * ease,
            )
            cube.position = pos
            if light and light.exists():
                light.position = pos
            if prog[0] >= 1.0:
                done[0] = True
                self._busy_cubes.discard(idx)

        self._timers.append(bs.Timer(0.03, tick, repeat=True))

    def _death_effect(self, pos: tuple) -> None:
        cubes = list(self._cubes)
        lights = list(self._lights)
        start_pos = []
        for c in cubes:
            try:
                start_pos.append(c.position if c.exists() else pos)
            except Exception:
                start_pos.append(pos)

        prog = [0.0]
        done = [False]

        def tick(prog=prog, done=done, cubes=cubes, lights=lights,
                 start_pos=start_pos, pos=pos):
            if done[0]:
                return
            if not any(c.exists() for c in cubes if hasattr(c, 'exists')):
                done[0] = True
                return
            prog[0] += 0.05
            t    = min(prog[0], 1.0)
            ease = t * t
            for i, c in enumerate(cubes):
                try:
                    if not c.exists():
                        continue
                    sp2 = start_pos[i]
                    c.position = (
                        sp2[0] + (pos[0] - sp2[0]) * ease,
                        sp2[1] + (pos[1] - sp2[1]) * ease,
                        sp2[2] + (pos[2] - sp2[2]) * ease,
                    )
                    c.mesh_scale = 0.08 * (1 - ease)
                    if i < len(lights) and lights[i].exists():
                        lights[i].position = c.position
                        lights[i].intensity = (1 - ease) * 0.6
                except Exception:
                    pass
            if prog[0] >= 1.0:
                done[0] = True
                bs.camerashake(5.0)
                bs.Timer(0.1, lambda: bs.camerashake(3.0))
                bs.Timer(0.2, lambda: bs.camerashake(2.0))
                self._spawn_fireflies(pos)
                for c in cubes:
                    try:
                        if c.exists():
                            c.delete()
                    except Exception:
                        pass
                for lgt in lights:
                    try:
                        if lgt.exists():
                            lgt.delete()
                    except Exception:
                        pass

        self._death_timer = bs.Timer(0.03, tick, repeat=True)

    def _spawn_fireflies(self, pos: tuple) -> None:
        timers = []
        for _ in range(35):
            spd = random.uniform(0.15, 0.45)
            dst = (
                pos[0] + random.uniform(-4.0, 4.0),
                pos[1] + random.uniform(0.5, 4.0),
                pos[2] + random.uniform(-4.0, 4.0),
            )
            color = (random.uniform(0.4, 1.0), 0.0, random.uniform(0.6, 1.0))
            n1 = bs.newnode('locator', attrs={
                'shape': 'circle', 'position': pos, 'color': color,
                'opacity': 0.9, 'draw_beauty': True, 'additive': False, 'size': [0.015],
            })
            n2 = bs.newnode('locator', attrs={
                'shape': 'box', 'position': pos, 'color': color,
                'opacity': 0.9, 'draw_beauty': True, 'additive': False, 'size': [0.015],
            })
            l = bs.newnode('light', attrs={'color': (0.6, 0.0, 1.0), 'radius': 0.02, 'intensity': 0.5})
            n1.connectattr('position', l, 'position')
            bs.animate_array(n1, 'position', 3, {0.0: pos, spd: dst})
            bs.animate_array(n2, 'position', 3, {0.0: pos, spd: dst})
            bs.animate(n1, 'opacity', {0.0: 0.9, spd: 0.9, spd + 0.3: 0.0})
            bs.animate(n2, 'opacity', {0.0: 0.9, spd: 0.9, spd + 0.3: 0.0})
            timers.append(bs.Timer(spd + 0.35, n1.delete))
            timers.append(bs.Timer(spd + 0.35, n2.delete))
            timers.append(bs.Timer(spd + 0.35, l.delete))
        self._firefly_timers = timers

    def _spawn_effect(self, spaz: PlayerSpaz) -> None:
        self._timers.append(bs.Timer(0.0, bs.WeakCallStrict(self._fase_sello, spaz.node.position)))
        self._timers.append(bs.Timer(0.8, bs.WeakCallStrict(self._fase_cubos)))
        self._timers.append(bs.Timer(2.8, bs.WeakCallStrict(self._fase_idle)))

    def _fase_sello(self, pos: tuple) -> None:
        nodes = self._sello

        def mk(i: int, nodes: list = nodes) -> None:
            for idx in (i, i + 6):
                a = idx * 2 * math.pi / 12
                n = bs.newnode('locator', attrs={
                    'shape': 'circle', 'color': (0.2, 0.5, 1.0),
                    'opacity': 0.0, 'size': (0.12, 0.12, 0.12),
                    'additive': True,
                    'position': (
                        pos[0] + math.cos(a) * 1.5,
                        pos[1] - 0.9,
                        pos[2] + math.sin(a) * 1.5,
                    ),
                })
                bs.animate(n, 'opacity', {0.0: 0.0, 0.3: 0.9})
                nodes.append(n)

        for j in range(6):
            self._timers.append(bs.Timer(j * 0.12, lambda j=j: mk(j)))

    def _fase_cubos(self) -> None:
        def mk(i: int) -> None:
            spaz = self._ref()
            if not spaz or not spaz.node or not spaz.node.exists():
                return
            pos = spaz.node.position
            c   = _CUBE_CONFIGS[i]
            sc  = 0.05 if c[3] == -1 else 0.08
            x   = pos[0] + math.cos(c[1]) * c[0]
            y   = pos[1] + c[2]
            z   = pos[2] + math.sin(c[1]) * c[0]
            cube = bs.newnode('prop', attrs={
                'mesh':          bs.getmesh('box'),
                'body':          'box',
                'color_texture': bs.gettexture('black'),
                'position':      (x, y, z),
                'gravity_scale': 0.0,
                'mesh_scale':    0.0,
                'shadow_size':   0.0,
                'materials':     [self._mat],
            })
            light = bs.newnode('light', attrs={
                'color':    (0.6, 0.0, 1.0),
                'radius':   0.0,
                'position': (x, y, z),
            })
            r_final = 0.06 if c[3] == -1 else 0.1
            bs.animate(cube,  'mesh_scale', {0.0: 0.0, 0.25: sc * 1.5, 0.4: sc})
            bs.animate(light, 'radius',     {0.0: 0.0, 0.4: r_final})
            self._cubes.append(cube)
            self._lights.append(light)
            self._nodes += [cube, light]

        for i in range(len(_CUBE_CONFIGS)):
            self._timers.append(bs.Timer(i * 0.18, lambda i=i: mk(i)))

    def _fase_idle(self) -> None:
        for n in self._sello:
            try:
                if n and n.exists():
                    bs.animate(n, 'opacity', {0.0: 0.9, 0.4: 0.0})
            except Exception:
                pass
        self._timers.append(bs.Timer(0.5, bs.WeakCallStrict(self._limpiar_sello)))

    def _limpiar_sello(self) -> None:
        for n in self._sello:
            try:
                if n and n.exists():
                    n.delete()
            except Exception:
                pass
        self._sello.clear()

    def _tick(self) -> None:
        spaz = self._ref()
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        self._last_pos[0] = spaz.node.position
        vel = spaz.node.velocity
        spd = (vel[0] ** 2 + vel[2] ** 2) ** 0.5
        self._angle[0] += 0.03 + min(spd / 10.0, 1.0) * 0.42
        a   = self._angle[0]
        pos = spaz.node.position

        for i, cfg in enumerate(_CUBE_CONFIGS):
            if i >= len(self._cubes):
                break
            if i in self._busy_cubes:
                continue
            r, base_a, y_off, direction = cfg
            angle = base_a + a * direction
            x = pos[0] + math.cos(angle) * r
            y = pos[1] + y_off
            z = pos[2] + math.sin(angle) * r
            intensity = 0.6 + math.sin(a * 3 + i) * 0.4
            try:
                if self._cubes[i] and self._cubes[i].exists():
                    self._cubes[i].position = (x, y, z)
                if self._lights[i] and self._lights[i].exists():
                    self._lights[i].position  = (x, y, z)
                    self._lights[i].intensity = intensity
            except Exception:
                pass

    def destroy(self) -> None:
        self._timers.clear()
        self._death_timer = None
        self._firefly_timers.clear()
        self._busy_cubes.clear()
        self._alive[0] = False
        for tc in self._targets.values():
            try:
                tc.destroy()
            except Exception:
                pass
        self._targets.clear()
        for lst in (self._sello, self._nodes):
            for n in lst:
                try:
                    if hasattr(n, 'exists') and n.exists():
                        n.delete()
                except Exception:
                    pass
        self._sello.clear()
        self._nodes.clear()
        self._cubes.clear()
        self._lights.clear()
