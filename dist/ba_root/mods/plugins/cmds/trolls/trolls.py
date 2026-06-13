from __future__ import annotations
import weakref
import random
import bascenev1 as bs

try:
    from plugins.perms import perms as _perms
    _PERMS_AVAILABLE = True
except Exception:
    _PERMS_AVAILABLE = False

_ACTIVE_BUNNIES: dict = {}

_SPAWN_MSGS = [
    ('Un conejo infernal aparece... y tiene hambre.', (1.0, 0.3, 0.3)),
    ('Se siente una presencia peluda y maliciosa...', (1.0, 0.5, 0.0)),
    ('El conejo ha sido invocado. Que Dios te ayude.', (0.8, 0.2, 1.0)),
    ('Algo saltarin se acerca. No es tu amigo.', (1.0, 0.3, 0.3)),
    ('El conejo huele el miedo. Y le gusta.', (0.9, 0.4, 0.0)),
    ('Las patas del conejo tocan el suelo. Silencio sepulcral.', (1.0, 0.2, 0.2)),
    ('Un ser de pura maldad peluda ha llegado.', (0.8, 0.1, 0.1)),
    ('El conejo no duerme. El conejo no perdona.', (1.0, 0.3, 0.0)),
    ('Presencia detectada. Nivel de amenaza: conejo.', (0.7, 0.3, 1.0)),
    ('El mapa tiembla. O tal vez son sus patitas.', (1.0, 0.4, 0.0)),
    ('Nadie escapa al conejo. Nadie.', (0.9, 0.1, 0.1)),
    ('El conejo ha aceptado el contrato.', (0.6, 0.2, 1.0)),
    ('Se oye un suave... boing. No es buena senal.', (1.0, 0.5, 0.1)),
]

_COUNTDOWN_MSGS = [
    ('El conejo flexiona sus patitas...', (1.0, 0.6, 0.2)),
    ('El conejo te esta mirando fijamente.', (1.0, 0.5, 0.1)),
    ('Preparate. El conejo se calienta.', (1.0, 0.4, 0.0)),
    ('Tick... tock... el conejo espera.', (0.9, 0.3, 0.0)),
    ('El conejo estira las orejas. Mal presagio.', (1.0, 0.5, 0.0)),
    ('Calma chicha. Por ahora.', (0.8, 0.4, 0.1)),
    ('El conejo respira hondo. Tu tambien deberas.', (1.0, 0.4, 0.1)),
    ('Los ojos del conejo brillan. No de alegria.', (0.9, 0.2, 0.0)),
]

_GO_MSGS = [
    ('CORRE.', (1.0, 0.1, 0.1)),
    ('ALLA VA.', (1.0, 0.0, 0.0)),
    ('EL CONEJO HA DESPERTADO.', (1.0, 0.2, 0.0)),
    ('SUELTENSE.', (1.0, 0.1, 0.1)),
    ('VA POR TI.', (1.0, 0.0, 0.0)),
    ('SIN PIEDAD.', (0.9, 0.0, 0.0)),
    ('EL CONEJO NO NEGOCIA.', (1.0, 0.1, 0.0)),
    ('BUENA SUERTE. LA VAS A NECESITAR.', (1.0, 0.2, 0.1)),
    ('AAAAAAAAAA.', (1.0, 0.0, 0.0)),
]

_HIT_MSGS_KICK = [
    ('El conejo toco al jugador. Adios.', (1.0, 0.4, 0.1)),
    ('Demasiado lento. Kick ejecutado.', (0.8, 0.8, 0.2)),
    ('El conejo cobra su precio. Hasta luego.', (1.0, 0.3, 0.0)),
    ('Touched. Kicked. Served.', (0.9, 0.5, 0.1)),
    ('Boing. Kick. Fin.', (1.0, 0.4, 0.0)),
    ('El conejo cumplio su mision. Kick aplicado.', (0.8, 0.7, 0.1)),
    ('No fue rapido suficiente. Bye.', (1.0, 0.3, 0.1)),
    ('El conejo sonrie. Tu ya no estas.', (0.9, 0.3, 0.0)),
    ('Contacto confirmado. Jugador desconectado.', (0.7, 0.8, 0.2)),
    ('GG. El conejo gana como siempre.', (1.0, 0.5, 0.0)),
]

