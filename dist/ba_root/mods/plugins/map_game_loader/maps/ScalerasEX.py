
# ba_meta require api 9
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs, random
import bascenev1lib.maps as _maps
from bauiv1lib.popup import PopupWindow
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Sequence, Any

class MyMapPoints:
    points = {}
    boxes = {}
    boxes['area_of_interest_bounds'] = (-1.0, -1.25, -3.55) + (
        0.0, 0.0, 0.0) + (33.1, 15.5, 22.8)
    boxes['map_bounds'] = (-1.0, -1.25, -3.55) + (0.0, 0.0, 0.0) + (
        33.1, 15.5, 22.8)
    points['ffa_spawn1'] = (-9.449999809265137, 3.5, -4.150000095367432)
    points['ffa_spawn2'] = (-3.450000047683716, 3.5, -4.150000095367432)
    points['ffa_spawn3'] = (1.5499999523162842, 3.5, -4.150000095367432)
    points['ffa_spawn4'] = (11.550000190734863, 3.5, -4.150000095367432)
    points['ffa_spawn5'] = (11.550000190734863, 0.5, 4.849999904632568)
    points['ffa_spawn6'] = (-6.449999809265137, 0.699999988079071, 3.6500000953674316)
    points['ffa_spawn7'] = (5.550000190734863, 0.699999988079071, 3.6500000953674316)
    points['ffa_spawn8'] = (5.550000190734863, 0.699999988079071, -1.350000023841858)
    points['ffa_spawn9'] = (-3.450000047683716, 0.699999988079071, -1.350000023841858)
    points['spawn1'] = (-9.449999809265137, 0.699999988079071, -0.3499999940395355)
    points['spawn2'] = (12.550000190734863, 0.699999988079071, -1.350000023841858)
    points['powerup_spawn1'] = (2.549999952316284, 0.699999988079071, -1.350000023841858)
    points['powerup_spawn2'] = (2.549999952316284, 0.699999988079071, 3.6500000953674316)
    points['powerup_spawn3'] = (-3.450000047683716, 0.699999988079071, 3.6500000953674316)
    points['powerup_spawn4'] = (-7.449999809265137, 3.700000047683716, -4.349999904632568)
    points['powerup_spawn5'] = (4.550000190734863, 3.700000047683716, -4.349999904632568)
    points['powerup_spawn6'] = (12.550000190734863, 3.700000047683716, -4.349999904632568)
    points['flag_default'] = (-0.44999998807907104, 0.699999988079071, 2.6500000953674316)
    points['tnt1'] = (-0.44999998807907104, 0.699999988079071, 0.6499999761581421)
    points['flag1'] = (-9.449999809265137, 0.699999988079071, -0.3499999940395355)
    points['flag2'] = (12.550000190734863, 0.699999988079071, -1.350000023841858)
    

