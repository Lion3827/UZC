
# ba_meta require api 9
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs, random
from bauiv1lib.popup import PopupWindow
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Sequence, Any

class MyMapPoints:
    points = {}
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.0, 0.7956858119, 0.0) + (
        0.0, 0.0, 0.0) + (30.80223883, 0.5961646365, 13.88431707)
    boxes['map_bounds'] = (0.0, 0.7956858119, -0.4689020853) + (0.0, 0.0, 0.0) + (
        35.16182389, 12.18696164, 21.52869693)
    points['ffa_spawn1'] = (-9.050000190734863, -2.299999952316284, -7.800000190734863)
    points['ffa_spawn2'] = (-9.050000190734863, -2.299999952316284, 0.699999988079071)
    points['ffa_spawn3'] = (8.449999809265137, -2.299999952316284, 0.699999988079071)
    points['ffa_spawn4'] = (8.449999809265137, -2.299999952316284, -8.800000190734863)
    points['ffa_spawn5'] = (14.449999809265137, 0.20000000298023224, -6.300000190734863)
    points['ffa_spawn6'] = (14.449999809265137, 0.20000000298023224, -1.2999999523162842)
    points['ffa_spawn7'] = (-14.550000190734863, 0.20000000298023224, -1.2999999523162842)
    points['ffa_spawn8'] = (-14.550000190734863, 0.20000000298023224, -6.300000190734863)
    points['ffa_spawn9'] = (-6.050000190734863, -2.299999952316284, -6.300000190734863)
    points['ffa_spawn10'] = (-6.050000190734863, -2.299999952316284, -1.2999999523162842)
    points['ffa_spawn11'] = (5.449999809265137, -2.299999952316284, -1.2999999523162842)
    points['ffa_spawn12'] = (5.449999809265137, -2.299999952316284, -6.800000190734863)
    points['ffa_spawn13'] = (-0.550000011920929, -2.299999952316284, -4.800000190734863)
    points['ffa_spawn14'] = (-0.550000011920929, -2.299999952316284, -3.299999952316284)
    points['spawn1'] = (-9.050000190734863, -1.7999999523162842, -3.299999952316284)
    points['spawn2'] = (8.449999809265137, -1.7999999523162842, -3.299999952316284)
    points['powerup_spawn1'] = (8.449999809265137, -1.7999999523162842, -1.2999999523162842)
    points['powerup_spawn2'] = (8.449999809265137, -1.7999999523162842, -6.300000190734863)
    points['powerup_spawn3'] = (-9.050000190734863, -1.7999999523162842, -5.300000190734863)
    points['powerup_spawn4'] = (-9.050000190734863, -1.7999999523162842, -1.2999999523162842)
    points['powerup_spawn5'] = (-3.049999952316284, -1.7999999523162842, -1.2999999523162842)
    points['powerup_spawn6'] = (-3.049999952316284, -1.7999999523162842, -5.300000190734863)
    points['powerup_spawn7'] = (2.450000047683716, -1.7999999523162842, -5.300000190734863)
    points['powerup_spawn8'] = (2.450000047683716, -1.7999999523162842, -1.2999999523162842)
    points['powerup_spawn9'] = (11.449999809265137, 0.20000000298023224, -1.2999999523162842)
    points['powerup_spawn10'] = (-12.050000190734863, 0.20000000298023224, -1.2999999523162842)
    points['powerup_spawn11'] = (-12.050000190734863, 0.20000000298023224, -6.300000190734863)
    points['powerup_spawn12'] = (11.449999809265137, 0.20000000298023224, -6.300000190734863)
    points['flag_default'] = (-0.550000011920929, -2.299999952316284, -4.300000190734863)
    points['tnt1'] = (2.450000047683716, -1.7999999523162842, -3.299999952316284)
    points['tnt2'] = (-3.049999952316284, -1.7999999523162842, -3.299999952316284)
    points['flag1'] = (-9.050000190734863, -1.7999999523162842, -3.299999952316284)
    points['flag2'] = (8.449999809265137, -1.7999999523162842, -3.299999952316284)
    

