# ba_meta require api 9
from __future__ import annotations
import random
import babase

_series_rain_timers: list = []
_round_rain_timers: list = []
_podium_spazzes: list = []
_nexus_map_holder: list = []


_podium_data: list = []

def _spawn_podium(activity: object) -> None:
    try:
        import bascenev1 as bs
        from bascenev1lib.actor.playerspaz import PlayerSpaz

        session = activity.session
        teams = sorted(
            session.sessionteams,
            key=lambda t: t.customdata.get('score', 0),
            reverse=True
        )

        spawn_positions = [
            (0.0,  2.0, 0.0),
            (2.0,  2.0, 0.0),
            (-2.0, 2.0, 0.0),
        ]

        _podium_spazzes.clear()
        _podium_data.clear()

        for i, team in enumerate(teams[:3]):
            if not team.players:
                _podium_data.append(None)
                continue
            sp = team.players[0]

            ap = None
            for p in activity.players:
                if p.sessionplayer is sp:
                    ap = p
                    break
            if ap is None:
                _podium_data.append(None)
                continue

            pos = spawn_positions[i]
            try:
                s = PlayerSpaz(
                    player=ap,
                    color=(0.05, 0.05, 0.05),
                    highlight=(0.05, 0.05, 0.05),
                    character=sp.character,
                )
                s.node.handlemessage('stand', pos[0], pos[1], pos[2], 0)
                s.node.invincible = True
                s.node.is_area_of_interest = False
                s.node.name = ''
                s.node.move_left_right = 0
                s.node.move_up_down = 0
                s.node.punch_pressed = False
                s.node.bomb_pressed = False
                s.node.pickup_pressed = False
                s.node.jump_pressed = False
                s.node.run = 0.0
                s.node.area_of_interest_radius = 0.5

                _podium_data.append({
                    'spaz': s,
                    'node': s.node,
                    'color': tuple(sp.color),
                    'highlight': tuple(sp.highlight),
                    'name': sp.getname(full=True),
                    'name_color': tuple(sp.color),
                    'pos': pos,
                })
                _podium_spazzes.append(s)
            except Exception as e:
                print(f'[nexus_podium] spawn {i}: {e}')
                _podium_data.append(None)

    except Exception as e:
        print(f'[nexus_podium] error: {e}')


def _reveal_podium(bs_module: object) -> None:
    bs = bs_module
    reveal_order = [2, 1, 0]
    delays = [0.0, 0.8, 1.6]

    for reveal_i, (place, delay) in enumerate(zip(reveal_order, delays)):
        if place >= len(_podium_data) or _podium_data[place] is None:
            continue
        d = _podium_data[place]
        nd = d['node']
        color = d['color']
        highlight = d['highlight']
        name = d['name']
        name_color = d['name_color']
        pos = d['pos']

        def _reveal(n=nd, c=color, h=highlight, nm=name, nc=name_color, p=pos, pl=place) -> None:
            if not n.exists():
                return
            bs.animate_array(n, 'color', 3, {0.0: (0.05, 0.05, 0.05), 0.5: c})
            bs.animate_array(n, 'highlight', 3, {0.0: (0.05, 0.05, 0.05), 0.5: h})
            n.name = nm
            n.name_color = nc
            n.is_area_of_interest = True

            light_color = (1.0, 0.9, 0.7)
            light = bs.newnode('light', attrs={
                'position': (p[0], p[1] + 2.0, p[2]),
                'intensity': 0.0,
                'radius': 2.5,
                'color': light_color,
                'volume_intensity_scale': 8.0,
                'height_attenuated': False,
            })
            bs.animate(light, 'intensity', {0.0: 0.0, 0.3: 0.3, 1.0: 0.15})
            _podium_spazzes.append(light)

            if pl == 0:
                n.handlemessage('celebrate', 999)
                n.is_area_of_interest = True

                def _keep_celebrate(n2=n) -> None:
                    if n2.exists():
                        n2.handlemessage('celebrate', 999)
                t = bs.Timer(0.8, _keep_celebrate, repeat=True)
                _series_rain_timers.append(t)

                def _do_rain() -> None:
                    bs.emitfx(
                        position=(
                            random.uniform(-4, 4),
                            4.0,
                            random.uniform(-4, 4),
                        ),
                        velocity=(0, -3.0, 0),
                        count=10, scale=0.8, spread=0.1,
                        chunk_type='spark', emit_type='chunks',
                    )
                rain_timer = bs.Timer(0.03, repeat=True, call=_do_rain)
                _series_rain_timers.append(rain_timer)

        bs.timer(delay, _reveal)