class MyMap(bs.Map):

    defs = MyMapPoints
    name = 'ScalerasEX'
    _base_map_key = 'FootballStadium'
    is_flying = True

    @classmethod
    def get_play_types(cls) -> list[str]:
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'eggTex3'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {}
        if cls._base_map_key:
            try:
                data['base'] = getattr(_maps, cls._base_map_key).on_preload()
            except Exception:
                pass
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.locs = []
        self.regions = []

        self.collision = bs.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        blkset = [
              dict(position=(-9.350000381469727, 1.399999976158142, -2.0999999046325684), color=(1.0, 0.0, 0.0), size=(2.5, 3.5, 1.0), draw_beauty=False),
              dict(position=(8.25, 1.2000000476837158, -3.200000047683716), color=(1.0, 0.0, 0.0), size=(2.5, 3.5, 1.0), draw_beauty=False),
              dict(position=(-9.050000190734863, 0.699999988079071, 3.3499999046325684), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 1.5), draw_beauty=False),
              dict(position=(-12.149999618530273, -0.20000000298023224, -0.800000011920929), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 1.5), draw_beauty=False),
              dict(position=(-12.149999618530273, -0.20000000298023224, -1.600000023841858), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 1.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.799999952316284, -4.800000190734863), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.5999999046325684, -4.599999904632568), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.4000000953674316, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.200000047683716, -4.199999809265137), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.0, -4.0), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 1.7999999523162842, -3.799999952316284), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 1.600000023841858, -3.5999999046325684), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 1.399999976158142, -3.4000000953674316), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 1.2000000476837158, -3.200000047683716), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 1.0, -3.0), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 0.800000011920929, -2.799999952316284), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 0.6000000238418579, -2.5999999046325684), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 0.4000000059604645, -2.4000000953674316), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 0.20000000298023224, -2.200000047683716), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 0.0, -2.0), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 0.5), draw_beauty=False),
              dict(position=(-12.149999618530273, 2.799999952316284, -5.699999809265137), color=(1.0, 0.0, 0.0), size=(3.0, 0.5, 2.0), draw_beauty=False),
              dict(position=(-5.449999809265137, 2.5999999046325684, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(10.5, 1.0, 3.5), draw_beauty=False),
              dict(position=(5.050000190734863, 2.5999999046325684, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(10.5, 1.0, 3.5), draw_beauty=False),
              dict(position=(9.050000190734863, 2.5999999046325684, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(10.5, 1.0, 3.5), draw_beauty=False),
              dict(position=(8.25, 1.5, 3.299999952316284), color=(1.0, 0.0, 0.0), size=(3.0, 4.5, 1.5), draw_beauty=False),
              ]

        for i, blk in enumerate(blkset):
            self.locs.append(
                bs.newnode('locator',
                    attrs={'shape': 'box',
                           'position': blk['position'],
                           'color': blk['color'],
                           'opacity': 1.0,
                           'draw_beauty': blk['draw_beauty'],
                           'size': blk['size'],
                           'additive': False}))

            self.regions.append(
                bs.newnode('region',
                    attrs={'scale': tuple(blk['size']),
                           'type': 'box',
                           'materials': [self.collision,
                                         shared.footing_material]}))
            self.locs[-1].connectattr('position', self.regions[-1], 'position')

        mshset = [
              dict(mesh='courtyardLevel', texture='courtyardLevelColor', position=(-0.10000000149011612, -6.0, -6.38378239159465e-16), angle=0.0),
              dict(mesh='courtyardLevel', texture='courtyardLevelColor', position=(-1.100000023841858, -6.0, -2.7755575615628914e-17), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-9.649999618530273, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-4.849999904632568, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-0.04999999329447746, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(4.75, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(9.550000190734863, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(11.65000057220459, -2.200000047683716, -10.050000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -2.200000047683716, -11.949999809265137), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -2.3999998569488525, -11.75), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -2.5999999046325684, -11.550000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -2.799999952316284, -11.34999942779541), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -3.0, -11.149999618530273), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -3.200000047683716, -10.949999809265137), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -3.3999998569488525, -10.75), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -3.5999999046325684, -10.550000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -3.799999952316284, -10.350000381469727), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -4.0, -10.149999618530273), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -4.200000286102295, -9.949999809265137), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -4.400000095367432, -9.75), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -4.599999904632568, -9.550000190734863), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -4.800000190734863, -9.350000381469727), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -5.0, -9.149999618530273), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-13.75, -5.199999809265137, -8.949999809265137), angle=270.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-14.550000190734863, -5.199999809265137, -7.449999809265137), angle=270.0),
              ]

        self._mesh_nodes = []
        self._mesh_mat = bs.Material()
        self._mesh_mat.add_actions(actions=(
            ('modify_part_collision', 'collide', False),
            ('modify_part_collision', 'physical', False)))

        for mv in mshset:
            nd = bs.newnode(type='spaz', attrs={
                'color': (1,1,1),
                'highlight': (1,1,1),
                'color_texture': bs.gettexture(mv['texture']),
                'color_mask_texture': bs.gettexture('bonesColorMask'),
                'head_mesh': bs.getmesh(mv['mesh']),
                'style': 'bones',
                'materials': [self._mesh_mat],
                'roller_materials': [self._mesh_mat],
                'extras_material': [self._mesh_mat],
                'punch_materials': [self._mesh_mat],
                'pickup_materials': [self._mesh_mat],
            })
            self._mesh_nodes.append((nd, mv['position'], mv['angle']))

        def _freeze_meshes():
            for nd, pos, angle in self._mesh_nodes:
                if nd.exists():
                    nd.handlemessage('stand', pos[0], pos[1], pos[2], angle)
                    nd.handlemessage('knockout', 500.0)
                    nd.area_of_interest_radius = 0.0
        self._freeze_timer = bs.Timer(0.001, _freeze_meshes, repeat=True)

        # Plataformas moviles
        _platset = [
              {'type': 'locator', 'size': [3.0, 0.5, 3.0], 'scale': 1.0, 'color': [0.8, 0.7, 0.5], 'texture': 'cragCastleLevelColor', 'keyframes': [(-6.55, -0.2, -0.95, 4.0), (-6.55, 3.3, -0.95, 3.0)]},
              {'type': 'locator', 'size': [3.0, 0.5, 2.5], 'scale': 1.0, 'color': [0.8, 0.7, 0.5], 'texture': 'cragCastleLevelColor', 'keyframes': [(8.25, 2.8, -1.45, 3.5), (8.25, 3.5, 1.35, 4.5)]},
              {'type': 'locator', 'size': [3.0, 0.5, 2.5], 'scale': 1.0, 'color': [0.8, 0.7, 0.5], 'texture': 'cragCastleLevelColor', 'keyframes': [(8.25, 3.0, 7.25, 3.0), (8.25, 3.5, 5.35, 3.0)]},
              ]
        self._plat_nodes = []
        for _pd in _platset:
            _shared = SharedObjects.get()
            _pos = (_pd['keyframes'][0][0], _pd['keyframes'][0][1], _pd['keyframes'][0][2])
            _col = bs.Material()
            _col.add_actions(actions=('modify_part_collision','collide',True),
                conditions=('they_have_material', _shared.player_material))
            if _pd['type'] == 'locator':
                _r = bs.newnode('region', attrs={
                    'position':_pos, 'scale':tuple(_pd['size']),
                    'type':'box', 'materials':(_shared.footing_material, _col)})
                _l = bs.newnode('locator', attrs={
                    'shape':'box', 'position':_pos, 'color':tuple(_pd['color']),
                    'opacity':1.0, 'draw_beauty':True, 'additive':False,
                    'size':list(_pd['size'])})
                _r.connectattr('position', _l, 'position')
            else:
                _dc = bs.Material()
                _dc.add_actions(actions=('modify_part_collision','collide',False))
                _r = bs.newnode('region', attrs={
                    'position':_pos,
                    'scale':(_pd['scale'],_pd['scale'],_pd['scale']),
                    'type':'box', 'materials':(_shared.footing_material, _col)})
                _l = bs.newnode('prop', attrs={
                    'mesh':bs.getmesh('box' if _pd['type']=='box' else _pd['type']),
                    'body':'puck', 'position':_pos,
                    'color_texture':bs.gettexture('cragCastleLevelColor'),
                    'shadow_size':0.0, 'gravity_scale':0.0, 'velocity':(0,0,0),
                    'mesh_scale':_pd['scale'], 'body_scale':0.1,
                    'reflection_scale':[0.0], 'materials':[_dc]})
                _r.connectattr('position', _l, 'position')
            _keys = {}
            _t = 0.0
            for _kf in _pd['keyframes']:
                _keys[_t] = (_kf[0], _kf[1], _kf[2])
                _t += _kf[3]
            _keys[_t] = (_pd['keyframes'][0][0], _pd['keyframes'][0][1], _pd['keyframes'][0][2])
            bs.animate_array(_r, 'position', 3, _keys, loop=True)
            self._plat_nodes.append((_r, _l))

        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': bs.getmesh('tipTopBG'),
                'lighting': False,
                'background': True,
                'color_texture': bs.gettexture('black')})

        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.0, 0.699999988079071, 0.699999988079071)
        gnode.ambient_color = (1.0, 1.0, 1.0)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

        # Base map
        if self.preloaddata.get('base'):
            bdata = self.preloaddata['base']
            mesh = bdata.get('mesh', bdata.get('mesh_top'))
            tex = bdata.get('tex')
            col = bdata.get('collision_mesh')
            if mesh and tex and col:
                bs.newnode('terrain', attrs={
                    'mesh': mesh,
                    'color_texture': tex,
                    'collision_mesh': col,
                    'lighting': True,
                    'background': False,
                    'materials': [shared.footing_material]})
            if bdata.get('mesh_bottom'):
                bs.newnode('terrain', attrs={
                    'mesh': bdata['mesh_bottom'],
                    'color_texture': tex,
                    'lighting': False,
                    'background': False})

        # TexBoxes
        self._no_phys = bs.Material()
        self._no_phys.add_actions(actions=(
            ('modify_part_collision','collide',False),
            ('modify_part_collision','physical',False)))
        self._col = bs.Material()
        self._col.add_actions(actions=(
            ('modify_part_collision','collide',True),
            ('modify_part_collision','physical',True)))
        txbset = [
              ]
        self._tex_timers = []
        for tb in txbset:
            nd = bs.newnode('prop', attrs={
                'mesh': bs.getmesh(tb.get('mesh','tnt')),
                'body': 'puck',
                'position': tb['position'],
                'shadow_size': 1.0,
                'velocity': (0,0,0),
                'color_texture': bs.gettexture(tb['texture']),
                'reflection_scale': [1.0],
                'gravity_scale': 0.0,
                'mesh_scale': tb['scale'],
                'body_scale': 1.0,
                'materials': [self._no_phys],
                'density': 0.0})
            r = bs.newnode('region', attrs={
                'position': tb['position'],
                'scale': (tb['scale'], tb['scale'], tb['scale']),
                'type': 'box',
                'materials': [shared.footing_material, self._col]})
            pos = tb['position']
            def _freeze(n=nd, r2=r, p=pos):
                if n.exists(): n.position = p; n.velocity = (0,0,0)
                if r2.exists(): r2.position = p
            self._tex_timers.append(bs.Timer(0.001, _freeze, repeat=True))