class MyMap(bs.Map):

    defs = MyMapPoints
    name = 'Superfortalezaduet'

    @classmethod
    def get_play_types(cls) -> list[str]:
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'eggTex3'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {}
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
              dict(position=(5.5, -3.4000000953674316, -4.5), color=(1.0, 0.0, 0.0), size=(3.5, 1.0, 11.0), draw_beauty=False),
              dict(position=(8.699999809265137, -3.200000047683716, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(3.0, 1.0, 12.5), draw_beauty=False),
              dict(position=(-9.199999809265137, -3.200000047683716, -4.400000095367432), color=(1.0, 0.0, 0.0), size=(3.0, 1.0, 12.5), draw_beauty=False),
              dict(position=(-0.4000000059604645, -3.200000047683716, -4.150000095367432), color=(1.0, 0.0, 0.0), size=(8.5, 1.0, 6.5), draw_beauty=False),
              dict(position=(-6.150000095367432, -3.200000047683716, -4.050000190734863), color=(1.0, 0.0, 0.0), size=(3.5, 1.0, 10.0), draw_beauty=False),
              dict(position=(-10.699999809265137, -3.200000047683716, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-11.149999618530273, -2.9000000953674316, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-11.75, -2.5999999046325684, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-12.350000381469727, -2.299999952316284, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-12.949999809265137, -2.0, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-13.550000190734863, -1.7000000476837158, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-14.149999618530273, -1.399999976158142, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-14.699999809265137, -1.100000023841858, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-14.949999809265137, -0.800000011920929, 0.75), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-15.25, -0.800000011920929, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-14.649999618530273, -1.100000023841858, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-14.100000381469727, -1.399999976158142, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-13.5, -1.7000000476837158, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-12.899999618530273, -2.0, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-12.300000190734863, -2.299999952316284, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-11.699999809265137, -2.5999999046325684, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(-11.0, -2.9000000953674316, -9.050000190734863), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(10.5, -3.0, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(11.100000381469727, -2.700000047683716, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(11.699999809265137, -2.4000000953674316, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(12.300000190734863, -2.0999999046325684, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(12.899999618530273, -1.7999999523162842, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(13.5, -1.5, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(14.100000381469727, -1.2000000476837158, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(14.699999809265137, -0.8999999761581421, 0.6000000238418579), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(15.050000190734863, -0.8999999761581421, 0.3499999940395355), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(15.050000190734863, -0.8999999761581421, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(14.449999809265137, -1.2000000476837158, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(13.850000381469727, -1.5, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(13.25, -1.7999999523162842, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(12.649999618530273, -2.0999999046325684, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(12.050000190734863, -2.4000000953674316, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(11.449999809265137, -2.700000047683716, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(10.850000381469727, -3.0, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(10.600000381469727, -3.299999952316284, -9.149999618530273), color=(1.0, 0.0, 0.0), size=(1.0, 1.0, 2.5), draw_beauty=False),
              dict(position=(13.0, -0.8999999761581421, -6.900000095367432), color=(1.0, 0.0, 0.0), size=(5.5, 1.0, 2.5), draw_beauty=False),
              dict(position=(12.949999809265137, -0.8999999761581421, -1.850000023841858), color=(1.0, 0.0, 0.0), size=(5.5, 1.0, 2.5), draw_beauty=False),
              dict(position=(-13.399999618530273, -0.8999999761581421, -1.850000023841858), color=(1.0, 0.0, 0.0), size=(5.5, 1.0, 2.5), draw_beauty=False),
              dict(position=(-13.350000381469727, -0.8999999761581421, -6.75), color=(1.0, 0.0, 0.0), size=(5.5, 1.0, 2.5), draw_beauty=False),
              dict(position=(-11.899999618530273, -3.5999999046325684, 1.5499999523162842), color=(1.0, 0.0, 0.0), size=(3.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-13.850000381469727, -2.0999999046325684, 1.5499999523162842), color=(1.0, 0.0, 0.0), size=(3.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-14.899999618530273, -0.8999999761581421, 1.5499999523162842), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(14.75, -0.8999999761581421, 1.350000023841858), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(12.600000381469727, -2.4000000953674316, 1.2999999523162842), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(11.149999618530273, -3.9000000953674316, 1.2999999523162842), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(14.550000190734863, -0.800000011920929, -10.149999618530273), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(13.050000190734863, -2.299999952316284, -10.149999618530273), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(11.100000381469727, -3.799999952316284, -10.149999618530273), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-11.449999809265137, -3.799999952316284, -10.0), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-12.75, -2.299999952316284, -9.800000190734863), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-14.949999809265137, -0.800000011920929, -9.800000190734863), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-15.199999809265137, -0.800000011920929, -9.800000190734863), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
              dict(position=(-13.050000190734863, -2.299999952316284, -9.800000190734863), color=(1.0, 0.0, 0.0), size=(2.0, 4.0, 0.5), draw_beauty=False),
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
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, 0.0), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, -1.0), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, -2.0), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, -3.0), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, -4.0), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -8.0, -5.0), angle=0.0),
              dict(mesh='roundaboutLevel', texture='roundaboutLevelColor', position=(-8.399999618530273, -5.799999952316284, -5.850000381469727), angle=90.0),
              dict(mesh='roundaboutLevel', texture='roundaboutLevelColor', position=(8.099999904632568, -5.799999952316284, -2.8499999046325684), angle=270.0),
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
        bs.timer(0.001, _freeze_meshes, repeat=True)

        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': bs.getmesh('tipTopBG'),
                'lighting': False,
                'background': True,
                'color_texture': bs.gettexture('black')})

        gnode = bs.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)

# ba_meta export babase.Plugin
class MapMaker(bs.Plugin):
    def on_app_running(self):
        bs.register_map(MyMap)
    