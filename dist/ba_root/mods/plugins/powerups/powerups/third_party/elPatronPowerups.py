# ba_meta require api 8
from __future__ import annotations

_sp_ = ('\n')

import babase
import bauiv1 as bui

from bascenev1lib.actor import bomb
from bascenev1lib.actor import powerupbox as pupbox
from bascenev1lib.actor.spazbot import SpazBot
from bauiv1lib.popup import (PopupWindow, PopupMenu)
from bascenev1lib.mainmenu import (MainMenuActivity, MainMenuSession)
from bascenev1lib.actor.popuptext import PopupText
from bauiv1lib.confirm import ConfirmWindow
from bascenev1lib.actor.spaz import *
from bascenev1lib.actor.bomb import BombFactory
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor import spazbot as bots


if TYPE_CHECKING:
    pass


# === Mod made by @Patron_Modz ===

def getlanguage(text, subs: str = None, almacen: list = []):
    if almacen == []: almacen = list(range(1000))
    lang = bui.app.lang.language
    translate = {"Reset":
                     {"Spanish": "Reiniciar",
                      "English": "Reset",
                      "Portuguese": "Reiniciar"},
                 "Nothing":
                     {"Spanish": "Sin potenciadores",
                      "English": "No powerups",
                      "Portuguese": "Sem powerups"},
                 "Action 1":
                     {"Spanish": "Potenciadores",
                      "English": "Powerups",
                      "Portuguese": "Powerups"},
                 "Action 2":
                     {"Spanish": "ConfiguraciÃƒÂ³n",
                      "English": "Settings",
                      "Portuguese": "DefiniÃƒÂ§ÃƒÂµes"},
                 "Action 3":
                     {"Spanish": "Extras",
                      "English": "Extras",
                      "Portuguese": "Extras"},
                 "Action 4":
                     {"Spanish": "Tienda",
                      "English": "Store",
                      "Portuguese": "Loja"},
                 "Action 5":
                     {"Spanish": "Canjear cÃƒÂ³digo",
                      "English": "Enter Code",
                      "Portuguese": "CÃƒÂ³digo promocional"},
                 "Custom":
                     {"Spanish": "",
                      "English": "Customize",
                      "Portuguese": "Customizar"},
                 "Impairment Bombs":
                     {"Spanish": "Bombas menoscabo",
                      "English": "Hyperactive bombs",
                      "Portuguese": "Bombas hiperativas"},
                 "Speed":
                     {"Spanish": "Velocidad",
                      "English": "Speed",
                      "Portuguese": "Velocidade"},
                 "Fire Bombs":
                     {"Spanish": "Bombas de fuego",
                      "English": "Fire Bombs",
                      "Portuguese": "Bombas de fogo"},
                 "Ice Man":
                     {"Spanish": "Hombre de hielo",
                      "English": "Ice man",
                      "Portuguese": "Homem de gelo"},
                 "Fly Bombs":
                     {"Spanish": "Bombas expansivas",
                      "English": "Expansive bombs",
                      "Portuguese": "Bombas expansivas"},
                 "Goodbye":
                     {"Spanish": "Ã‚Â¡Hasta luego!",
                      "English": "Goodbye!",
                      "Portuguese": "Adeus!"},
                 "Healing Damage":
                     {"Spanish": "Auto-curaciÃƒÂ³n",
                      "English": "Healing Damage",
                      "Portuguese": "Auto-cura"},
                 "Tank Shield":
                     {"Spanish": "SÃƒÂºper blindaje",
                      "English": "Reinforced shield",
                      "Portuguese": "Escudo reforÃƒÂ§ado"},
                 "Red Shield":
                     {"Spanish": "Escudo rojo",
                      "English": "Red Shield",
                      "Portuguese": "Escudo vermelho"},
                 "Tank Shield PTG":
                     {"Spanish": "Porcentaje de disminuciÃƒÂ³n",
                      "English": "Percentage decreased",
                      "Portuguese": "Percentual reduzido"},
                 "Healing Damage PTG":
                     {"Spanish": "Porcentaje de recuperaciÃƒÂ³n de salud",
                      "English": "Percentage of health recovered",
                      "Portuguese": "Porcentagem de recuperaÃƒÂ§ÃƒÂ£o de saÃƒÂºde"},
                 "SY: BALL":
                     {"Spanish": "Esfera",
                      "English": "Sphere",
                      "Portuguese": "Esfera"},
                 "SY: Impact":
                     {"Spanish": "Especial",
                      "English": "Special",
                      "Portuguese": "Especial"},
                 "SY: Egg":
                     {"Spanish": "Huevito",
                      "English": "Egg shape",
                      "Portuguese": "Ovo"},
                 "Powerup Scale":
                     {"Spanish": "TamaÃƒÂ±o del potenciador",
                      "English": "Powerups size",
                      "Portuguese": "Tamanho de powerups"},
                 "Powerup With Shield":
                     {"Spanish": "Potenciadores con escudo",
                      "English": "Powerups with shield",
                      "Portuguese": "Powerups com escudo"},
                 "Powerup Time":
                     {"Spanish": "Mostrar Temporizador",
                      "English": "Show end time",
                      "Portuguese": "Mostrar cronÃƒÂ´metro"},
                 "Powerup Style":
                     {"Spanish": "Forma de los potenciadores",
                      "English": "Shape of powerup",
                      "Portuguese": "Forma de powerup"},
                 "Powerup Name":
                     {"Spanish": "Mostrar nombre en los potenciadores",
                      "English": "Show name on powerups",
                      "Portuguese": "Mostrar nome em powerups"},
                 "Percentage":
                     {"Spanish": "Probabilidad",
                      "English": "Show percentage",
                      "Portuguese": "Mostrar porcentagem"},
                 "Only Items":
                     {"Spanish": "SÃƒÂ³lo Accesorios",
                      "English": "Only utensils",
                      "Portuguese": "Apenas utensilios"},
                 "New":
                     {"Spanish": "Nuevo",
                      "English": "New",
                      "Portuguese": "Novo"},
                 "Only Bombs":
                     {"Spanish": "SÃƒÂ³lo Bombas",
                      "English": "Only bombs",
                      "Portuguese": "Apenas bombas"},
                 "Coins 0":
                     {"Spanish": "Monedas Insuficientes",
                      "English": "Insufficient coins",
                      "Portuguese": "Moedas insuficientes"},
                 "Purchase":
                     {"Spanish": "Compra realizada correctamente",
                      "English": "Successful purchase",
                      "Portuguese": "Compra Bem Sucedida"},
                 "Double Product":
                     {"Spanish": "Ya has comprado este artÃƒÂ­culo",
                      "English": "You've already bought this",
                      "Portuguese": "Voce ja comprou isto"},
                 "Bought":
                     {"Spanish": "Comprado",
                      "English": "Bought",
                      "Portuguese": "Comprou"},
                 "Confirm Purchase":
                     {
                         "Spanish": f'Tienes {subs} monedas. {_sp_} Ã‚Â¿Deseas comprar esto?',
                         "English": f'You have {subs} coins. {_sp_} Do you want to buy this?',
                         "Portuguese": f'VocÃƒÂª tem {subs} moedas. {_sp_} Deseja comprar isto?'},
                 "FireBombs Store":
                     {"Spanish": 'Bombas de fuego',
                      "English": 'Fire bombs',
                      "Portuguese": 'Bombas de incÃƒÂªndio'},
                 "Timer Store":
                     {"Spanish": 'Temporizador',
                      "English": 'Timer',
                      "Portuguese": 'Timer'},
                 "Percentages Store":
                     {"Spanish": 'Extras',
                      "English": 'Extras',
                      "Portuguese": 'Extras'},
                 "Block Option Store":
                     {
                         "Spanish": f"Uuups..{_sp_}Esta opciÃƒÂ³n estÃƒÂ¡ bloqueada.{_sp_} Para acceder a ella puedes {_sp_} comprarla en la tienda.{_sp_} Gracias...",
                         "English": f"Oooops...{_sp_}This option is blocked. {_sp_} To access it you can buy {_sp_} it in the store.{_sp_} Thank you...",
                         "Portuguese": f"Ooops...{_sp_}Esta opÃƒÂ§ÃƒÂ£o estÃƒÂ¡ bloqueada. {_sp_} Para acessÃƒÂ¡-lo, vocÃƒÂª pode {_sp_} comprÃƒÂ¡-lo na loja.{_sp_} Obrigado..."},
                 "True Code":
                     {"Spanish": "Ã‚Â¡CÃƒÂ³digo canjeado!",
                      "English": "Successful code!",
                      "Portuguese": "Ã‚Â¡CÃƒÂ³digo vÃƒÂ¡lido!"},
                 "False Code":
                     {"Spanish": "CÃƒÂ³digo ya canjeado",
                      "English": "Expired code",
                      "Portuguese": "CÃƒÂ³digo expirado"},
                 "Invalid Code":
                     {"Spanish": "CÃƒÂ³digo invÃƒÂ¡lido",
                      "English": "Invalid code",
                      "Portuguese": "CÃƒÂ³digo invÃƒÂ¡lido"},
                 "Reward Code":
                     {"Spanish": f"Ã‚Â¡Felicitaciones! Ã‚Â¡Ganaste {subs} monedas!",
                      "English": f"Congratulations! You've {subs} coins",
                      "Portuguese": f"ParabÃƒÂ©ns! VocÃƒÂª tem {subs} moedas"},
                 "Creator":
                     {"Spanish": "Mod creado por @PatrÃƒÂ³nModz",
                      "English": "Mod created by @PatrÃƒÂ³nModz",
                      "Portuguese": "Mod creado by @PatrÃƒÂ³nModz"},
                 "Mod Info":
                     {
                         "Spanish": f"Un mod genial que te permite gestionar {_sp_} los potenciadores a tu antojo. {_sp_} tambiÃƒÂ©n incluye 8 potenciadores extra{_sp_} dejando 17 en total... Ã‚Â¡Guay!",
                         "English": f"A cool mod that allows you to manage {_sp_} powerups at your whims. {_sp_} also includes 8 extra powerups{_sp_} leaving 17 in total... Wow!",
                         "Portuguese": f"Um mod legal que permite que vocÃƒÂª gerencie os{_sp_} powerups de de acordo com seus caprichos. {_sp_} tambÃƒÂ©m inclui 8 powerups extras,{_sp_} deixando 17 no total... Uau!"},
                 "Coins Message":
                     {"Spanish": f"Recompensa: {subs} Monedas",
                      "English": f"Reward: {subs} Coins",
                      "Portuguese": f"Recompensa: {subs} Moedas"},
                 "Coins Limit Message":
                     {
                         "Spanish": f"Ganaste {almacen[0]} Monedas.{_sp_} Pero has superado el lÃƒÂ­mite de {almacen[1]}",
                         "English": f"You won {almacen[0]} Coins. {_sp_} But you have exceeded the limit of {almacen[1]}",
                         "Portuguese": f"VocÃƒÂª ganhou {almacen[0]} Moedas. {_sp_} Mas vocÃƒÂª excedeu o limite de {almacen[1]}"},
                 }
    languages = ['Spanish', 'Portuguese', 'English']
    if lang not in languages: lang = 'English'

    if text not in translate:
        return text

    return translate[text][lang]


apg = babase.app.config

if apg.get('PPM Settings') is None:
    apg['PPM Settings'] = {}

def settings_distribution():
    defaults = {'Powerup Scale': 1.0, 'Powerup Style': 'Auto', 'Powerup Name': False, 'Powerup With Shield': False, 'Powerup Time': False, 'Tank Shield PTG': 50, 'Healing Damage PTG': 50}
    for k, v in defaults.items():
        if k not in apg['PPM Settings']:
            apg['PPM Settings'][k] = v
    return apg['PPM Settings']

apg['PPM Settings'] = settings_distribution()

config = apg['PPM Settings']


def default_powerups():
    defaults = {'Shield': 3, 'Punch': 3, 'Mine Bombs': 3, 'Impact Bombs': 3, 'Ice Bombs': 3, 'Triple': 3, 'Sticky Bombs': 3, 'Curse': 3, 'Health': 3, 'Speed': 3, 'Healing Damage': 3, 'Goodbye': 3, 'Ice Man': 3, 'Tank Shield': 3, 'Impairment Bombs': 3, 'Fire Bombs': 0, 'Fly Bombs': 3, 'Bomb Cena': 3, 'Red Shield': 3, 'supplies': 3, 'superhuman_healing': 1, 'super_shield': 2, 'T784_bomb': 3, 'blackhole_bomb': 1, 'Xfactor_bomb': 3, 'gloo_wall_bomb': 3, 'nitrogen_bomb': 3, 'stun_bomb': 3, 'teleport_bomb': 2, 's.m.b_bomb': 2, 'attraction_bomb': 2, 'cosmic_bomb': 1, 'electro-bombs': 3, 'cosmic_box': 1}
    if apg.get('PPM Powerups') is None:
        apg['PPM Powerups'] = defaults
    for k, v in defaults.items():
        if k not in apg['PPM Powerups']:
            apg['PPM Powerups'][k] = v
    return apg['PPM Powerups']


config['Powerups'] = default_powerups()

powerups = config['Powerups']

# === EXTRAS ===

GLOBAL = {"Tab": 'Action 1',
          "Cls Powerup": 0,
          "Coins Message": []}

_original_drop_bomb = None
all_bombs: list = ["curative", "s.m.b", "Xfactor"]
ex_calls: dict = dict()

class ExBuilder:
    cooldown_t784: float = 0.1
    hitpoints_t784: int = 840
    max_cure_t784: int = 180
    min_cure_t784: int = 35
    size_t784: float = 12.0
    damage_t784: int = 280
    duration_gw: int = 15
    duration_cb: int = 3
    extra_power_cb: float = 1.5
    damage_eb: int = 40
    repeat_eb: int = 9
    eff_eb: float = 0.2
    sombrita_hp: int = 3000
    shield_hitpoints_sh: int = 30
    percentage_sh: int = 25
    time_sh: float = 1.5
    reduction_ss: int = 90
    duration_ss: int = 7

ex = ExBuilder


# === STORE ===
def promo_codes():
    return {"G-Am54igO42Os": [True, 1100],
            "P-tRo8nM8dZ": [True, 2800],
            "Y-tU2B3S": [True, 500],
            "B-0mB3RYT2z": [True, 910],
            "B-Asd14mON9G0D": [True, 910],
            "D-rAcK0cJ23": [True, 910],
            "E-a27ZO6f3Y": [True, 600],
            "E-Am54igO42Os": [True, 600],
            "E-M4uN3K34XB": [True, 840],
            "PM-731ClcAF": [True, 50000]}


def store_items():
    return {"Buy Firebombs": False,
            "Buy Option": False,
            "Buy Percentage": False}


if apg.get('Bear Coin') is None:
    apg['Bear Coin'] = 0
    apg.apply_and_commit()

if apg.get('Bear Coin') is not None:
    if apg['Bear Coin'] <= 0:
        apg['Bear Coin'] = 0
    apg['Bear Coin'] = int(apg['Bear Coin'])

if apg.get('Bear Store') is None:
    apg['Bear Store'] = {}

for i, j in store_items().items():
    store = apg['Bear Store']
    if i not in store:
        if store.get(i) is None:
            store[i] = j
    apg.apply_and_commit()

STORE = apg['Bear Store']

if STORE.get('Promo Code') is None:
    STORE['Promo Code'] = promo_codes()

for i, x in promo_codes().items():
    pmcode = STORE['Promo Code']
    if i not in pmcode:
        if pmcode.get(i) is None:
            pmcode[i] = x

apg.apply_and_commit()


class BearStore:
    def __init__(self,
                 price: int = 1000,
                 value: str = '',
                 callback: Callable[[], None] = None):

        self.price = price
        self.value = value
        self.store = STORE[value]
        self.coins = apg['Bear Coin']
        self.callback = callback

    def buy(self):
        if not self.store:
            if self.coins >= (self.price):
                def confirm():
                    STORE[self.value] = True
                    apg['Bear Coin'] -= int(self.price)
                    bs.broadcastmessage(getlanguage('Purchase'), (0, 1, 0))
                    bs.getsound('cashRegister').play()
                    apg.apply_and_commit()
                    self.callback()

                ConfirmWindow(getlanguage('Confirm Purchase', subs=self.coins),
                              width=400, height=120, action=confirm,
                              ok_text=babase.Lstr(resource='okText'))
            else:
                bs.broadcastmessage(getlanguage('Coins 0'), (1, 0, 0))
                bs.getsound('error').play()
        else:
            bs.broadcastmessage(getlanguage('Double Product'), (1, 0, 0))
            bs.getsound('error').play()

    def __del__(self):
        apg['Bear Coin'] = int(apg['Bear Coin'])
        apg.apply_and_commit()


class PromoCode:
    def __init__(self, code: str = ''):
        self.code = code
        self.codes_store = STORE['Promo Code']
        if self.code in self.codes_store:
            self.code_type = STORE['Promo Code'][code]
            self.promo_code_expire = self.code_type[0]
            self.promo_code_amount = self.code_type[1]

    def __del__(self):
        apg['Bear Coin'] = int(apg['Bear Coin'])
        apg.apply_and_commit()

    def code_confirmation(self):
        if self.code != "":
            bs.broadcastmessage(
                babase.Lstr(resource='submittingPromoCodeText'), (0, 1, 0))
            bs.timer(2, babase.CallStrict(self.validate_code))

    def validate_code(self):
        if self.code in self.codes_store:
            if self.promo_code_expire:
                bs.timer(1.5, babase.CallStrict(self.successful_code))
                bs.broadcastmessage(getlanguage('True Code'), (0, 1, 0))
                bs.getsound('cheer').play()
                self.code_type[0] = False
            else:
                bs.broadcastmessage(getlanguage('False Code'), (1, 0, 0))
                bs.getsound('error').play()
        else:
            bs.broadcastmessage(getlanguage('Invalid Code'), (1, 0, 0))
            bs.getsound('error').play()

    def successful_code(self):
        apg['Bear Coin'] += self.promo_code_amount
        bs.broadcastmessage(getlanguage('Reward Code',
                                        subs=self.promo_code_amount), (0, 1, 0))
        bs.getsound('cashRegister2').play()


MainMenuActivity.super_transition_in = MainMenuActivity.on_transition_in


def new_on_transition_in(self):
    self.super_transition_in()
    limit = 8400
    bear_coin = apg['Bear Coin']
    coins_message = GLOBAL['Coins Message']
    try:
        if not (STORE['Buy Firebombs'] and
                STORE['Buy Option'] and
                STORE['Buy Percentage']):

            if coins_message != []:
                result = 0
                for i in coins_message:
                    result += i

                if not bear_coin >= (limit - 1):
                    bs.broadcastmessage(
                        getlanguage('Coins Message', subs=result), (0, 1, 0))
                    bs.getsound('cashRegister').play()
                else:
                    bs.broadcastmessage(getlanguage('Coins Limit Message',
                                                    almacen=[result, limit]),
                                        (1, 0, 0))
                    bs.getsound('error').play()
                self.bear_coin_message = True
                GLOBAL['Coins Message'] = []
    except:
        pass


