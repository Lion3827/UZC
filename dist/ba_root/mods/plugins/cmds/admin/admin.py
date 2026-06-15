from __future__ import annotations
import bascenev1 as bs

try:
    from plugins.perms import perms as _perms
    _PERMS_AVAILABLE = True
except Exception:
    _PERMS_AVAILABLE = False


def _reply(msg: str, color: tuple = (1.0, 1.0, 1.0)) -> None:
    try:
        import _bascenev1
        _bascenev1.chatmessage(msg)
    except Exception:
        try:
            _bascenev1.chatmessage(msg, color=color)
        except Exception:
            pass


def _get_session_players() -> list:
    try:
        session = bs.get_foreground_host_session()
        if session:
            return list(session.sessionplayers)
    except Exception:
        pass
    return []


def _find_player(arg: str) -> object | None:
    if arg.lstrip('-').isdigit():
        cid = int(arg)
        try:
            roster = bs.get_game_roster()
            acc    = None
            for entry in roster:
                if entry.get('client_id') == cid:
                    acc = entry.get('account_id')
                    break
            if acc:
                for sp in _get_session_players():
                    try:
                        if sp.get_v1_account_id() == acc:
                            return sp
                    except Exception:
                        pass
        except Exception:
            pass
        return None
    query = arg.lower()
    for sp in _get_session_players():
        try:
            if query in sp.getname().lower():
                return sp
        except Exception:
            pass
    return None


_COLOR_NAMES: dict = {
    'red':    (1.0, 0.2, 0.2),
    'blue':   (0.2, 0.4, 1.0),
    'green':  (0.2, 0.9, 0.3),
    'gold':   (1.0, 0.8, 0.1),
    'cyan':   (0.2, 0.9, 1.0),
    'purple': (0.7, 0.2, 1.0),
    'pink':   (1.0, 0.4, 0.8),
    'orange': (1.0, 0.5, 0.1),
    'white':  (1.0, 1.0, 1.0),
    'lime':   (0.6, 1.0, 0.1),
    'teal':   (0.1, 0.9, 0.7),
}


def _parse_color(token: str) -> tuple | None:
    if token in _COLOR_NAMES:
        return _COLOR_NAMES[token]
    if token.startswith('#') and len(token) == 7:
        try:
            r = int(token[1:3], 16) / 255.0
            g = int(token[3:5], 16) / 255.0
            b = int(token[5:7], 16) / 255.0
            return (r, g, b)
        except ValueError:
            return None
    return None


_VALID_ANIMS  = ('wave_bright', 'color_travel', 'rainbow', 'pulse', 'static', 'wave', 'silver_wave')
_VALID_ENTERS = ('wave_in', 'drop_in', 'explode_in', 'spin_in', 'random_in', 'fade_in')


def _resolve_text(text: str) -> str:
    try:
        from plugins.tag import tag as _tag
        return _tag._resolve_symbols(text)
    except Exception:
        return text.replace('_', ' ')


def _parse_tag_args(args: list) -> tuple | None:
    color_stops = []
    anim        = 'wave_bright'
    enter       = 'wave_in'
    wave_speed  = 0.8
    i = 0
    while i < len(args):
        token = args[i].lower()
        if token == '-anim' and i + 1 < len(args):
            v = args[i + 1].lower()
            if v in _VALID_ANIMS:
                anim = v
            i += 2
            continue
        if token == '-enter' and i + 1 < len(args):
            v = args[i + 1].lower()
            if v in _VALID_ENTERS:
                enter = v
            i += 2
            continue
        if token == '-speed' and i + 1 < len(args):
            try:
                wave_speed = max(0.1, min(10.0, float(args[i + 1])))
            except ValueError:
                pass
            i += 2
            continue
        c = _parse_color(token)
        if c:
            color_stops.append(c)
        i += 1
    if not color_stops:
        return None
    return color_stops, anim, enter, wave_speed