_HIT_MSGS_BAN = [
    ('El conejo toco al jugador. Baneado. Eternamente.', (1.0, 0.2, 0.2)),
    ('GG. El conejo no perdona. Ban aplicado.', (0.8, 0.1, 0.1)),
    ('Fin del camino. El conejo es implacable.', (1.0, 0.1, 0.1)),
    ('Tocado. Baneado. No vuelvas.', (0.9, 0.0, 0.0)),
    ('El conejo cobro la deuda. Ban permanente.', (1.0, 0.1, 0.0)),
    ('Contacto. Ban. Historia.', (0.8, 0.0, 0.0)),
    ('El conejo archiva tu caso. Permanentemente.', (0.7, 0.1, 0.1)),
    ('No hay apelacion ante el conejo. Ban total.', (1.0, 0.0, 0.0)),
    ('El conejo lo sentencio. Sin fianza.', (0.9, 0.1, 0.0)),
    ('Justicia peluda ejecutada.', (0.8, 0.1, 0.1)),
]

_SAVED_MSGS = [
    ('El jugador derroto al conejo. Perdonado... por ahora.', (0.4, 1.0, 0.4)),
    ('Increible. El conejo fue vencido en combate.', (0.3, 1.0, 0.5)),
    ('El jugador gano su libertad a golpes. Respeto.', (0.5, 1.0, 0.3)),
    ('El conejo fue derrotado. Esta vez.', (0.4, 0.9, 0.4)),
    ('Imposible. El conejo... perdio.', (0.3, 1.0, 0.4)),
    ('El jugador le planto cara al conejo y sobrevivio.', (0.4, 1.0, 0.3)),
    ('El conejo yace derrotado. Inesperado.', (0.5, 0.9, 0.3)),
    ('Victoria en combate singular. El jugador queda libre.', (0.3, 1.0, 0.5)),
    ('El conejo subestimo a su presa. Error fatal.', (0.4, 1.0, 0.4)),
    ('Boing... boing... silencio. El conejo cayo.', (0.5, 1.0, 0.3)),
    ('La presa se convirtio en cazador. Libertad ganada.', (0.3, 0.9, 0.5)),
    ('El conejo retrocede. Por primera vez en su historia.', (0.4, 1.0, 0.4)),
]


def _reply(msg: str, color: tuple = (1.0, 1.0, 1.0)) -> None:
    try:
        import _bascenev1
        _bascenev1.chatmessage(msg)
    except Exception:
        try:
            bs.broadcastmessage(msg, color=color)
        except Exception:
            pass


def _cleanup_all() -> None:
    for chaser in list(_ACTIVE_BUNNIES.values()):
        try:
            chaser.destroy()
        except Exception:
            pass
    _ACTIVE_BUNNIES.clear()


def _make_buffed_bunny() -> type:
    from bascenev1lib.actor.spazbot import BouncyBot

    class BuffedBunny(BouncyBot):
        punchiness       = 1.0
        charge_speed_min = 1.2
        charge_speed_max = 1.8
        run              = True
        run_dist_min     = 0.0
        bouncy           = True

    return BuffedBunny