SpazBot.super_handlemessage = SpazBot.handlemessage


def bot_handlemessage(self, msg: Any):
    self.super_handlemessage(msg)
    if isinstance(msg, bs.DieMessage):
        if not self.die:
            self.die = True
            self.limit = 8400
            self.free_coins = random.randint(1, 25)
            self.bear_coins = apg['Bear Coin']

            if not self.bear_coins >= (self.limit):
                self.bear_coins += self.free_coins
                GLOBAL['Coins Message'].append(self.free_coins)

                if self.bear_coins >= (self.limit):
                    self.bear_coins = self.limit

                apg['Bear Coin'] = int(self.bear_coins)
                apg.apply_and_commit()

            else:
                GLOBAL['Coins Message'].append(self.free_coins)


def cls_pow_color():
    return [(1, 0.1, 0.1), (0.1, 0.5, 0.9), (0.1, 0.9, 0.9),
            (0.1, 0.9, 0.1), (0.1, 1, 0.5), (1, 1, 0.2), (2, 0.5, 0.5),
            (1, 0, 6)]


def random_color():
    a = random.random() * 3
    b = random.random() * 3
    c = random.random() * 3
    return (a, b, c)


def powerup_dist():
    return (('triple_bombs', powerups['Triple']),
            ('ice_bombs', powerups['Ice Bombs']),
            ('punch', powerups['Punch']),
            ('impact_bombs', powerups['Impact Bombs']),
            ('land_mines', powerups['Mine Bombs']),
            ('sticky_bombs', powerups['Sticky Bombs']),
            ('shield', powerups['Shield']),
            ('health', powerups['Health']),
            ('curse', powerups['Curse']),
            ('speed', powerups['Speed']),
            ('health_damage', powerups['Healing Damage']),
            ('goodbye', powerups['Goodbye']),
            ('ice_man', powerups['Ice Man']),
            ('tank_shield', powerups['Tank Shield']),
            ('impairment_bombs', powerups['Impairment Bombs']),
            ('fire_bombs', powerups['Fire Bombs']),
            ('fly_bombs', powerups['Fly Bombs']),
            ('bomb_cena', powerups['Bomb Cena']),
            ('red_shield', powerups['Red Shield']),
            ('supplies', powerups['supplies']),
            ('superhuman_healing', powerups['superhuman_healing']),
            ('super_shield', powerups['super_shield']),
            ('T784_bomb', powerups['T784_bomb']),
            ('blackhole_bomb', powerups['blackhole_bomb']),
            ('Xfactor_bomb', powerups['Xfactor_bomb']),
            ('gloo_wall_bomb', powerups['gloo_wall_bomb']),
            ('attraction_bomb', powerups['attraction_bomb']),
            ('cosmic_bomb', powerups['cosmic_bomb']),
            ('electro-bombs', powerups['electro-bombs']),
            ('cosmic_box', powerups['cosmic_box']),
            ('nitrogen_bomb', powerups['nitrogen_bomb']),
            ('stun_bomb', powerups['stun_bomb']),
            ('teleport_bomb', powerups['teleport_bomb']),
            ('s.m.b_bomb', powerups['s.m.b_bomb']))


def percentage_tank_shield():
    percentage = config['Tank Shield PTG']
    percentage_text = ('0.') + str(percentage)
    return float(percentage_text)


def percentage_health_damage():
    percentage = config['Healing Damage PTG']
    percentage_text = ('0.') + str(percentage)
    return float(percentage_text)


# === Modify class ===

class NewPowerupBoxFactory(pupbox.PowerupBoxFactory):
    def __init__(self) -> None:
        super().__init__()
        self.tex_speed = bs.gettexture('powerupSpeed')
        self.tex_health_damage = bs.gettexture('heart')
        self.tex_goodbye = bs.gettexture('achievementOnslaught')
        self.tex_ice_man = bs.gettexture('ouyaUButton')
        self.tex_tank_shield = bs.gettexture('achievementSuperPunch')
        self.tex_impairment_bombs = bs.gettexture('levelIcon')
        self.tex_fire_bombs = bs.gettexture('ouyaOButton')
        self.tex_fly_bombs = bs.gettexture('star')
        self.tex_bomb_cena = bs.gettexture('plusButton')
        self.tex_red_shield = bs.gettexture('crossOutMask')
        self.tex_supplies = bs.gettexture('logoEaster')
        self.tex_superhuman_healing = bs.gettexture('achievementStayinAlive')
        self.tex_super_shield = bs.gettexture('ouyaOButton')
        self.tex_T784_bomb = bs.gettexture('star')
        self.tex_blackhole_bomb = bs.gettexture('replayIcon')
        self.tex_Xfactor_bomb = bs.gettexture('textClearButton')
        self.tex_smb_bomb = bs.gettexture('powerupCurse')

        self.tex_nitrogen_bomb = bs.gettexture('powerupIceBombs')
        self.tex_cosmic_bomb = bs.gettexture('achievementFootballShutout')
        self.tex_electro_bombs = bs.gettexture('levelIcon')
        self.tex_cosmic_box = bs.gettexture('achievementSuperPunch')
        self.tex_stun_bomb = bs.gettexture('eggTex3')
        self.tex_teleport_bomb = bs.gettexture('rightButton')
        self.tex_gloo_wall_bomb = bs.gettexture('bombColorIce')
        self.tex_attraction_bomb = bs.gettexture('backIcon')

        self._powerupdist = []
        for powerup, freq in powerup_dist():
            for _i in range(int(freq)):
                self._powerupdist.append(powerup)

    def get_random_powerup_type(self, forcetype=None, excludetypes=None):

        try:
            self.mapa = bs.getactivity()._map.getname()
        except:
            self.mapa = None

        speed_banned_maps = ['Hockey Stadium', 'Lake Frigid', 'Happy Thoughts']

        if self.mapa in speed_banned_maps:
            powerup_disable = ['speed']
        else:
            powerup_disable = []

        if excludetypes is None:
            excludetypes = []
        if forcetype:
            ptype = forcetype
        else:
            if self._lastpoweruptype == 'curse':
                ptype = 'health'
            else:
                while True:
                    ptype = self._powerupdist[random.randint(
                        0,
                        len(self._powerupdist) - 1)]
                    if ptype not in excludetypes and ptype not in powerup_disable: break
        self._lastpoweruptype = ptype
        return ptype


def fire_effect(self):
    if self.node.exists():
        bs.emitfx(position=self.node.position,
                  scale=3, count=50 * 2, spread=0.3,
                  chunk_type='sweat')
    else:
        self.fire_effect_time = None


###########BOMBS
Bomb._pm_old_bomb = Bomb.__init__


def _bomb_init(self,
               position: Sequence[float] = (0.0, 1.0, 0.0),
               velocity: Sequence[float] = (0.0, 0.0, 0.0),
               bomb_type: str = 'normal',
               blast_radius: float = 2.0,
               bomb_scale: float = 1.0,
               source_player: bs.Player = None,
               owner: bs.Node = None):

    self.bm_type = bomb_type
    new_bomb_type = 'ice' if bomb_type in ['ice_bubble', 'impairment', 'fire', 'fly'] else bomb_type

    # Call original __init__
    try:
        _src = bs.existing(source_player)
        _bombcena = _src is not None and getattr(getattr(_src, 'actor', None), '_bombcena_active', False)
    except Exception:
        _bombcena = False
    self._pm_old_bomb(position=position,
                      velocity=velocity,
                      bomb_type=new_bomb_type,
                      blast_radius=blast_radius,
                      bomb_scale=bomb_scale,
                      source_player=source_player,
                      owner=owner)

    tex = self.node.color_texture

    if self.bm_type == 'ice_bubble':
        self.bomb_type = self.bm_type
        self.node.mesh = None
        self.shield_ice = bs.newnode('shield', owner=self.node,
                                     attrs={'color': (0.5, 1.0, 7.0), 'radius': 0.6})
        self.node.connectattr('position', self.shield_ice, 'position')

    elif self.bm_type == 'fire':
        self.bomb_type = self.bm_type
        self.node.mesh = None
        self.shield_fire = bs.newnode('shield', owner=self.node,
                                      attrs={'color': (6.5, 6.5, 2.0), 'radius': 0.6})
        self.node.connectattr('position', self.shield_fire, 'position')
        self.fire_effect_time = bs.Timer(0.1, babase.CallPartial(fire_effect, self), repeat=True)

    elif self.bm_type == 'impairment':
        self.bomb_type = self.bm_type
        tex = bs.gettexture('eggTex3')

    elif self.bm_type == 'fly':
        self.bomb_type = self.bm_type
        tex = bs.gettexture('eggTex1')

    self.node.color_texture = tex
    self.hit_subtype = self.bomb_type

    if self.bomb_type == 'ice_bubble':
        self.blast_radius *= 1.2
    elif self.bomb_type == 'fly':
        self.blast_radius *= 2.2

    if _bombcena:
        self.blast_radius *= 2.0
        bs.animate(self.node, 'mesh_scale', {0: 0, 0.1: 2.5})
    _n = self.node
    bs.timer(0.3, lambda: bs.animate(_n, 'mesh_scale', {0: 2.0}) if _bombcena and _n and _n.exists() else None)
    bs.timer(0.3, lambda: bs.animate(_n, "mesh_scale", {0: 2.5}) if _bombcena and _n and _n.exists() else None)




def bomb_handlemessage(self, msg: Any) -> Any:
    assert not self.expired

    if isinstance(msg, bs.DieMessage):
        if self.node:
            self.node.delete()

    elif isinstance(msg, bomb.ExplodeHitMessage):
        node = bs.getcollision().opposingnode
        assert self.node
        nodepos = self.node.position
        try:
            _src = bs.existing(self._source_player)
            _bombcena = _src is not None and getattr(getattr(_src, 'actor', None), '_bombcena_active', False)
        except Exception:
            _bombcena = False
        mag = 2000.0 * (2.0 if _bombcena else 1.0)
        if self.blast_type in ('ice', 'ice_bubble'):
            mag *= 0.5
        elif self.blast_type == 'land_mine':
            mag *= 2.5
        elif self.blast_type == 'tnt':
            mag *= 2.0
        elif self.blast_type == 'fire':
            mag *= 0.6
        elif self.blast_type == 'fly':
            mag *= 5.5

        node.handlemessage(
            bs.HitMessage(pos=nodepos,
                          velocity=(0, 0, 0),
                          magnitude=mag,
                          hit_type=self.hit_type,
                          hit_subtype=self.hit_subtype,
                          radius=self.radius,
                          source_player=babase.existing(self._source_player)))
        if self.blast_type in ('ice', 'ice_bubble'):
            bomb.BombFactory.get().freeze_sound.play(10, position=nodepos)
            node.handlemessage(bs.FreezeMessage())

    return None


def powerup_translated(self, type: str):
    powerups_names = {'triple_bombs': babase.Lstr(
        resource='helpWindow.' + 'powerupBombNameText'),
                      'ice_bombs': babase.Lstr(
                          resource='helpWindow.' + 'powerupIceBombsNameText'),
                      'punch': babase.Lstr(
                          resource='helpWindow.' + 'powerupPunchNameText'),
                      'impact_bombs': babase.Lstr(
                          resource='helpWindow.' + 'powerupImpactBombsNameText'),
                      'land_mines': babase.Lstr(
                          resource='helpWindow.' + 'powerupLandMinesNameText'),
                      'sticky_bombs': babase.Lstr(
                          resource='helpWindow.' + 'powerupStickyBombsNameText'),
                      'shield': babase.Lstr(
                          resource='helpWindow.' + 'powerupShieldNameText'),
                      'health': babase.Lstr(
                          resource='helpWindow.' + 'powerupHealthNameText'),
                      'curse': babase.Lstr(
                          resource='helpWindow.' + 'powerupCurseNameText'),
                      'speed': getlanguage('Speed'),
                      'health_damage': getlanguage('Healing Damage'),
                      'goodbye': getlanguage('Goodbye'),
                      'ice_man': getlanguage('Ice Man'),
                      'tank_shield': getlanguage('Tank Shield'),
                      'impairment_bombs': getlanguage('Impairment Bombs'),
                      'fire_bombs': getlanguage('Fire Bombs'),
                      'fly_bombs': getlanguage('Fly Bombs'),
                      'red_shield': getlanguage('Red Shield')}
    self.texts['Name'].text = powerups_names[type]


###########POWERUP
pupbox.PowerupBox._old_pbx_ = pupbox.PowerupBox.__init__


def _pbx_(self, position: Sequence[float] = (0.0, 1.0, 0.0),
          poweruptype: str = 'triple_bombs',
          expire: bool = True):
    self.news: list = []
    for x, i in powerup_dist(): self.news.append(x)

    self.box: list = []
    self.texts = {}
    self.news = self.news[9:]
    self.box.append(poweruptype)
    self.npowerup = self.box[0]
    factory = NewPowerupBoxFactory.get()

    if self.npowerup in self.news:
        new_poweruptype = 'shield'
    else:
        new_poweruptype = poweruptype
    self._old_pbx_(position, new_poweruptype, expire)

    type = new_poweruptype
    tex = self.node.color_texture
    mesh = self.node.mesh

    if self.npowerup == 'cosmic_bomb':
        type = self.npowerup
        tex = factory.tex_cosmic_bomb
    elif self.npowerup == 'electro-bombs':
        type = self.npowerup
        tex = factory.tex_electro_bombs
    elif self.npowerup == 'cosmic_box':
        type = self.npowerup
        tex = factory.tex_cosmic_box
    elif self.npowerup == 's.m.b_bomb':
        type = self.npowerup
        tex = factory.tex_smb_bomb
    elif self.npowerup == 'speed':
        type = self.npowerup
        tex = factory.tex_speed
    elif self.npowerup == 'health_damage':
        type = self.npowerup
        tex = factory.tex_health_damage
    elif self.npowerup == 'goodbye':
        type = self.npowerup
        tex = factory.tex_goodbye
    elif self.npowerup == 'ice_man':
        type = self.npowerup
        tex = factory.tex_ice_man
    elif self.npowerup == 'tank_shield':
        type = self.npowerup
        tex = factory.tex_tank_shield
    elif self.npowerup == 'impairment_bombs':
        type = self.npowerup
        tex = factory.tex_impairment_bombs
    elif self.npowerup == 'fire_bombs':
        type = self.npowerup
        tex = factory.tex_fire_bombs
    elif self.npowerup == 'fly_bombs':
        type = self.npowerup
        tex = factory.tex_fly_bombs
    elif self.npowerup == 'bomb_cena':
        type = self.npowerup
        tex = factory.tex_bomb_cena
    elif self.npowerup == 'supplies':
        type = self.npowerup
        tex = factory.tex_supplies
    elif self.npowerup == 'superhuman_healing':
        type = self.npowerup
        tex = factory.tex_superhuman_healing
    elif self.npowerup == 'super_shield':
        type = self.npowerup
        tex = factory.tex_super_shield
    elif self.npowerup == 'T784_bomb':
        type = self.npowerup
        tex = factory.tex_T784_bomb
    elif self.npowerup == 'blackhole_bomb':
        type = self.npowerup
        tex = factory.tex_blackhole_bomb
    elif self.npowerup == 'Xfactor_bomb':
        type = self.npowerup
        tex = factory.tex_Xfactor_bomb
    elif self.npowerup == 'gloo_wall_bomb':
        type = self.npowerup
        tex = factory.tex_gloo_wall_bomb
    elif self.npowerup == 'attraction_bomb':
        type = self.npowerup
        tex = factory.tex_attraction_bomb
    elif self.npowerup == 'nitrogen_bomb':
        type = self.npowerup
        tex = factory.tex_nitrogen_bomb
    elif self.npowerup == 'stun_bomb':
        type = self.npowerup
        tex = factory.tex_stun_bomb
    elif self.npowerup == 'teleport_bomb':
        type = self.npowerup
        tex = factory.tex_teleport_bomb
    elif self.npowerup == 'red_shield':
        type = self.npowerup
        tex = factory.tex_red_shield

    self.poweruptype = type
    self.node.mesh = mesh
    self.node.color_texture = tex
    n_scale = config['Powerup Scale']
    style = config['Powerup Style']

    curve = bs.animate(self.node, 'mesh_scale', {0: 0, 0.14: 1.6, 0.2: n_scale})
    bs.timer(0.2, curve.delete)

    def util_text(type: str, text: str, scale: float = 1,
                  color: list = [1, 1, 1],
                  position: list = [0, 0.7, 0], colors_name: bool = False):
        m = bs.newnode('math', owner=self.node, attrs={'input1':
                                                           (position[0],
                                                            position[1],
                                                            position[2]),
                                                       'operation': 'add'})
        self.node.connectattr('position', m, 'input2')
        self.texts[type] = bs.newnode('text', owner=self.node,
                                      attrs={'text': str(text),
                                             'in_world': True,
                                             'scale': 0.02,
                                             'shadow': 0.5,
                                             'flatness': 1.0,
                                             'color': (
                                             color[0], color[1], color[2]),
                                             'h_align': 'center'})
        m.connectattr('output', self.texts[type], 'position')
        bs.animate(self.texts[type], 'scale',
                   {0: 0.017, 0.4: 0.017, 0.5: 0.01 * scale})

        if colors_name:
            bs.animate_array(self.texts[type], 'color', 3,
                             {0: (1, 0, 0),
                              0.2: (1, 0.5, 0),
                              0.4: (1, 1, 0),
                              0.6: (0, 1, 0),
                              0.8: (0, 1, 1),
                              1.0: (1, 0, 1),
                              1.2: (1, 0, 0)})

    def update_time(time):
        if self.texts['Time'].exists():
            self.texts['Time'].text = str(time)

    if config['Powerup Time']:
        interval = int(pupbox.DEFAULT_POWERUP_INTERVAL)
        time2 = (interval - 1)
        time = 1

        util_text('Time', time2, scale=1.5, color=(2, 2, 2),
                  position=[0, 0.9, 0], colors_name=False)

        while (interval + 3):
            bs.timer(time - 1, babase.CallPartial(update_time, f'{time2}s'))

            if time2 == 0:
                break

            time += 1
            time2 -= 1

    if config['Powerup With Shield']:
        scale = config['Powerup Scale']
        self.shield = bs.newnode('shield', owner=self.node,
                                 attrs={'color': (1, 1, 0),
                                        'radius': 1.3 * scale})
        self.node.connectattr('position', self.shield, 'position')
        bs.animate_array(self.shield, 'color', 3,
                         {0: (2, 0, 0), 0.5: (0, 2, 0), 1: (0, 1, 6),
                          1.5: (2, 0, 0)}, True)

    if config['Powerup Name']:
        util_text('Name', self.poweruptype, scale=1.2,
                  position=[0, 0.4, 0], colors_name=True)
        powerup_translated(self, self.poweruptype)

    if style == 'SY: BALL':
        self.node.mesh = bs.getmesh('frostyPelvis')
    elif style == 'SY: Impact':
        self.node.mesh = bs.getmesh('impactBomb')
    elif style == 'SY: Egg':
        self.node.mesh = bs.getmesh('egg')