def _apply_series_patch() -> None:
    try:
        import bascenev1 as bs
        from bascenev1lib.activity.multiteamvictory import TeamSeriesVictoryScoreScreenActivity

        if getattr(TeamSeriesVictoryScoreScreenActivity, '_nexus_series_patched', False):
            return

        _orig_init = TeamSeriesVictoryScoreScreenActivity.__init__
        _orig_on_begin = TeamSeriesVictoryScoreScreenActivity.on_begin
        _orig_show_winner = TeamSeriesVictoryScoreScreenActivity._show_winner

        def _new_init(self, settings: dict) -> None:
            _orig_init(self, settings)
            try:
                import importlib.util, sys, os, babase
                if 'WinnerMap' not in sys.modules:
                    _wmod = next((m for k, m in sys.modules.items()
                        if k.startswith('_map_game_loader__map__') and hasattr(m, 'MyMap')), None)
                    if _wmod is None:
                        raise RuntimeError('WinnerMap no encontrado en map_game_loader')
                    sys.modules['WinnerMap'] = _wmod
                sys.modules['WinnerMap'].MyMap.preload()
            except Exception as e:
                print(f'[nexus_series] preload Winner: {e}')

        def _new_on_begin(self) -> None:
            _orig_on_begin(self)
            try:
                import sys, weakref as _wr2
                _wself2 = _wr2.ref(self)
                def _swap_map() -> None:
                    a = _wself2()
                    if a is None:
                        return
                    with a.context:
                        _nexus_map_holder.clear()
                        _nexus_map_holder.append(sys.modules['WinnerMap'].MyMap())
                bs.timer(0.1, _swap_map)
                _podium_spazzes.clear()
                self.globalsnode.tint = (0.0, 0.0, 0.0)
                self.globalsnode.ambient_color = (0.1, 0.1, 0.1)

                def _force_bounds() -> None:
                    a2 = _wself2()
                    if a2 is not None:
                        a2.globalsnode.area_of_interest_bounds = (-5.5, -0.5, -2.5, 5.5, 7.0, 2.5)
                bs.timer(0.3, _force_bounds)
                bs.timer(1.0, _force_bounds)
                bs.timer(2.5, _force_bounds)

                def _on_expire() -> None:
                    _nexus_map_holder.clear()
                    _series_rain_timers.clear()
                bs.timer(30.0, _on_expire)

                def _do_podium_early() -> None:
                    try:
                        a = _wself2()
                        if a is None:
                            return
                        with a.context:
                            _spawn_podium(a)
                    except Exception as e:
                        print(f'[nexus_podium] early: {e}')
                bs.timer(0.0, _do_podium_early)

            except Exception as e:
                print(f'[nexus_series] on_begin: {e}')

        def _new_show_winner(self, team: bs.SessionTeam) -> None:
            try:
                self._nexus_series_winner_team = team

                bs.animate_array(self.globalsnode, 'tint', 3, {
                    0.0: (0.0, 0.0, 0.0),
                    0.4: (0.1, 0.05, 0.2),
                    0.8: (0.25, 0.15, 0.5),
                    1.6: (0.4, 0.3, 0.8),
                })
                bs.animate_array(self.globalsnode, 'ambient_color', 3, {
                    0.0: (0.1, 0.1, 0.1),
                    0.8: (0.35, 0.3, 0.4),
                    1.6: (0.5, 0.45, 0.55),
                })

                _reveal_podium(bs)

            except Exception as e:
                print(f'[nexus_series] show_winner: {e}')
            _orig_show_winner(self, team)

        TeamSeriesVictoryScoreScreenActivity.__init__ = _new_init
        TeamSeriesVictoryScoreScreenActivity.on_begin = _new_on_begin
        TeamSeriesVictoryScoreScreenActivity._show_winner = _new_show_winner
        TeamSeriesVictoryScoreScreenActivity._nexus_series_patched = True
        print('[nexus_series] patch OK')

    except Exception as e:
        print(f'[nexus_series] error al patchear: {e}')