class _BunnyChaser:

    def __init__(self, target_sp: object, kick_only: bool = True,
                 act: object = None, countdown: int = 3) -> None:
        from bascenev1lib.actor.spazbot import SpazBotSet, BouncyBot

        try:
            self._target_aid = target_sp.get_account_id()
        except Exception:
            self._target_aid = None

        self._kick_only    = kick_only
        self._target_cid   = target_sp.inputdevice.client_id
        self._dead         = False
        self._moving       = False
        self._timers: list = []
        self._act_ref      = weakref.ref(act)
        self._bot          = None
        self._botset       = None
        self._patched_spaz = None
        self._countdown    = max(1, countdown)

        self._spawn_bot(act)
        self._start_watchdog()

    def _start_watchdog(self) -> None:
        self_ref = weakref.ref(self)

        def _watch() -> None:
            chaser = self_ref()
            if not chaser or chaser._dead:
                return
            act = chaser._get_act()
            if act is None:
                chaser._silent_destroy()
                return
            current = bs.get_foreground_host_activity()
            if current is not act:
                chaser._silent_destroy()

        self._timers.append(bs.Timer(1.0, _watch, repeat=True))

    def _silent_destroy(self) -> None:
        if self._dead:
            return
        self._dead = True
        self._timers.clear()
        _ACTIVE_BUNNIES.pop(self._target_cid, None)
        botset = self._botset
        self._botset = None
        self._bot = None
        if botset:
            try:
                botset.clear()
            except Exception:
                pass

    def _get_act(self) -> object | None:
        try:
            return self._act_ref()
        except Exception:
            return None

    def _get_safe_pos(self) -> tuple:
        try:
            act = self._get_act()
            return act.map.get_start_position(0)
        except Exception:
            return (0.0, 2.0, 0.0)

    def _spawn_bot(self, act: object) -> None:
        from bascenev1lib.actor.spazbot import SpazBotSet, BouncyBot

        try:
            spawn_pos = act.map.get_start_position(0)
        except Exception:
            spawn_pos = (0.0, 2.0, 0.0)

        self._botset = SpazBotSet()
        self._botset.stop_moving()

        self_ref = weakref.ref(self)

        def _on_spawn(bot: object) -> None:
            chaser = self_ref()
            if not chaser:
                return
            chaser._bot = bot
            if bot.node and bot.node.exists():
                try:
                    bot.node.max_health = 99999
                    bot.node.health     = 99999
                except Exception:
                    pass
            original_handle = bot.handlemessage
            original_shatter = bot.shatter
            bot_ref = weakref.ref(bot)

            def patched_shatter(extreme: bool = False) -> None:
                chaser = self_ref()
                if chaser and not chaser._dead:
                    b = bot_ref()
                    if b and b.node and b.node.exists():
                        b.frozen = False
                        b.node.frozen = False
                    return
                original_shatter(extreme=extreme)

            bot.shatter = patched_shatter

            def patched_handle(msg: object) -> None:
                chaser = self_ref()
                if not chaser:
                    original_handle(msg)
                    return

                if isinstance(msg, bs.FreezeMessage):
                    return

                if isinstance(msg, bs.HitMessage):
                    hit_type    = getattr(msg, 'hit_type', '')
                    srcnode     = getattr(msg, 'srcnode', None)
                    target_spaz = chaser._get_target_spaz()
                    target_node = (
                        target_spaz.node
                        if target_spaz and hasattr(target_spaz, 'node')
                        else None
                    )
                    from_target = (
                        target_node is not None
                        and target_node.exists()
                        and srcnode == target_node
                        and hit_type == 'punch'
                    )
                    if from_target:
                        original_handle(msg)
                    return

                if isinstance(msg, bs.DieMessage):
                    if chaser._dead:
                        original_handle(msg)
                        return
                    if msg.how == bs.DeathType.FALL:
                        b = bot_ref()
                        if b:
                            b.handlemessage(
                                bs.StandMessage(
                                    position=chaser._get_safe_pos(), angle=0.0
                                )
                            )
                        return
                    chaser._on_bot_defeated()
                    original_handle(msg)
                    return

                original_handle(msg)

            bot.handlemessage = patched_handle
            chaser._patch_target(bot)
            chaser._start_countdown()

        BuffedBunny = _make_buffed_bunny()
        self._botset.spawn_bot(
            BuffedBunny,
            pos=bs.Vec3(spawn_pos),
            spawn_time=0.1,
            on_spawn_call=_on_spawn,
        )

        msg, color = random.choice(_SPAWN_MSGS)
        _reply(msg, color)

    def _start_countdown(self) -> None:
        msg, color = random.choice(_COUNTDOWN_MSGS)
        _reply(msg, color)

        self_ref = weakref.ref(self)
        countdown = self._countdown

        def _tick(remaining: list) -> None:
            chaser = self_ref()
            if not chaser or chaser._dead:
                return
            n = remaining[0]
            if n > 0:
                _reply(str(n) + '...', (1.0, max(0.0, 1.0 - n * 0.2), 0.0))
                remaining[0] -= 1
                chaser._timers.append(
                    bs.Timer(1.0, lambda: _tick(remaining))
                )
            else:
                go_msg, go_color = random.choice(_GO_MSGS)
                _reply(go_msg, go_color)
                chaser._moving = True
                chaser._timers.append(
                    bs.Timer(0.05, bs.WeakCallStrict(chaser._update), repeat=True)
                )

        _tick([countdown])

    def _patch_target(self, bot: object) -> None:
        target_spaz = self._get_target_spaz()
        if not target_spaz:
            self_ref = weakref.ref(self)
            bot_ref  = weakref.ref(bot)

            def _retry() -> None:
                chaser = self_ref()
                b = bot_ref()
                if chaser and b:
                    chaser._patch_target(b)

            self._timers.append(bs.Timer(0.5, _retry))
            return

        self_ref = weakref.ref(self)
        bot_ref  = weakref.ref(bot)
        original_handle = target_spaz.handlemessage

        def patched_handle(msg: object) -> None:
            chaser = self_ref()
            if not chaser:
                original_handle(msg)
                return
            b = bot_ref()
            if (isinstance(msg, bs.DieMessage)
                    and not chaser._dead
                    and chaser._moving
                    and b
                    and b.node
                    and b.node.exists()):
                killer_node = getattr(msg, 'killed_by', None)
                if killer_node is None:
                    try:
                        killer_node = target_spaz.node.hold_node
                    except Exception:
                        pass
                if killer_node == b.node:
                    original_handle(msg)
                    chaser._on_hit()
                    return
            original_handle(msg)

        target_spaz.handlemessage = patched_handle
        self._patched_spaz = target_spaz

    def _on_bot_defeated(self) -> None:
        if self._dead:
            return
        self._dead = True
        self._timers.clear()
        _ACTIVE_BUNNIES.pop(self._target_cid, None)
        self._botset = None
        self._bot = None
        msg, color = random.choice(_SAVED_MSGS)
        _reply(msg, color)

    def _on_hit(self) -> None:
        if self._dead:
            return
        bot = self._bot
        if not bot or not bot.is_alive():
            return
        self._dead = True
        self._timers.clear()

        act = self._get_act()
        botset = self._botset
        self._botset = None
        self._bot = None

        if act and botset:
            try:
                with act.context:
                    botset.clear()
            except Exception:
                pass
        elif bot and bot.node and bot.node.exists():
            try:
                bot.handlemessage(bs.DieMessage(immediate=True))
            except Exception:
                pass

        _ACTIVE_BUNNIES.pop(self._target_cid, None)

        if self._kick_only:
            msg, color = random.choice(_HIT_MSGS_KICK)
        else:
            msg, color = random.choice(_HIT_MSGS_BAN)
        _reply(msg, color)

        try:
            import _bascenev1
            if self._kick_only:
                _bascenev1.disconnect_client(self._target_cid, ban_time=300)
            else:
                _bascenev1.disconnect_client(self._target_cid, ban_time=-1)
        except Exception as e:
            print(f'[bunny] disconnect error: {e}')

    def _get_target_spaz(self) -> object | None:
        try:
            act = self._get_act()
            if not act:
                return None
            for player in act.players:
                try:
                    if player.sessionplayer.get_account_id() == self._target_aid:
                        return player.actor
                except Exception:
                    pass
        except Exception:
            pass
        return None

    def _update(self) -> None:
        if self._dead or not self._moving:
            return
        bot = self._bot
        if not bot or not bot.node or not bot.node.exists():
            return

        try:
            target_spaz = self._get_target_spaz()

            if target_spaz and target_spaz is not self._patched_spaz:
                self._patch_target(bot)

            if target_spaz and target_spaz.node and target_spaz.node.exists():
                tpos = target_spaz.node.position
                vel  = target_spaz.node.velocity or (0.0, 0.0, 0.0)
                bot.set_player_points(
                    [(bs.Vec3(tpos), bs.Vec3(vel[0], vel[1], vel[2]))]
                )
                bot.update_ai()
            else:
                bot.set_player_points([])
                bot.update_ai()
        except Exception as e:
            print(f'[bunny] update error: {e}')

    def destroy(self) -> None:
        self._dead = True
        self._timers.clear()
        act = self._get_act()
        botset = self._botset
        self._botset = None
        self._bot = None
        if act and botset:
            try:
                with act.context:
                    botset.clear()
            except Exception:
                pass