###########SPAZ
def _speed_off_flash(self):
    if self.node:
        factory = NewPowerupBoxFactory.get()
        self.node.billboard_texture = factory.tex_speed
        self.node.billboard_opacity = 1.0
        self.node.billboard_cross_out = True


def _speed_wear_off(self):
    if self.node:
        self.node.hockey = False
        self.node.billboard_opacity = 0.0
        bs.getsound('powerdown01').play()


def _ice_man_off_flash(self):
    if self.node:
        factory = NewPowerupBoxFactory.get()
        self.node.billboard_texture = factory.tex_ice_man
        self.node.billboard_opacity = 1.0
        self.node.billboard_cross_out = True


def _ice_man_wear_off(self):
    if self.node:
        f = self.color[0]
        i = (0, 1, 4)

        bomb = self.bmb_color[0]
        if bomb != 'ice_bubble':
            self.bomb_type = bomb
        else:
            self.bomb_type = 'normal'

        self.freeze_punch = False
        self.node.billboard_opacity = 0.0
        bs.animate_array(self.node, 'color', 3, {0: f, 0.3: i, 0.6: f})
        bs.getsound('powerdown01').play()


def _bombcena_wear_off(self):
    self._bombcena_active = False
    self._bombcena_wear_off = lambda: (setattr(self, '_bombcena_active', False), bs.getsound('powerdown01').play() if self.node else None)
    bs.getsound('powerdown01').play()
    if self.node:
        self.node.billboard_opacity = 0.0

Spaz._pm2_spz_old = Spaz.__init__


def _init_spaz_(self, *args, **kwargs):
    self._pm2_spz_old(*args, **kwargs)
    self.edg_eff = False
    self.kill_eff = False
    self.freeze_punch = False
    self.die = False
    self.color: list = []
    self.color.append(self.node.color)

    self.tankshield = {"Tank": False,
                       "Reduction": False,
                       "Shield": None}
    self._bombcena_active = False
    self._bombcena_wear_off = lambda: (setattr(self, '_bombcena_active', False), bs.getsound('powerdown01').play() if self.node else None)


Spaz._super_on_punch_press = Spaz.on_punch_press


def spaz_on_punch_press(self) -> None:
    self._super_on_punch_press()

    if self.tankshield['Tank']:
        try:
            self.tankshield['Reduction'] = True

            shield = bs.newnode('shield', owner=self.node,
                                attrs={'color': (4, 1, 4), 'radius': 1.3})
            self.node.connectattr('position_center', shield, 'position')

            self.tankshield['Shield'] = shield
        except:
            pass


Spaz._super_on_punch_release = Spaz.on_punch_release


def spaz_on_punch_release(self) -> None:
    self._super_on_punch_release()
    try:
        self.tankshield['Shield'].delete()
        self.tankshield['Reduction'] = False
    except:
        pass


def new_get_bomb_type_tex(self):
    factory = NewPowerupBoxFactory.get()
    if self.bomb_type == 'sticky':
        return factory.tex_sticky_bombs
    if self.bomb_type == 'ice':
        return factory.tex_ice_bombs
    if self.bomb_type == 'impact':
        return factory.tex_impact_bombs
    if self.bomb_type == 'impairment':
        return factory.tex_impairment_bombs
    if self.bomb_type == 'fire':
        return factory.tex_fire_bombs
    if self.bomb_type == 'fly':
        return factory.tex_fly_bombs
    return factory.tex_impact_bombs
    # raise ValueError('invalid bomb type')


def new_handlemessage(self, msg: Any) -> Any:
    assert not self.expired

    if isinstance(msg, bs.PickedUpMessage):
        if self.node:
            self.node.handlemessage('hurt_sound')
            self.node.handlemessage('picked_up')

        self._num_times_hit += 1

    elif isinstance(msg, bs.ShouldShatterMessage):
        bs.timer(0.001, babase.CallStrict(self.shatter))

    elif isinstance(msg, bs.ImpactDamageMessage):
        bs.timer(0.001, babase.CallPartial(self._hit_self, msg.intensity))

    elif isinstance(msg, bs.PowerupMessage):
        factory = NewPowerupBoxFactory.get()
        if self._dead or not self.node:
            return True
        if self.pick_up_powerup_callback is not None:
            self.pick_up_powerup_callback(self)
        if msg.poweruptype == 'triple_bombs':
            tex = PowerupBoxFactory.get().tex_bomb
            self._flash_billboard(tex)
            self.set_bomb_count(3)
            if self.powerups_expire:
                self.node.mini_billboard_1_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_1_start_time = t_ms
                self.node.mini_billboard_1_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._multi_bomb_wear_off_timer = (bs.Timer(
                    (POWERUP_WEAR_OFF_TIME - 2000),
                    babase.CallStrict(self._multi_bomb_wear_off_flash)))
                self._multi_bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    babase.CallStrict(self._multi_bomb_wear_off)))
        elif msg.poweruptype == 'land_mines':
            self.set_land_mine_count(min(self.land_mine_count + 3, 3))
        elif msg.poweruptype == 'impact_bombs':
            self.bomb_type = 'impact'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    babase.CallStrict(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    babase.CallStrict(self._bomb_wear_off)))
        elif msg.poweruptype == 'sticky_bombs':
            self.bomb_type = 'sticky'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    babase.CallStrict(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    babase.CallStrict(self._bomb_wear_off)))
        elif msg.poweruptype == 'punch':
            self._has_boxing_gloves = True
            tex = PowerupBoxFactory.get().tex_punch
            self._flash_billboard(tex)
            self.equip_boxing_gloves()
            if self.powerups_expire:
                self.node.boxing_gloves_flashing = False
                self.node.mini_billboard_3_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_3_start_time = t_ms
                self.node.mini_billboard_3_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._boxing_gloves_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    bs.WeakCall(self._gloves_wear_off_flash)))
                self._boxing_gloves_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    bs.WeakCall(self._gloves_wear_off),))
        elif msg.poweruptype == 'shield':
            factory = SpazFactory.get()
            self.equip_shields(decay=factory.shield_decay_rate > 0)
        elif msg.poweruptype == 'curse':
            self.curse()
        elif msg.poweruptype == 'ice_bombs':
            self.bomb_type = 'ice'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    bs.WeakCall(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    bs.WeakCall(self._bomb_wear_off)))
        elif msg.poweruptype == 'health':
            if self.edg_eff:
                f = self.color[0]
                r = (2, 0, 0)
                g = (0, 2, 0)
                bs.animate_array(self.node, 'color', 3, {0: r, 0.6: g, 1.0: f})
                self.edg_eff = False
            if self._cursed:
                self._cursed = False
                factory = SpazFactory.get()
                for attr in ['materials', 'roller_materials']:
                    materials = getattr(self.node, attr)
                    if factory.curse_material in materials:
                        setattr(
                            self.node, attr,
                            tuple(m for m in materials
                                  if m != factory.curse_material))
                self.node.curse_death_time = 0
            self.hitpoints = self.hitpoints_max
            self._flash_billboard(PowerupBoxFactory.get().tex_health)
            self.node.hurt = 0
            self._last_hit_time = None
            self._num_times_hit = 0

        elif msg.poweruptype == 'tank_shield':
            self.tankshield['Tank'] = True
            self.edg_eff = False
            tex = factory.tex_tank_shield
            self._flash_billboard(tex)

        elif msg.poweruptype == 'health_damage':
            tex = factory.tex_health_damage
            self.edg_eff = True
            f = self.color[0]
            i = (2, 0.5, 2)
            bs.animate_array(self.node, 'color', 3, {0: i, 0.5: i, 0.6: f})
            self._flash_billboard(tex)
            self.tankshield['Tank'] = False
            self.freeze_punch = False

        elif msg.poweruptype == 'goodbye':
            tex = factory.tex_goodbye
            self._flash_billboard(tex)
            self.kill_eff = True

        elif msg.poweruptype == 'bomb_cena':
            tex = factory.tex_bomb_cena
            self._flash_billboard(tex)
            self._bombcena_active = True
            if self.powerups_expire:
                bomb_cena_time = POWERUP_WEAR_OFF_TIME
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (t_ms + bomb_cena_time)
                self._bombcena_wear_off_flash_timer = (bs.Timer(
                    bomb_cena_time - 2000,
                    bs.WeakCall(self._bomb_wear_off_flash)))
                self._bombcena_timer = (bs.Timer(
                    bomb_cena_time,
                    babase.CallStrict(self._bombcena_wear_off)))


        elif msg.poweruptype == 'red_shield':
            factory = NewPowerupBoxFactory.get()
            tex = factory.tex_red_shield
            self._flash_billboard(tex)
            self.node.handlemessage(bs.PowerupMessage(poweruptype='shield'))
            self.node.handlemessage(bs.PowerupAcceptMessage())
            _owner = self
            def _apply_red_color() -> None:
                if _owner.shield and _owner.shield.exists():
                    _owner.shield.color = (5.0, 0.0, 0.0)
            bs.timer(0.01, _apply_red_color)
            def _watch_shield() -> None:
                if not _owner.node or not _owner.node.exists():
                    return
                if not _owner.shield:
                    pos = tuple(_owner.node.position)
                    bs.emitfx(position=pos, count=40, scale=2.0, spread=1.5, chunk_type='spark', emit_type='chunks')
                    bs.emitfx(position=pos, count=30, scale=3.0, spread=1.0, chunk_type='rock', emit_type='tendrils', tendril_type='smoke')
                    owner_node = _owner.node
                    for n in bs.getnodes():
                        if n.getnodetype() != 'spaz' or n == owner_node:
                            continue
                        npos = n.position
                        dx = npos[0] - pos[0]
                        dy = npos[1] - pos[1]
                        dz = npos[2] - pos[2]
                        dist = max(0.01, (dx**2 + dy**2 + dz**2)**0.5)
                        fx = dx/dist * 3000.0
                        fy = dy/dist * 3000.0 + 800.0
                        fz = dz/dist * 3000.0
                        n.handlemessage(bs.HitMessage(
                            pos=pos,
                            velocity=(fx, fy, fz),
                            magnitude=2000.0,
                            hit_type='explosion',
                            hit_subtype='normal',
                            radius=2.5,
                            source_player=None))
                    return
                bs.timer(0.1, _watch_shield)
            bs.timer(0.05, _watch_shield)

        elif msg.poweruptype == 'fly_bombs':
            self.bomb_type = 'fly'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    bs.WeakCall(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    bs.WeakCall(self._bomb_wear_off)))

        elif msg.poweruptype == 'fire_bombs':
            self.bomb_type = 'fire'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    bs.WeakCall(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    bs.WeakCall(self._bomb_wear_off)))

        elif msg.poweruptype == 'impairment_bombs':
            self.bomb_type = 'impairment'
            tex = self._get_bomb_type_tex()
            self._flash_billboard(tex)
            if self.powerups_expire:
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (
                    t_ms + POWERUP_WEAR_OFF_TIME)
                self._bomb_wear_off_flash_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME - 2000,
                    bs.WeakCall(self._bomb_wear_off_flash)))
                self._bomb_wear_off_timer = (bs.Timer(
                    POWERUP_WEAR_OFF_TIME,
                    bs.WeakCall(self._bomb_wear_off)))

        elif msg.poweruptype == 'ice_man':
            tex = factory.tex_ice_man
            self.bomb_type = 'ice_bubble'
            self.freeze_punch = True
            self.edg_eff = False
            self.node.color = (0, 1, 4)
            self._flash_billboard(tex)

            if self.powerups_expire:
                ice_man_time = 17000
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (t_ms + ice_man_time)

                self.ice_man_flash_timer = (bs.Timer(
                    ice_man_time - 2000,
                    babase.CallPartial(_ice_man_off_flash, self)))

                self.ice_man_timer = (bs.Timer(ice_man_time,
                                               babase.CallPartial(_ice_man_wear_off,
                                                           self)))

        elif msg.poweruptype == 'speed':
            self.node.hockey = True
            tex = factory.tex_speed
            self._flash_billboard(tex)
            if self.powerups_expire:
                speed_time = 15000
                self.node.mini_billboard_2_texture = tex
                t_ms = int(bs.time() * 1000)
                assert isinstance(t_ms, int)
                self.node.mini_billboard_2_start_time = t_ms
                self.node.mini_billboard_2_end_time = (t_ms + speed_time)

                self.speed_flash_timer = (bs.Timer(
                    speed_time - 2000,
                    babase.CallPartial(_speed_off_flash, self)))

                self.speed_timer = (bs.apptimer(speed_time,
                                                babase.CallPartial(_speed_wear_off,
                                                            self)))

        # EX Powerups dispatch
        ex_tags = ['s.m.b_bomb', 'supplies','superhuman_healing','super_shield','T784_bomb','blackhole_bomb','Xfactor_bomb','gloo_wall_bomb','nitrogen_bomb','stun_bomb','teleport_bomb','attraction_bomb','cosmic_bomb','electro-bombs','cosmic_box']
        if msg.poweruptype in ex_tags:
            self.ex_powerup_call(msg.poweruptype)

        self.bmb_color: list = []
        self.bmb_color.append(self.bomb_type)

        self.node.handlemessage('flash')
        if msg.sourcenode:
            msg.sourcenode.handlemessage(bs.PowerupAcceptMessage())
        return True

    elif isinstance(msg, bs.FreezeMessage):
        if not self.node:
            return None
        if self.node.invincible:
            SpazFactory.get().block_sound.play(1.0, position=self.node.position)
            return None
        if self.shield:
            return None
        if not self.frozen:
            self.frozen = True
            self.node.frozen = True
            bs.timer(5.0, babase.CallPartial(self.handlemessage,
                                      bs.ThawMessage()))
            if self.hitpoints <= 0:
                self.shatter()
        if self.freeze_punch:
            self.handlemessage(bs.ThawMessage())

    elif isinstance(msg, bs.ThawMessage):
        if self.frozen and not self.shattered and self.node:
            self.frozen = False
            self.node.frozen = False

    elif isinstance(msg, bs.HitMessage):
        if not self.node:
            return None
        if self.node.invincible:
            SpazFactory.get().block_sound.play(1.0, position=self.node.position)
            return True

        local_time = int(bs.time() * 1000)
        assert isinstance(local_time, int)
        if (self._last_hit_time is None
            or local_time - self._last_hit_time > 1000):
            self._num_times_hit += 1
            self._last_hit_time = local_time

        mag = msg.magnitude * self.impact_scale
        velocity_mag = msg.velocity_magnitude * self.impact_scale
        damage_scale = 0.22

        def fire_effect():
            if not self.shield:
                if self.node.exists():
                    bs.emitfx(position=self.node.position,
                              scale=3, count=50 * 2, spread=0.3,
                              chunk_type='sweat')
                    self.node.handlemessage('celebrate', 560)
                else:
                    self._fire_time = None
            else:
                self._fire_time = None

        def fire(time, damage):
            if not self.shield and not self._dead:
                self.hitpoints -= damage
                bs.show_damage_count(f'-{damage}HP',
                                         self.node.position,
                                         msg.force_direction)
                bs.getsound('fuse01').play()

            if duration != time:
                self._fire_time = bs.Timer(0.1, babase.CallStrict(fire_effect),
                                           repeat=True)
            else:
                self._fire_time = None

            if self.hitpoints < 0:
                self.node.handlemessage(bs.DieMessage())

        if msg.hit_subtype == 'fly':
            damage_scale = 0.0

            if self.shield:
                self.shield_hitpoints -= 300

                if self.shield_hitpoints < 0:
                    self.shield.delete()
                    self.shield = None
                    SpazFactory.get().shield_down_sound.play(1.0,
                                                             position=self.node.position)
        elif msg.hit_subtype == 'fire':
            index = 1
            duration = 5
            damage = 103
            if not self.shield:
                for firex in range(duration):
                    bs.timer(index, babase.CallPartial(fire, index, damage))
                    self._fire_time = bs.Timer(0.1, babase.CallStrict(fire_effect),
                                               repeat=True)
                    index += 1
            else:
                self.shield_hitpoints -= 80
                if self.shield_hitpoints < 1:
                    self.shield.delete()
                    self.shield = None
                    SpazFactory.get().shield_down_sound.play(1.0,
                                                             position=self.node.position)
        elif msg.hit_subtype == 'impairment':
            damage_scale = 0

            if self.shield:
                self.shield.delete()
                self.shield = None
                SpazFactory.get().shield_down_sound.play(1.0,
                                                         position=self.node.position)
            else:
                hitpoints = int(self.hitpoints * 0.80)
                self.hitpoints -= int(hitpoints)
                bs.show_damage_count((f'-{int(hitpoints / 10)}%'),
                                         self.node.position,
                                         msg.force_direction)

                if self.hitpoints < 0 or hitpoints < 95:
                    self.node.handlemessage(bs.DieMessage())

        if self.shield:
            if msg.flat_damage:
                damage = msg.flat_damage * self.impact_scale
            else:
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                    velocity_mag, msg.radius, 1, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
                damage = damage_scale * self.node.damage

            assert self.shield_hitpoints is not None
            self.shield_hitpoints -= int(damage)
            self.shield.hurt = (
                1.0 -
                float(self.shield_hitpoints) / self.shield_hitpoints_max)

            max_spillover = SpazFactory.get().max_shield_spillover_damage
            if self.shield_hitpoints <= 0:

                self.shield.delete()
                self.shield = None
                SpazFactory.get().shield_down_sound.play(1.0,
                                                         position=self.node.position)

                npos = self.node.position
                bs.emitfx(position=(npos[0], npos[1] + 0.9, npos[2]),
                          velocity=self.node.velocity,
                          count=random.randrange(20, 30),
                          scale=1.0,
                          spread=0.6,
                          chunk_type='spark')

            else:
                SpazFactory.get().shield_hit_sound.play(0.5,
                                                        position=self.node.position)

            assert msg.force_direction is not None
            bs.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 1.0,
                                msg.force_direction[1] * 1.0,
                                msg.force_direction[2] * 1.0),
                      count=min(30, 5 + int(damage * 0.005)),
                      scale=0.5,
                      spread=0.3,
                      chunk_type='spark')

            if self.shield_hitpoints <= -max_spillover:
                leftover_damage = -max_spillover - self.shield_hitpoints
                shield_leftover_ratio = leftover_damage / damage

                mag *= shield_leftover_ratio
                velocity_mag *= shield_leftover_ratio
            else:
                return True
        else:
            shield_leftover_ratio = 1.0

        if msg.flat_damage:
            damage = int(msg.flat_damage * self.impact_scale *
                         shield_leftover_ratio)
        else:
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                msg.velocity[0], msg.velocity[1], msg.velocity[2], mag,
                velocity_mag, msg.radius, 0, msg.force_direction[0],
                msg.force_direction[1], msg.force_direction[2])

            damage = int(damage_scale * self.node.damage)

        if self.tankshield['Reduction']:
            porcentaje = percentage_tank_shield()
            dism = int(damage * porcentaje)
            damage = int(damage - dism)

            bs.show_damage_count('-' + str(int(damage / 10)) + '%',
                                     msg.pos, msg.force_direction)

        self.node.handlemessage('hurt_sound')

        if self.edg_eff:
            porcentaje = percentage_health_damage()
            dmg_dism = int(damage * porcentaje)
            self.hitpoints += dmg_dism

            PopupText(text=f'+{int(dmg_dism / 10)}%', scale=1.5,
                      position=self.node.position, color=(0, 1, 0)).autoretain()
            bs.animate_array(self.node, 'color', 3,
                             {0: (0, 1, 0), 0.39: (0, 2, 0),
                              0.4: self.color[0]})
            bs.getsound('healthPowerup').play()

        if msg.hit_type == 'punch':
            self.on_punched(damage)

            try:
                if msg.get_source_player(bs.Player).actor.freeze_punch:
                    self.node.color = (0, 1, 4)
                    bs.getsound('freeze').play()
                    self.node.handlemessage(bs.FreezeMessage())
            except:
                pass

            if damage > 350:
                assert msg.force_direction is not None
                bs.show_damage_count('-' + str(int(damage / 10)) + '%',
                                         msg.pos, msg.force_direction)

            if msg.hit_subtype == 'super_punch':
                SpazFactory.get().punch_sound_stronger.play(1.0,
                                                            position=self.node.position)
            if damage > 500:
                sounds = SpazFactory.get().punch_sound_strong
                sound = sounds[random.randrange(len(sounds))]
            else:
                sound = SpazFactory.get().punch_sound
            sound.play(1.0, position=self.node.position)

            assert msg.force_direction is not None
            bs.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 0.5,
                                msg.force_direction[1] * 0.5,
                                msg.force_direction[2] * 0.5),
                      count=min(10, 1 + int(damage * 0.0025)),
                      scale=0.3,
                      spread=0.03)

            bs.emitfx(position=msg.pos,
                      chunk_type='sweat',
                      velocity=(msg.force_direction[0] * 1.3,
                                msg.force_direction[1] * 1.3 + 5.0,
                                msg.force_direction[2] * 1.3),
                      count=min(30, 1 + int(damage * 0.04)),
                      scale=0.9,
                      spread=0.28)

            hurtiness = damage * 0.003
            punchpos = (msg.pos[0] + msg.force_direction[0] * 0.02,
                        msg.pos[1] + msg.force_direction[1] * 0.02,
                        msg.pos[2] + msg.force_direction[2] * 0.02)
            flash_color = (1.0, 0.8, 0.4)
            light = bs.newnode(
                'light',
                attrs={
                    'position': punchpos,
                    'radius': 0.12 + hurtiness * 0.12,
                    'intensity': 0.3 * (1.0 + 1.0 * hurtiness),
                    'height_attenuated': False,
                    'color': flash_color
                })
            bs.timer(0.06, light.delete)

            flash = bs.newnode('flash',
                               attrs={
                                   'position': punchpos,
                                   'size': 0.17 + 0.17 * hurtiness,
                                   'color': flash_color
                               })
            bs.timer(0.06, flash.delete)

        if msg.hit_type == 'impact':
            assert msg.force_direction is not None
            bs.emitfx(position=msg.pos,
                      velocity=(msg.force_direction[0] * 2.0,
                                msg.force_direction[1] * 2.0,
                                msg.force_direction[2] * 2.0),
                      count=min(10, 1 + int(damage * 0.01)),
                      scale=0.4,
                      spread=0.1)
        if self.hitpoints > 0:
            if msg.hit_type == 'impact' and damage > self.hitpoints:
                newdamage = max(damage - 200, self.hitpoints - 10)
                damage = newdamage
            self.node.handlemessage('flash')

            if damage > 0.0 and self.node.hold_node:
                self.node.hold_node = None
            self.hitpoints -= damage
            self.node.hurt = 1.0 - float(
                self.hitpoints) / self.hitpoints_max

            if self._cursed and damage > 0:
                bs.timer(
                    0.05,
                    babase.CallPartial(self.curse_explode,
                                msg.get_source_player(bs.Player)))

            if self.frozen and (damage > 200 or self.hitpoints <= 0):
                self.shatter()
            elif self.hitpoints <= 0:
                self.node.handlemessage(
                    bs.DieMessage(how=bs.DeathType.IMPACT))

        if self.hitpoints <= 0:
            damage_avg = self.node.damage_smoothed * damage_scale
            if damage_avg > 1000:
                self.shatter()

    elif isinstance(msg, BombDiedMessage):
        self.bomb_count += 1

    elif isinstance(msg, bs.DieMessage):
        def drop_bomb():
            for xbomb in range(3):
                p = self.node.position
                pos = (p[0] + xbomb, p[1] + 5, p[2] - xbomb)
                ball = bomb.Bomb(position=pos, bomb_type='impact').autoretain()
                ball.node.mesh_scale = 0.6
                ball.node.mesh = bs.getmesh('egg')
                ball.node.gravity_scale = 2

        if self.edg_eff:
            self.edg_eff = False

        wasdead = self._dead
        self._dead = True
        self.hitpoints = 0
        if msg.immediate:
            if self.node:
                self.node.delete()
        elif self.node:
            self.node.hurt = 1.0
            if self.play_big_death_sound and not wasdead:
                SpazFactory.get().single_player_death_sound.play()
            self.node.dead = True
            bs.timer(2.0, self.node.delete)

            t = 0
            if self.kill_eff:
                for bombs in range(3):
                    bs.timer(t, babase.CallStrict(drop_bomb))
                    t += 0.15
                self.kill_eff = False

    elif isinstance(msg, bs.OutOfBoundsMessage):
        self.handlemessage(bs.DieMessage(how=bs.DeathType.FALL))

    elif isinstance(msg, bs.StandMessage):
        self._last_stand_pos = (msg.position[0], msg.position[1],
                                msg.position[2])
        if self.node:
            self.node.handlemessage('stand', msg.position[0],
                                    msg.position[1], msg.position[2],
                                    msg.angle)

    elif isinstance(msg, CurseExplodeMessage):
        self.curse_explode()

    elif isinstance(msg, PunchHitMessage):
        if not self.node:
            return None
        node = bs.getcollision().opposingnode

        if node and (node not in self._punched_nodes):

            punch_momentum_angular = (self.node.punch_momentum_angular *
                                      self._punch_power_scale)
            punch_power = self.node.punch_power * self._punch_power_scale

            if node.getnodetype() != 'spaz':
                sounds = SpazFactory.get().impact_sounds_medium
                sound = sounds[random.randrange(len(sounds))]
                sound.play(1.0, position=self.node.position)

            ppos = self.node.punch_position
            punchdir = self.node.punch_velocity
            vel = self.node.punch_momentum_linear

            self._punched_nodes.add(node)
            node.handlemessage(
                bs.HitMessage(
                    pos=ppos,
                    velocity=vel,
                    magnitude=punch_power * punch_momentum_angular * 110.0,
                    velocity_magnitude=punch_power * 40,
                    radius=0,
                    srcnode=self.node,
                    source_player=self.source_player,
                    force_direction=punchdir,
                    hit_type='punch',
                    hit_subtype=('super_punch' if self._has_boxing_gloves
                                 else 'default')))

            mag = -400.0
            if self._hockey:
                mag *= 0.5
            if len(self._punched_nodes) == 1:
                self.node.handlemessage('kick_back', ppos[0], ppos[1],
                                        ppos[2], punchdir[0], punchdir[1],
                                        punchdir[2], mag)
    elif isinstance(msg, PickupMessage):
        if not self.node:
            return None

        try:
            collision = bs.getcollision()
            opposingnode = collision.opposingnode
            opposingbody = collision.opposingbody
        except bs.NotFoundError:
            return True

        try:
            if opposingnode.invincible:
                return True
        except Exception:
            pass

        if (opposingnode.getnodetype() == 'spaz'
            and not opposingnode.shattered and opposingbody == 4):
            opposingbody = 1

        held = self.node.hold_node
        if held and held.getnodetype() == 'flag':
            return True

        self.node.hold_body = opposingbody
        self.node.hold_node = opposingnode
    elif isinstance(msg, bs.CelebrateMessage):
        if self.node:
            self.node.handlemessage('celebrate', int(msg.duration * 1000))

    return None