def _apply_patch() -> None:
    try:
        import bascenev1 as bs
        from bascenev1._multiteamsession import MultiTeamSession

        if getattr(MultiTeamSession, '_nexus_patched', False):
            print('[nexus] ya patcheado skip')
            return

        _original = MultiTeamSession.announce_game_results

        def _patched(self, activity, results, delay: float, announce_winning_team: bool = True) -> None:
            _original(self, activity, results, delay, announce_winning_team)

            if not announce_winning_team:
                return
            winning_sessionteam = results.winning_sessionteam
            if winning_sessionteam is None:
                return

            def _do_effects() -> None:
                try:
                    a = bs.get_foreground_host_activity()
                    if a is None:
                        return
                    with a.context:
                        winner_node = None
                        try:
                            assert winning_sessionteam.activityteam is not None
                            for p in winning_sessionteam.activityteam.players:
                                if p.actor and p.actor.node and p.actor.node.exists():
                                    p.actor.node.is_area_of_interest = True
                                    winner_node = p.actor.node
                            for p in a.players:
                                if p.actor and p.actor.node and p.actor.node.exists():
                                    if p.actor.node is not winner_node:
                                        p.actor.node.is_area_of_interest = False
                            a.globalsnode.camera_mode = 'follow'
                        except Exception as e:
                            print(f'[nexus] camera: {e}')

                        try:
                            bs.animate_array(a.globalsnode, 'tint', 3, {
                                0.0: (1.0, 1.0, 1.0),
                                0.75: (0.4, 0.3, 0.8),
                            })
                        except Exception as e:
                            print(f'[nexus] tint: {e}')

                        a._nexus_winner_node = winner_node

                        import weakref as _wr
                        _wact = _wr.ref(a)
                        def _rain() -> None:
                            try:
                                _a2 = _wact()
                                if _a2 is None: return
                                nd = getattr(_a2, '_nexus_winner_node', None)
                                if nd is None or not nd.exists():
                                    return
                                pos = nd.position
                                bs.emitfx(
                                    position=(
                                        pos[0] + random.uniform(-3, 3),
                                        pos[1] + 4.0,
                                        pos[2] + random.uniform(-3, 3),
                                    ),
                                    velocity=(0, -3.0, 0),
                                    count=10, scale=0.8, spread=0.1,
                                    chunk_type='spark', emit_type='chunks',
                                )
                            except Exception:
                                pass

                        timer = bs.Timer(0.03, repeat=True, call=_rain)
                        _round_rain_timers.append(timer)

                        def _stop() -> None:
                            try:
                                _round_rain_timers.clear()
                                _a3 = _wact()
                                if _a3 is not None:
                                    with _a3.context:
                                        _a3._nexus_winner_node = None
                            except Exception:
                                pass

                        bs.timer(4.5, _stop)

                except Exception as e:
                    print(f'[nexus] error general: {e}')

            bs.timer(delay + 0.1, _do_effects)

        MultiTeamSession.announce_game_results = _patched
        MultiTeamSession._nexus_patched = True
        print('[nexus_score_screen] patch OK')

    except Exception as e:
        print(f'[nexus_score_screen] error al patchear: {e}')



_ffa_map_holder: list = []

def _apply_ffa_patch() -> None:
    try:
        import bascenev1 as bs
        from bascenev1lib.activity.freeforallvictory import FreeForAllVictoryScoreScreenActivity

        if getattr(FreeForAllVictoryScoreScreenActivity, '_nexus_ffa_patched', False):
            return

        _orig_on_begin = FreeForAllVictoryScoreScreenActivity.on_begin

        def _new_on_begin(self) -> None:
            _orig_on_begin(self)
            try:
                import importlib, weakref
                if self._background is not None:
                    self._background.handlemessage(bs.DieMessage())
                    self._background = None

                session = self.session
                map_name = session._next_game_spec['settings']['map']

                try:
                    importlib.import_module(map_name.replace(' ', ''))
                except Exception:
                    pass

                def _get_all_map_classes():
                    return {c.getname(): c for sc in [bs.Map] for c in (lambda f: f(f, sc))(lambda f, c: c.__subclasses__() + [x for s in c.__subclasses__() for x in f(f, s)])}

                all_maps = _get_all_map_classes()
                map_cls = all_maps.get(map_name)

                if map_cls is not None:
                    try:
                        map_cls.preload()
                        _ffa_map_holder.clear()
                        _ffa_map_holder.append(map_cls())
                        print(f'[nexus_ffa] mapa preview: {map_name}')
                    except Exception as e:
                        print(f'[nexus_ffa] instancia mapa: {e}')
                else:
                    print(f'[nexus_ffa] mapa no encontrado: {map_name}')

                self.globalsnode.tint = (0.0, 0.0, 0.0)
                self.globalsnode.ambient_color = (0.1, 0.1, 0.1)

                bs.animate_array(self.globalsnode, 'tint', 3, {
                    0.0: (0.0, 0.0, 0.0),
                    1.0: (0.3, 0.25, 0.4),
                    2.0: (0.5, 0.45, 0.6),
                })
                bs.animate_array(self.globalsnode, 'ambient_color', 3, {
                    0.0: (0.1, 0.1, 0.1),
                    1.0: (0.4, 0.35, 0.45),
                    2.0: (0.6, 0.55, 0.65),
                })

                _wself = weakref.ref(self)
                def _force_bounds() -> None:
                    a = _wself()
                    if a is not None:
                        a.globalsnode.area_of_interest_bounds = (-6.0, -1.0, -3.0, 6.0, 6.0, 3.0)
                bs.timer(0.1, _force_bounds)
                bs.timer(0.5, _force_bounds)
                bs.timer(1.5, _force_bounds)

                def _on_expire() -> None:
                    _ffa_map_holder.clear()
                bs.timer(20.0, _on_expire)

            except Exception as e:
                print(f'[nexus_ffa] on_begin: {e}')

        FreeForAllVictoryScoreScreenActivity.on_begin = _new_on_begin
        FreeForAllVictoryScoreScreenActivity._nexus_ffa_patched = True
        print('[nexus_ffa] patch OK')

    except Exception as e:
        print(f'[nexus_ffa] error al patchear: {e}')

# ba_meta export babase.Plugin
class NexusScoreScreen(babase.Plugin):
    def on_app_running(self) -> None:
        _apply_patch()
        _apply_series_patch()
        _apply_ffa_patch()
def enable():
    _apply_patch()
    _apply_series_patch()
    _apply_ffa_patch()