def cmd_bunny(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /bunny <clientID> [ban] [segundos]', (1.0, 0.6, 0.2))
        return
    try:
        target_cid = int(args[0])
    except ValueError:
        _reply('clientID debe ser un numero.', (1.0, 0.4, 0.4))
        return

    kick_only = 'ban' not in [a.lower() for a in args]

    countdown = 3
    for a in args[1:]:
        if a.isdigit():
            countdown = max(1, min(int(a), 30))
            break

    try:
        roster = bs.get_game_roster()
        target_acc = None
        for entry in roster:
            if entry.get('client_id') == target_cid:
                target_acc = entry.get('account_id')
                break
        if not target_acc:
            _reply('Jugador no encontrado.', (1.0, 0.4, 0.4))
            return

        session = bs.get_foreground_host_session()
        if not session:
            _reply('No hay sesion activa.', (1.0, 0.4, 0.4))
            return

        target_sp = None
        for s in session.sessionplayers:
            try:
                if s.get_account_id() == target_acc:
                    target_sp = s
                    break
            except Exception:
                pass

        if not target_sp:
            _reply('Jugador no encontrado en sesion.', (1.0, 0.4, 0.4))
            return

        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.', (1.0, 0.4, 0.4))
            return

        if target_cid in _ACTIVE_BUNNIES:
            _ACTIVE_BUNNIES[target_cid].destroy()

        with act.context:
            chaser = _BunnyChaser(
                target_sp,
                kick_only=kick_only,
                act=act,
                countdown=countdown,
            )
            _ACTIVE_BUNNIES[target_cid] = chaser

    except Exception as e:
        _reply(f'Error: {e}', (1.0, 0.4, 0.4))
        print(f'[bunny] cmd error: {e}')


def cmd_nuke(sp: object, args: list) -> None:
    try:
        from plugins.nuke import nuke as _nuke
        ice     = 'ice' in [a.lower() for a in args]
        seconds = 15
        for a in args:
            if a.isdigit():
                seconds = max(5, min(int(a), 120))
                break
        act = bs.get_foreground_host_activity()
        if act:
            with act.context:
                _nuke.spawn_nuke(seconds, ice)
        else:
            _reply('No hay partida activa.')
    except Exception as e:
        _reply(f'Nuke error: {e}')
        print(f'[cmds.trolls] nuke error: {e}')


def _get_actor_by_cid(cid: int) -> object | None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            return None
        for player in act.players:
            try:
                if player.sessionplayer.inputdevice.client_id == cid:
                    return player.actor
            except Exception:
                pass
    except Exception:
        pass
    return None


def _get_all_actors() -> list:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            return []
        return [p.actor for p in act.players if p.actor and p.actor.exists()]
    except Exception:
        return []


def _send_private(msg: str, cid: int) -> None:
    try:
        bs.broadcastmessage(msg, clients=[cid], transient=True)
    except Exception:
        pass


def cmd_kill(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.DieMessage())
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.DieMessage())
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.DieMessage())
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] kill error: {e}')