class PowerupManagerWindow(PopupWindow):
    def __init__(self, transition='in_right'):
        columns = 2
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width * 0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width * 0.95
        self.tab_buttons: set = {}
        self.list_cls_power: list = []
        self.default_powerups = default_powerups()
        self.default_power_list = list(self.default_powerups)
        self.coins = apg['Bear Coin']
        self.popup_cls_power = None

        if not STORE['Buy Firebombs']:
            powerups['Fire Bombs'] = 0
            self.default_power_list.remove('Fire Bombs')

        self.charstr = [babase.charstr(babase.SpecialChar.LEFT_ARROW),
                        babase.charstr(babase.SpecialChar.RIGHT_ARROW),
                        babase.charstr(babase.SpecialChar.UP_ARROW),
                        babase.charstr(babase.SpecialChar.DOWN_ARROW)]

        self.tabdefs = {"Action 1": ['powerupIceBombs', (1, 1, 1)],
                        "Action 2": ['settingsIcon', (0, 1, 0)],
                        "Action 3": ['inventoryIcon', (1, 1, 1)],
                        "Action 4": ['storeIcon', (1, 1, 1)],
                        "Action 5": ['advancedIcon', (1, 1, 1)],
                        "About": ['heart', (1.5, 0.3, 0.3)]}

        if (STORE['Buy Firebombs'] and
            STORE['Buy Option'] and
            STORE['Buy Percentage']):
            self.tabdefs = {"Action 1": ['powerupIceBombs', (1, 1, 1)],
                            "Action 2": ['settingsIcon', (0, 1, 0)],
                            "Action 3": ['inventoryIcon', (1, 1, 1)],
                            "About": ['heart', (1.5, 0.3, 0.3)]}

        self.listdef = list(self.tabdefs)

        self.count = len(self.tabdefs)

        self._current_tab = GLOBAL['Tab']

        app = bui.app.ui_v1
        uiscale = app.uiscale

        self._root_widget = bui.containerwidget(size=(width + 90, height + 80),
                                                transition=transition,
                                                scale=1.5 if uiscale is babase.UIScale.SMALL else 1.0,
                                                stack_offset=(0,
                                                              -30) if uiscale is babase.UIScale.SMALL else (
                                                0, 0))

        self._backButton = b = bui.buttonwidget(parent=self._root_widget,
                                                autoselect=True,
                                                position=(
                                                60, self._height - 15),
                                                size=(130, 60),
                                                scale=0.8, text_scale=1.2,
                                                label=babase.Lstr(
                                                    resource='backText'),
                                                button_type='back',
                                                on_activate_call=babase.CallStrict(
                                                    self._back))
        bui.buttonwidget(edit=self._backButton, button_type='backSmall',
                         size=(60, 60),
                         label=babase.charstr(babase.SpecialChar.BACK))
        bui.containerwidget(edit=self._root_widget, cancel_button=b)

        self.titletext = bui.textwidget(parent=self._root_widget,
                                        position=(0, height - 15),
                                        size=(width, 50),
                                        h_align="center",
                                        color=bui.app.ui_v1.title_color,
                                        v_align="center", maxwidth=width * 1.3)

        index = 0
        for tab in range(self.count):
            for tab2 in range(columns):

                tag = self.listdef[index]

                position = (
                620 + (tab2 * 120), self._height - 50 * 2.5 - (tab * 120))

                if tag == 'About':
                    text = babase.Lstr(resource='gatherWindow.aboutText')
                elif tab == 'Action 4':
                    text = babase.Lstr(resource='storeText')
                else:
                    text = getlanguage(tag)

                self.tab_buttons[tag] = bui.buttonwidget(
                    parent=self._root_widget, autoselect=True,
                    position=position, size=(110, 110),
                    scale=1, label='', enable_sound=False,
                    button_type='square',
                    on_activate_call=babase.CallPartial(self._set_tab, tag,
                                                 sound=True))

                self.text = bui.textwidget(parent=self._root_widget,
                                           position=(
                                           position[0] + 55, position[1] + 30),
                                           size=(0, 0), scale=1,
                                           color=bui.app.ui_v1.title_color,
                                           draw_controller=self.tab_buttons[
                                               tag], maxwidth=100,
                                           text=text, h_align='center',
                                           v_align='center')

                self.image = bui.imagewidget(parent=self._root_widget,
                                             size=(60, 60),
                                             color=self.tabdefs[tag][1],
                                             draw_controller=self.tab_buttons[
                                                 tag],
                                             position=(position[0] + 25,
                                                       position[1] + 40),
                                             texture=bs.gettexture(
                                                 self.tabdefs[tag][0]))

                index += 1

                if self.count == index:
                    break

            if self.count == index:
                break

        self._scrollwidget = None
        self._tab_container = None
        self._set_tab(self._current_tab)

    def __del__(self):
        apg.apply_and_commit()

    def _set_tab(self, tab, sound: bool = False):
        self.sound = sound
        GLOBAL['Tab'] = tab
        apg.apply_and_commit()

        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()

        if self.sound:
            bs.getsound('click01').play()

        if self._scrollwidget:
            self._scrollwidget.delete()

        self._scrollwidget = bui.scrollwidget(parent=self._root_widget,
                                              position=(
                                              self._width * 0.08, 51 * 1.8),
                                              size=(self._sub_width - 140,
                                                    self._scroll_height + 60 * 1.2))

        if tab == 'Action 4':
            if self._scrollwidget:
                self._scrollwidget.delete()
            self._scrollwidget = bui.hscrollwidget(parent=self._root_widget,
                                                      position=(
                                                      self._width * 0.08,
                                                      51 * 1.8), size=(
                self._sub_width - 140, self._scroll_height + 60 * 1.2),
                                                      capture_arrows=True,
                                                      claims_left_right=True)
            bui.textwidget(edit=self.titletext,
                           text=babase.Lstr(resource='storeText'))
        elif tab == 'About':
            bui.textwidget(edit=self.titletext,
                           text=babase.Lstr(resource='gatherWindow.aboutText'))
        else:
            bui.textwidget(edit=self.titletext, text=getlanguage(tab))

        choices = ['Reset', 'Only Bombs', 'Only Items', 'New', 'Nothing']
        c_display = []

        for display in choices:
            choices_display = babase.Lstr(translate=("", getlanguage(display)))
            c_display.append(choices_display)

        if tab == 'Action 1':
            self.popup_cls_power = PopupMenu(
                parent=self._root_widget,
                position=(130, self._width * 0.61),
                button_size=(150, 50), scale=2.5,
                choices=choices, width=150,
                choices_display=c_display,
                current_choice=GLOBAL['Cls Powerup'],
                on_value_change_call=self._set_concept)
            self.list_cls_power.append(self.popup_cls_power._button)

            self.button_cls_power = bui.buttonwidget(parent=self._root_widget,
                                                     position=(
                                                     500, self._width * 0.61),
                                                     size=(50, 50),
                                                     autoselect=True,
                                                     scale=1, label=('%'),
                                                     text_scale=1,
                                                     button_type='square',
                                                     on_activate_call=self._percentage_window)
            self.list_cls_power.append(self.button_cls_power)

            rewindow = [self.popup_cls_power._button, self.button_cls_power]

            for cls in self.list_cls_power:  # this is very important so that pupups don't accumulate
                if cls not in rewindow:
                    cls.delete()

        elif tab == 'Action 4':
            self.button_coin = bui.buttonwidget(parent=self._root_widget,
                                                icon=bs.gettexture('coin'),
                                                position=(
                                                550, self._width * 0.614),
                                                size=(160, 40),
                                                textcolor=(0, 1, 0),
                                                color=(0, 1, 6),
                                                scale=1,
                                                label=str(apg['Bear Coin']),
                                                text_scale=1, autoselect=True,
                                                on_activate_call=None)  # self._percentage_window)
            self.list_cls_power.append(self.button_coin)

            try:
                rewindow.append(self.button_coin)
            except:
                rewindow = [self.button_coin]
            for cls in self.list_cls_power:  # this is very important so that pupups don't accumulate
                if cls not in rewindow:
                    cls.delete()

        else:
            try:
                for cls in self.list_cls_power:
                    cls.delete()
            except:
                pass

        if tab == 'Action 1':
            sub_height = len(self.default_power_list) * 90
            v = sub_height - 55
            width = 300
            posi = 0
            id_power = list(self.default_powerups)
            new_powerups = id_power[9:]
            self.listpower = {}

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height),
                background=False, selection_loops_to_parent=True)

            for power in self.default_power_list:
                if power == id_power[0]:
                    text = 'helpWindow.powerupShieldNameText'
                    tex = bs.gettexture('powerupShield')
                elif power == id_power[1]:
                    text = 'helpWindow.powerupPunchNameText'
                    tex = bs.gettexture('powerupPunch')
                elif power == id_power[2]:
                    text = 'helpWindow.powerupLandMinesNameText'
                    tex = bs.gettexture('powerupLandMines')
                elif power == id_power[3]:
                    text = 'helpWindow.powerupImpactBombsNameText'
                    tex = bs.gettexture('powerupImpactBombs')
                elif power == id_power[4]:
                    text = 'helpWindow.powerupIceBombsNameText'
                    tex = bs.gettexture('powerupIceBombs')
                elif power == id_power[5]:
                    text = 'helpWindow.powerupBombNameText'
                    tex = bs.gettexture('powerupBomb')
                elif power == id_power[6]:
                    text = 'helpWindow.powerupStickyBombsNameText'
                    tex = bs.gettexture('powerupStickyBombs')
                elif power == id_power[7]:
                    text = 'helpWindow.powerupCurseNameText'
                    tex = bs.gettexture('powerupCurse')
                elif power == id_power[8]:
                    text = 'helpWindow.powerupHealthNameText'
                    tex = bs.gettexture('powerupHealth')
                elif power == id_power[9]:
                    text = power
                    tex = bs.gettexture('powerupSpeed')
                elif power == id_power[10]:
                    text = power
                    tex = bs.gettexture('heart')
                elif power == id_power[11]:
                    text = "Goodbye!"
                    tex = bs.gettexture('achievementOnslaught')
                elif power == id_power[12]:
                    text = power
                    tex = bs.gettexture('ouyaUButton')
                elif power == id_power[13]:
                    text = power
                    tex = bs.gettexture('achievementSuperPunch')
                elif power == id_power[14]:
                    text = power
                    tex = bs.gettexture('levelIcon')
                elif power == id_power[15]:
                    text = power
                    tex = bs.gettexture('ouyaOButton')
                elif power == id_power[16]:
                    text = power
                    tex = bs.gettexture('star')

                if power in new_powerups:
                    label = getlanguage(power)
                else:
                    label = babase.Lstr(resource=text)

                apperance = powerups[power]
                position = (90, v - posi)

                t = bui.textwidget(parent=c, position=(
                position[0] - 30, position[1] - 15), size=(width, 50),
                                   h_align="center",
                                   color=(bui.app.ui_v1.title_color),
                                   text=label, v_align="center",
                                   maxwidth=width * 1.3)

                self.powprev = bui.imagewidget(parent=c,
                                               position=(position[0] - 70,
                                                         position[1] - 10),
                                               size=(50, 50), texture=tex)

                dipos = 0
                for direc in ['-', '+']:
                    bui.buttonwidget(parent=c, autoselect=True,
                                     position=(position[0] + 270 + dipos,
                                               position[1] - 10),
                                     size=(100, 100),
                                     scale=0.4, label=direc,
                                     button_type='square', text_scale=4,
                                     on_activate_call=babase.CallPartial(
                                         self.apperance_powerups, power, direc))
                    dipos += 100

                textwidget = bui.textwidget(parent=c, position=(
                position[0] + 190, position[1] - 15), size=(width, 50),
                                            h_align="center",
                                            color=cls_pow_color()[apperance],
                                            text=str(apperance),
                                            v_align="center",
                                            maxwidth=width * 1.3)
                self.listpower[power] = textwidget

                posi += 90

        elif tab == 'Action 2':
            sub_height = 370 if not STORE['Buy Option'] else 450
            v = sub_height - 55
            width = 300

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height),
                background=False, selection_loops_to_parent=True)

            position = (40, v - 20)

            c_display = []
            choices = ['Auto', 'SY: BALL', 'SY: Impact', 'SY: Egg']
            for display in choices:
                choices_display = babase.Lstr(
                    translate=("", getlanguage(display)))
                c_display.append(choices_display)

            popup = PopupMenu(parent=c,
                              position=(position[0] + 300, position[1]),
                              button_size=(150, 50), scale=2.5,
                              choices=choices, width=150,
                              choices_display=c_display,
                              current_choice=config['Powerup Style'],
                              on_value_change_call=babase.CallPartial(self._all_popup,
                                                               'Powerup Style'))

            text = getlanguage('Powerup Style')
            wt = (len(text) * 0.80)
            t = bui.textwidget(parent=c,
                               position=(position[0] - 60 + wt, position[1]),
                               size=(width, 50), maxwidth=width * 0.9,
                               scale=1.1, h_align="center",
                               color=bui.app.ui_v1.title_color,
                               text=getlanguage('Powerup Style'),
                               v_align="center")

            dipos = 0
            for direc in ['-', '+']:
                bui.buttonwidget(parent=c, autoselect=True,
                                 position=(
                                 position[0] + 310 + dipos, position[1] - 100),
                                 size=(100, 100),
                                 repeat=True, scale=0.4, label=direc,
                                 button_type='square', text_scale=4,
                                 on_activate_call=babase.CallPartial(
                                     self._powerups_scale, direc))
                dipos += 100

            txt_scale = config['Powerup Scale']
            self.txt_scale = bui.textwidget(parent=c, position=(
            position[0] + 230, position[1] - 105), size=(width, 50),
                                            scale=1.1, h_align="center",
                                            color=(0, 1, 0),
                                            text=str(txt_scale),
                                            v_align="center",
                                            maxwidth=width * 1.3)

            text = getlanguage('Powerup Scale')
            wt = (len(text) * 0.80)
            t = bui.textwidget(parent=c, position=(
            position[0] - 60 + wt, position[1] - 100), size=(width, 50),
                               maxwidth=width * 0.9,
                               scale=1.1, h_align="center",
                               color=bui.app.ui_v1.title_color, text=text,
                               v_align="center")

            position = (position[0] - 20, position[1] + 40)

            self.check = bui.checkboxwidget(parent=c, position=(
            position[0] + 30, position[1] - 230), value=config['Powerup Name'],
                                            on_value_change_call=babase.CallPartial(
                                                self._switches, 'Powerup Name'),
                                            maxwidth=self._scroll_width * 0.9,
                                            text=getlanguage('Powerup Name'),
                                            autoselect=True)

            self.check = bui.checkboxwidget(parent=c, position=(
            position[0] + 30, position[1] - 230 * 1.3),
                                            value=config['Powerup With Shield'],
                                            on_value_change_call=babase.CallPartial(
                                                self._switches,
                                                'Powerup With Shield'),
                                            maxwidth=self._scroll_width * 0.9,
                                            text=getlanguage(
                                                'Powerup With Shield'),
                                            autoselect=True)

            if STORE['Buy Option']:
                self.check = bui.checkboxwidget(parent=c, position=(
                position[0] + 30, position[1] - 230 * 1.6),
                                                value=config['Powerup Time'],
                                                on_value_change_call=babase.CallPartial(
                                                    self._switches,
                                                    'Powerup Time'),
                                                maxwidth=self._scroll_width * 0.9,
                                                text=getlanguage(
                                                    'Powerup Time'),
                                                autoselect=True)

        elif tab == 'Action 3':
            sub_height = 300
            v = sub_height - 55
            width = 300

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height),
                background=False, selection_loops_to_parent=True)

            v -= 20
            position = (110, v - 45 * 1.72)

            if not STORE['Buy Percentage']:
                t = bui.textwidget(parent=c, position=(90, v - 100),
                                   size=(30 + width, 50),
                                   h_align="center",
                                   text=getlanguage('Block Option Store'),
                                   color=bui.app.ui_v1.title_color,
                                   v_align="center", maxwidth=width * 1.5,
                                   scale=1.5)

                i = bui.imagewidget(parent=c,
                                    position=(
                                    position[0] + 100, position[1] - 205),
                                    size=(80, 80),
                                    texture=bs.gettexture('lock'))
            else:
                t = bui.textwidget(parent=c, position=(
                position[0] - 14, position[1] + 70), size=(30 + width, 50),
                                   h_align="center",
                                   text=f"{getlanguage('Tank Shield PTG')} ({getlanguage('Tank Shield')})",
                                   color=bui.app.ui_v1.title_color,
                                   v_align="center", maxwidth=width * 1.5,
                                   scale=1.5)

                b = bui.buttonwidget(parent=c, autoselect=True,
                                     position=position, size=(100, 100),
                                     repeat=True,
                                     scale=0.6, label=self.charstr[3],
                                     button_type='square', text_scale=2,
                                     on_activate_call=babase.CallPartial(
                                         self.tank_shield_percentage,
                                         'Decrement'))

                b = bui.buttonwidget(parent=c, autoselect=True, repeat=True,
                                     text_scale=2,
                                     position=(position[0] * 3.2, position[1]),
                                     size=(100, 100),
                                     scale=0.6, label=self.charstr[2],
                                     button_type='square',
                                     on_activate_call=babase.CallPartial(
                                         self.tank_shield_percentage,
                                         'Increment'))

                porcentaje = config['Tank Shield PTG']
                if porcentaje > 59:
                    color = (0, 1, 0)
                elif porcentaje < 40:
                    color = (1, 1, 0)
                else:
                    color = (0, 1, 0.8)

                self.tank_text = bui.textwidget(parent=c, position=(
                position[0] - 14, position[1] + 5),
                                                size=(30 + width, 50),
                                                h_align="center",
                                                text=str(porcentaje) + '%',
                                                color=color,
                                                v_align="center",
                                                maxwidth=width * 1.3, scale=2)

                # ----->

                position = (110, v - 160 * 1.6)
                t = bui.textwidget(parent=c, position=(
                position[0] - 14, position[1] + 70), size=(30 + width, 50),
                                   h_align="center",
                                   text=f"{getlanguage('Healing Damage PTG')}{_sp_}({getlanguage('Healing Damage')})",
                                   color=bui.app.ui_v1.title_color,
                                   v_align="center", maxwidth=width * 1.3,
                                   scale=1.4)

                b = bui.buttonwidget(parent=c, autoselect=True,
                                     position=position, size=(100, 100),
                                     repeat=True,
                                     scale=0.6, label=self.charstr[3],
                                     button_type='square', text_scale=2,
                                     on_activate_call=babase.CallPartial(
                                         self.health_damage_percentage,
                                         'Decrement'))

                b = bui.buttonwidget(parent=c, autoselect=True, repeat=True,
                                     text_scale=2,
                                     position=(position[0] * 3.2, position[1]),
                                     size=(100, 100),
                                     scale=0.6, label=self.charstr[2],
                                     button_type='square',
                                     on_activate_call=babase.CallPartial(
                                         self.health_damage_percentage,
                                         'Increment'))

                porcentaje = config['Healing Damage PTG']
                if porcentaje > 59:
                    color = (0, 1, 0)
                elif porcentaje < 40:
                    color = (1, 1, 0)
                else:
                    color = (0, 1, 0.8)

                self.hlg_text = bui.textwidget(parent=c, position=(
                position[0] - 14, position[1] + 5),
                                               size=(30 + width, 50),
                                               h_align="center",
                                               text=str(porcentaje) + '%',
                                               color=color,
                                               v_align="center",
                                               maxwidth=width * 1.3, scale=2)

        elif tab == 'Percentage':
            sub_height = len(self.default_power_list) * 90
            v = sub_height - 55
            width = 300
            posi = 0
            id_power = list(self.default_powerups)
            new_powerups = id_power[9:]
            self.listpower = {}

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height),
                background=False, selection_loops_to_parent=True)

            for power in self.default_power_list:
                if power == id_power[0]:
                    text = 'helpWindow.powerupShieldNameText'
                    tex = bs.gettexture('powerupShield')
                elif power == id_power[1]:
                    text = 'helpWindow.powerupPunchNameText'
                    tex = bs.gettexture('powerupPunch')
                elif power == id_power[2]:
                    text = 'helpWindow.powerupLandMinesNameText'
                    tex = bs.gettexture('powerupLandMines')
                elif power == id_power[3]:
                    text = 'helpWindow.powerupImpactBombsNameText'
                    tex = bs.gettexture('powerupImpactBombs')
                elif power == id_power[4]:
                    text = 'helpWindow.powerupIceBombsNameText'
                    tex = bs.gettexture('powerupIceBombs')
                elif power == id_power[5]:
                    text = 'helpWindow.powerupBombNameText'
                    tex = bs.gettexture('powerupBomb')
                elif power == id_power[6]:
                    text = 'helpWindow.powerupStickyBombsNameText'
                    tex = bs.gettexture('powerupStickyBombs')
                elif power == id_power[7]:
                    text = 'helpWindow.powerupCurseNameText'
                    tex = bs.gettexture('powerupCurse')
                elif power == id_power[8]:
                    text = 'helpWindow.powerupHealthNameText'
                    tex = bs.gettexture('powerupHealth')
                elif power == id_power[9]:
                    text = power
                    tex = bs.gettexture('powerupSpeed')
                elif power == id_power[10]:
                    text = power
                    tex = bs.gettexture('heart')
                elif power == id_power[11]:
                    text = "Goodbye!"
                    tex = bs.gettexture('achievementOnslaught')
                elif power == id_power[12]:
                    text = power
                    tex = bs.gettexture('ouyaUButton')
                elif power == id_power[13]:
                    text = power
                    tex = bs.gettexture('achievementSuperPunch')
                elif power == id_power[14]:
                    text = power
                    tex = bs.gettexture('levelIcon')
                elif power == id_power[15]:
                    text = power
                    tex = bs.gettexture('ouyaOButton')
                elif power == id_power[16]:
                    text = power
                    tex = bs.gettexture('star')

                if power in new_powerups:
                    label = getlanguage(power)
                else:
                    label = babase.Lstr(resource=text)

                apperance = powerups[power]
                position = (90, v - posi)

                t = bui.textwidget(parent=c, position=(
                position[0] - 30, position[1] - 15), size=(width, 50),
                                   h_align="center",
                                   color=(bui.app.ui_v1.title_color),
                                   text=label, v_align="center",
                                   maxwidth=width * 1.3)

                self.powprev = bui.imagewidget(parent=c,
                                               position=(position[0] - 70,
                                                         position[1] - 10),
                                               size=(50, 50), texture=tex)

                ptg = str(self.total_percentage(power))
                t = bui.textwidget(parent=c, position=(
                position[0] + 170, position[1] - 10), size=(width, 50),
                                   h_align="center", color=(0, 1, 0),
                                   text=(f'{ptg}%'), v_align="center",
                                   maxwidth=width * 1.3)

                posi += 90

        elif tab == 'Action 4':
            sub_height = 370
            width = 300
            v = sub_height - 55
            u = width - 60

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(width + 500, sub_height),
                background=False, selection_loops_to_parent=True)

            position = (u + 150, v - 250)
            n_pos = 0
            prices = [7560, 5150, 3360]
            str_name = ["FireBombs Store", "Timer Store", "Percentages Store"]
            images = ["ouyaOButton", "settingsIcon", "inventoryIcon"]

            index = 0
            for store in store_items():
                p = prices[index]
                txt = str_name[index]
                label = getlanguage(txt)
                tx_pos = len(label) * 1.8
                lb_scale = len(label) * 0.20
                preview = images[index]

                if STORE[store]:
                    text = getlanguage('Bought')
                    icon = bs.gettexture('graphicsIcon')
                    color = (0.52, 0.48, 0.63)
                    txt_scale = 1.5
                else:
                    text = str(p)
                    icon = bs.gettexture('coin')
                    color = (0.5, 0.4, 0.93)
                    txt_scale = 2

                b = bui.buttonwidget(parent=c, autoselect=True, position=(
                position[0] + 210 - n_pos, position[1]),
                                     size=(250, 80), scale=0.7, label=text,
                                     text_scale=txt_scale, icon=icon,
                                     color=color,
                                     iconscale=1.7,
                                     on_activate_call=babase.CallPartial(
                                         self._buy_object, store, p))

                s = 180
                b = bui.buttonwidget(parent=c, autoselect=True, position=(
                position[0] + 210 - n_pos, position[1] + 55),
                                     size=(s, s + 30), scale=1, label='',
                                     color=color, button_type='square',
                                     on_activate_call=babase.CallPartial(
                                         self._buy_object, store, p))

                s -= 80
                i = bui.imagewidget(parent=c, draw_controller=b,
                                    position=(position[0] + 250 - n_pos,
                                              position[1] + 140),
                                    size=(s, s), texture=bs.gettexture(preview))

                t = bui.textwidget(parent=c, position=(
                position[0] + 270 - n_pos, position[1] + 101),
                                   h_align="center",
                                   color=(bui.app.ui_v1.title_color),
                                   text=label, v_align="center", maxwidth=130)

                n_pos += 280
                index += 1

        elif tab == 'Action 5':
            sub_height = 370
            v = sub_height - 55
            width = 300

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height), background=False,
                selection_loops_to_parent=True)

            position = (0, v - 30)

            t = bui.textwidget(parent=c,
                               position=(position[0] + 80, position[1] - 30),
                               size=(width + 60, 50), scale=1,
                               h_align="center",
                               color=(bui.app.ui_v1.title_color),
                               text=babase.Lstr(
                                   resource='settingsWindowAdvanced.enterPromoCodeText'),
                               v_align="center", maxwidth=width * 1.3)

            self.promocode_text = bui.textwidget(parent=c, position=(
            position[0] + 80, position[1] - 100), size=(width + 60, 50),
                                                 scale=1,
                                                 editable=True,
                                                 h_align="center", color=(
                    bui.app.ui_v1.title_color), text='', v_align="center",
                                                 maxwidth=width * 1.3,
                                                 max_chars=30,
                                                 description=babase.Lstr(
                                                     resource='settingsWindowAdvanced.enterPromoCodeText'))

            self.promocode_button = bui.buttonwidget(
                parent=c, position=(position[0] + 160, position[1] - 170),
                size=(200, 60), scale=1.0,
                label=babase.Lstr(resource='submitText'),
                on_activate_call=self._promocode)

        else:
            sub_height = 0
            v = sub_height - 55
            width = 300

            self._tab_container = c = bui.containerwidget(
                parent=self._scrollwidget,
                size=(self._sub_width, sub_height),
                background=False, selection_loops_to_parent=True)

            t = bui.textwidget(parent=c, position=(110, v - 20),
                               size=(width, 50),
                               scale=1.4, color=(0.2, 1.2, 0.2),
                               h_align="center", v_align="center",
                               text=("Ultimate Powerup Manager v1.7"),
                               maxwidth=width * 30)

            t = bui.textwidget(parent=c, position=(110, v - 90),
                               size=(width, 50),
                               scale=1, color=(1.3, 0.5, 1.0), h_align="center",
                               v_align="center",
                               text=getlanguage('Creator'), maxwidth=width * 30)

            t = bui.textwidget(parent=c, position=(110, v - 220),
                               size=(width, 50),
                               scale=1, color=(1.0, 1.2, 0.3), h_align="center",
                               v_align="center",
                               text=getlanguage('Mod Info'),
                               maxwidth=width * 30)

        for select_tab, button_tab in self.tab_buttons.items():
            if select_tab == tab:
                bui.buttonwidget(edit=button_tab, color=(0.5, 0.4, 1.5))
            else:
                bui.buttonwidget(edit=button_tab, color=(0.52, 0.48, 0.63))

    def _all_popup(self, tag: str, popup: str) -> None:
        config[tag] = popup
        apg.apply_and_commit()

    def _set_concept(self, concept: str) -> None:
        GLOBAL['Cls Powerup'] = concept

        if concept == 'Reset':
            for power, deflt in default_powerups().items():
                powerups[power] = deflt
        elif concept == 'Nothing':
            for power in default_powerups():
                powerups[power] = 0
        elif concept == 'Only Bombs':
            for power, deflt in default_powerups().items():
                if 'Bombs' not in power:
                    powerups[power] = 0
                else:
                    powerups[power] = 3
        elif concept == 'Only Items':
            for power, deflt in default_powerups().items():
                if 'Bombs' in power:
                    powerups[power] = 0
                else:
                    powerups[power] = deflt
        elif concept == 'New':
            default_power = default_powerups()
            new_powerups = list(default_power)[9:]
            for power, deflt in default_power.items():
                if power not in new_powerups:
                    powerups[power] = 0
                else:
                    powerups[power] = deflt

        if not STORE['Buy Firebombs']:
            powerups['Fire Bombs'] = 0

        self._set_tab('Action 1')

    def tank_shield_percentage(self, tag):
        max = 96
        min = 40
        if tag == 'Increment':
            config['Tank Shield PTG'] += 1
            if config['Tank Shield PTG'] > max:
                config['Tank Shield PTG'] = min
        elif tag == 'Decrement':
            config['Tank Shield PTG'] -= 1
            if config['Tank Shield PTG'] < min:
                config['Tank Shield PTG'] = max

        porcentaje = config['Tank Shield PTG']
        if porcentaje > 59:
            color = (0, 1, 0)
        elif porcentaje < 40:
            color = (1, 1, 0)
        else:
            color = (0, 1, 0.8)
        bui.textwidget(edit=self.tank_text,
                       text=str(porcentaje) + '%', color=color)

    def health_damage_percentage(self, tag):
        max = 80
        min = 35
        if tag == 'Increment':
            config['Healing Damage PTG'] += 1
            if config['Healing Damage PTG'] > max:
                config['Healing Damage PTG'] = min
        elif tag == 'Decrement':
            config['Healing Damage PTG'] -= 1
            if config['Healing Damage PTG'] < min:
                config['Healing Damage PTG'] = max

        porcentaje = config['Healing Damage PTG']
        if porcentaje > 59:
            color = (0, 1, 0)
        elif porcentaje < 40:
            color = (1, 1, 0)
        else:
            color = (0, 1, 0.8)
        bui.textwidget(edit=self.hlg_text,
                       text=str(porcentaje) + '%', color=color)

    def apperance_powerups(self, powerup: str, ID: str):
        max = 7
        if ID == "-":
            if powerups[powerup] == 0:
                powerups[powerup] = max
            else:
                powerups[powerup] -= 1
        elif ID == "+":
            if powerups[powerup] == max:
                powerups[powerup] = 0
            else:
                powerups[powerup] += 1
        enum = powerups[powerup]
        bui.textwidget(edit=self.listpower[powerup],
                       text=str(powerups[powerup]),
                       color=cls_pow_color()[enum])

    def _powerups_scale(self, ID: str):
        max = 1.5
        min = 0.5
        sc = 0.1
        if ID == "-":
            if config['Powerup Scale'] < (min + 0.1):
                config['Powerup Scale'] = max
            else:
                config['Powerup Scale'] -= sc
        elif ID == "+":
            if config['Powerup Scale'] > (max - 0.1):
                config['Powerup Scale'] = min
            else:
                config['Powerup Scale'] += sc
        config['Powerup Scale'] = round(config['Powerup Scale'], 1)
        bui.textwidget(edit=self.txt_scale,
                       text=str(config['Powerup Scale']))

    def total_percentage(self, power):
        total = 0
        pw = powerups[power]
        for i, i2 in powerups.items():
            total += i2
        if total == 0:
            return float(total)
        else:
            ptg = (100 * pw / total)
            result = round(ptg, 2)
            return result

    def store_refresh(self, tag: str):
        if tag == 'Buy Firebombs':
            powerups['Fire Bombs'] = 3
            self.default_power_list.append('Fire Bombs')
        self._set_tab('Action 4')

    def _buy_object(self, tag: str, price: int):
        store = BearStore(value=tag, price=price,
                          callback=babase.CallPartial(self.store_refresh, tag))
        store.buy()

    def _promocode(self):
        code = bui.textwidget(query=self.promocode_text)
        promo = PromoCode(code=code)
        promo.code_confirmation()
        bui.textwidget(edit=self.promocode_text, text="")

    def _switches(self, tag, m):
        config[tag] = False if m == 0 else True
        apg.apply_and_commit()

    def _percentage_window(self):
        self._set_tab('Percentage')

    def _back(self):
        bui.containerwidget(edit=self._root_widget, transition='out_left')
        pass


