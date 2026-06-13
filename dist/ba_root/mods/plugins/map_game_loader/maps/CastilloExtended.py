
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
    boxes['area_of_interest_bounds'] = (0.0, 4.0, -5.0) + (
        0.0, 0.0, 0.0) + (18.0, 16.0, 18.0)
    boxes['map_bounds'] = (0.0, 2.0, -10.0) + (0.0, 0.0, 0.0) + (
        60.0, 30.0, 60.0)
    points['ffa_spawn1'] = (0.0, 4.5, -10.0)
    points['ffa_spawn2'] = (1.0, 4.5, -10.0)
    points['ffa_spawn3'] = (-2.0, 5.5, -1.0)
    points['ffa_spawn4'] = (-2.0, 5.5, -7.0)
    points['ffa_spawn5'] = (2.5, 5.5, -7.0)
    points['ffa_spawn6'] = (2.5, 5.5, -0.5)
    points['ffa_spawn7'] = (5.0, 6.0, -4.5)
    points['ffa_spawn8'] = (-4.5, 6.0, -4.5)
    points['ffa_spawn9'] = (-7.0, 6.5, -7.5)
    points['ffa_spawn10'] = (7.5, 6.5, -7.5)
    points['ffa_spawn11'] = (7.5, 6.5, -0.5)
    points['ffa_spawn12'] = (-7.0, 6.5, -0.5)
    points['ffa_spawn13'] = (-7.5, 5.0, 2.5)
    points['ffa_spawn14'] = (7.5, 5.0, 2.5)
    points['ffa_spawn15'] = (0.5, 5.0, 2.5)
    points['ffa_spawn16'] = (0.0, 4.5, 6.0)
    points['ffa_spawn17'] = (0.0, 4.5, 7.5)
    points['ffa_spawn18'] = (-5.5, 4.5, 7.5)
    points['ffa_spawn19'] = (6.5, 4.5, 7.5)
    points['spawn1'] = (-7.0, 6.5, -4.5)
    points['spawn2'] = (7.5, 6.5, -4.5)
    points['powerup_spawn1'] = (1.5, 4.5, 6.0)
    points['powerup_spawn2'] = (-1.5, 4.5, 6.0)
    points['powerup_spawn3'] = (-5.5, 4.5, 8.0)
    points['powerup_spawn4'] = (6.0, 4.5, 8.0)
    points['powerup_spawn5'] = (5.5, 5.0, 2.5)
    points['powerup_spawn6'] = (-6.0, 5.0, 2.5)
    points['powerup_spawn7'] = (-4.5, 6.0, -1.0)
    points['powerup_spawn8'] = (5.0, 6.0, -1.0)
    points['powerup_spawn9'] = (5.0, 6.0, -7.0)
    points['powerup_spawn10'] = (-4.5, 6.0, -7.0)
    points['powerup_spawn11'] = (7.5, 6.5, -0.5)
    points['powerup_spawn12'] = (-7.0, 6.5, -7.5)
    points['flag_default'] = (0.44999998807907104, 5.0, -4.099999904632568)
    points['tnt1'] = (0.30000001192092896, 5.0, -4.0)
    points['tnt2'] = (-0.05000000074505806, 4.0, 6.400000095367432)
    points['flag1'] = (-7.0, 6.5, -4.5)
    points['flag2'] = (7.5, 6.5, -4.5)
    

class MyMap(bs.Map):

    defs = MyMapPoints
    name = 'CastilloExtended'
    is_flying = True

    @classmethod
    def get_play_types(cls) -> list[str]:
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'eggTex3'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = _maps.StepRightUp.on_preload()
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
              dict(position=(0.0, 3.5, -11.0), color=(1.0, 0.0, 0.0), size=(9.0, 1.0, 3.5), draw_beauty=False),
              dict(position=(6.0, 3.299999952316284, 7.75), color=(1.0, 0.0, 0.0), size=(3.5, 1.0, 5.5), draw_beauty=False),
              dict(position=(-5.599999904632568, 3.299999952316284, 7.650000095367432), color=(1.0, 0.0, 0.0), size=(3.5, 1.0, 5.5), draw_beauty=False),
              dict(position=(0.15000000596046448, 3.299999952316284, 6.699999809265137), color=(1.0, 0.0, 0.0), size=(8.5, 1.0, 4.0), draw_beauty=False),
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
              dict(mesh='trees', texture='treesColor', position=(1.5, 4.5, -23.0), angle=0.0),
              dict(mesh='trees', texture='treesColor', position=(-4.5, 3.5, -27.0), angle=150.0),
              dict(mesh='trees', texture='treesColor', position=(-0.5, 3.5, -25.5), angle=150.0),
              dict(mesh='trees', texture='treesColor', position=(3.0, 3.5, -25.5), angle=150.0),
              dict(mesh='trees', texture='treesColor', position=(0.5, 3.5, -30.0), angle=150.0),
              dict(mesh='trees', texture='treesColor', position=(3.0, 3.5, -30.0), angle=150.0),
              dict(mesh='trees', texture='treesColor', position=(5.0, 3.5, -30.0), angle=150.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(1.5, -1.5, -6.0), angle=90.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(6.0, -1.5, -6.0), angle=90.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(-3.0, -1.5, -6.0), angle=90.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.5, -1.5, 5.5), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.5, -1.5, 9.5), angle=0.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(3.5, -1.5, 0.0), angle=90.0),
              dict(mesh='bridgitLevelTop', texture='bridgitLevelColor', position=(0.0, -1.5, 0.0), angle=90.0),
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

        # Step Right Up base
        shared2 = SharedObjects.get()
        bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['mesh'],
            'color_texture': self.preloaddata['tex'],
            'collision_mesh': self.preloaddata['collision_mesh'],
            'lighting': True,
            'background': False,
            'materials': [shared2.footing_material]})
        bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['mesh_bottom'],
            'color_texture': self.preloaddata['tex'],
            'lighting': False,
            'background': False})

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
    