def cmd_heal(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='health'))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='health'))
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='health'))
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] heal error: {e}')


def cmd_curse(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='curse'))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='curse'))
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='curse'))
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] curse error: {e}')


def cmd_shield(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='shield'))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='shield'))
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='shield'))
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] shield error: {e}')


def cmd_gloves(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='punch'))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='punch'))
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.PowerupMessage(poweruptype='punch'))
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] gloves error: {e}')


def cmd_freeze(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.FreezeMessage())
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.FreezeMessage())
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.FreezeMessage())
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] freeze error: {e}')


def cmd_unfreeze(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.ThawMessage())
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.ThawMessage())
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.ThawMessage())
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] unfreeze error: {e}')


def cmd_sleep(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.node.handlemessage('knockout', 8000)
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.node.handlemessage('knockout', 8000)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.node.handlemessage('knockout', 8000)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] sleep error: {e}')


def cmd_fly(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.node.fly = not actor.node.fly
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.node.fly = not actor.node.fly
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.node.fly = not actor.node.fly
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] fly error: {e}')


def cmd_invisible(sp: object, args: list) -> None:
    def _apply(actor: object) -> None:
        if not actor or not actor.exists():
            return
        n = actor.node
        if n.torso_mesh is not None:
            n.head_mesh = None
            n.torso_mesh = None
            n.upper_arm_mesh = None
            n.forearm_mesh = None
            n.pelvis_mesh = None
            n.hand_mesh = None
            n.toes_mesh = None
            n.upper_leg_mesh = None
            n.lower_leg_mesh = None
            n.style = 'cyborg'

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    _apply(actor)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor:
                    _apply(actor)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] invisible error: {e}')