def cmd_kick(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /kick <id|nombre>')
        return
    target = _find_player(args[0])
    if not target:
        _reply('Jugador no encontrado.')
        return
    try:
        name = target.getname()
        cid  = target.inputdevice.client_id
        import _bascenev1
        _bascenev1.disconnect_client(cid, ban_time=300)
        _reply(f'{name} fue kickeado (5 min).', (1.0, 0.5, 0.2))
    except Exception as e:
        print(f'[cmds.admin] kick error: {e}')


def cmd_ban(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /ban <id|nombre> [razon]')
        return
    target = _find_player(args[0])
    if not target:
        _reply('Jugador no encontrado.')
        return
    try:
        name = target.getname()
        acc  = target.get_account_id()
        reason = ' '.join(args[1:]) if len(args) > 1 else ''
        if _PERMS_AVAILABLE:
            _perms.ban(acc, reason)
        cid = target.inputdevice.client_id
        import _bascenev1
        _bascenev1.disconnect_client(cid, ban_time=300)
        msg = f'{name} fue baneado permanentemente.'
        if reason:
            msg += f' Razon: {reason}'
        _reply(msg, (1.0, 0.2, 0.2))
        print(f'[cmds.admin] ban: {acc} — {reason}')
    except Exception as e:
        print(f'[cmds.admin] ban error: {e}')


def cmd_mute(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /mute <id|nombre>')
        return
    target = _find_player(args[0])
    if not target:
        _reply('Jugador no encontrado.')
        return
    try:
        name = target.getname()
        target.set_admin_muted(True)
        _reply(f'{name} fue muteado.', (0.8, 0.8, 0.2))
    except Exception as e:
        print(f'[cmds.admin] mute error: {e}')


def cmd_end(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if act:
            with act.context:
                act.end_game()
            _reply('Partida finalizada.')
        else:
            _reply('No hay partida activa.')
    except Exception as e:
        print(f'[cmds.admin] end error: {e}')


def cmd_role(sp: object, args: list) -> None:
    if not _PERMS_AVAILABLE:
        _reply('Sistema de roles no disponible.')
        return
    acc = sp.get_v1_account_id()
    if not args:
        _reply('Uso: /role set <client_id> <rol>')
        _reply('/role remove <client_id>')
        _reply('/role create <nombre_> <color> [-anim ..] [-speed N]')
        _reply('/role addcmd <rol> <cmd>')
        return
    sub = args[0].lower()

    if sub == 'set':
        if len(args) < 3:
            _reply('Uso: /role set <client_id> <rol>')
            return
        try:
            target_cid = int(args[1])
        except ValueError:
            _reply('client_id invalido.')
            return
        role_name = args[2].lower()
        valid     = _perms.get_all_roles()
        if role_name not in valid:
            _reply(f'Rol invalido. Roles: {", ".join(valid)}')
            return
        target_acc = _perms.get_acc_from_client_id(target_cid)
        if not target_acc:
            _reply(f'Client {target_cid} no encontrado.')
            return
        caller_role    = _perms.get_role(acc)
        caller_level   = _perms.get_role_level(caller_role)
        target_role    = _perms.get_role(target_acc)
        target_cur_lvl = _perms.get_role_level(target_role)
        new_role_level = _perms.get_role_level(role_name)
        if new_role_level >= caller_level:
            _reply(f'No podes asignar un rol igual o superior al tuyo (level {caller_level}).')
            return
        if target_cur_lvl >= caller_level:
            _reply('No podes modificar el rol de alguien con nivel igual o superior al tuyo.')
            return
        _perms.set_account_role(target_acc, role_name)
        try:
            from plugins.tag import tag as _tag
            _tag.apply_live(target_acc)
        except Exception:
            pass
        bs.broadcastmessage(f'Tu rol fue actualizado a {role_name.upper()}. Renace para verlo.')
        _reply(f'Rol {role_name.upper()} asignado.')

    elif sub == 'remove':
        if len(args) < 2:
            _reply('Uso: /role remove <client_id>')
            return
        try:
            target_cid = int(args[1])
        except ValueError:
            _reply('client_id invalido.')
            return
        target_acc = _perms.get_acc_from_client_id(target_cid)
        if not target_acc:
            _reply(f'Client {target_cid} no encontrado.')
            return
        caller_role    = _perms.get_role(acc)
        caller_level   = _perms.get_role_level(caller_role)
        target_role    = _perms.get_role(target_acc)
        target_cur_lvl = _perms.get_role_level(target_role)
        if target_cur_lvl >= caller_level:
            _reply('No podes remover el rol de alguien con nivel igual o superior al tuyo.')
            return
        _perms.remove_account_role(target_acc)
        try:
            from plugins.tag import tag as _tag
            _tag.apply_live(target_acc)
        except Exception:
            pass
        _bascenev1.chatmessage('Tu rol fue removido. Renace para verlo.')
        _reply('Rol removido.')

    elif sub == 'create':
        caller_role  = _perms.get_role(acc)
        caller_level = _perms.get_role_level(caller_role)
        if caller_level < 80:
            _reply('No tenes permiso para crear roles.')
            return
        if len(args) < 4:
            _reply('Uso: /role create <level> <nombre_> <color>')
            _reply('[-anim wave_bright|rainbow|pulse|static] [-enter drop_in|explode_in|spin_in]')
            _reply('Colores: red blue green gold cyan')
            _reply('purple pink orange white lime teal | #RRGGBB')
            return
        try:
            new_level = int(args[1])
        except ValueError:
            _reply('Level invalido. Debe ser un numero entero.')
            return
        if new_level <= 0:
            _reply('Level debe ser mayor a 0.')
            return
        if new_level >= caller_level:
            _reply(f'No podes crear un rol con level {new_level}. Tu level es {caller_level}.')
            return
        role_name = args[2].lower().replace('_', ' ')
        result    = _parse_tag_args(args[3:])
        if result is None:
            _reply('Color invalido.')
            return
        color_stops, anim, enter, wave_speed = result
        if role_name in _perms.get_all_roles():
            _reply(f'El rol {role_name.upper()} ya existe.')
            return
        _perms.create_role(role_name, {
            'level':       new_level,
            'text':        role_name.upper(),
            'color_stops': [list(c) for c in color_stops],
            'anim':        anim,
            'enter':       enter,
            'wave_speed':  wave_speed,
            'commands':    [],
            'ids':         [],
        })
        _reply(f'Rol {role_name.upper()} creado (level {new_level}).')

    elif sub == 'addcmd':
        if _perms.get_role(acc) != 'owner':
            _reply('Solo el owner puede modificar permisos.')
            return
        if len(args) < 3:
            _reply('Uso: /role addcmd <rol> <cmd>')
            return
        role_name = args[1].lower()
        cmd_name  = args[2].lower()
        if role_name not in _perms.get_all_roles():
            _reply(f'Rol {role_name} no existe.')
            return
        _perms.add_role_perm(role_name, cmd_name)
        _reply(f'Cmd {cmd_name} agregado a {role_name.upper()}.')

    else:
        _reply('Subcomando invalido: set | remove | create | addcmd')


def cmd_tag(sp: object, args: list) -> None:
    if not _PERMS_AVAILABLE:
        _reply('Sistema de tags no disponible.')
        return
    if not args:
        _reply('Uso: /tag set <client_id> <TEXTO_> <color>')
        _reply('/tag remove <client_id>')
        return
    sub = args[0].lower()

    if sub == 'set':
        if len(args) < 4:
            _reply('Uso: /tag set <client_id> <TEXTO_> <color1> [color2]')
            _reply('[-anim wave_bright|rainbow|pulse|static] [-enter drop_in|explode_in|spin_in]')
            _reply('Colores: red blue green gold cyan')
            _reply('purple pink orange white lime teal | #RRGGBB')
            return
        try:
            target_cid = int(args[1])
        except ValueError:
            _reply('client_id invalido.')
            return
        raw_text = _resolve_text(args[2])
        result   = _parse_tag_args(args[3:])
        if result is None:
            _reply('Color invalido.')
            return
        color_stops, anim, enter, wave_speed = result
        target_acc = _perms.get_acc_from_client_id(target_cid)
        if not target_acc:
            _reply(f'Client {target_cid} no encontrado.')
            return
        _perms.set_tag(target_acc, {
            'text':        raw_text,
            'color_stops': [list(c) for c in color_stops],
            'anim':        anim,
            'enter':       enter,
            'wave_speed':  wave_speed,
        })
        try:
            from plugins.tag import tag as _tag
            _tag.apply_live(target_acc)
        except Exception:
            pass
        _bascenev1.chatmessage(f'Tu tag fue actualizado a [{raw_text}]. Renace para verlo.')
        _reply(f'Tag [{raw_text}] asignado.')

    elif sub == 'remove':
        if len(args) < 2:
            _reply('Uso: /tag remove <client_id>')
            return
        try:
            target_cid = int(args[1])
        except ValueError:
            _reply('client_id invalido.')
            return
        target_acc = _perms.get_acc_from_client_id(target_cid)
        if not target_acc:
            _reply(f'Client {target_cid} no encontrado.')
            return
        _perms.remove_tag(target_acc)
        try:
            from plugins.tag import tag as _tag
            _tag.apply_live(target_acc)
        except Exception:
            pass
        _bascenev1.chatmessage('Tu tag fue removido. Renace para verlo.')
        _reply('Tag removido.')

    else:
        _reply('Subcomando invalido: set | remove')


def cmd_ef(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /ef <cube|tesla> <client_id>')
        _reply('/ef remove <cube|tesla> <client_id>')
        return
    try:
        from plugins.effects import effects as _fx
    except Exception as e:
        _reply(f'Effects no disponible: {e}')
        return

    if args[0].lower() == 'remove':
        if len(args) < 3:
            _reply('Uso: /ef remove <cube|tesla> <client_id>')
            return
        effect = args[1].lower()
        if effect not in ('cube', 'tesla'):
            _reply('Efecto invalido: cube | tesla')
            return
        try:
            target_cid = int(args[2])
        except ValueError:
            _reply('client_id invalido.')
            return
        target_acc = _perms.get_acc_from_client_id(target_cid) if _PERMS_AVAILABLE else None
        if not target_acc:
            _reply(f'Client {target_cid} no encontrado.')
            return
        if _PERMS_AVAILABLE:
            _perms.remove_effect(target_acc, effect)
        _fx.remove(target_acc, effect)
        _reply(f'{effect.upper()} removido de client {target_cid}.')
        return

    effect = args[0].lower()
    if effect not in ('cube', 'tesla'):
        _reply('Efecto invalido: cube | tesla')
        return
    if len(args) < 2:
        _reply(f'Uso: /ef {effect} <client_id>')
        return
    try:
        target_cid = int(args[1])
    except ValueError:
        _reply('client_id invalido.')
        return
    target_acc = _perms.get_acc_from_client_id(target_cid) if _PERMS_AVAILABLE else None
    if not target_acc:
        _reply(f'Client {target_cid} no encontrado.')
        return
    if _PERMS_AVAILABLE:
        _perms.set_effect(target_acc, effect)
    if _fx.apply_live(target_acc, effect):
        _reply(f'{effect.upper()} aplicado a client {target_cid}.')
    else:
        _fx._ACTIVE[f'{target_acc}_{effect}_on'] = True
        _reply(f'{effect.upper()} guardado — se aplicará al renacer.')


def cmd_terrain(sp: object, args: list) -> None:
    try:
        import struct, os
        from bascenev1lib.gameutils import SharedObjects
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        shared = SharedObjects.get()
        with act.context:
            bs.newnode('terrain', attrs={
                'collision_mesh': bs.getcollisionmesh('av_bridge_v5Collide'),
                'mesh':           bs.getmesh('av_bridge_v5'),
                'color_texture':  bs.gettexture('bridgitLevelColor'),
                'materials':      [shared.footing_material],
            })
        _reply('Terrain creado.')
    except Exception as e:
        import traceback
        _reply(f'Error: {e} | {traceback.format_exc()[-200:]}')


def cmd_unban(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /unban <account_id>')
        return
    try:
        acc = args[0]
        if _PERMS_AVAILABLE:
            _perms.unban(acc)
            _reply(f'Desbaneado: {acc}', (0.2, 1.0, 0.4))
        else:
            _reply('Sistema de permisos no disponible.')
    except Exception as e:
        print(f'[cmds.admin] unban error: {e}')


def cmd_remove(sp: object, args: list) -> None:
    try:
        session = bs.get_foreground_host_session()
        if not session:
            _reply('No hay sesion activa.')
            return
        if not args or args[0].lower() == 'all':
            for p in session.sessionplayers:
                try:
                    p.remove_from_game()
                except Exception:
                    pass
            _reply('Todos removidos del juego.')
        else:
            cid = int(args[0])
            for p in session.sessionplayers:
                try:
                    if p.inputdevice.client_id == cid:
                        p.remove_from_game()
                        _reply(f'Client {cid} removido del juego.')
                        return
                except Exception:
                    pass
            _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.admin] remove error: {e}')


def cmd_slowmo(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            act.globalsnode.slow_motion = not act.globalsnode.slow_motion
            state = 'activado' if act.globalsnode.slow_motion else 'desactivado'
            _reply(f'Slow motion {state}.')
    except Exception as e:
        print(f'[cmds.admin] slowmo error: {e}')


def cmd_pause(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            act.globalsnode.paused = not act.globalsnode.paused
            state = 'pausada' if act.globalsnode.paused else 'reanudada'
            _reply(f'Partida {state}.')
    except Exception as e:
        print(f'[cmds.admin] pause error: {e}')


def cmd_nv(sp: object, args: list) -> None:
    def _is_close(a: tuple, b: tuple, tol: float = 1e-5) -> bool:
        return all(abs(x - y) < tol for x, y in zip(a, b))

    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        nv_tint    = (0.5, 0.5, 1.0)
        nv_ambient = (1.5, 1.5, 1.5)
        with act.context:
            if _is_close(act.globalsnode.tint, nv_tint):
                act.globalsnode.tint          = (1.0, 1.0, 1.0)
                act.globalsnode.ambient_color = (1.0, 1.0, 1.0)
                _reply('Night vision desactivado.')
            else:
                act.globalsnode.tint          = nv_tint
                act.globalsnode.ambient_color = nv_ambient
                _reply('Night vision activado.')
    except Exception as e:
        print(f'[cmds.admin] nv error: {e}')


def cmd_tint(sp: object, args: list) -> None:
    if len(args) < 3:
        _reply('Uso: /tint <r> <g> <b> (ej: 1.0 0.5 0.5)')
        return
    try:
        r, g, b = float(args[0]), float(args[1]), float(args[2])
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            act.globalsnode.tint = (r, g, b)
        _reply(f'Tint: ({r}, {g}, {b})')
    except Exception as e:
        print(f'[cmds.admin] tint error: {e}')


def cmd_camera(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            if act.globalsnode.camera_mode != 'rotate':
                act.globalsnode.camera_mode = 'rotate'
                _reply('Camara: modo rotacion.')
            else:
                act.globalsnode.camera_mode = 'normal'
                _reply('Camara: modo normal.')
    except Exception as e:
        print(f'[cmds.admin] camera error: {e}')


def cmd_party(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /party <public|private>')
        return
    sub = args[0].lower()
    if sub == 'public':
        bs.set_public_party_enabled(True)
        _reply('Servidor publico.')
    elif sub == 'private':
        bs.set_public_party_enabled(False)
        _reply('Servidor privado.')
    else:
        _reply('Uso: /party <public|private>')


def cmd_maxplayers(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /maxplayers <numero>')
        return
    try:
        n = int(args[0])
        bs.set_public_party_max_size(n)
        _reply(f'Max jugadores: {n}')
    except Exception as e:
        print(f'[cmds.admin] maxplayers error: {e}')


def cmd_unmute(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /unmute <id|nombre>')
        return
    target = _find_player(args[0])
    if not target:
        _reply('Jugador no encontrado.')
        return
    try:
        name = target.getname()
        target.set_admin_muted(False)
        _reply(f'{name} fue desmuteado.', (0.8, 0.8, 0.2))
    except Exception as e:
        print(f'[cmds.admin] unmute error: {e}')


def cmd_quit(sp: object, args: list) -> None:
    try:
        import babase
        _reply('Reiniciando servidor...', (1.0, 0.4, 0.4))
        bs.timer(1.0, babase.quit)
    except Exception as e:
        print(f'[cmds.admin] quit error: {e}')


def cmd_playlist(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /playlist <nombre>')
        return
    try:
        name = args[0]
        session = bs.get_foreground_host_session()
        if not session:
            _reply('No hay sesion activa.')
            return
        session.playlist_name = name
        _reply(f'Playlist cambiada a: {name}')
    except Exception as e:
        _reply(f'Error al cambiar playlist: {e}')
        print(f'[cmds.admin] playlist error: {e}')


def cmd_kickvote(sp: object, args: list) -> None:
    if len(args) < 2:
        _reply('Uso: /kickvote <enable|disable> <cid|all>')
        return
    try:
        import _babase
        sub = args[0].lower()
        target = args[1].lower()

        if sub not in ('enable', 'disable'):
            _reply('Subcomando invalido: enable | disable')
            return

        if target == 'all':
            _babase.set_enable_default_kick_voting(sub == 'enable')
            estado = 'habilitado' if sub == 'enable' else 'deshabilitado'
            _reply(f'Voto kick {estado} para todos.')
        else:
            cid = int(target)
            roster = bs.get_game_roster()
            for entry in roster:
                if entry.get('client_id') == cid:
                    import _bascenev1
                    if sub == 'enable':
                        _reply(f'Voto kick habilitado para client {cid}.')
                    else:
                        _bascenev1.disable_kickvote(entry['account_id'])
                        _reply(f'Voto kick deshabilitado para client {cid}.')
                    return
            _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.admin] kickvote error: {e}')


def cmd_info(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /info <client_id>')
        return
    try:
        from plugins.stats import stats as _stats
    except Exception:
        _reply('Stats no disponible.')
        return
    try:
        cid = int(args[0])
        roster = bs.get_game_roster()
        acc = None
        nombre = None
        for entry in roster:
            if entry.get('client_id') == cid:
                acc = entry.get('account_id')
                try:
                    nombre = entry['players'][0]['name_full']
                except Exception:
                    nombre = entry.get('display_string', '?')
                break
        if not acc:
            _reply('Jugador no encontrado.')
            return
        caller_cid = sp.inputdevice.client_id
        _reply(f'--- Info de {nombre} ---', (0.6, 0.9, 1.0))
        _reply(f'Account ID: {acc}', (0.8, 0.8, 0.8))
        _reply(f'Nombre: {nombre}', (0.8, 0.8, 0.8))
        p = _stats.get_player(acc)
        device_ids = p.get('device_ids', []) if p else []
        if not device_ids:
            _reply('Sin cuentas vinculadas registradas.', (0.8, 0.8, 0.8))
            return
        vinculadas = []
        all_stats = _stats.get_stats()
        for other_aid, other_p in all_stats.items():
            if other_aid == acc:
                continue
            other_devices = other_p.get('device_ids', [])
            if any(d in other_devices for d in device_ids):
                vinculadas.append(f"{other_p.get('name', '?')} ({other_aid})")
        if vinculadas:
            _reply(f'Cuentas vinculadas ({len(vinculadas)}):', (1.0, 0.7, 0.2))
            for v in vinculadas:
                _reply(f'  • {v}', (0.8, 0.8, 0.8))
        else:
            _reply('Sin cuentas vinculadas detectadas.', (0.8, 0.8, 0.8))
    except Exception as e:
        print(f'[cmds.admin] info error: {e}')


def cmd_gp(sp: object, args: list) -> None:
    if not args:
        _reply('Uso: /gp <client_id>')
        return
    try:
        cid = int(args[0])
        session = bs.get_foreground_host_session()
        if not session:
            _reply('No hay sesion activa.')
            return
        caller_cid = sp.inputdevice.client_id
        for p in session.sessionplayers:
            try:
                if p.inputdevice.client_id == cid:
                    nombre = p.getname(full=True, icon=False)
                    perfiles = p.inputdevice.get_player_profiles()
                    _reply(f'--- Perfiles de {nombre} ---', (0.6, 0.9, 1.0))
                    if not perfiles:
                        _reply('Sin perfiles registrados.', (0.8, 0.8, 0.8))
                        return
                    for i, perfil in enumerate(perfiles, 1):
                        _reply(f'{i}. {perfil}', (0.8, 0.8, 0.8))
                    return
            except Exception:
                pass
        _reply('Jugador no encontrado.')
    except Exception as e:
        print(f'[cmds.admin] gp error: {e}')


def cmd_dv(sp: object, args: list) -> None:
    try:
        act = bs.get_foreground_host_activity()
        if not act:
            _reply('No hay partida activa.')
            return
        with act.context:
            act.globalsnode.tint          = (1.0, 1.0, 1.0)
            act.globalsnode.ambient_color = (1.0, 1.0, 1.0)
            _reply('Modo dia activado.')
    except Exception as e:
        print(f'[cmds.admin] dv error: {e}')


def cmd_lm(sp: object, args: list) -> None:
    try:
        import _bascenev1
        msgs = bs.get_chat_messages()
        if not msgs:
            _reply('No hay mensajes recientes.')
            return
        for m in msgs:
            text = m if isinstance(m, str) else str(m)
            _bascenev1.chatmessage(text)
    except Exception as e:
        print(f'[cmds.admin] lm error: {e}')


CMDS: dict = {
    'kick':       (None, cmd_kick),
    'ban':        (None, cmd_ban),
    'mute':       (None, cmd_mute),
    'end':        (None, cmd_end),
    'role':       (None, cmd_role),
    'tag':        (None, cmd_tag),
    'ef':         (None, cmd_ef),
    'terrain':    (None, cmd_terrain),
    'unban':      (None, cmd_unban),
    'remove':     (None, cmd_remove),
    'slowmo':     (None, cmd_slowmo),
    'sm':         (None, cmd_slowmo),
    'pause':      (None, cmd_pause),
    'nv':         (None, cmd_nv),
    'tint':       (None, cmd_tint),
    'camera':     (None, cmd_camera),
    'party':      (None, cmd_party),
    'maxplayers': (None, cmd_maxplayers),
    'lm':         (None, cmd_lm),
    'unmute':     (None, cmd_unmute),
    'quit':       (None, cmd_quit),
    'playlist':   (None, cmd_playlist),
    'kickvote':   (None, cmd_kickvote),
    'info':       (None, cmd_info),
    'gp':         (None, cmd_gp),
    'dv':         (None, cmd_dv),
}