def _start_ambiente(effects):
    import random as _random
    import bascenev1 as _bs
    a = _bs.getactivity()
    if not hasattr(a, '_amb_timers'):
        a._amb_timers = []
        a._amb_nodes = []
    for eff in effects:
        etype = eff.get('type','firefly')
        color = tuple(eff.get('color',(1,0.8,0)))
        count = eff.get('count',3)
        scale = eff.get('scale',1.0)
        speed = eff.get('speed',0.5)
        interval = eff.get('interval',0.5)
        zone = eff.get('zone',(0,3,0))

        if etype == 'firefly':
            def _make_ff(col=color, z=zone, sc=scale):
                nd = _bs.newnode('locator', attrs={
                    'shape':'circle','position':z,
                    'color':col,'opacity':0.7,
                    'draw_beauty':True,'additive':True,
                    'size':[sc*0.12]})
                lt = _bs.newnode('light', owner=nd, attrs={
                    'intensity':0.5,'height_attenuated':True,
                    'radius':sc*0.3,'color':col})
                nd.connectattr('position', lt, 'position')
                keys = {}
                t = 0
                lx,ly,lz = z[0],z[1],z[2]
                for _ in range(8):
                    lx = lx + _random.uniform(-3,3)
                    ly = abs(ly + _random.uniform(-0.5,1.5))
                    lz = lz + _random.uniform(-3,3)
                    keys[t] = (lx, ly, lz)
                    t += _random.uniform(4,10)
                _bs.animate_array(nd,'position',3,keys,loop=True)
                _bs.animate(lt,'radius',{0:0,2:sc*0.4,5:sc*0.15,8:sc*0.35,12:0},loop=True)
                return nd, lt
            for _ in range(count):
                nd, lt = _make_ff()
                a._amb_nodes.extend([nd, lt])

        elif etype == 'fireworks':
            def _shoot(z=zone, sc=scale, cnt=count, col=color):
                px = z[0] + _random.uniform(-6,6)
                py = z[1] + _random.uniform(2,8)
                pz = z[2] + _random.uniform(-6,6)
                for _ in range(5):
                    _bs.emitfx(position=(px,py,pz), count=cnt,
                        emit_type='chunks', chunk_type='spark',
                        scale=sc*2.0, spread=3.0, velocity=(0,2,0))
                flash = _bs.newnode('light', attrs={
                    'position':(px,py,pz),'radius':0.1,
                    'intensity':2.0,'color':col,
                    'volume_intensity_scale':20})
                _bs.animate(flash,'radius',{0:0.1,0.1:sc*10,0.8:0.0},loop=False)
                _bs.animate(flash,'intensity',{0:2.0,0.8:0.0},loop=False)
                _bs.timer(1.0, flash.delete)
            t2 = _bs.Timer(interval, _shoot, repeat=True)
            a._amb_timers.append(t2)

        elif etype == 'smoke':
            def _puff(z=zone, sc=scale, cnt=count):
                _bs.emitfx(position=(z[0]+_random.uniform(-3,3), z[1]+_random.uniform(0,2), z[2]+_random.uniform(-3,3)),
                    count=cnt, emit_type='tendrils', tendril_type='smoke',
                    scale=sc, spread=1.5)
            t3 = _bs.Timer(interval, _puff, repeat=True)
            a._amb_timers.append(t3)

        elif etype == 'snow':
            def _flake(z=zone, sc=scale, cnt=count):
                _bs.emitfx(position=(z[0]+_random.uniform(-5,5), z[1]+4, z[2]+_random.uniform(-5,5)),
                    count=cnt, emit_type='chunks', chunk_type='ice',
                    scale=sc*0.4, spread=2.0, velocity=(0,-1.5,0))
            t4 = _bs.Timer(interval, _flake, repeat=True)
            a._amb_timers.append(t4)

        elif etype == 'sparks':
            def _spark(z=zone, sc=scale, cnt=count):
                _bs.emitfx(position=(z[0]+_random.uniform(-2,2), z[1]+_random.uniform(0,3), z[2]+_random.uniform(-2,2)),
                    count=cnt, emit_type='chunks', chunk_type='spark',
                    scale=sc*0.5, spread=1.0, velocity=(0,0.5,0))
            t5 = _bs.Timer(interval, _spark, repeat=True)
            a._amb_timers.append(t5)

        elif etype == 'ambient_light':
            lt = _bs.newnode('light', attrs={
                'position':tuple(zone),'radius':scale*15,
                'intensity':0.3,'volume_intensity_scale':8,'color':color})
            keys = {}
            cols = [color,
                (_random.uniform(0.5,1.2),_random.uniform(0,0.5),_random.uniform(0,0.3)),
                (_random.uniform(0,0.3),_random.uniform(0.3,0.8),_random.uniform(0.5,1.2)),
                color]
            for i,c in enumerate(cols):
                keys[i*4] = c
            _bs.animate_array(lt,'color',3,keys,loop=True)
            a._amb_nodes.append(lt)

_AMBIENT_DATA = []

# ba_meta export babase.Plugin
class MapMaker(bs.Plugin):
    def on_app_running(self):
        bs.register_map(MyMap)
        if _AMBIENT_DATA:
            import babase as _bab
            def _wait():
                try:
                    a = __import__('bascenev1').getactivity()
                    if a is not None:
                        with a.context:
                            _start_ambiente(_AMBIENT_DATA)
                except Exception:
                    pass
            _bab.apptimer(2.0, _wait)
    