def cmd_headless(sp: object, args: list) -> None:
    def _apply(actor: object) -> None:
        if not actor or not actor.exists():
            return
        n = actor.node
        if n.head_mesh is not None:
            n.head_mesh = None
            n.style = 'cyborg'

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    _apply(actor)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor:
                    _apply(actor)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] headless error: {e}')


def cmd_creepy(sp: object, args: list) -> None:
    def _apply(actor: object) -> None:
        if not actor or not actor.exists():
            return
        n = actor.node
        if n.head_mesh is not None:
            n.head_mesh = None
            actor.handlemessage(bs.PowerupMessage(poweruptype='punch'))
            actor.handlemessage(bs.PowerupMessage(poweruptype='shield'))

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    _apply(actor)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor:
                    _apply(actor)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] creepy error: {e}')


def cmd_celebrate(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                actor = _get_actor_by_cid(sp.inputdevice.client_id)
                if actor and actor.exists():
                    actor.handlemessage(bs.CelebrateMessage())
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    actor.handlemessage(bs.CelebrateMessage())
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor and actor.exists():
                    actor.handlemessage(bs.CelebrateMessage())
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] celebrate error: {e}')


def cmd_godmode_OLD(sp: object, args: list) -> None:
    def _apply(actor: object) -> None:
        if not actor or not actor.exists():
            return
        if actor._punch_power_scale != 7:
            actor._punch_power_scale = 7
            actor.node.hockey = True
            actor.node.invincible = True
        else:
            actor._punch_power_scale = 1.2
            actor.node.hockey = False
            actor.node.invincible = False

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    _apply(actor)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor:
                    _apply(actor)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] godmode error: {e}')


