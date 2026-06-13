# ba_meta require api 9

from __future__ import annotations
import bascenev1 as bs
from bascenev1._gameactivity import GameActivity
from bascenev1lib.actor.spaz import Spaz



class SetupTextUI:
    def __init__(self) -> None:
        activity = bs.getactivity()
        with activity.context:

            self.battle = bs.newnode(
                'text',
                attrs={
                    'text': 'SnowYoutube',
                    'scale': 0.85,
                    'shadow': 0.5,
                    'position': (51.5, 75),
                    'h_attach': 'left',
                    'v_attach': 'bottom',
                    'color': (1, 1, 1)
                }
            )

            self.discord_logo = bs.newnode(
                'image',
                attrs={
                    'texture': bs.gettexture('discordLogo'),
                    'position': (33, 60),
                    'scale': (35, 35),
                    'color': (0.4, 0.4, 1),
                    'attach': 'bottomLeft'
                }
            )

            self.discord_bg = bs.newnode(
                'image',
                attrs={
                    'texture': bs.gettexture('buttonSquare'),
                    'position': (34, 89),
                    'scale': (36, 27),
                    'color': (1.8, 0, 0),
                    'attach': 'bottomLeft'
                }
            )

            self.discord_icon = bs.newnode(
                'image',
                attrs={
                    'texture': bs.gettexture('nextLevelIcon'),
                    'position': (34, 88),
                    'scale': (28, 30),
                    'color': (1.5, 1.5, 1.5),
                    'attach': 'bottomLeft'
                }
            )

            self.discord_text = bs.newnode(
                'text',
                attrs={
                    'text': '       Únete al Discord\nCon el boton de stats',
                    'scale': 0.75,
                    'shadow': 0,
                    'position': (15.1, 50),
                    'h_attach': 'left',
                    'v_attach': 'bottom',
                    'color': (0.40, 0.40, 1.2)
                }
            )



# ba_meta export babase.Plugin
class features(bs.Plugin):

    def on_app_running(self) -> None:
        old = GameActivity.on_begin

        def new(self) -> None:
            old(self)

            SetupTextUI()

        GameActivity.on_begin = new