# ===== EX POWERUPS CLASSES =====

class _TouchMessage:
    pass
class ExplodeMessage:
    pass
class ExplodeBombMessage:
    pass

class ExBlast(bomb.Blast):
    def __init__(self, position=(0.0,1.0,0.0), velocity=(0.0,0.0,0.0), owner=None, **kwargs):
        super().__init__(position=position, **kwargs)
        self.owner = owner
        self.position = position
        self.velocity = velocity

    def handlemessage(self, msg):
        assert not self.expired
        if isinstance(msg, bomb.ExplodeHitMessage):
            node = bs.getcollision().opposingnode
            cls_node = node.getdelegate(object)
            pos = self.position
            nodepos = self.node.position
            mag = 2000.0
            if self.blast_type == 'nitrogen':
                mag = 672.0
                if node.getnodetype() == 'spaz':
                    if cls_node.shield:
                        mag = 1300.0
                    else:
                        node.handlemessage(bs.FreezeMessage())
            elif self.blast_type == 'stun':
                if node.getnodetype() == 'spaz':
                    node.handlemessage('knockout', 3500.0)
                    mag = 400.0
                else:
                    mag = 400.0
            elif self.blast_type == 's.m.b':
                if node.getnodetype() == 'spaz':
                    p = nodepos
                    n = node.position
                    dx = n[0]-p[0]; dy = n[1]-p[1]; dz = n[2]-p[2]
                    dist = max(0.01,(dx**2+dy**2+dz**2)**0.5)
                    fx = dx/dist*6000.0
                    fy = dy/dist*6000.0+1200.0
                    fz = dz/dist*6000.0
                    node.handlemessage('impulse',p[0],p[1],p[2],
                        fx,fy,fz,6000,6000,0,0,fx,fy,fz)
                return
            elif self.blast_type == 'curative':
                if node.getnodetype() == 'spaz':
                    ex_health(cls_node, 100)
                return
            elif self.blast_type == 'teleport':
                if node.getnodetype() == 'spaz':
                    owner_cls = (self.owner.getdelegate(object)
                                 if self.owner else None)
                    if owner_cls and owner_cls.node == node:
                        import random as _r
                        p = node.position
                        node.handlemessage(bs.StandMessage(
                            position=(p[0]+_r.uniform(-3,3),
                                      p[1]+1,
                                      p[2]+_r.uniform(-3,3))))
                        ex_health(owner_cls, 150)
                return
            elif self.blast_type == 'cosmic':
                owner_cls = (self.owner.getdelegate(object)
                             if self.owner else None)
                if owner_cls and not getattr(owner_cls,'cosmic_power',False):
                    owner_cls.cosmic_power = True
                    c = list(owner_cls.node.color)
                    c[1] = min(c[1]+1.5, 3.0)
                    owner_cls.node.color = tuple(c)
                    bs.timer(15.0, bs.Call(_ex_cosmic_wear_off, owner_cls))
                return
            elif self.blast_type == 'electro':
                team = ex_get_team(self._source_player)
                if self.owner == node:
                    return
                if node in team:
                    return
                ex_electricity(node, self.owner)
            elif self.blast_type == 'blackhole':
                if node.getnodetype() == 'spaz':
                    if self.owner != node:
                        p = nodepos
                        n = node.position
                        dx = p[0]-n[0]; dy = p[1]-n[1]; dz = p[2]-n[2]
                        dist = max(0.01,(dx**2+dy**2+dz**2)**0.5)
                        fx = dx/dist*5000.0
                        fy = dy/dist*5000.0
                        fz = dz/dist*5000.0
                        node.handlemessage('impulse',n[0],n[1],n[2],
                            fx,fy,fz,5000,5000,0,0,fx,fy,fz)
                        node.handlemessage('knockout', 4000.0)
                return
            elif self.blast_type == 'attraction':
                if node.getnodetype() == 'spaz':
                    p = self.position
                    n = node.position
                    dx = p[0]-n[0]; dy = p[1]-n[1]+2; dz = p[2]-n[2]
                    dist = max(0.01,(dx**2+dy**2+dz**2)**0.5)
                    fx = dx/dist*800.0
                    fy = min(dy/dist*800.0, 300.0)
                    fz = dz/dist*800.0
                    node.handlemessage('impulse',n[0],n[1],n[2],
                        fx,fy,fz,800,800,0,0,fx,fy,fz)
                    node.handlemessage('knockout', 1500.0)
                return
            elif self.blast_type == 'super_shield':
                team = ex_get_team(self._source_player)
                if self.owner == node:
                    return
                if node in team:
                    return
                return ex_impulse(node,
                    bs.HitMessage(pos=self.position,
                                  velocity=self.velocity,
                                  magnitude=1200,
                                  hit_subtype='stun',
                                  radius=800))
            if self.blast_type == 'gloo':
                if not getattr(self, '_gloo_spawned', False):
                    self._gloo_spawned = True
                    p = nodepos
                    shared = SharedObjects.get()
                    wall_mat = bs.Material()
                    wall_mat.add_actions(
                        conditions=('they_have_material', shared.object_material),
                        actions=(('modify_part_collision','collide',True),
                                 ('modify_part_collision','physical',True)))
                    for i in range(5):
                        wall = bs.newnode('prop',
                            attrs={'position':(p[0]+i*0.6-1.2, p[1]+0.5, p[2]),
                                   'body':'box',
                                   'mesh': bs.getmesh('tray'),
                                   'color_texture': bs.gettexture('bombColorIce'),
                                   'reflection':'soft',
                                   'reflection_scale':[1.0],
                                   'shadow_size':0.3,
                                   'mesh_scale':0.8,
                                   'density':99999.0,
                                   'materials':[shared.object_material, wall_mat]})
                        bs.timer(ex.duration_gw, wall.delete)
                return
            node.handlemessage(
                bs.HitMessage(pos=nodepos, velocity=(0,0,0),
                              magnitude=mag, hit_type=self.hit_type,
                              hit_subtype=self.hit_subtype,
                              radius=self.radius,
                              source_player=bs.existing(self._source_player)))
        else:
            return super().handlemessage(msg)