def cmd_superpunch(sp: object, args: list) -> None:
    def _apply(actor: object) -> None:
        if not actor or not actor.exists():
            return
        if actor._punch_power_scale != 15:
            actor._punch_power_scale = 15
            actor._punch_cooldown = 0
        else:
            actor._punch_power_scale = 1.2
            actor._punch_cooldown = 400

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == 'all':
                for actor in _get_all_actors():
                    _apply(actor)
            else:
                cid = int(args[0])
                actor = _get_actor_by_cid(cid)
                if actor:
                    _apply(actor)
                else:
                    _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.trolls] superpunch error: {e}')


def cmd_speed(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /speed <valor> (ej: 1.0 = normal, 2.0 = doble)')
        return
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        val = max(0.1, min(float(args[0]), 10.0))
        with act.context:
            act.globalsnode.time_scale = val
        _reply(f'Velocidad: {val}x')
    except Exception as e:
        print(f'[cmds.trolls] speed error: {e}')


VALID_BOMB_TYPES = ["normal", "impact", "sticky", "ice", "triple", "steampunk", "land_mine"]


def cmd_godmode(sp: object, args: list) -> None:
    def _apply(actor, btype):
        if not actor or not actor.exists():
            return
        is_gm = actor._punch_power_scale == 7
        if not is_gm:
            actor._punch_power_scale = 7
            actor._punch_cooldown = 0
            actor._jump_cooldown = 0
            actor.node.invincible = True
            actor.node.hockey = True
            actor.bomb_type = btype
            actor.bomb_type_default = btype
            actor.default_bomb_type = btype
            actor.bomb_count = 99
            actor.default_bomb_count = 99
            actor._max_bomb_count = 99
            actor.blast_radius = 4.0
            actor.impact_scale = 5.0
            actor.bomb_scale = 3.0
            actor._fly_timer = bs.Timer(0.05, lambda: actor.node.handlemessage("impulse", actor.node.position[0], actor.node.position[1], actor.node.position[2], actor.node.move_left_right * 4, actor.node.position[1] + 14, actor.node.move_up_down * -4, 3, 3, 0, 0, actor.node.move_left_right * 4, actor.node.position[1] + 14, actor.node.move_up_down * -4) if actor.node.exists() and actor.node.jump_pressed else None, repeat=True)
        else:
            actor._punch_power_scale = 1.2
            actor._punch_cooldown = 400
            actor._jump_cooldown = 200
            actor.node.invincible = False
            actor.node.hockey = False
            actor.bomb_type = "normal"
            actor.bomb_type_default = "normal"
            actor.default_bomb_type = "normal"
            actor.bomb_count = 3
            actor.default_bomb_count = 3
            actor._max_bomb_count = 3
            actor.blast_radius = 2.0
            actor.impact_scale = 1.0
            actor.bomb_scale = 1.0
            actor._fly_timer = None
            try:
                pass
            except Exception:
                pass
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply("No hay partida activa.")
            return
        btype = "impact"
        target_cid = None
        all_players = False
        if args and args[0].lower() in VALID_BOMB_TYPES:
            btype = args[0].lower()
            if len(args) > 1:
                if args[1].lower() == "all":
                    all_players = True
                else:
                    try: target_cid = int(args[1])
                    except: return
        elif args and args[0].lower() == "all":
            all_players = True
        elif args:
            try: target_cid = int(args[0])
            except: return
        with act.context:
            if all_players:
                for p in _get_all_actors(): _apply(p, btype)
            elif target_cid is not None:
                actor = _get_actor_by_cid(target_cid)
                if actor: _apply(actor, btype)
                else: _reply("Jugador no encontrado.")
            else:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id), btype)
    except Exception as e:
        print(f"[cmds.trolls] godmode error: {e}")