class Tr784(bs.Actor):
    def __init__(self, owner=None, position=(0.0,1.0,0.0)):
        super().__init__()
        self.owner = owner
        self.touch = 0
        self.hitpoints = int(ex_cosmic(owner, ex.hitpoints_t784))
        self.last_ball = None
        self._player = owner.source_player
        self.scale = scale = 0.75
        self.team = []
        self.nodes = []
        if self._player is not None:
            self.team = self._player.team.players
        mat3 = ex_materials()[4]
        shared = SharedObjects.get()
        mesh = bs.getmesh('powerup')
        tex = bs.gettexture('ouyaOButton')
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'crate', 'body_scale': scale,
                   'position': position, 'mesh': mesh,
                   'shadow_size': 0.5, 'density': 9.0,
                   'color_texture': tex, 'reflection': 'soft',
                   'reflection_scale': [1.4],
                   'materials': (mat3, shared.footing_material,
                                 shared.object_material)})
        bs.animate(self.node, 'mesh_scale', {0:0, 0.14:scale*1.6, 0.20:scale})
        self.owner.add_death_action(
            bs.WeakCall(self.handlemessage, bs.DieMessage()))
        scale2 = ex_cosmic(owner, ex.size_t784)
        self.loc_color = (0,1,6)
        self.loc = bs.newnode('locator',
            owner=self.node,
            attrs={'shape':'circleOutline', 'color': self.loc_color,
                   'opacity': 0.3, 'size': [scale2],
                   'draw_beauty': False, 'additive': False})
        self.node.connectattr('position', self.loc, 'position')
        self.region = None
        self.region_scale(x=True)
        self.hp = ExText(text=str(self.hitpoints), node=self.node,
                          position=(0.0,0.45,0.0))
        ex_fake_explosion(radius=1.9, position=self.node.position)

    def region_scale(self, x=False, e=False):
        if not self.node:
            return
        if x:
            scale = ex_cosmic(self.owner, ex.size_t784)
            mat1 = ex_materials_cb(self.call)
            self.region = bs.newnode('region',
                owner=self.node,
                attrs={'type':'sphere', 'materials':[mat1]})
            self.node.connectattr('position', self.region, 'position')
            t = ex.cooldown_t784
            bs.animate_array(self.region, 'scale', 3,
                {0.00: tuple(scale*0.0 for s in range(3)),
                 t-0.01: tuple(scale*0.0 for s in range(3)),
                 t: tuple(scale*0.5 for s in range(3)),
                 t+0.01: tuple(scale*0.5 for s in range(3))}, loop=x)
        else:
            if self.region:
                self.region.delete()
                self.region = None

    def call(self):
        node = bs.getcollision().opposingnode
        if len(self.nodes) == 0:
            bs.timer(0.01, self.shoot)
        if self.owner != node:
            if node in ex_get_team(self._player):
                return
        if node not in self.nodes:
            self.nodes.append(node)
            try:
                cls_node = node.getdelegate(object)
                if cls_node._dead:
                    self.nodes.remove(node)
            except: 
                self.nodes.remove(node)

    def shoot(self):
        if not any(self.nodes):
            return
        if len(self.nodes) >= 2:
            if self.owner in self.nodes:
                self.nodes.remove(self.owner)
        node = self.nodes[0]
        self.nodes.clear()
        if self.last_ball is not None:
            if not self.last_ball.node:
                self.last_ball = None
            else:
                return
        for player in self.team:
            if self.owner != node:
                if player.actor and player.actor.node == node:
                    return
        try:
            scale_radius = ex_cosmic(self.owner, ex.size_t784) * 0.5
            ball = T784Ball(owner=self.owner, enemy=node,
                position=self.node.position,
                turret_pos=self.node.position,
                turret_radius=scale_radius).autoretain()
            self.last_ball = ball
            node_vel = ex_getnodepos([node, ball.node], x=6.6)
            ball.node.velocity = node_vel
            self.region_scale(x=False)
            ball.node.add_death_action(
                bs.Call(self.region_scale, x=True, e=self.owner != node))
            color = self.loc_color
            bs.animate_array(self.loc, 'color', 3,
                {0: color, 0.1: (1,0,0), 0.2: color})
            bs.getsound('corkPop').play()
        except Exception:
            pass

    def dead(self):
        pos = self.node.position
        ex_fake_explosion(color=(2.0,0.1,0.1), radius=1.2, sound=True, position=pos)

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.dead()
                if self.region:
                    self.region.delete()
                self.node.delete()
        elif isinstance(msg, bs.HitMessage):
            ex_hitmessage(msg, delegate=self, reduction=0)
            if self.hp.node:
                self.hp.node.text = str(self.hitpoints)
        else:
            super().handlemessage(msg)


class T784Ball(bs.Actor):
    def __init__(self, owner=None, enemy=None, position=(0.0,1.0,0.0), turret_pos=None, turret_radius=6.0):
        super().__init__()
        self.owner = owner
        self.enemy = enemy
        self.scale = scale = 0.15
        self.touch = 0
        self.turret_pos = turret_pos if turret_pos else position
        self.turret_radius = turret_radius
        self.out_of_range = False
        self._dead = False
        shared = SharedObjects.get()
        mesh = bs.getmesh('shield')
        tex = bs.gettexture('eggTex2')
        mat1 = ex_materials_cb(self.call)
        mat2 = ex_materials()[4]
        position = (position[0], position[1]+0.5, position[2])
        self.node = bs.newnode('prop',
            owner=enemy, delegate=self,
            attrs={'body':'sphere', 'mesh_scale': scale, 'body_scale': 0.35,
                   'position': position, 'mesh': mesh, 'shadow_size': 0.5,
                   'color_texture': tex, 'reflection': 'soft',
                   'reflection_scale': [1.4],
                   'materials': (mat1, mat2, shared.object_material)})
        bs.timer(5.0, bs.WeakCall(self.handlemessage, bs.DieMessage()))
        bs.timer(0.05, bs.WeakCall(self._home))

    def _home(self):
        if not self.node or self._dead:
            return
        if not self.enemy or self.out_of_range:
            return
        p = self.node.position
        tp = self.turret_pos
        dist_to_turret = ((p[0]-tp[0])**2 + (p[1]-tp[1])**2 + (p[2]-tp[2])**2) ** 0.5
        if dist_to_turret > self.turret_radius:
            self.out_of_range = True
            bs.timer(1.0, bs.WeakCall(self.handlemessage, bs.DieMessage()))
            return
        ep = self.enemy.position
        dx = ep[0]-p[0]; dy = (ep[1]+0.5)-p[1]; dz = ep[2]-p[2]
        d = max(0.01, (dx**2+dy**2+dz**2)**0.5)
        speed = 5.5
        self.node.velocity = (dx/d*speed, dy/d*speed, dz/d*speed)
        bs.timer(0.05, bs.WeakCall(self._home))

    def call(self):
        if self.touch != 0:
            self.touch = 0
            return
        self.touch += 1
        node = bs.getcollision().opposingnode
        cls_node = node.getdelegate(object)
        if getattr(cls_node, '_dead', None):
            return
        if self.owner == node:
            ex_health(cls_node, ex.max_cure_t784)
        else:
            if not getattr(node, 'invincible', False):
                mag = ex.damage_t784
                msg = bs.HitMessage(srcnode=self.owner, velocity=(0,0,0),
                                     flat_damage=mag, hit_subtype='T784')
                node.handlemessage(msg)
                PopupText(text='-'+str(msg.flat_damage)+'HP',
                    color=(0.8,0.1,0.1), scale=1.0,
                    random_offset=0.0, position=node.position).autoretain()
        self.handlemessage(bs.DieMessage())

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            self._dead = True
            if self.node:
                self.node.delete()
        else:
            super().handlemessage(msg)


class ExPortal(bs.Actor):
    def __init__(self, owner=None, bomb_node=None, position=(0.0,1.0,0.0)):
        super().__init__()
        self.scale = scale = 6.0
        self.owner_node = owner
        self.bomb_node = bomb_node
        self._dead = False
        mat = ex_materials_cb(self.call)
        self.node = bs.newnode('region',
            delegate=self,
            attrs={'scale': [scale*0.6 for s in range(3)],
                   'type': 'sphere', 'position': position,
                   'materials': [mat]})
        if bomb_node is not None:
            bomb_node.connectattr('position', self.node, 'position')
        self.shield = bs.newnode('shield', owner=self.node,
            attrs={'radius': scale, 'color': (0.5,0.5,0.5), 'hurt': -1.5})
        self.node.connectattr('position', self.shield, 'position')
        bs.timer(0.5, bs.WeakCall(self.effect))

    def effect(self):
        if self._dead or not self.shield:
            return
        s = self.scale
        bs.animate(self.shield, 'radius', {0: s, 1.0: 0})
        bs.timer(1.0, bs.WeakCall(self._finish))

    def _finish(self):
        if self._dead:
            return
        if self.bomb_node:
            pos = self.bomb_node.position
            ExBlast(owner=self.owner_node, blast_radius=4.0,
                    blast_type='blackhole', position=pos,
                    velocity=(0.0,0.0,0.0),
                    source_player=getattr(self.owner_node, 'source_player', None)
                    ).autoretain()
            ex_fake_explosion(position=pos, color=(0.3,0.0,0.5), radius=2.5)
            bs.getsound('shieldDown').play()
            self._spawn_sombrita()
        self.handlemessage(bs.DieMessage())

    def _spawn_sombrita(self):
        owner_cls = self.owner_node.getdelegate(object) if self.owner_node else None
        if owner_cls is None:
            return
        pos = self.bomb_node.position
        owner_cls._ex_bots = ExBotSet()
        owner_cls._ex_bots.owner = self.owner_node
        owner_cls._ex_bots.spawn_bot(
            bot_type=bs.Call(SombritaBot, source_player=self.owner_node.source_player),
            pos=pos, spawn_time=1.0, on_spawn_call=None)
        self.owner_node.add_death_action(
            bs.Call(setattr, owner_cls, '_ex_bots', None))

    def call(self):
        node = bs.getcollision().opposingnode
        cls_node = node.getdelegate(object)
        if self.owner_node == node:
            return
        if node in ex_get_team(self.owner_node.source_player):
            return
        if self.bomb_node:
            cls_node._pick_up(self.bomb_node)
            node.handlemessage('knockout', 5000.0)

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            self._dead = True
            if self.bomb_node:
                self.bomb_node.delete()
                self.bomb_node = None
            if self.shield:
                self.shield.delete()
                self.shield = None
            if self.node:
                self.node.delete()
                self.node = None
        else:
            super().handlemessage(msg)


class SombritaBot(bots.BrawlerBot):
    run = True
    default_boxing_gloves = False
    character = 'Taobao Mascot'

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.hitpoints = self.hitpoints_max = ex.sombrita_hp
        self.node.color, self.node.highlight = [(0.0, 0.0, 0.0)] * 2
        self.node.color_texture, self.node.color_mask_texture = [bs.gettexture('black')] * 2
        self._punch_power_scale = 2.0

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                if msg.immediate:
                    ex_fake_explosion(self.node.position, sound=False,
                        color=tuple(max(round(random.random()*2,1),0.5) for s in range(3)))
                return Spaz.handlemessage(self, msg)
        else:
            if isinstance(msg, PunchHitMessage):
                try:
                    node = bs.getcollision().opposingnode
                    if node.getnodetype() == 'spaz':
                        self._pick_up(node)
                except Exception:
                    pass
            return super().handlemessage(msg)


class ExBotSet(bots.SpazBotSet):
    owner = None


class MiniZone:
    def __init__(self, type='freeze', duration=5.0, radius=1.5, owner=None,
                 color=(0,1.5,1.5), position=(0.0,1.0,0.0)):
        scale = radius
        self.type = type
        self.owner = owner
        self.hypothermic_material = ex_materials_cb(self.call)
        self.show_zone = bs.newnode('shield',
            owner=self.owner,
            attrs={'position': position, 'color': color, 'radius': scale})
        self.region = bs.newnode('region',
            owner=self.show_zone,
            attrs={'position': position,
                   'scale': [scale*0.6 for s in range(3)],
                   'type': 'sphere',
                   'materials': [self.hypothermic_material]})
        self.show_zone.connectattr('position', self.region, 'position')
        bs.timer(duration, self.end)

    def end(self):
        if self.show_zone:
            r = self.show_zone.radius
            bs.animate(self.show_zone, 'radius', {0: r, 0.1: 0})
            bs.timer(0.1, self.show_zone.delete)

    def call(self):
        node = bs.getcollision().opposingnode
        cls_node = node.getdelegate(object)
        if self.type == 'freeze':
            node.handlemessage(bs.FreezeMessage())
        elif self.type == 'stun':
            if isinstance(cls_node, Spaz):
                ex_impulse(node,
                    bs.HitMessage(pos=self.show_zone.position,
                                  velocity=(0,0,0),
                                  magnitude=260,
                                  hit_subtype='stun',
                                  radius=560))
                bs.timer(0.0, lambda: node.handlemessage('knockout', 2000.0))
                bs.timer(1.5, lambda: node.handlemessage('knockout', 2000.0))
                ex_fake_explosion(color=(1.0,1.0,2.0), radius=0.8, sound=False,
                                  position=node.position)
                bs.getsound('shieldHit').play()



class Smb(bs.Actor):
    def __init__(self, angle=0, owner=None, position=(0.0, 1.0, 0.0)):
        super().__init__()
        self.owner = owner
        self.scale = scale = 0.7
        mat1 = ex_materials_cb(self.call)
        shared = SharedObjects.get()
        mesh = bs.getmesh('shield')
        texs = ['aliColorMask', 'aliColor', 'eggTex3', 'eggTex2']
        tex = bs.gettexture(texs[angle])
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'sphere',
                   'body_scale': 4,
                   'position': position,
                   'mesh': mesh,
                   'shadow_size': 0.5,
                   'color_texture': tex,
                   'reflection': 'soft',
                   'reflection_scale': [1.3],
                   'materials': [mat1, shared.object_material]})
        bs.animate(self.node, 'mesh_scale',
            {0: 0, 0.14: scale * 1.6, 0.20: scale})
        self.direction(angle)

    def call(self):
        if not self.node:
            return
        node = bs.getcollision().opposingnode
        if self.owner == node:
            return
        pos = [x * 50 for x in self.node.position]
        pos[1] = -50
        vel = getattr(self.node, 'velocity', (0.0, 0.0, 0.0))
        if hasattr(node, 'hold_node'):
            node.hold_node = None

        def impulse():
            if self.node and node:
                ex_impulse(node,
                    bs.HitMessage(pos=pos,
                                  velocity=vel,
                                  magnitude=500 * 4,
                                  hit_subtype='s.m.b',
                                  radius=7840))

        def blast(ix=None, imp=0.5):
            if node:
                p = node.position
                x = 0.5
                if ix == 0:
                    bpos = (p[0], p[1] + x, p[2])
                elif ix == 1:
                    bpos = (p[0], p[1] - x, p[2])
                else:
                    bpos = (p[0], p[1] - 0.3, p[2])
                ExBlast(owner=self.owner,
                        blast_radius=imp, blast_type='super_shield',
                        position=bpos, velocity=node.velocity,
                        source_player=getattr(self.owner, 'source_player', None))

        blast()
        impulse()
        bs.timer(0.2, impulse)
        for n1, n2 in enumerate([0.8, 1.5]):
            bs.timer(n2, bs.Call(blast, n1, n2))

    def direction(self, angle):
        reduction = 44.44
        mypos = self.node.position
        dis = ex_calculate(18.0, 100 - reduction)
        duration = ex_calculate(1.3, 100 - reduction)
        myangle = [(mypos[0] + dis, mypos[1], mypos[2]),
                   (mypos[0] - dis, mypos[1], mypos[2]),
                   (mypos[0], mypos[1], mypos[2] + dis),
                   (mypos[0], mypos[1], mypos[2] - dis)][min(angle, 3)]
        bs.animate_array(self.node, 'position', 3,
            {0: mypos, duration: myangle})
        bs.timer(duration, bs.Call(self.handlemessage, bs.DieMessage()))

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            super().handlemessage(msg)

class GlooWall(bs.Actor):
    def __init__(self, owner=None, position=(0.0,0.7,0.0)):
        super().__init__()
        self.owner = owner
        self.scale = scale = 2.550
        mat1 = ex_materials_cb(self.call)
        shared = SharedObjects.get()
        mesh = bs.getmesh('box')
        tex = bs.gettexture('bombColorIce')
        position = (position[0], position[1] + 1.0, position[2])
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'crate', 'body_scale': scale,
                   'position': position, 'mesh': mesh,
                   'density': 1.0, 'shadow_size': 0.0,
                   'color_texture': tex, 'reflection': 'soft',
                   'sticky': True, 'reflection_scale': [2.6],
                   'materials': [mat1, shared.footing_material]})
        bs.animate(self.node, 'mesh_scale',
            {0: 0, 0.14: scale * 1.6, 0.20: scale - 1.0})
        bs.timer(ex.duration_gw, bs.Call(self.handlemessage, bs.DieMessage()))

    def call(self):
        node = bs.getcollision().opposingnode
        cls_node = node.getdelegate(object)
        cls_node._pick_up(self.node)

    def _dead(self):
        ex_fake_explosion(color=(0.0,0.0,2.0), radius=1.9, position=self.node.position)
        bs.emitfx(position=self.node.position, velocity=(0.0,12.0,0.0),
                  count=50, spread=2.0, scale=1.7, chunk_type='ice')
        try:
            MiniZone(owner=None, position=self.node.position)
        except Exception as e:
            print(e)

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self._dead()
                self.node.delete()
        else:
            super().handlemessage(msg)


def _ex_cosmic_wear_off(owner_cls):
    if not owner_cls or not owner_cls.node:
        return
    owner_cls.cosmic_power = False
    c = list(owner_cls.node.color)
    if len(c) >= 2:
        c[1] = max(0.0, c[1] - 1.5)
        owner_cls.node.color = tuple(c)


class ExBomb(bomb.Bomb):
    def __init__(self, bomb_type='normal', **kwargs):
        self.ex_bomb_type = bomb_type
        self.type = {
            'Xfactor': 'impact', 's.m.b': 'impact', 'T784': 'impact',
            'gloo': 'impact', 'teleport': 'impact', 'cosmic': 'impact',
            'blackhole': 'impact', 'curative': 'impact', 'attraction': 'land_mine',
        }.get(bomb_type, 'normal')
        super().__init__(bomb_type=self.type, **kwargs)
        tex = self.node.color_texture
        mod = self.node.mesh
        scale = None
        self.xp_sound = None
        if bomb_type == 'nitrogen':
            tex = bs.gettexture('powerupIceBombs')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [1.3]
            self.xp_sound = 'hiss'
        elif bomb_type == 's.m.b':
            tex = bs.gettexture('powerupIceBombs')
            mod = bs.getmesh('shield')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [2.6]
            scale = 0.25
        elif bomb_type == 'Xfactor':
            tex = bs.gettexture('eggTex1')
            mod = bs.getmesh('egg')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [0.23]
            bs.timer(0.001, bs.WeakCall(self._add_xfactor_materials))
            scale = 0.5
        elif bomb_type == 'T784':
            tex = bs.gettexture('ouyaOButton')
            mod = bs.getmesh('shield')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [1.4]
            self.blast_radius = 0.0
            scale = 0.25
        elif bomb_type == 'stun':
            tex = bs.gettexture('eggTex3')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [1.8]
        elif bomb_type == 'teleport':
            tex = bs.gettexture('rightButton')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [1.3]
        elif bomb_type == 'gloo':
            tex = bs.gettexture('bombColorIce')
            mod = bs.getmesh('shield')
            scale = 0.3
        elif bomb_type == 'cosmic':
            tex = bs.gettexture('achievementFootballShutout')
        elif bomb_type == 'electro':
            tex = bs.gettexture('levelIcon')
        elif bomb_type == 'blackhole':
            tex = bs.gettexture('rgbStripes')
            self.node.reflection = 'soft'
            self.node.reflection_scale = [0.0]
            self.blast_radius *= 3.0
            scale = 0.9
        elif bomb_type == 'attraction':
            tex = bs.gettexture('backIcon')
        self.node.color_texture = tex
        self.node.mesh = mod
        if scale is not None:
            self.node.mesh_scale = scale

    def explode(self):
        if self._exploded:
            return
        self._exploded = True
        if self.ex_bomb_type == 'T784':
            if self.node:
                Tr784(owner=self.owner, position=self.node.position).autoretain()
            bs.timer(0.001, bs.WeakCallStrict(self.handlemessage, bs.DieMessage()))
            return
        if self.ex_bomb_type == 'blackhole':
            if self.node and not getattr(self, '_portal_spawned', False):
                self._portal_spawned = True
                self.node.sticky = True
                ExPortal(owner=self.owner, bomb_node=self.node,
                         position=self.node.position).autoretain()
            return
        if self.node:
            blast = ExBlast(
                position=self.node.position,
                velocity=self.node.velocity,
                blast_radius=self.blast_radius,
                blast_type=self.ex_bomb_type,
                source_player=bs.existing(self._source_player),
                hit_type=self.hit_type,
                hit_subtype=self.hit_subtype,
                owner=self.node,
            ).autoretain()
            for callback in self._explode_callbacks:
                callback(self, blast)
        if self.ex_bomb_type == 'nitrogen' and self.node:
            MiniZone(owner=self.owner, position=self.node.position)
        bs.timer(0.001, bs.WeakCallStrict(self.handlemessage, bs.DieMessage()))

    def arm(self):
        if self.ex_bomb_type == 'Xfactor':
            return
        tex = self.node.color_texture if self.node else None
        super().arm()
        if self.node and tex:
            self.node.color_texture = tex
        if self.ex_bomb_type == 'attraction':
            mat = ex_materials_cb(self._attraction_trigger)
            self._attr_mat = mat
            self.node.materials += (mat,)

    def _attraction_trigger(self):
        if not getattr(self, '_exploded', False):
            self.explode()
    def _add_xfactor_materials(self):
        if self.node:
            mats = ex_materials()
            self._xf_mat1 = mats[2]
            self._xf_mat2 = mats[3]
            self.node.materials += (self._xf_mat1, self._xf_mat2,)

    def handlemessage(self, msg):
        if isinstance(msg, _TouchMessage):
            if self.ex_bomb_type == 'Xfactor' and not getattr(self, '_xf_active', False):
                self._xf_active = True
                mat = ex_materials_cb(self._xfactor_chase)
                self.region = bs.newnode('region',
                    owner=self.node,
                    attrs={'scale': [60.0 for s in range(3)],
                           'type': 'sphere',
                           'materials': [mat]})
                self.node.connectattr('position', self.region, 'position')
                v = self.node.velocity
                self.node.velocity = (v[0], v[1]+12, v[2])
            return
        elif isinstance(msg, ExplodeBombMessage):
            self.explode()
        elif isinstance(msg, ExplodeMessage):
            if self.ex_bomb_type == 'Xfactor':
                node = bs.getcollision().opposingnode
                if self.owner != node:
                    self.explode()
            else:
                self.explode()
        elif isinstance(msg, bomb.ExplodeMessage):
            if self.ex_bomb_type == 'Xfactor':
                return
            elif self.ex_bomb_type == 's.m.b':
                smb_eff(owner=self.owner, position=self.node.position)
            elif self.ex_bomb_type == 'cosmic':
                owner_cls = (self.owner.getdelegate(object)
                             if self.owner else None)
                if owner_cls and not getattr(owner_cls, 'cosmic_power', False):
                    owner_cls.cosmic_power = True
                    c = list(owner_cls.node.color)
                    c[1] = min(c[1] + 1.5, 3.0)
                    owner_cls.node.color = tuple(c)
                    bs.timer(15.0, bs.Call(_ex_cosmic_wear_off, owner_cls))
            elif self.ex_bomb_type == 'electro':
                owner = self.owner
                for node in bs.getnodes():
                    if node.getnodetype() != 'spaz':
                        continue
                    if node == owner:
                        continue
                    p1 = self.node.position
                    p2 = node.position
                    dx = p1[0]-p2[0]; dy = p1[1]-p2[1]; dz = p1[2]-p2[2]
                    dist = (dx**2 + dy**2 + dz**2) ** 0.5
                    if dist < 6.0:
                        cls_node = node.getdelegate(object)
                        if cls_node and not getattr(cls_node, '_eb_eff', False):
                            cls_node._eb_eff = True
                            def zap(n=node, c=cls_node):
                                for i in range(5):
                                    def hit(nn=n, cc=c, ii=i):
                                        if not nn:
                                            return
                                        nn.handlemessage(bs.HitMessage(
                                            srcnode=owner,
                                            velocity=(0,0,0),
                                            flat_damage=30,
                                            hit_subtype='electro'))
                                        nn.handlemessage('knockout', 80.0)
                                        if ii == 4:
                                            cc._eb_eff = False
                                    bs.timer(0.3 * i, hit)
                            zap()
            elif self.ex_bomb_type == 'gloo':
                GlooWall(owner=self.owner, position=self.node.position).autoretain()
                return self.handlemessage(bs.DieMessage())
            elif self.ex_bomb_type == 'teleport':
                if self.owner is not None:
                    self.owner.handlemessage(
                        bs.StandMessage(position=self.node.position))
                    self.owner.handlemessage(
                        bs.PowerupMessage(poweruptype='health'))
                ex_fake_explosion(
                    position=self.node.position,
                    color=(1.2, 0.23, 0.23),
                    sound=False, radius=1.8)
                bs.getsound('spawn').play(0.3)
                return self.handlemessage(bs.DieMessage())
            elif self.ex_bomb_type == 'stun':
                MiniZone(owner=self.owner, type='stun',
                         duration=8.0, color=(2.0, 0.0, 2.0),
                         radius=2.0, position=self.node.position)
            self.explode()
        elif isinstance(msg, bs.HitMessage):
            if self.ex_bomb_type == 'Xfactor':
                return
            super().handlemessage(msg)
        else:
            super().handlemessage(msg)

    def _xfactor_chase(self):
        if not self.node:
            return
        node = bs.getcollision().opposingnode
        cls_node = node.getdelegate(object)
        team = ex_get_team(getattr(self, '_source_player', None))
        if self.owner != node:
            if node in team:
                return
        if self.owner == node or getattr(cls_node, '_dead', None):
            return
        x = 5.0
        node_vel = ex_getnodepos([node, self.node], x=x)
        dis = ex_getnodedis([self.node, node])
        if dis[0] <= 3.0:
            cls_node._pick_up(self.node)
            node.handlemessage('knockout', 2000.0)
            if cls_node.shield:
                if not getattr(cls_node, 'ex_super_shield_active', None):
                    cls_node.shield.delete()
                    cls_node.shield = None
                    bs.getsound('shieldDown').play()
        vel = (
            node_vel[0] * 1.0 if dis[0] < 6 else node_vel[0] * 0.5,
            2.5,
            node_vel[2] * 1.0 if dis[0] < 6 else node_vel[2] * 0.2)
        self.node.velocity = vel


# ===== EX helper functions =====

def ex_cosmic(node, value):
    cls_node = node.getdelegate(object)
    if getattr(cls_node, '_eb_eff', False):
        return value
    m = bs.HitMessage(srcnode=node)
    return value * m.magnitude