def cmd_fly3d(sp: object, args: list) -> None:
    def _apply(actor):
        if not actor or not actor.exists():
            return
        if hasattr(actor, "_fly3d_timer") and actor._fly3d_timer is not None:
            actor._fly3d_timer = None
            actor._jump_cooldown = 200
        else:
            actor._jump_cooldown = 0
            actor._fly3d_timer = bs.Timer(0.05, lambda: actor.node.handlemessage("impulse", actor.node.position[0], actor.node.position[1], actor.node.position[2], actor.node.move_left_right * 4, actor.node.position[1] + 14, actor.node.move_up_down * -4, 3, 3, 0, 0, actor.node.move_left_right * 4, actor.node.position[1] + 14, actor.node.move_up_down * -4) if actor.node.exists() and actor.node.jump_pressed else None, repeat=True)
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply("No hay partida activa.")
            return
        with act.context:
            if not args:
                _apply(_get_actor_by_cid(sp.inputdevice.client_id))
            elif args[0].lower() == "all":
                for actor in _get_all_actors(): _apply(actor)
            else:
                try: cid = int(args[0])
                except: return
                actor = _get_actor_by_cid(cid)
                if actor: _apply(actor)
                else: _reply("Jugador no encontrado.")
    except Exception as e:
        print(f"[cmds.trolls] fly3d error: {e}")


def cmd_bomb(sp: object, args: list) -> None:
    def _apply_type(actor, btype):
        if not actor or not actor.exists():
            return
        actor.bomb_type = btype
        actor.bomb_type_default = btype
        actor.default_bomb_type = btype
    def _apply_count(actor, n):
        if not actor or not actor.exists():
            return
        actor.bomb_count = n
        actor.default_bomb_count = n
        actor._max_bomb_count = n
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply("No hay partida activa.")
            return
        if not args:
            _reply("Uso: /bomb <tipo> [all|id] o /bomb count <n> [all]")
            return
        with act.context:
            if args[0].lower() == "count":
                if len(args) < 2:
                    _reply("Uso: /bomb count <n>")
                    return
                try: n = int(args[1])
                except: return
                if len(args) > 2 and args[2].lower() == "all":
                    for actor in _get_all_actors(): _apply_count(actor, n)
                else:
                    _apply_count(_get_actor_by_cid(sp.inputdevice.client_id), n)
            elif args[0].lower() in VALID_BOMB_TYPES:
                btype = args[0].lower()
                if len(args) > 1 and args[1].lower() == "all":
                    for actor in _get_all_actors(): _apply_type(actor, btype)
                elif len(args) > 1:
                    try: cid = int(args[1])
                    except: return
                    actor = _get_actor_by_cid(cid)
                    if actor: _apply_type(actor, btype)
                    else: _reply("Jugador no encontrado.")
                else:
                    _apply_type(_get_actor_by_cid(sp.inputdevice.client_id), btype)
            else:
                _reply("Tipo invalido. Usa: normal impact sticky ice triple steampunk")
    except Exception as e:
        print(f"[cmds.trolls] bomb error: {e}")

CMDS: dict = {
    'nuke':      ('nuke',  cmd_nuke),
    'bunny':     ('admin', cmd_bunny),
    'kill':      ('admin', cmd_kill),
    'heal':      ('admin', cmd_heal),
    'curse':     ('admin', cmd_curse),
    'shield':    ('admin', cmd_shield),
    'gloves':    ('admin', cmd_gloves),
    'freeze':    ('admin', cmd_freeze),
    'unfreeze':  ('admin', cmd_unfreeze),
    'sleep':     ('admin', cmd_sleep),
    'fly':       ('admin', cmd_fly),
    'invisible': ('admin', cmd_invisible),
    'inv':       ('admin', cmd_invisible),
    'headless':  ('admin', cmd_headless),
    'head':      ('admin', cmd_headless),
    'creepy':    ('admin', cmd_creepy),
    'creep':     ('admin', cmd_creepy),
    'celebrate': ('admin', cmd_celebrate),
    'godmode':   ('admin', cmd_godmode),
    'gm':        ('admin', cmd_godmode),
    'fly3d':    ('admin', cmd_fly3d),
    'bomb':     ('admin', cmd_bomb),
    'superpunch':('admin', cmd_superpunch),
    'sp':        ('admin', cmd_superpunch),
    'speed':     ('admin', cmd_speed),
}