def ex_hitmessage(msg, delegate=None, reduction=0, die=True):
    mag = msg.magnitude * 1.0
    velocity_mag = msg.velocity_magnitude
    if not hasattr(delegate, 'hitpoints_max'):
        delegate.hitpoints_max = delegate.hitpoints
    if not msg.flat_damage:
        if bool(reduction):
            damage = round(ex_calculate(mag + velocity_mag, reduction), 2)
        else:
            damage = round(mag + velocity_mag, 2)
    else:
        damage = round(msg.flat_damage, 2)
    if msg.hit_type == 'explosion':
        damage = min(ex_calculate(damage, 40), ex.hitpoints_t784 * 0.5)
    elif msg.hit_type == 'punch':
        damage = min(damage, 1000)
    damage = int(damage)
    delegate.hitpoints = max(delegate.hitpoints - damage, 0)
    if damage != 0:
        dmg = f'-{int(ex_petage(damage, delegate.hitpoints_max, 0))}%'
        bs.show_damage_count(dmg, delegate.node.position, msg.force_direction)
    if die:
        if delegate.hitpoints == 0:
            delegate.node.handlemessage(bs.DieMessage())

class ExText:
    def __init__(self, text='', node=None, position=(0.0,0.5,0.0)):
        self.node = bs.newnode('text',
            owner=node,
            attrs={'text': text, 'in_world': True,
                   'shadow': 1.0, 'flatness': 1.0,
                   'h_align': 'center', 'v_align': 'center',
                   'scale': 0.01, 'position': position})
        if node:
            node.connectattr('position', self.node, 'position')

def ex_get_team(player):
    try:
        if player is not None:
            team = []
            players = getattr(player.team, 'players', [])
            for p in players:
                team.append(p.actor.node)
            return team
        return []
    except:
        return []

def ex_getspazzes():
    spazzes = []
    if bs.getnodes():
        for node in bs.getnodes():
            if node.getnodetype() == 'spaz':
                spazzes.append(node)
    return spazzes

def ex_calculate(a, b, c=2):
    try:
        return round(a * b / 100, c)
    except:
        return 0

def ex_petage(a, b, c=2):
    try:
        return round(100 * a / b, c)
    except:
        return 0

def smb_eff(**kwargs):
    for i in range(4):
        Smb(i, **kwargs).autoretain()
    bs.getsound('cheer').play()

def ex_impulse(owner, msg):
    if isinstance(msg, bs.HitMessage):
        for i in range(2):
            owner.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2],
                msg.magnitude, msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1], msg.force_direction[2])

def ex_getnodepos(nodes, x=5.0):
    return (
        (nodes[0].position[0] - nodes[1].position[0]) * x,
        (nodes[0].position[1] - nodes[1].position[1]) * x,
        (nodes[0].position[2] - nodes[1].position[2]) * x)

def ex_getnodedis(nodes):
    dis = [abs(nodes[0].position[0] - nodes[1].position[0]),
           abs(nodes[0].position[2] - nodes[1].position[2])]
    dis.sort(reverse=True)
    return dis

def ex_fake_explosion(position, radius=1.8, sound=True, color=(0.23,0.23,0.23)):
    explosion = bs.newnode('explosion',
        attrs={'position': position, 'color': color, 'radius': radius, 'big': False})
    bs.timer(1.0, explosion.delete)
    if sound:
        sounds = ['explosion0'+str(n) for n in range(1,6)]
        bs.getsound(random.choice(sounds)).play()

def ex_health(cls_node, hp=0):
    popup = lambda x: PopupText(text=x, color=(0.1,1.0,0.1), scale=1.5,
        random_offset=0.0, position=cls_node.node.position).autoretain()
    if cls_node.shield:
        hp_max = cls_node.shield_hitpoints_max
        if cls_node.shield_hitpoints >= hp_max:
            hp = 35
        cls_node.shield_hitpoints += hp
        popup('+'+str(hp)+'SHP')
    else:
        hp_max = cls_node.hitpoints_max
        if cls_node.hitpoints >= hp_max:
            hp = 35
        cls_node.hitpoints += hp
        popup('+'+str(hp)+'HP')
        bs.getsound('healthPowerup').play()

def ex_electricity(node, owner):
    cls_node = node.getdelegate(object)
    def call(i):
        if not node:
            return
        msg = bs.HitMessage(srcnode=owner, velocity=(0,0,0),
                            flat_damage=ex.damage_eb, hit_subtype='electro')
        node.handlemessage(msg)
        if node.getnodetype() == 'spaz':
            node.handlemessage('knockout', 100.0)
            if ex.repeat_eb == i+1:
                cls_node._eb_eff = False
            PopupText(text='-'+str(msg.flat_damage)+'HP',
                color=(0.8,0.1,0.1), scale=1.0,
                random_offset=0.0, position=node.position).autoretain()
    if node.getnodetype() == 'spaz':
        cls_node._eb_eff = True
    if not getattr(node, 'invincible', False):
        for i in range(ex.repeat_eb):
            bs.timer(2.0*(i+1), bs.Call(call, i))

def ex_zap(node):
    if not node:
        return
    def misil(loc):
        a = (loc.position[0], 8.0, loc.position[2])
        b = (0.0, -9.0, 0.0)
        boom = bomb.Bomb(position=a, bomb_type='impact',
            blast_radius=5.0, velocity=b, bomb_scale=2.38).autoretain()
        boom.node.add_death_action(bs.Call(loc.delete))
    loc = bs.newnode('locator', attrs={
        'shape': 'circleOutline', 'position': node.position,
        'color': (6,0,0), 'opacity': 0.3, 'size': [2.5],
        'draw_beauty': False, 'additive': True})
    bs.timer(0.7, bs.Call(misil, loc))

def ex_supp(self):
    nodes = []
    for node in ex_getspazzes():
        if self.node != node and node not in ex_get_team(self._player):
            nodes.append(node)
    for i, node in enumerate(nodes):
        bs.timer(0.15*i, bs.Call(ex_zap, node))

def ex_materials():
    factory = pupbox.PowerupBoxFactory.get()
    spazfactory = SpazFactory.get()
    shared = SharedObjects.get()
    powerup_material = bs.Material()
    freeze_material = bs.Material()
    xfactor_material1 = bs.Material()
    xfactor_material2 = bs.Material()
    no_pickup_material = bs.Material()
    no_collision_material = bs.Material()
    touch_material = bs.Material()
    no_object_material = bs.Material()
    collision_material = bs.Material()
    no_object_material.add_actions(
        conditions=('they_have_material', shared.object_material),
        actions=(('modify_part_collision','collide',False),
                 ('modify_part_collision','physical',False)))
    no_collision_material.add_actions(
        actions=(('modify_part_collision','collide',False),))
    xfactor_material1.add_actions(
        conditions=('they_have_material', shared.footing_material),
        actions=(('modify_part_collision','collide',True),
                 ('modify_part_collision','physical',True),
                 ('message','our_node','at_connect',_TouchMessage())))
    xfactor_material2.add_actions(
        conditions=('they_have_material', shared.player_material),
        actions=(('modify_part_collision','collide',True),
                 ('modify_part_collision','physical',False),
                 ('message','our_node','at_connect',ExplodeMessage())))
    no_pickup_material.add_actions(
        conditions=('they_have_material', shared.pickup_material),
        actions=('modify_part_collision','collide',False))
    powerup_material.add_actions(
        conditions=('they_have_material', shared.pickup_material),
        actions=('modify_part_collision','collide',False))
    powerup_material.add_actions(
        conditions=('they_have_material', factory.powerup_accept_material),
        actions=(('modify_part_collision','collide',True),
                 ('modify_part_collision','physical',False),
                 ('message','our_node','at_connect',pupbox._TouchedMessage())))
    collision_material.add_actions(
        actions=(('modify_part_collision','collide',True),))
    return [powerup_material, freeze_material, xfactor_material1,
            xfactor_material2, no_pickup_material, no_collision_material,
            touch_material, no_object_material, collision_material]

def ex_materials_cb(callback):
    shared = SharedObjects.get()
    mat = bs.Material()
    mat.add_actions(
        conditions=('they_have_material', shared.player_material),
        actions=(('modify_part_collision', 'collide', True),
                 ('modify_part_collision', 'physical', False),
                 ('call', 'at_connect', callback)))
    return mat

def ex_timer_in_nodes(node, time=5, call=None, callback=None, position=(0.0,0.7,0.0)):
    if type(time) is not int:
        raise TypeError("'"+str(time)+"' is not type 'int'")
    time = [s+1 for s in range(int(time))]
    time.sort(reverse=True)
    time.append(0)
    def text(i):
        if not node:
            return
        if i != 0 and callable(call):
            try: call(i)
            except: call()
        if i > 0:
            c = tuple(max(random.random()*2, 0.3) for q in range(3))
            m = bs.newnode('math', owner=node,
                attrs={'input1': (position[0],position[1],position[2]),
                       'operation': 'add'})
            node.connectattr('position', m, 'input2')
            popup = PopupText(text=str(i), color=c, scale=1.8,
                random_offset=0.0, position=node.position).autoretain()
            m.connectattr('output', popup.node, 'position')
            bs.timer(1.0, babase.CallPartial(popup.handlemessage, bs.DieMessage()))
        if i == 0 and callable(callback):
            callback()
    for i, n in enumerate(time):
        bs.timer(0.0+i, babase.CallPartial(text, n))

def ex_superhuman_health(self):
    if self._dead or not self.node:
        self.ex_superhuman_health_active = None
        return
    popup = lambda x: PopupText(text=x, color=(0.1,1.0,0.1), scale=1.5,
        random_offset=0.0, position=self.node.position).autoretain()
    tm = ex.time_sh / 2
    if self.shield:
        ex_shield = getattr(self, 'ex_shield_sh_color', None)
        if self.shield.color == ex_shield and self.shield_hitpoints < 1000:
            self.shield_hitpoints += ex.shield_hitpoints_sh
            self.shield_hitpoints_max = self.shield_hitpoints
            self.shield_hitpoints = min(self.shield_hitpoints, 1000)
            popup('+'+str(ex.shield_hitpoints_sh)+'SHP')
    else:
        hp = self.hitpoints_max - self.hitpoints
        cure = int(hp / 100 * ex.percentage_sh)
        cure = max(cure, 25)
        if self.hitpoints < self.hitpoints_max:
            self.hitpoints = min(self.hitpoints+cure, self.hitpoints_max)
            text = '+'+str(max(int(cure*100/self.hitpoints_max),1))+'%'
            popup(text)
            tm = ex.time_sh
            bs.getsound('healthPowerup').play()
        else:
            self.equip_shields()
            self.shield.color = (0.0, 1.0, 0.0)
            self.shield_hitpoints = 0
            self.ex_shield_sh_color = self.shield.color
    bs.timer(tm, babase.CallPartial(ex_superhuman_health, self))

def ex_super_shield(self):
    if self._dead or not self.node or self.ex_super_shield_active is None:
        self.ex_super_shield_active = None
        return
    def break_shield(self=self):
        if self.shield:
            ex_shield = getattr(self, 'ex_shield_ss_color', None)
            if self.shield.color != ex_shield:
                self.ex_super_shield_active = None
                return
        s = 100000000
        damage = (s - self.shield_hitpoints)
        if self.shield is not None:
            self.shield.delete()
            self.shield = None
            self.ex_super_shield_active = None
            bs.getsound('shieldDown').play()
        self.shield_hitpoints = s
        if damage > 0:
            tank = int(damage - ex_calculate(damage, ex.reduction_ss))
            msg = bs.HitMessage(srcnode=self.node, flat_damage=tank, velocity=(0,0,0))
            self.node.handlemessage(msg)
            text = '-'+str(int(ex_petage(tank, self.hitpoints_max)))+'%'
            PopupText(text=text, random_offset=0.0,
                color=(0.8,0.1,0.1), scale=1.5,
                position=self.node.position).autoretain()
    def blast(self=self):
        ExBlast(owner=self.node, blast_radius=2.5,
                blast_type='super_shield',
                position=self.node.position,
                velocity=(80.0,20.0,80.0),
                source_player=self.source_player)
    def all_calls():
        break_shield()
        blast()
    if self.shield:
        ex_shield = getattr(self, 'ex_shield_ss_color', None)
        if self.shield.color != ex_shield:
            self.shield.delete()
            self.shield = None
    else:
        self.equip_shields()
        self.shield.color = (1.2, 1.2, 0.0)
        self.shield_hitpoints = 100000000
        self.ex_shield_ss_color = self.shield.color
        self.shield_hitpoints_max = self.shield_hitpoints
        ex_timer_in_nodes(self.shield, time=ex.duration_ss,
            callback=all_calls, position=(0.0,1.2,0.0))
    bs.timer(0.5, babase.CallPartial(ex_super_shield, self))

def ex_powerup_call(self, tag):
    if tag == 's.m.b_bomb':
        if 's.m.b' not in all_bombs:
            all_bombs.append('s.m.b')
        self.ex_bomb = 's.m.b'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_smb_bomb
        self._flash_billboard(tex)
    elif tag == 'cosmic_bomb':
        if 'cosmic' not in all_bombs:
            all_bombs.append('cosmic')
        self.ex_bomb = 'cosmic'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_cosmic_bomb
        self._flash_billboard(tex)
    elif tag == 'electro-bombs':
        if 'electro' not in all_bombs:
            all_bombs.append('electro')
        self.ex_bomb = 'electro'
        tex = NewPowerupBoxFactory.get().tex_electro_bombs
        self._flash_billboard(tex)
    elif tag == 'cosmic_box':
        if not getattr(self, 'cosmic_power', False):
            self.cosmic_power = True
            c = list(self.node.color)
            c[1] = min(c[1] + 1.5, 3.0)
            self.node.color = tuple(c)
            tex = NewPowerupBoxFactory.get().tex_cosmic_box
            self._flash_billboard(tex)
            bs.timer(15.0, bs.WeakCall(_ex_cosmic_wear_off, self))
    elif tag == 'Xfactor_bomb':
        if 'Xfactor' not in all_bombs:
            all_bombs.append('Xfactor')
        self.ex_bomb = 'Xfactor'
        self.ex_count_bomb = 2
        tex = NewPowerupBoxFactory.get().tex_Xfactor_bomb
        self._flash_billboard(tex)
    elif tag == 'nitrogen_bomb':
        if 'nitrogen' not in all_bombs:
            all_bombs.append('nitrogen')
        self.ex_bomb = 'nitrogen'
        tex = NewPowerupBoxFactory.get().tex_nitrogen_bomb
        self._flash_billboard(tex)
    elif tag == 'stun_bomb':
        if 'stun' not in all_bombs:
            all_bombs.append('stun')
        self.ex_bomb = 'stun'
        tex = NewPowerupBoxFactory.get().tex_stun_bomb
        self._flash_billboard(tex)
    elif tag == 'attraction_bomb':
        if 'attraction' not in all_bombs:
            all_bombs.append('attraction')
        self.ex_bomb = 'attraction'
        self.ex_count_bomb = 2
        tex = NewPowerupBoxFactory.get().tex_attraction_bomb
        self._flash_billboard(tex)
    elif tag == 'teleport_bomb':
        if 'teleport' not in all_bombs:
            all_bombs.append('teleport')
        self.ex_bomb = 'teleport'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_teleport_bomb
        self._flash_billboard(tex)
    elif tag == 'gloo_wall_bomb':
        if 'gloo' not in all_bombs:
            all_bombs.append('gloo')
        self.ex_bomb = 'gloo'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_gloo_wall_bomb
        self._flash_billboard(tex)
    elif tag == 'blackhole_bomb':
        if 'blackhole' not in all_bombs:
            all_bombs.append('blackhole')
        self.ex_bomb = 'blackhole'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_blackhole_bomb
        self._flash_billboard(tex)
    elif tag == 'T784_bomb':
        if 'T784' not in all_bombs:
            all_bombs.append('T784')
        self.ex_bomb = 'T784'
        self.ex_count_bomb = 1
        tex = NewPowerupBoxFactory.get().tex_T784_bomb
        self._flash_billboard(tex)
    elif tag == 'supplies':
        ex_supp(self)
    elif tag == 'super_shield':
        if not getattr(self, 'ex_super_shield_active', None):
            self.ex_super_shield_active = True
            ex_super_shield(self)
    elif tag == 'superhuman_healing':
        if not getattr(self, 'ex_superhuman_health_active', None):
            self.ex_superhuman_health_active = True
            ex_superhuman_health(self)

def ex_drop_bomb(self):
    bomb_type = self.bomb_type
    if getattr(self, 'ex_bomb', None):
        bomb_type = self.ex_bomb
    if bomb_type not in all_bombs:
        return _original_drop_bomb(self)
    if self.node.counter_text != '':
        return _original_drop_bomb(self)
    if (self.land_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
        return None
    assert self.node
    pos = self.node.position_forward
    vel = self.node.velocity
    b = ExBomb(position=(pos[0], pos[1], pos[2]),
               velocity=(vel[0], vel[1], vel[2]),
               bomb_scale=1.0, bomb_type=bomb_type,
               blast_radius=self.blast_radius,
               source_player=self.source_player,
               owner=self.node).autoretain()
    assert b.node
    if getattr(self, 'ex_count_bomb', 0) > 0:
        self.ex_count_bomb -= 1
        PopupText(text='x'+str(self.ex_count_bomb),
            color=(0.1,1.0,0.1), scale=1.8,
            random_offset=0.0, position=self.node.position).autoretain()
        if self.ex_count_bomb < 1:
            del self.ex_bomb
    else:
        self.bomb_count -= 1
        b.node.add_death_action(
            babase.CallPartial(self.handlemessage, BombDiedMessage()))
    self._pick_up(b.node)
    for clb in self._dropped_bomb_callbacks:
        clb(self, b)
    return b

def enable():
    global _original_drop_bomb
    pupbox.PowerupBoxFactory = NewPowerupBoxFactory
    pupbox.PowerupBox.__init__ = _pbx_
    Bomb.__init__ = _bomb_init
    SpazBot.handlemessage = bot_handlemessage
    Blast.handlemessage = bomb_handlemessage
    Spaz.handlemessage = new_handlemessage
    Spaz.__init__ = _init_spaz_
    Spaz._get_bomb_type_tex = new_get_bomb_type_tex
    Spaz.on_punch_press = spaz_on_punch_press
    Spaz.on_punch_release = spaz_on_punch_release
    _original_drop_bomb = Spaz.drop_bomb
    Spaz.drop_bomb = ex_drop_bomb
    Spaz.ex_powerup_call = ex_powerup_call
    MainMenuActivity.on_transition_in = new_on_transition_in

