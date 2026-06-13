# ba_meta require api 9

from __future__ import annotations
import subprocess
import sys
import os
import threading

_BOT_SCRIPT = r'''
import discord
from discord.ext import commands
from discord import app_commands
import json, os, io, math, asyncio
from PIL import Image, ImageDraw, ImageFont

# --- bot_config.json ---
import json as _json
_BOT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bot_config.json')
with open(_BOT_CONFIG_PATH, 'r', encoding='utf-8') as _f:
    _CFG = _json.load(_f)
BOT_TOKEN    = _CFG['token']
_BASE        = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
_DATA_BASE   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nexus_data'))
PERMS_PATH   = os.path.join(_BASE, 'plugins', 'perms', 'perms_data.json')
RELOAD_FLAG  = os.path.join(_BASE, 'plugins', 'perms', '.reload')
ALLOWED_ROLE = _CFG['allowed_role']
CHAT_WEBHOOK      = _CFG['webhooks']['chat']
CHAT_JSON         = os.path.join(_DATA_BASE, 'chat.json')
DC_TO_BS          = os.path.join(_DATA_BASE, 'dc_to_bs.txt')
LIVE_CHAT_CHANNEL = _CFG['channels']['live_chat']
REPORTS_WEBHOOK   = _CFG['webhooks']['reports']
REPORTS_JSON      = os.path.join(_DATA_BASE, 'reports.json')
CHARS_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bs_chars')
ICONS_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bs_icons')

VERIFY_CHANNEL  = _CFG['channels']['verify']
LOGS_CHANNEL    = _CFG['channels']['logs']
VERIFY_NOTIFY   = os.path.join(_DATA_BASE, 'verify_notify.json')
PENDING_VERIFY  = os.path.join(_DATA_BASE, 'pending_verify.json')
VERIFIED_PATH   = os.path.join(_DATA_BASE, 'verified.json')
ROSTER_PATH     = os.path.join(_DATA_BASE, 'roster.json')
TICKETS_PATH    = os.path.join(_DATA_BASE, 'tickets.json')

_CHAR_DEFAULT_ICON = {
    'neoSpaz':     '\ue01e',
    'ninja':       '\ue04b',
    'bones':       '\ue046',
    'kronk':       '\ue049',
    'mel':         '\ue047',
    'zoe':         '\ue047',
    'pixie':       '\ue047',
    'bunny':       '\ue047',
    'bear':        '\ue04a',
    'penguin':     '\ue04a',
    'frosty':      '\ue064',
    'santa':       '\ue064',
    'jack':        '\ue046',
    'ali':         '\ue067',
    'wrestler':    '\ue067',
    'gladiator':   '\ue049',
    'warrior':     '\ue049',
    'superhero':   '\ue063',
    'agent':       '\ue042',
    'cyborg':      '\ue063',
    'robot':       '\ue063',
    'wizard':      '\ue048',
    'witch':       '\ue048',
    'operaSinger': '\ue047',
    'oldLady':     '\ue041',
    'cowboy':      '\ue041',
    'jumpsuit':    '\ue04f',
    'assassin':    '\ue04b',
    'alien':       '\ue045',
    'actionHero':  '\ue04f',
}

ANIMS  = ['static', 'wave', 'wave_bright', 'pulse', 'rainbow', 'color_travel']
ENTERS = ['fade_in', 'wave_in', 'drop_in', 'explode_in', 'spin_in', 'random_in']

import threading as _threading
import aiohttp as _aiohttp_mod
import numpy as _np

_chat_seen_ids: set = set()
_chat_lock = _threading.Lock()

def _init_chat_seen_ids() -> None:
    import json as _json
    if not os.path.exists(CHAT_JSON):
        return
    try:
        with open(CHAT_JSON, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        with _chat_lock:
            for msg in data.get('messages', []):
                mid = msg.get('id')
                if mid:
                    _chat_seen_ids.add(mid)
        print(f'[chat] {len(_chat_seen_ids)} mensajes existentes marcados como vistos')
    except Exception as e:
        print(f'[chat] _init_chat_seen_ids error: {e}')

def _tint_image(avatar: 'Image.Image', color: list, highlight: list,
                char: str = '') -> 'Image.Image':
    mask_path = os.path.join(CHARS_DIR, f'{char}Mask.png') if char else ''
    if not mask_path or not os.path.exists(mask_path):
        return avatar

    base = _np.array(avatar).astype(_np.float32) / 255.0
    mask = _np.array(
        Image.open(mask_path).convert('RGBA').resize(avatar.size, Image.LANCZOS)
    ).astype(_np.float32) / 255.0

    tint1 = _np.array(color[:3],     dtype=_np.float32)
    tint2 = _np.array(highlight[:3], dtype=_np.float32)

    m_r = mask[:, :, 0:1]
    m_g = mask[:, :, 1:2]
    base_weight = _np.clip(1.0 - m_r - m_g, 0.0, 1.0)

    result = _np.zeros_like(base)
    result[:, :, :3] = (
        base[:, :, :3] * base_weight +
        base[:, :, :3] * m_r * tint1 +
        base[:, :, :3] * m_g * tint2
    )
    result[:, :, 3] = base[:, :, 3]

    return Image.fromarray((_np.clip(result, 0.0, 1.0) * 255).astype(_np.uint8), 'RGBA')

def _render_verify_card(player: dict) -> io.BytesIO:
    W, H     = 520, 130
    PAD      = 14
    AVATAR_S = 90
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw   = ImageDraw.Draw(canvas)
    bg = Image.new('RGBA', (W, H), (20, 22, 35, 235))
    canvas.alpha_composite(bg)
    char     = player.get('character', 'neoSpaz')
    char_png = os.path.join(CHARS_DIR, f'{char}.png')
    if not os.path.exists(char_png):
        char_png = os.path.join(CHARS_DIR, 'neoSpaz.png')
    color     = player.get('color',     [1.0, 1.0, 1.0])
    highlight = player.get('highlight', [1.0, 1.0, 1.0])
    if os.path.exists(char_png):
        avatar = Image.open(char_png).convert('RGBA').resize((AVATAR_S, AVATAR_S))
        try:
            avatar = _tint_image(avatar, color, highlight, char=char)
        except Exception:
            pass
        ay = (H - AVATAR_S) // 2
        canvas.alpha_composite(avatar, (PAD, ay))
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
        font_sub   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub   = font_title
        font_small = font_title
    r = int(max(0, min(1, color[0])) * 255)
    g = int(max(0, min(1, color[1])) * 255)
    b = int(max(0, min(1, color[2])) * 255)
    text_x = PAD + AVATAR_S + PAD
    account_name = player.get('account_name', '')
    profile_name = player.get('name', '???')
    aid          = player.get('aid', '')
    if account_name:
        icon_char = ''
        clean_name = account_name
        if account_name and 0xe000 <= ord(account_name[0]) <= 0xf8ff:
            icon_char  = account_name[0]
            clean_name = account_name[1:].strip()
        icon_x = text_x
        name_x = text_x
        if icon_char:
            icon_hex  = f'{ord(icon_char):04x}'
            icon_path = os.path.join(ICONS_DIR, f'{icon_hex}.png')
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path).convert('RGBA').resize((22, 22), Image.LANCZOS)
                canvas.alpha_composite(icon_img, (text_x, 8))
                name_x = text_x + 26
        draw.text((name_x, 8),  clean_name,            font=font_title, fill=(r, g, b, 255))
        draw.text((text_x, 32), f'Perfil: {profile_name}', font=font_sub,   fill=(180, 180, 200, 200))
        draw.text((text_x, 50), f'ID: {aid}',           font=font_small, fill=(120, 120, 140, 170))
        draw.text((text_x, 68), '\u00bfEste es tu',    font=font_sub,   fill=(200, 200, 215, 220))
        draw.text((text_x, 84), 'nombre de cuenta?',   font=font_sub,   fill=(200, 200, 215, 220))
        draw.text((text_x, 100),'Confirm\u00e1 abajo.',font=font_small, fill=(130, 130, 150, 180))
    else:
        draw.text((text_x, 14), profile_name,           font=font_title, fill=(r, g, b, 255))
        draw.text((text_x, 38), f'ID: {aid}',           font=font_sub,   fill=(160, 160, 180, 200))
        draw.text((text_x, 58), '\u00bfEsta es tu',    font=font_sub,   fill=(200, 200, 215, 220))
        draw.text((text_x, 74), 'cuenta de BombSquad?',font=font_sub,   fill=(200, 200, 215, 220))
        draw.text((text_x, 92), 'Confirm\u00e1 abajo.',font=font_small, fill=(130, 130, 150, 180))
    draw.rectangle([0, 0, 4, H], fill=(r, g, b, 220))
    draw.rectangle([0, 0, W, 2], fill=(r, g, b, 80))
    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

def _render_log_card(player: dict, role: str, member_num: int) -> io.BytesIO:
    W, H     = 520, 120
    PAD      = 10
    AVATAR_S = 85

    if role == 'uzc1':
        accent = (130, 80, 200)   # morado
    else:
        accent = (140, 140, 160)  # plomo

    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw   = ImageDraw.Draw(canvas)

    bg = Image.new('RGBA', (W, H), (14, 14, 22, 245))
    canvas.alpha_composite(bg)

    for x in range(6):
        alpha = int(220 * (1 - x / 6))
        draw.rectangle([x, 0, x, H], fill=(*accent, alpha))

    draw.rectangle([0, 0, W, 2], fill=(*accent, 120))
    draw.rectangle([0, H-2, W, H], fill=(*accent, 60))

    char     = player.get('character', 'neoSpaz')
    char_png = os.path.join(CHARS_DIR, f'{char}.png')
    if not os.path.exists(char_png):
        char_png = os.path.join(CHARS_DIR, 'neoSpaz.png')
    color     = player.get('color',     [1.0, 1.0, 1.0])
    highlight = player.get('highlight', [1.0, 1.0, 1.0])
    if os.path.exists(char_png):
        avatar = Image.open(char_png).convert('RGBA').resize((AVATAR_S, AVATAR_S))
        try:
            avatar = _tint_image(avatar, color, highlight, char=char)
        except Exception:
            pass
        ay = (H - AVATAR_S) // 2
        canvas.alpha_composite(avatar, (PAD, ay))

    try:
        font_big   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19)
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
        font_sub   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    except Exception:
        font_big = font_title = font_sub = font_small = ImageFont.load_default()

    r = int(max(0, min(1, color[0])) * 255)
    g = int(max(0, min(1, color[1])) * 255)
    b = int(max(0, min(1, color[2])) * 255)

    text_x       = PAD + AVATAR_S + PAD
    account_name = player.get('account_name', '')
    profile_name = player.get('name', '???')
    aid          = player.get('aid', '')

    clean_name = account_name
    name_x     = text_x
    if account_name and 0xe000 <= ord(account_name[0]) <= 0xf8ff:
        icon_char = account_name[0]
        clean_name = account_name[1:].strip()
        icon_hex  = f'{ord(icon_char):04x}'
        icon_path = os.path.join(ICONS_DIR, f'{icon_hex}.png')
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).convert('RGBA').resize((22, 22), Image.LANCZOS)
            canvas.alpha_composite(icon_img, (text_x, 8))
            name_x = text_x + 26

    display = clean_name if clean_name else profile_name

    draw.text((name_x, 6),   display,                          font=font_big,   fill=(r, g, b, 255))
    draw.text((text_x, 32),  f'Perfil: {profile_name}',      font=font_sub,   fill=(170, 170, 195, 210))
    draw.text((text_x, 47),  f'ID: {aid}',                   font=font_small, fill=(110, 110, 135, 170))

    role_label = 'UZC' if role == 'uzc1' else 'ALT'
    draw.text((text_x, 64),  f'Rol: {role_label}',           font=font_sub,   fill=(*accent, 230))

    draw.text((text_x, 80),  f'Miembro #{member_num}',       font=font_sub,   fill=(160, 160, 180, 200))

    badge_text = '✅ Verificado'
    try:
        bw = font_small.getlength(badge_text)
    except Exception:
        bw = 70
    draw.text((W - bw - 10, H - 16), badge_text, font=font_small, fill=(*accent, 200))

    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

def _remove_pending_token(token: str) -> None:
    try:
        if not os.path.exists(PENDING_VERIFY):
            return
        with open(PENDING_VERIFY, 'r', encoding='utf-8') as f:
            pending = json.load(f)
        pending.pop(token, None)
        with open(PENDING_VERIFY, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)
    except Exception as e:
        print(f'[verify] error: {e}')

def _get_player_from_roster(acc: str) -> dict | None:
    try:
        if os.path.exists(ROSTER_PATH):
            with open(ROSTER_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for p in data.get('players', []):
                if p.get('aid') == acc:
                    return p
    except Exception:
        pass
    try:
        stats_path = os.path.join(_DATA_BASE, 'stats.json')
        if os.path.exists(stats_path):
            with open(stats_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            p = data.get('stats', {}).get(acc)
            if p:
                return {
                    'aid':          acc,
                    'name':         p.get('name', acc),
                    'account_name': p.get('account_name', ''),
                    'character':    p.get('character', 'neoSpaz'),
                    'color':        p.get('color',     [1.0, 1.0, 1.0]),
                    'highlight':    p.get('highlight', [1.0, 1.0, 1.0]),
                }
    except Exception:
        pass
    return None

def _load_tickets() -> dict:
    try:
        if os.path.exists(TICKETS_PATH):
            with open(TICKETS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _save_tickets(data: dict) -> None:
    try:
        with open(TICKETS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f'[tickets] save error: {e}')

class CloseTicketView(discord.ui.View):
    def __init__(self, channel_id: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id

    @discord.ui.button(label='\U0001f512 Cerrar ticket', style=discord.ButtonStyle.secondary)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(r.id == ALLOWED_ROLE for r in interaction.user.roles):
            await interaction.response.send_message('\u26d4 Solo admins pueden cerrar tickets.', ephemeral=True)
            return
        channel = interaction.channel
        tickets = _load_tickets()
        tickets = {k: v for k, v in tickets.items() if v.get('channel_id') != channel.id}
        _save_tickets(tickets)
        await interaction.response.send_message('\U0001f512 Cerrando ticket...', ephemeral=True)
        await asyncio.sleep(3)
        try:
            await channel.delete()
        except Exception as e:
            print(f'[tickets] close error: {e}')

class RoleChoiceView(discord.ui.View):
    def __init__(self, acc: str, player: dict, discord_id: int, ticket_channel: 'discord.TextChannel'):
        super().__init__(timeout=None)
        self.acc            = acc
        self.player         = player
        self.discord_id     = discord_id
        self.ticket_channel = ticket_channel
        self.used           = False

    async def _assign_role(self, interaction: discord.Interaction, discord_role_id: int, bs_role: str, label: str):
        if self.used:
            await interaction.response.send_message('\u26a0\ufe0f Ya elegiste.', ephemeral=True)
            return
        self.used = True
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f'\u2705 Verificado con rol **{label}**. \u00a1Bienvenidx!',
            view=self
        )
        async def _do_work():
            try:
                guild = interaction.guild
                try:
                    member = await guild.fetch_member(self.discord_id)
                except Exception:
                    member = guild.get_member(self.discord_id)
                if member:
                    try:
                        role = guild.get_role(discord_role_id)
                        if role:
                            await member.add_roles(role)
                            print(f'[verify] rol Discord asignado a {self.discord_id}')
                        else:
                            print(f'[verify] role objeto es None para id={discord_role_id}')
                    except Exception as e:
                        print(f'[verify] add_role error: {e}')
                try:
                    pending_roles_path = os.path.join(_DATA_BASE, 'pending_bs_roles.json')
                    pr = {}
                    if os.path.exists(pending_roles_path):
                        with open(pending_roles_path, 'r', encoding='utf-8') as f:
                            pr = json.load(f)
                    pr[self.acc] = bs_role
                    with open(pending_roles_path, 'w', encoding='utf-8') as f:
                        json.dump(pr, f, indent=2)
                except Exception as e:
                    print(f'[verify] bs_role error: {e}')
                try:
                    logs_ch = bot.get_channel(LOGS_CHANNEL)
                    if logs_ch:
                        member_num = 1
                        try:
                            with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
                                member_num = len(json.load(f))
                        except Exception:
                            pass
                        buf  = await asyncio.get_event_loop().run_in_executor(None, _render_log_card, self.player, bs_role, member_num)
                        file = discord.File(buf, filename="log_card.png")
                        color_accent = 0x7B4FCC if bs_role == "uzc1" else 0x8C8CA0
                        embed = discord.Embed(
                            title="\u2705 Verificaci\u00f3n exitosa",
                            color=color_accent
                        )
                        embed.add_field(name="Usuario Discord", value=f"<@{self.discord_id}>", inline=True)
                        embed.add_field(name="Rol asignado",    value=label,                   inline=True)
                        embed.set_image(url="attachment://log_card.png")
                        embed.set_footer(text=f'Verificado el {__import__("datetime").datetime.now().strftime("%d/%m/%Y %H:%M")}')
                        await logs_ch.send(embed=embed, file=file)
                except Exception as e:
                    print(f"[verify] log error: {e}")
                if self.ticket_channel:
                    try:
                        await self.ticket_channel.send(
                            f'\u2705 <@{self.discord_id}> verificadx con rol **{label}**. '
                            f'Un admin puede cerrar este ticket cuando quiera.',
                            view=CloseTicketView(self.ticket_channel.id)
                        )
                    except Exception as e:
                        print(f'[verify] ticket error: {e}')
            except Exception as e:
                print(f'[verify] _do_work error: {e}')
        await _do_work()

    @discord.ui.button(label='\u2b21 UZC', style=discord.ButtonStyle.primary)
    async def choose_modern(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._assign_role(interaction, _CFG['roles']['uzc'], 'uzc1', 'UZC')

    @discord.ui.button(label='\u2b21 ALT', style=discord.ButtonStyle.secondary)
    async def choose_legacy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._assign_role(interaction, _CFG['roles']['alt'], 'alt1', 'ALT')

class StartVerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='\U0001f3ae Verificarme', style=discord.ButtonStyle.success, custom_id='start_verify')
    async def start_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        user  = interaction.user
        if os.path.exists(VERIFIED_PATH):
            try:
                with open(VERIFIED_PATH, 'r', encoding='utf-8') as f:
                    verified = json.load(f)
                for data in verified.values():
                    if data.get('discord_id') == user.id:
                        await interaction.followup.send('\u26a0\ufe0f Ya est\u00e1s verificadx.', ephemeral=True)
                        return
            except Exception:
                pass
        tickets = _load_tickets()
        if str(user.id) in tickets:
            ch = guild.get_channel(tickets[str(user.id)]['channel_id'])
            if ch:
                await interaction.followup.send(f'\u26a0\ufe0f Ya ten\u00e9s un ticket abierto: {ch.mention}', ephemeral=True)
                return
            else:
                del tickets[str(user.id)]
                _save_tickets(tickets)
        overwrites = {
            guild.default_role:          discord.PermissionOverwrite(read_messages=False),
            user:                        discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.get_role(ALLOWED_ROLE): discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        safe_name = ''.join(c for c in user.display_name if c.isalnum() or c in '-_')[:20] or 'usuario'
        category  = guild.get_channel(VERIFY_CHANNEL)
        cat       = category.category if category else None
        channel   = await guild.create_text_channel(
            f'verificar-{safe_name}',
            overwrites=overwrites,
            category=cat,
            topic=f'Ticket de verificaci\u00f3n para {user}'
        )
        tickets[str(user.id)] = {'channel_id': channel.id, 'created_at': __import__('time').time()}
        _save_tickets(tickets)
        import uuid, time as _t
        token   = uuid.uuid4().hex[:12].upper()
        expires = _t.time() + 7200
        pending = {}
        if os.path.exists(PENDING_VERIFY):
            try:
                with open(PENDING_VERIFY, 'r', encoding='utf-8') as f:
                    pending = json.load(f)
            except Exception:
                pass
        pending[token] = {
            'acc':        None,
            'discord_id': user.id,
            'expires':    expires,
            'channel_id': channel.id,
        }
        with open(PENDING_VERIFY, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)
        embed = discord.Embed(
            title='\U0001f3ae C\u00f3mo verificarte',
            description=(
                f'Hola {user.mention}! Segu\u00ed estos pasos:\n\n'
                f'**1.** Entr\u00e1 al servidor de BombSquad\n'
                f'**2.** Escrib\u00ed en el chat del juego:\n'
                f'```/v {token}```\n'
                f'**3.** Confirm\u00e1 tu cuenta con el bot\u00f3n que aparece\n\n'
                f'\u23f0 Este token expira en **2 horas**.'
            ),
            color=0x5865f2
        )
        embed.set_footer(text='Si ten\u00e9s problemas un admin puede ayudarte aqu\u00ed.')
        await channel.send(
            content=f'{user.mention} \u2014 Tu ticket de verificaci\u00f3n',
            embed=embed
        )
        await interaction.followup.send(f'\u2705 Ticket creado: {channel.mention}', ephemeral=True)

class VerifyConfirmView(discord.ui.View):
    def __init__(self, token: str, acc: str, player: dict, discord_id: int, ticket_channel: 'discord.TextChannel'):
        super().__init__(timeout=7200)
        self.token          = token
        self.acc            = acc
        self.player         = player
        self.discord_id     = discord_id
        self.ticket_channel = ticket_channel
        self.used           = False

    @discord.ui.button(label='\u2713  S\u00ed, es mi cuenta', style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.discord_id:
            await interaction.response.send_message('\u274c Este bot\u00f3n no es tuyo.', ephemeral=True)
            return
        if self.used:
            await interaction.response.send_message('\u26a0\ufe0f Ya fue usado.', ephemeral=True)
            return
        self.used = True
        import time as _t
        verified = {}
        if os.path.exists(VERIFIED_PATH):
            try:
                with open(VERIFIED_PATH, 'r', encoding='utf-8') as f:
                    verified = json.load(f)
            except Exception:
                pass
        verified[self.acc] = {
            'discord_id':   self.discord_id,
            'discord_name': str(interaction.user),
            'bs_name':      self.player.get('name', '???'),
            'account_name': self.player.get('account_name', ''),
            'verified_at':  _t.time()
        }
        with open(VERIFIED_PATH, 'w', encoding='utf-8') as f:
            json.dump(verified, f, indent=2, ensure_ascii=False)
        _remove_pending_token(self.token)
        role_view = RoleChoiceView(self.acc, self.player, self.discord_id, self.ticket_channel)
        await interaction.response.edit_message(
            content=f'\u2705 Cuenta confirmada. **\u00bfQu\u00e9 rol prefer\u00eds?**',
            view=role_view
        )

    @discord.ui.button(label='\u2717  No es m\u00eda', style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.discord_id:
            await interaction.response.send_message('\u274c Este bot\u00f3n no es tuyo.', ephemeral=True)
            return
        self.used = True
        _remove_pending_token(self.token)
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content='\u274c Cuenta rechazada. Ejecut\u00e1 /v TOKEN de nuevo en el juego.',
            view=self
        )

def _render_chat_card(entry: dict) -> io.BytesIO:
    W, H     = 520, 95
    PAD      = 10
    AVATAR_S = 60

    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw   = ImageDraw.Draw(canvas)

    bg = Image.new('RGBA', (W, H), (30, 30, 40, 220))
    canvas.alpha_composite(bg)

    char     = entry.get('character', 'neoSpaz')
    char_png = os.path.join(CHARS_DIR, f'{char}.png')
    if not os.path.exists(char_png):
        char_png = os.path.join(CHARS_DIR, 'neoSpaz.png')

    if os.path.exists(char_png):
        avatar    = Image.open(char_png).convert('RGBA').resize((AVATAR_S, AVATAR_S))
        color     = entry.get('color',     [1.0, 1.0, 1.0])
        highlight = entry.get('highlight', [1.0, 1.0, 1.0])
        try:
            avatar = _tint_image(avatar, color, highlight, char=char)
        except Exception as e:
            print(f'[chat] tint error: {e}')
        ay = (H - AVATAR_S) // 2
        canvas.alpha_composite(avatar, (PAD, ay))

    try:
        font_name = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
        font_msg  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except Exception:
        font_name = ImageFont.load_default()
        font_msg  = font_name

    text_x = PAD + AVATAR_S + PAD

    tag_text = entry.get('tag_text', '')
    tag_icon = entry.get('tag_icon', '')

    if not tag_icon:
        char = entry.get('character', 'neoSpaz')
        tag_icon = _CHAR_DEFAULT_ICON.get(char, '\ue01e')

    icon_img = None
    if tag_icon:
        code      = f'{ord(tag_icon):04x}'
        icon_path = os.path.join(ICONS_DIR, f'{code}.png')
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).convert('RGBA').resize((18, 18))

    tag_color_raw = entry.get('color', [1.0, 1.0, 1.0])
    r = int(max(0, min(1, tag_color_raw[0])) * 255)
    g = int(max(0, min(1, tag_color_raw[1])) * 255)
    b = int(max(0, min(1, tag_color_raw[2])) * 255)
    name_color = (r, g, b, 255)

    name_y = 14
    cur_x  = text_x

    if icon_img:
        canvas.alpha_composite(icon_img, (cur_x, name_y))
        cur_x += 22

    display_name = entry.get('name', '???')
    draw.text((cur_x, name_y), display_name, font=font_name, fill=name_color)

    msg = entry.get('message', '')
    draw.text((text_x, name_y + 22), msg, font=font_msg, fill=(210, 210, 220, 255))

    try:
        font_pb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
    except Exception:
        font_pb = font_msg
    pb = entry.get('account_id', '')
    draw.text((text_x, H - 13), pb, font=font_pb, fill=(90, 90, 110, 200))

    draw.rectangle([0, 0, 3, H], fill=(r, g, b, 200))

    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

async def _chat_watcher(session: _aiohttp_mod.ClientSession) -> None:
    import asyncio
    import time as _time
    _init_chat_seen_ids()
    while True:
        await asyncio.sleep(2)
        if not os.path.exists(CHAT_JSON):
            continue
        try:
            with open(CHAT_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
            messages = data.get('messages', [])
            now = _time.time()
            new_msgs = []
            with _chat_lock:
                for msg in messages:
                    mid = msg.get('id')
                    if mid and mid not in _chat_seen_ids:
                        ts = msg.get('timestamp', 0)
                        if ts and (now - ts) > 30:
                            _chat_seen_ids.add(mid)
                            continue
                        new_msgs.append(msg)

            for msg in new_msgs:
                mid = msg.get('id')
                try:
                    buf  = await asyncio.get_event_loop().run_in_executor(None, _render_chat_card, msg)
                    form = _aiohttp_mod.FormData()
                    form.add_field('file', buf, filename='chat.png', content_type='image/png')
                    async with session.post(CHAT_WEBHOOK, data=form) as resp:
                        if resp.status == 429:
                            retry_after = float((await resp.json()).get('retry_after', 2))
                            print(f'[chat] rate limit, esperando {retry_after}s')
                            await asyncio.sleep(retry_after)
                        elif resp.status in (200, 204):
                            with _chat_lock:
                                _chat_seen_ids.add(mid)
                        else:
                            print(f'[chat] webhook error: {resp.status}')
                except Exception as e:
                    print(f'[chat] error enviando mensaje: {e}')
                await asyncio.sleep(1.5)
        except Exception as e:
            print(f'[chat] loop error: {e}')

COLORS_PRESET = {
    'Rojo':      [(1.0, 0.0, 0.0)],
    'Azul':      [(0.2, 0.5, 1.0)],
    'Verde':     [(0.0, 1.0, 0.3)],
    'Amarillo':  [(1.0, 0.9, 0.0)],
    'Morado':    [(0.7, 0.0, 1.0)],
    'Blanco':    [(1.0, 1.0, 1.0)],
    'Naranja':   [(1.0, 0.5, 0.0)],
    'Cian':      [(0.0, 1.0, 1.0)],
    'Rosa':      [(1.0, 0.3, 0.7)],
    'Oro':       [(1.0, 0.84, 0.0)],
    'Arcoiris':  [(1.0,0.0,0.0),(1.0,0.5,0.0),(1.0,1.0,0.0),(0.0,1.0,0.0),(0.0,0.5,1.0),(0.5,0.0,1.0)],
    'Fuego':     [(1.0,0.0,0.0),(1.0,0.6,0.0),(1.0,1.0,0.0)],
    'Hielo':     [(0.4,0.8,1.0),(1.0,1.0,1.0)],
    'Diamante':  [(0.4,0.8,1.0),(0.8,1.0,1.0),(0.4,0.8,1.0)],
    'Leyenda':   [(1.0,0.55,0.0),(1.0,1.0,0.0),(1.0,0.55,0.0)],
}

def _load_perms() -> dict:
    if os.path.exists(PERMS_PATH):
        with open(PERMS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'accounts': {}, 'role_defs': {}, 'role_perms': {}, 'tags': {}, 'hierarchy': {}}

def _save_perms(data: dict) -> None:
    import shutil
    tmp = PERMS_PATH + '.tmp'
    bak = PERMS_PATH + '.backup'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(PERMS_PATH):
        shutil.copyfile(PERMS_PATH, bak)
    os.replace(tmp, PERMS_PATH)
    open(RELOAD_FLAG, 'w').close()

def save_tag(acc: str, tag_cfg: dict) -> None:
    data = _load_perms()
    data.setdefault('tags', {})[acc] = tag_cfg
    _save_perms(data)

def remove_tag(acc: str) -> None:
    data = _load_perms()
    data.get('tags', {}).pop(acc, None)
    _save_perms(data)

def get_tag(acc: str) -> dict | None:
    return _load_perms().get('tags', {}).get(acc)

def _parse_color_input(text: str) -> tuple | None:
    text = text.strip()
    if text.startswith('#') and len(text) == 7:
        try:
            r = int(text[1:3], 16) / 255.0
            g = int(text[3:5], 16) / 255.0
            b = int(text[5:7], 16) / 255.0
            return (r, g, b)
        except ValueError:
            return None
    parts = [p.strip() for p in text.replace(';', ',').split(',')]
    if len(parts) == 3:
        try:
            vals = [float(p) for p in parts]
            if any(v > 1.0 for v in vals):
                vals = [v / 255.0 for v in vals]
            if all(0.0 <= v <= 1.0 for v in vals):
                return tuple(vals)
        except ValueError:
            pass
    return None

def _color_swatch(colors: list) -> str:
    emoji_map = [
        ((0.8,0.2,0.2), '\U0001f534'), ((0.2,0.4,1.0), '\U0001f535'), ((0.2,0.8,0.2), '\U0001f7e2'),
        ((1.0,0.8,0.0), '\U0001f7e1'), ((1.0,0.5,0.0), '\U0001f7e0'), ((0.5,0.0,0.5), '\U0001f7e3'),
        ((0.6,0.3,0.1), '\U0001f7e4'), ((0.0,0.0,0.0), '\u26ab'), ((1.0,1.0,1.0), '\u26aa'),
    ]
    result = []
    for c in colors:
        best = '\U0001f518'
        best_dist = 999
        for ref, em in emoji_map:
            d = sum((c[i]-ref[i])**2 for i in range(3))
            if d < best_dist:
                best_dist = d
                best = em
        hex_val = '#{:02X}{:02X}{:02X}'.format(int(c[0]*255), int(c[1]*255), int(c[2]*255))
        result.append(f'{best}`{hex_val}`')
    return '  '.join(result)

_CHAR_WIDTHS = {
    'A':16.758,'B':15.898,'C':15.555,'D':16.156,'E':14.352,'F':13.148,
    'G':15.898,'H':17.102,'I':7.906,'J':9.625,'K':15.727,'L':13.234,
    'M':20.883,'N':17.102,'O':17.102,'P':15.039,'Q':17.359,'R':15.984,
    'S':15.555,'T':15.039,'U':16.156,'V':15.469,'W':20.453,'X':15.297,
    'Y':15.469,'Z':14.953,'a':12.547,'b':12.891,'c':11.773,'d':13.062,
    'e':12.633,'f':8.594,'g':13.406,'h':13.062,'i':6.359,'j':7.305,
    'k':12.375,'l':6.188,'m':20.367,'n':13.32,'o':13.062,'p':12.633,
    'q':12.633,'r':10.227,'s':12.461,'t':8.766,'u':13.406,'v':12.375,
    'w':17.359,'x':12.289,'y':12.375,'z':11.258,'0':13.922,'1':13.922,
    '2':13.922,'3':13.922,'4':13.922,'5':13.922,'6':13.922,'7':13.922,
    '8':13.922,'9':13.922,'!':7.82,' ':6.961,
}
_DEFAULT_WIDTH = 14.0

def _char_w(c: str) -> float:
    return _CHAR_WIDTHS.get(c, _DEFAULT_WIDTH)

def _text_total_width(text: str) -> float:
    return sum(_char_w(c) for c in text)

_RAINBOW = [
    (1.0,0.0,0.0),(1.0,0.5,0.0),(1.0,1.0,0.0),
    (0.0,1.0,0.0),(0.0,0.5,1.0),(0.5,0.0,1.0),(1.0,0.0,0.5),
]

def _lerp(c1, c2, t):
    return (c1[0]+(c2[0]-c1[0])*t, c1[1]+(c2[1]-c1[1])*t, c1[2]+(c2[2]-c1[2])*t)

def _make_gradient(text, stops):
    visible = [c for c in text if c != ' ']
    n = len(visible)
    if n == 0: return [(1.0,1.0,1.0)]*len(text)
    if len(stops) == 1: return [tuple(stops[0])]*len(text)
    vis = []
    for i in range(n):
        t = i/max(n-1,1)
        sc = len(stops)-1
        seg = min(int(t*sc), sc-1)
        vis.append(_lerp(stops[seg], stops[seg+1], t*sc-seg))
    res, vi = [], 0
    for c in text:
        if c == ' ': res.append((1.0,1.0,1.0))
        else: res.append(vis[vi]); vi += 1
    return res

def _colors_frame(text, stops, anim, frame, total):
    t = frame/total
    if anim == 'static':
        return _make_gradient(text, stops)
    elif anim == 'wave_bright':
        base = _make_gradient(text, stops)
        n = max(len(text)-1, 1)
        return [tuple(min(1.0, ch*(0.55+0.45*math.sin((i/n*2 - t)*math.pi*2))) for ch in base[i]) for i in range(len(text))]
    elif anim == 'wave':
        base = _make_gradient(text, stops)
        n = max(len(text)-1, 1)
        return [tuple(ch*(0.4+0.6*math.sin((i/n*2 - t)*math.pi*2)) for ch in base[i]) for i in range(len(text))]
    elif anim == 'pulse':
        base = _make_gradient(text, stops)
        b = 0.45+0.55*math.sin(t*math.pi*2)
        return [tuple(min(1.0,ch*b) for ch in c) for c in base]
    elif anim == 'rainbow':
        n = len(_RAINBOW)
        out = []
        for i in range(len(text)):
            off = (i/max(len(text)-1,1)+t)%1.0
            idx = off*n; lo = int(idx)%n; hi=(lo+1)%n
            out.append(_lerp(_RAINBOW[lo], _RAINBOW[hi], idx-int(idx)))
        return out
    elif anim == 'color_travel':
        out = []
        for i in range(len(text)):
            pos = ((i/max(len(text)-1,1))+t)%1.0
            sc = len(stops)-1; seg = min(int(pos*sc),sc-1)
            out.append(_lerp(stops[seg], stops[(seg+1)%len(stops)], pos*sc-seg))
        return out
    return _make_gradient(text, stops)

def _to_rgb(c):
    return (max(0,min(255,int(c[0]*255))), max(0,min(255,int(c[1]*255))), max(0,min(255,int(c[2]*255))))

def _render_frame(text, colors, anim, enter, font, small, W, H):
    img  = Image.new('RGBA', (W, H), (18, 18, 28, 255))
    draw = ImageDraw.Draw(img)
    total_w = _text_total_width(text)
    scale = (W * 0.68) / max(total_w, 1.0)
    try:
        sample_bbox = font.getbbox('A')
        char_h = sample_bbox[3] - sample_bbox[1]
    except:
        char_h = 40
    ty = (H - char_h) // 2 - 8
    cx = (W - total_w * scale) / 2.0
    sx = cx
    for i, char in enumerate(text):
        cw = _char_w(char) * scale
        try:
            cb = font.getbbox(char)
            glyph_w = cb[2] - cb[0]
            glyph_off = cb[0]
        except:
            glyph_w = int(cw)
            glyph_off = 0
        x_draw = sx + (cw - glyph_w) / 2 - glyph_off
        draw.text((x_draw + 2, ty + 2), char, font=font, fill=(0, 0, 0, 180))
        sx += cw
    cx2 = (W - total_w * scale) / 2.0
    for i, char in enumerate(text):
        cw = _char_w(char) * scale
        try:
            cb = font.getbbox(char)
            glyph_w = cb[2] - cb[0]
            glyph_off = cb[0]
        except:
            glyph_w = int(cw)
            glyph_off = 0
        x_draw = cx2 + (cw - glyph_w) / 2 - glyph_off
        color = colors[i] if i < len(colors) else (1.0, 1.0, 1.0)
        draw.text((x_draw, ty), char, font=font, fill=_to_rgb(color))
        cx2 += cw
    draw.text((10, H - 22), f'anim: {anim}  |  enter: {enter}', font=small, fill=(140, 140, 160))
    return img.convert('RGB')

def _render_preview(text, stops, anim, enter):
    W, H = 520, 120
    try:
        font  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44)
        small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    except:
        font = small = ImageFont.load_default()
    if anim == 'static':
        img = _render_frame(text, _colors_frame(text, stops, anim, 0, 1), anim, enter, font, small, W, H)
        buf = io.BytesIO(); img.save(buf, 'PNG'); buf.seek(0)
        return buf, 'png'
    ANIM_CFG = {
        'wave_bright':  (64, 45),
        'wave':         (64, 45),
        'rainbow':      (64, 35),
        'color_travel': (64, 45),
        'pulse':        (64, 55),
    }
    FRAMES, DELAY = ANIM_CFG.get(anim, (64, 45))
    frames = [_render_frame(text, _colors_frame(text, stops, anim, f, FRAMES), anim, enter, font, small, W, H) for f in range(FRAMES)]
    buf = io.BytesIO()
    frames[0].save(buf, 'GIF', save_all=True, append_images=frames[1:], loop=0, duration=DELAY, optimize=False)
    buf.seek(0)
    return buf, 'gif'

class TagSession:
    def __init__(self, acc):
        self.acc         = acc
        self.text        = 'NEXUS'
        self.color_key   = 'Blanco'
        self.color_stops = [(1.0,1.0,1.0)]
        self.anim        = 'wave_bright'
        self.enter       = 'wave_in'
        self.wave_speed  = 0.8

    def to_cfg(self):
        return {
            'text':        self.text,
            'color_stops': [list(c) for c in self.color_stops],
            'anim':        self.anim,
            'enter':       self.enter,
            'wave_speed':  self.wave_speed,
        }

    def preview(self):
        return _render_preview(self.text, self.color_stops, self.anim, self.enter)

_sessions: dict = {}

def _has_perm(user) -> bool:
    return any(r.id == ALLOWED_ROLE for r in user.roles)

async def _update_preview(interaction, session, followup=False):
    buf, ext = await asyncio.get_event_loop().run_in_executor(None, session.preview)
    fname = f'preview.{ext}'
    file  = discord.File(buf, filename=fname)
    embed = discord.Embed(title='\U0001f3a8 Editor de Tag', color=0x1a1d2e)
    embed.add_field(name='Texto',  value=f'`{session.text}`',   inline=True)
    embed.add_field(name='Color',  value=session.color_key,      inline=True)
    embed.add_field(name='Anim',   value=session.anim,           inline=True)
    embed.add_field(name='Enter',  value=session.enter,          inline=True)
    embed.add_field(name='Cuenta', value=f'`{session.acc}`',     inline=True)
    if session.color_stops:
        embed.add_field(
            name=f'Gradiente ({len(session.color_stops)} color{"es" if len(session.color_stops)>1 else ""})',
            value=_color_swatch(session.color_stops),
            inline=False
        )
    embed.set_image(url=f'attachment://{fname}')
    if followup:
        await interaction.followup.send(embed=embed, file=file, view=TagButtons(), ephemeral=True)
    else:
        await interaction.response.edit_message(embed=embed, attachments=[file], view=TagButtons())

class ColorSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=n, value=n) for n in COLORS_PRESET]
        super().__init__(placeholder='Preset de color/gradiente...', options=options, row=0)
    async def callback(self, interaction):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        s.color_key   = self.values[0]
        s.color_stops = list(COLORS_PRESET[self.values[0]])
        await _update_preview(interaction, s)

class AnimSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=a, value=a) for a in ANIMS]
        super().__init__(placeholder='Animacion...', options=options, row=1)
    async def callback(self, interaction):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        s.anim = self.values[0]
        await _update_preview(interaction, s)

class EnterSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=e, value=e) for e in ENTERS]
        super().__init__(placeholder='Entrada...', options=options, row=2)
    async def callback(self, interaction):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        s.enter = self.values[0]
        await _update_preview(interaction, s)

_QUICK_COLORS = [
    ('\U0001f534 Rojo',     (1.0, 0.0, 0.0)),
    ('\U0001f7e0 Naranja',  (1.0, 0.5, 0.0)),
    ('\U0001f7e1 Amarillo', (1.0, 0.9, 0.0)),
    ('\U0001f7e2 Verde',    (0.0, 1.0, 0.3)),
    ('\U0001f535 Azul',     (0.2, 0.5, 1.0)),
    ('\U0001f7e3 Morado',   (0.7, 0.0, 1.0)),
    ('\U0001fa77 Rosa',     (1.0, 0.3, 0.7)),
    ('\U0001fa75 Cian',     (0.0, 1.0, 1.0)),
    ('\u26aa Blanco',   (1.0, 1.0, 1.0)),
    ('\U0001f7e4 Marron',   (0.6, 0.3, 0.1)),
    ('\U0001f7e0 Oro',      (1.0, 0.84, 0.0)),
    ('\u270f\ufe0f Personalizado (HEX/RGB)', None),
]

class ColorPickerSelect(discord.ui.Select):
    def __init__(self, session):
        self.session = session
        options = [discord.SelectOption(label=name, value=str(i)) for i, (name, _) in enumerate(_QUICK_COLORS)]
        super().__init__(placeholder='Elige un color...', options=options)

    async def callback(self, interaction):
        idx = int(self.values[0])
        name, color = _QUICK_COLORS[idx]
        if color is None:
            await interaction.response.send_modal(ColorModal(self.session))
            return
        s = self.session
        if s.color_stops == [(1.0,1.0,1.0)] and s.color_key == 'Blanco':
            s.color_stops = []
        s.color_stops.append(color)
        s.color_key = 'Personalizado'
        await interaction.response.edit_message(content='\u2705 Color agregado.', embed=None, attachments=[], view=None)
        await _update_preview(interaction, s, followup=True)

class ColorPickerView(discord.ui.View):
    def __init__(self, session):
        super().__init__(timeout=60)
        self.add_item(ColorPickerSelect(session))

_BS_ICONS = [
    ('\ue043', 'Corona'),
    ('\ue046', 'Calavera'),
    ('\ue047', 'Corazon'),
    ('\ue044', 'Yin Yang'),
    ('\ue045', 'Ojo'),
    ('\ue048', 'Dragon'),
    ('\ue049', 'Casco'),
    ('\ue04a', 'Hongo'),
    ('\ue04b', 'Estrella Ninja'),
    ('\ue04c', 'Casco Vikingo'),
    ('\ue04d', 'Luna'),
    ('\ue04e', 'Arana'),
    ('\ue04f', 'Fireball'),
    ('\ue041', 'Sombrero Fedora'),
    ('\ue042', 'HAL'),
    ('\ue02a', 'Trofeo Oro'),
    ('\ue02b', 'Trofeo Plata'),
    ('\ue02c', 'Trofeo Bronce'),
    ('\ue02d', 'Medalla 1'),
    ('\ue02e', 'Medalla 2'),
    ('\ue02f', 'Trofeo Copa'),
    ('\ue01d', 'Token'),
    ('\ue01e', 'Logo BS'),
    ('\ue01f', 'Ticket'),
    ('\ue029', 'Ticket 2'),
    ('\ue027', 'Fiesta'),
    ('\ue031', 'Bomba Explodinary'),
    ('\ue062', 'Bomba Santa'),
    ('\ue064', 'Gorro Navidad'),
    ('\ue065', 'Papa'),
    ('\ue066', 'Palmera'),
    ('\ue067', 'Guante Boxeo'),
    ('\ue063', 'V2'),
    ('\ue026', 'Discord'),
    ('\ue05b', 'Steam'),
    ('\ue05a', 'Oculus'),
    ('\ue05c', 'Nvidia'),
    ('\ue020', 'Google Play'),
    ('\ue021', 'Game Center'),
    ('\ue030', 'Cuenta Local'),
    ('\ue028', 'Cuenta Test'),
    ('\ue019', 'OUYA O'),
    ('\ue01a', 'OUYA U'),
    ('\ue01b', 'OUYA Y'),
    ('\ue01c', 'OUYA A'),
    ('\ue022', 'Dado 1'),
    ('\ue023', 'Dado 2'),
    ('\ue024', 'Dado 3'),
    ('\ue025', 'Dado 4'),
    ('\ue032', 'USA'),
    ('\ue033', 'Mexico'),
    ('\ue035', 'Brasil'),
    ('\ue039', 'Canada'),
    ('\ue05f', 'Argentina'),
    ('\ue060', 'Filipinas'),
    ('\ue061', 'Chile'),
    ('\ue034', 'Alemania'),
    ('\ue038', 'UK'),
    ('\ue03c', 'Francia'),
    ('\ue03e', 'Italia'),
    ('\ue040', 'Holanda'),
    ('\ue057', 'Rep. Checa'),
    ('\ue05e', 'Polonia'),
    ('\ue036', 'Rusia'),
    ('\ue037', 'China'),
    ('\ue03a', 'India'),
    ('\ue03b', 'Japon'),
    ('\ue03d', 'Indonesia'),
    ('\ue03f', 'Corea del Sur'),
    ('\ue056', 'Malasia'),
    ('\ue058', 'Australia'),
    ('\ue059', 'Singapur'),
    ('\ue05d', 'Iran'),
    ('\ue050', 'Emiratos'),
    ('\ue051', 'Qatar'),
    ('\ue052', 'Egipto'),
    ('\ue053', 'Kuwait'),
    ('\ue054', 'Argelia'),
    ('\ue055', 'Arabia Saudita'),
]

_ICONS_PER_PAGE = 20
_ICON_PAGES = [_BS_ICONS[i:i+_ICONS_PER_PAGE] for i in range(0, len(_BS_ICONS), _ICONS_PER_PAGE)]

def _build_icon_grid_image(page: int) -> io.BytesIO:
    icons = _ICON_PAGES[page]
    COLS   = 5
    ROWS   = math.ceil(len(icons) / COLS)
    CELL   = 90
    PAD    = 6
    LABEL_H = 14
    W = COLS * (CELL + PAD) + PAD
    H = ROWS * (CELL + LABEL_H + PAD) + PAD
    canvas = Image.new('RGB', (W, H), (25, 25, 35))
    draw   = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    except Exception:
        font = ImageFont.load_default()
    import os
    base      = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base, 'bs_icons')
    for i, (uni, name) in enumerate(icons):
        col = i % COLS
        row = i // COLS
        x = PAD + col * (CELL + PAD)
        y = PAD + row * (CELL + LABEL_H + PAD)
        code      = f'{ord(uni):04x}'
        icon_path = os.path.join(icons_dir, f'{code}.png')
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).convert('RGB').resize((CELL, CELL))
            canvas.paste(icon, (x, y))
        else:
            draw.rectangle([x, y, x + CELL, y + CELL], fill=(50, 50, 60))
        draw.text((x, y + CELL + 1), name, font=font, fill=(180, 180, 200))
    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

class IconSelect(discord.ui.Select):
    def __init__(self, session, page: int, position: str):
        self.session  = session
        self.page     = page
        self.position = position
        icons   = _ICON_PAGES[page]
        options = [
            discord.SelectOption(label=name, value=uni, description=f'\\u{ord(uni):04x}')
            for uni, name in icons
        ]
        super().__init__(placeholder=f'Elige un icono (pag {page+1}/{len(_ICON_PAGES)})...', options=options)

    async def callback(self, interaction):
        uni = self.values[0]
        s   = self.session
        if self.position == 'inicio':
            s.text = uni + s.text
        elif self.position == 'final':
            s.text = s.text + uni
        else:
            s.text = uni + s.text + uni
        await interaction.response.edit_message(content='\u2705 Icono agregado.', embed=None, attachments=[], view=None)
        await _update_preview(interaction, s, followup=True)

class IconPageView(discord.ui.View):
    def __init__(self, session, page: int, position: str):
        super().__init__(timeout=120)
        self.session  = session
        self.page     = page
        self.position = position
        self.add_item(IconSelect(session, page, position))

    @discord.ui.button(label='\u25c0 Anterior', style=discord.ButtonStyle.secondary, row=1)
    async def prev_page(self, interaction, button):
        await self._switch(interaction, (self.page - 1) % len(_ICON_PAGES))

    @discord.ui.button(label='\u25b6 Siguiente', style=discord.ButtonStyle.secondary, row=1)
    async def next_page(self, interaction, button):
        await self._switch(interaction, (self.page + 1) % len(_ICON_PAGES))

    async def _switch(self, interaction, new_page: int):
        buf   = await asyncio.get_event_loop().run_in_executor(None, _build_icon_grid_image, new_page)
        file  = discord.File(buf, filename='iconos.png')
        view  = IconPageView(self.session, new_page, self.position)
        embed = discord.Embed(title=f'\U0001f3ae Iconos BS \u2014 Pagina {new_page+1}/{len(_ICON_PAGES)}', color=0x1a1d2e)
        embed.set_image(url='attachment://iconos.png')
        await interaction.response.edit_message(embed=embed, attachments=[file], view=view)

class IconPositionView(discord.ui.View):
    def __init__(self, session):
        super().__init__(timeout=60)
        self.session = session

    @discord.ui.button(label='\u2b05\ufe0f Inicio', style=discord.ButtonStyle.primary)
    async def pos_inicio(self, interaction, button):
        await self._open(interaction, 'inicio')

    @discord.ui.button(label='\u27a1\ufe0f Final', style=discord.ButtonStyle.primary)
    async def pos_final(self, interaction, button):
        await self._open(interaction, 'final')

    @discord.ui.button(label='\u2194\ufe0f Ambos', style=discord.ButtonStyle.secondary)
    async def pos_ambos(self, interaction, button):
        await self._open(interaction, 'ambos')

    async def _open(self, interaction, position: str):
        buf   = await asyncio.get_event_loop().run_in_executor(None, _build_icon_grid_image, 0)
        file  = discord.File(buf, filename='iconos.png')
        view  = IconPageView(self.session, 0, position)
        embed = discord.Embed(title=f'\U0001f3ae Iconos BS \u2014 Pagina 1/{len(_ICON_PAGES)}', color=0x1a1d2e)
        embed.set_image(url='attachment://iconos.png')
        await interaction.response.edit_message(embed=embed, attachments=[file], view=view)

class SaveDefModal(discord.ui.Modal, title='Guardar como definicion'):
    def_name = discord.ui.TextInput(label='Nombre', placeholder='ej: altpha_season', max_length=30)
    def __init__(self, session):
        super().__init__()
        self.session = session
    async def on_submit(self, interaction):
        name = self.def_name.value.strip().lower().replace(' ', '_')
        if not name:
            await interaction.response.send_message('\u274c Nombre invalido.', ephemeral=True)
            return
        data = _load_perms()
        data.setdefault('tag_defs', {})[name] = self.session.to_cfg()
        _save_perms(data)
        await interaction.response.send_message(f'\u2705 Tag def `{name}` guardada.', ephemeral=True)

class TagButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ColorSelect())
        self.add_item(AnimSelect())
        self.add_item(EnterSelect())

    @discord.ui.button(label='\u270f\ufe0f Texto', style=discord.ButtonStyle.secondary, row=3)
    async def change_text(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        await interaction.response.send_modal(TextModal(s))

    @discord.ui.button(label='\U0001f3a8 Agregar color', style=discord.ButtonStyle.primary, row=3)
    async def add_color(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        await interaction.response.send_message(
            'Elige un color basico o escribe uno personalizado:',
            view=ColorPickerView(s),
            ephemeral=True
        )

    @discord.ui.button(label='\U0001f3ae Icono BS', style=discord.ButtonStyle.primary, row=3)
    async def add_icon(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        await interaction.response.send_message(
            '\u00bfDonde quieres el icono?',
            view=IconPositionView(s),
            ephemeral=True
        )

    @discord.ui.button(label='\u2705 Guardar', style=discord.ButtonStyle.success, row=4)
    async def save(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        save_tag(s.acc, s.to_cfg())
        _sessions.pop(interaction.user.id, None)
        await interaction.response.edit_message(
            content=f'\u2705 Tag guardado para `{s.acc}`.',
            attachments=[], view=None, embed=None
        )
        buf, ext = await asyncio.get_event_loop().run_in_executor(None, s.preview)
        fname = f'preview.{ext}'
        file  = discord.File(buf, filename=fname)
        embed = discord.Embed(title=f'\U0001f3a8 Tag actualizado', color=0x1a1d2e)
        embed.add_field(name='Cuenta', value=f'`{s.acc}`', inline=True)
        embed.add_field(name='Texto',  value=f'`{s.text}`', inline=True)
        embed.add_field(name='Anim',   value=s.anim, inline=True)
        embed.set_image(url=f'attachment://{fname}')
        embed.set_footer(text=f'Editado por {interaction.user.display_name}')
        await interaction.channel.send(embed=embed, file=file)

    @discord.ui.button(label='\U0001f5d1\ufe0f Eliminar tag', style=discord.ButtonStyle.danger, row=4)
    async def delete_tag(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        remove_tag(s.acc)
        _sessions.pop(interaction.user.id, None)
        await interaction.response.edit_message(
            content=f'\U0001f5d1\ufe0f Tag eliminado para `{s.acc}`.',
            attachments=[], view=None, embed=None
        )

    @discord.ui.button(label='\U0001f5d1\ufe0f Limpiar colores', style=discord.ButtonStyle.secondary, row=4)
    async def clear_colors(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        s.color_stops = [(1.0,1.0,1.0)]
        s.color_key   = 'Blanco'
        await _update_preview(interaction, s)

    @discord.ui.button(label='\u274c Cancelar', style=discord.ButtonStyle.secondary, row=4)
    async def cancel(self, interaction, button):
        _sessions.pop(interaction.user.id, None)
        await interaction.response.edit_message(content='Cancelado.', attachments=[], view=None, embed=None)

    @discord.ui.button(label='\U0001f4be Guardar como def', style=discord.ButtonStyle.secondary, row=4)
    async def save_as_def(self, interaction, button):
        s = _sessions.get(interaction.user.id)
        if not s:
            await interaction.response.send_message('Sesion expirada.', ephemeral=True); return
        await interaction.response.send_modal(SaveDefModal(s))

    async def on_timeout(self):
        pass

class TextModal(discord.ui.Modal, title='Cambiar texto del tag'):
    text = discord.ui.TextInput(label='Texto', placeholder='Max 20 caracteres', max_length=20)
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.text.default = session.text
    async def on_submit(self, interaction):
        self.session.text = self.text.value
        await _update_preview(interaction, self.session)

class ColorModal(discord.ui.Modal, title='Agregar color al gradiente'):
    color_input = discord.ui.TextInput(
        label='Color (Hex o RGB)',
        placeholder='Ej: #FF5500  o  255, 85, 0  o  1.0, 0.33, 0.0',
        max_length=30,
    )
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def on_submit(self, interaction):
        color = _parse_color_input(self.color_input.value)
        if color is None:
            await interaction.response.send_message(
                '\u274c Color invalido. Usa `#RRGGBB`, `R, G, B` (0-255) o `R, G, B` (0.0-1.0)',
                ephemeral=True
            )
            return
        if self.session.color_stops == [(1.0,1.0,1.0)] and self.session.color_key == 'Blanco':
            self.session.color_stops = []
        self.session.color_stops.append(color)
        self.session.color_key = 'Personalizado'
        await _update_preview(interaction, self.session)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot  = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

@tree.command(name='tag', description='Crear o editar el tag de un jugador')
@app_commands.describe(acc='Account ID del jugador (ej: unown_id:xxxxx)')
async def tag_cmd(interaction, acc: str):
    if not _has_perm(interaction.user):
        await interaction.response.send_message('No tienes permiso.', ephemeral=True)
        return
    try:
        await interaction.response.defer(ephemeral=True)
    except Exception:
        return
    s = TagSession(acc)
    existing = get_tag(acc)
    if existing:
        s.text        = existing.get('text', 'NEXUS')
        s.color_stops = [tuple(c) for c in existing.get('color_stops', [(1.0,1.0,1.0)])]
        s.anim        = existing.get('anim', 'wave_bright')
        s.enter       = existing.get('enter', 'wave_in')
        s.wave_speed  = existing.get('wave_speed', 1.0)
        s.color_key   = 'Personalizado'
        for k, v in COLORS_PRESET.items():
            if [list(c) for c in s.color_stops] == [list(c) for c in v]:
                s.color_key = k; break
    _sessions[interaction.user.id] = s
    buf, ext = await asyncio.get_event_loop().run_in_executor(None, s.preview)
    fname = f'preview.{ext}'
    file  = discord.File(buf, filename=fname)
    embed = discord.Embed(title='\U0001f3a8 Editor de Tag', color=0x1a1d2e)
    embed.add_field(name='Texto',  value=f'`{s.text}`',  inline=True)
    embed.add_field(name='Color',  value=s.color_key,     inline=True)
    embed.add_field(name='Anim',   value=s.anim,          inline=True)
    embed.add_field(name='Enter',  value=s.enter,         inline=True)
    embed.add_field(name='Cuenta', value=f'`{acc}`',      inline=True)
    if s.color_stops:
        embed.add_field(
            name=f'Gradiente ({len(s.color_stops)} color{"es" if len(s.color_stops)>1 else ""})',
            value=_color_swatch(s.color_stops),
            inline=False
        )
    embed.set_image(url=f'attachment://{fname}')
    embed.set_footer(text='La sesion expira en 5 minutos sin actividad.')
    await interaction.followup.send(embed=embed, file=file, view=TagButtons(), ephemeral=True)

@tree.command(name='tagcreator', description='Crear una definicion de tag reutilizable')
async def tagcreator_cmd(interaction):
    if not _has_perm(interaction.user):
        await interaction.response.send_message('No tienes permiso.', ephemeral=True)
        return
    try:
        await interaction.response.defer(ephemeral=True)
    except Exception:
        return
    s = TagSession('__def__')
    _sessions[interaction.user.id] = s
    buf, ext = await asyncio.get_event_loop().run_in_executor(None, s.preview)
    fname = f'preview.{ext}'
    file  = discord.File(buf, filename=fname)
    embed = discord.Embed(title='\U0001f3a8 Crear Tag Def', color=0x1a1d2e)
    embed.add_field(name='Texto',  value=f'`{s.text}`',  inline=True)
    embed.add_field(name='Color',  value=s.color_key,     inline=True)
    embed.add_field(name='Anim',   value=s.anim,          inline=True)
    embed.add_field(name='Enter',  value=s.enter,         inline=True)
    embed.set_image(url=f'attachment://{fname}')
    embed.set_footer(text='Usa "Guardar como def" para nombrarla y guardarla.')
    await interaction.followup.send(embed=embed, file=file, view=TagButtons(), ephemeral=True)

def _render_dc_card(author_name: str, content: str) -> io.BytesIO:
    W, H     = 520, 95
    PAD      = 10
    AVATAR_S = 60
    canvas   = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw     = ImageDraw.Draw(canvas)
    bg       = Image.new('RGBA', (W, H), (20, 25, 40, 230))
    canvas.alpha_composite(bg)
    code      = f'{ord(chr(0xe026)):04x}'
    icon_path = os.path.join(ICONS_DIR, f'{code}.png')
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert('RGBA').resize((AVATAR_S, AVATAR_S))
        canvas.alpha_composite(icon, (PAD, (H - AVATAR_S) // 2))
    try:
        font_name = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
        font_msg  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
        font_pb   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
    except Exception:
        font_name = ImageFont.load_default()
        font_msg  = font_name
        font_pb   = font_name
    text_x = PAD + AVATAR_S + PAD
    name_color = (88, 101, 242, 255)
    draw.text((text_x, 14), author_name, font=font_name, fill=name_color)
    draw.text((text_x, 36), content, font=font_msg, fill=(210, 210, 220, 255))
    draw.text((text_x, H - 13), 'Discord \u2192 NexusServer', font=font_pb, fill=(90, 90, 110, 200))
    draw.rectangle([0, 0, 3, H], fill=(88, 101, 242, 200))
    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != LIVE_CHAT_CHANNEL:
        return
    content = message.content.strip()
    if not content:
        return
    try:
        with open(DC_TO_BS, 'a', encoding='utf-8') as f:
            f.write(f'DC | {message.author.display_name}: {content}\n')
    except Exception as e:
        print(f'[chat] dc_to_bs write error: {e}')
    try:
        buf  = await asyncio.get_event_loop().run_in_executor(
            None, _render_dc_card, message.author.display_name, content
        )
        async with _aiohttp_mod.ClientSession() as session:
            form = _aiohttp_mod.FormData()
            form.add_field('file', buf, filename='dc_chat.png', content_type='image/png')
            await session.post(CHAT_WEBHOOK, data=form)
    except Exception as e:
        print(f'[chat] dc card error: {e}')

LIVE_PLAYERS_CHANNEL = _CFG['channels']['live_players']
LADDER_CHANNEL       = _CFG['channels']['ladder']
ROSTER_JSON          = os.path.join(_DATA_BASE, 'roster.json')
STATS_JSON           = os.path.join(_DATA_BASE, 'stats.json')
SEASON_JSON          = os.path.join(_DATA_BASE, 'season.json')
CONFIG_TOML          = os.path.normpath(os.path.join(_BASE, '..', '..', 'config.toml'))

def _read_max_players() -> int:
    try:
        with open(CONFIG_TOML, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('max_players'):
                    return int(line.split('=')[1].strip())
    except Exception:
        pass
    return 8

def _get_player_rank(aid: str) -> str:
    try:
        import json as _json
        stats_path = STATS_JSON
        if not os.path.exists(stats_path):
            return '---'
        with open(stats_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        stats = data.get('stats', {})
        entries = sorted(stats.values(), key=lambda x: x.get('ns', 0), reverse=True)
        for i, e in enumerate(entries):
            if e.get('aid') == aid:
                return f'#{i+1}'
        return '---'
    except Exception:
        return '---'

def _render_live_players(players: list, max_players: int) -> io.BytesIO:
    COLS   = 4
    CELL_W = 140
    CELL_H = 165
    HEADER = 48
    PAD    = 8
    AVATAR = 72

    rows = max(1, (max_players + COLS - 1) // COLS)
    W    = COLS * CELL_W + PAD * 2
    H    = HEADER + rows * CELL_H + PAD

    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw   = ImageDraw.Draw(canvas)
    bg     = Image.new('RGBA', (W, H), (18, 18, 28, 240))
    canvas.alpha_composite(bg)

    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
        font_name  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
        font_sub   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
        font_rank  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_name = font_sub = font_rank = font_title

    draw.rectangle([0, 0, W, HEADER], fill=(25, 25, 45, 255))
    draw.rectangle([0, HEADER - 2, W, HEADER], fill=(70, 70, 200, 220))
    title = f'JUGADORES EN LINEA  {len(players)}/{max_players}'
    draw.text((PAD, 14), title, font=font_title, fill=(210, 210, 255, 255))

    for slot in range(max_players):
        col = slot % COLS
        row = slot // COLS
        cx  = PAD + col * CELL_W
        cy  = HEADER + row * CELL_H

        cell_bg = (22, 22, 36, 230) if (col + row) % 2 == 0 else (28, 28, 44, 230)
        draw.rectangle([cx, cy, cx + CELL_W - 2, cy + CELL_H - 2], fill=cell_bg)

        if slot < len(players):
            p         = players[slot]
            char      = p.get('character', 'neoSpaz')
            color     = p.get('color',    [1.0, 1.0, 1.0])
            highlight = p.get('highlight',[1.0, 1.0, 1.0])
            name      = p.get('name', '???')[:14]
            ping      = p.get('ping', -1)
            aid       = p.get('aid', '')
            tag_icon  = p.get('tag_icon', '')

            r = int(max(0, min(1, color[0])) * 255)
            g = int(max(0, min(1, color[1])) * 255)
            b = int(max(0, min(1, color[2])) * 255)

            draw.rectangle([cx, cy + 4, cx + CELL_W - 2, cy + 7], fill=(r, g, b, 220))

            char_png = os.path.join(CHARS_DIR, f'{char}.png')
            if not os.path.exists(char_png):
                char_png = os.path.join(CHARS_DIR, 'neoSpaz.png')
            av_x = cx + (CELL_W - AVATAR) // 2
            av_y = cy + 8
            if os.path.exists(char_png):
                avatar = Image.open(char_png).convert('RGBA').resize((AVATAR, AVATAR))
                try:
                    avatar = _tint_image(avatar, color, highlight, char=char)
                except Exception:
                    pass
                canvas.alpha_composite(avatar, (av_x, av_y))

            if tag_icon:
                code      = f'{ord(tag_icon):04x}'
                icon_path = os.path.join(ICONS_DIR, f'{code}.png')
                if os.path.exists(icon_path):
                    icon_img = Image.open(icon_path).convert('RGBA').resize((16, 16))
                    canvas.alpha_composite(icon_img, (cx + 4, cy + 6))

            text_y = av_y + AVATAR + 4

            draw.text((cx + CELL_W // 2, text_y), name, font=font_name,
                      fill=(r, g, b, 255), anchor='mt')

            rank = _get_player_rank(aid)
            draw.text((cx + CELL_W // 2, text_y + 14), rank, font=font_rank,
                      fill=(255, 215, 0, 220), anchor='mt')

            if ping >= 0:
                ping_color = (80, 220, 80, 255) if ping < 80 else (220, 200, 80, 255) if ping < 150 else (220, 80, 80, 255)
                ping_dot   = '\u25cf'
                draw.text((cx + CELL_W // 2, text_y + 27), f'{ping_dot} {int(ping)}ms', font=font_sub,
                          fill=ping_color, anchor='mt')
            else:
                draw.text((cx + CELL_W // 2, text_y + 27), 'N/A', font=font_sub,
                          fill=(120, 120, 140, 200), anchor='mt')

            pb_short = aid[:16] + '..' if len(aid) > 16 else aid
            draw.text((cx + CELL_W // 2, text_y + 40), pb_short, font=font_sub,
                      fill=(70, 70, 100, 180), anchor='mt')

        else:
            draw.rectangle([cx + 10, cy + 20, cx + CELL_W - 12, cy + CELL_H - 20],
                           fill=(30, 30, 45, 180), outline=(40, 40, 60, 150))
            draw.text((cx + CELL_W // 2, cy + CELL_H // 2), '---', font=font_sub,
                      fill=(60, 60, 80, 180), anchor='mm')

    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

_live_players_msg_id = None

async def _live_players_watcher() -> None:
    global _live_players_msg_id
    import asyncio
    await asyncio.sleep(5)

    channel = bot.get_channel(LIVE_PLAYERS_CHANNEL)
    if not channel:
        print('[live_players] canal no encontrado')
        return

    max_players = _read_max_players()

    async for msg in channel.history(limit=20):
        if msg.author.id == bot.user.id:
            _live_players_msg_id = msg.id
            break

    while True:
        try:
            players = []
            if os.path.exists(ROSTER_JSON):
                with open(ROSTER_JSON, 'r', encoding='utf-8') as f:
                    players = json.load(f).get('players', [])

            if not players:
                for _ in range(30):
                    await asyncio.sleep(1)
                    flag = ROSTER_JSON + '.flag'
                    if os.path.exists(flag):
                        try:
                            os.remove(flag)
                        except Exception:
                            pass
                        break
                continue
            buf = await asyncio.get_event_loop().run_in_executor(
                None, _render_live_players, players, max_players
            )
            file = discord.File(buf, filename='live_players.png')
            embed = discord.Embed(color=0x1a1d3e)
            embed.set_image(url='attachment://live_players.png')
            embed.set_footer(text='Actualizado cada 30s')

            if _live_players_msg_id:
                try:
                    msg = await channel.fetch_message(_live_players_msg_id)
                    await msg.edit(embed=embed, attachments=[file])
                except Exception:
                    _live_players_msg_id = None

            if not _live_players_msg_id:
                buf2 = await asyncio.get_event_loop().run_in_executor(
                    None, _render_live_players, players, max_players
                )
                file2 = discord.File(buf2, filename='live_players.png')
                embed2 = discord.Embed(color=0x1a1d3e)
                embed2.set_image(url='attachment://live_players.png')
                embed2.set_footer(text='Actualizado cada 30s')
                msg = await channel.send(embed=embed2, file=file2)
                _live_players_msg_id = msg.id

        except Exception as e:
            print(f'[live_players] error: {e}')

        for _ in range(30):
            await asyncio.sleep(1)
            flag = ROSTER_JSON + '.flag'
            if os.path.exists(flag):
                try:
                    os.remove(flag)
                except Exception:
                    pass
                break
                break
            await asyncio.sleep(1)

_report_seen_ts: set = set()
_report_lock2 = _threading.Lock()

def _init_report_seen() -> None:
    if not os.path.exists(REPORTS_JSON):
        return
    try:
        with open(REPORTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with _report_lock2:
            for r in data:
                ts = r.get('ts_unix')
                if ts:
                    _report_seen_ts.add(ts)
        print(f'[reports] {len(_report_seen_ts)} reportes existentes marcados como vistos')
    except Exception as e:
        print(f'[reports] _init_report_seen error: {e}')

def _render_reporter_card(report: dict) -> io.BytesIO:
    entry = {
        'character': report.get('reporter_character', 'neoSpaz'),
        'color':     report.get('reporter_color',     [1.0, 1.0, 1.0]),
        'highlight': report.get('reporter_highlight', [1.0, 1.0, 1.0]),
        'name':      report.get('reporter_name', '?'),
        'message':   f"Reporto a {report.get('target_name', '?')} \u2014 {report.get('reason', '')}",
        'account_id': report.get('reporter_aid', ''),
        'tag_text':  '',
        'tag_icon':  '',
        'tag_color': report.get('reporter_color', [1.0, 1.0, 1.0]),
    }
    return _render_chat_card(entry)

async def _report_watcher(session: '_aiohttp_mod.ClientSession') -> None:
    import asyncio
    import time as _time
    _init_report_seen()
    while True:
        for _ in range(30):
            await asyncio.sleep(1)
            flag = ROSTER_JSON + '.flag'
            if os.path.exists(flag):
                try:
                    os.remove(flag)
                except Exception:
                    pass
                break
                break
            await asyncio.sleep(1)
        if not os.path.exists(REPORTS_JSON):
            continue
        try:
            with open(REPORTS_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
            now = _time.time()
            new_reports = []
            with _report_lock2:
                for r in data:
                    ts = r.get('ts_unix')
                    if ts and ts not in _report_seen_ts:
                        if (now - ts) > 60:
                            _report_seen_ts.add(ts)
                            continue
                        new_reports.append(r)

            for r in new_reports:
                ts = r.get('ts_unix')
                try:
                    ctx = r.get('context', {})
                    snapshot = r.get('chat_snapshot', [])
                    chat_lines = '\n'.join(
                        f"**{m.get('name','?')}:** {m.get('msg','')}"
                        for m in snapshot[-15:]
                    ) or 'Sin mensajes.'

                    embed_data = {
                        'embeds': [{
                            'title': '\U0001f6a8 NUEVO REPORTE',
                            'color': 0xFF3333,
                            'fields': [
                                {'name': '\U0001f464 Reportado',  'value': f"{r.get('target_name','?')}\n`{r.get('target_aid','?')}`",   'inline': True},
                                {'name': '\U0001f4e2 Reportador', 'value': f"{r.get('reporter_name','?')}\n`{r.get('reporter_aid','?')}`", 'inline': True},
                                {'name': '\U0001f4dd Raz\u00f3n',      'value': r.get('reason', '?'),                                           'inline': False},
                                {'name': '\U0001f3ae Actividad',  'value': ctx.get('activity', '?'),                                       'inline': True},
                                {'name': '\U0001f465 Online',     'value': str(ctx.get('players_online', '?')),                            'inline': True},
                                {'name': '\U0001f4ac Chat',       'value': chat_lines[:1024],                                              'inline': False},
                            ],
                            'footer': {'text': r.get('ts', '')},
                        }]
                    }

                    async with session.post(REPORTS_WEBHOOK, json=embed_data) as resp:
                        if resp.status == 429:
                            retry = float((await resp.json()).get('retry_after', 2))
                            await asyncio.sleep(retry)
                        elif resp.status not in (200, 204):
                            print(f'[reports] embed error: {resp.status}')

                    await asyncio.sleep(1.0)

                    buf = await asyncio.get_event_loop().run_in_executor(None, _render_reporter_card, r)
                    form = _aiohttp_mod.FormData()
                    form.add_field('file', buf, filename='reporter.png', content_type='image/png')
                    async with session.post(REPORTS_WEBHOOK, data=form) as resp:
                        if resp.status == 429:
                            retry = float((await resp.json()).get('retry_after', 2))
                            await asyncio.sleep(retry)
                        elif resp.status not in (200, 204):
                            print(f'[reports] imagen error: {resp.status}')

                    with _report_lock2:
                        _report_seen_ts.add(ts)
                    await asyncio.sleep(1.5)

                except Exception as e:
                    print(f'[reports] error enviando reporte: {e}')
        except Exception as e:
            print(f'[reports] loop error: {e}')

def _read_stats_top10() -> list:
    try:
        if not os.path.exists(STATS_JSON):
            return []
        with open(STATS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        stats = data.get('stats', {})
        sorted_players = sorted(stats.values(), key=lambda p: (p.get('kills', 0), p.get('wins', 0)), reverse=True)
        return sorted_players[:10]
    except Exception as e:
        print(f'[ladder] error leyendo stats: {e}')
        return []

def _read_season_number() -> int:
    try:
        season_path = SEASON_JSON
        if os.path.exists(season_path):
            with open(season_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('season_number', 1)
    except Exception:
        pass
    return 1

def _render_ladder_top10(players: list, season_number: int, season_ended: bool = False) -> io.BytesIO:
    W      = 560
    HEADER = 70
    ROW_H  = 62
    PAD    = 10
    H      = HEADER + ROW_H * max(len(players), 1) + PAD

    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw   = ImageDraw.Draw(canvas)
    bg     = Image.new('RGBA', (W, H), (14, 14, 24, 250))
    canvas.alpha_composite(bg)

    try:
        font_title  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
        font_rank   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        font_name   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
        font_sub    = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
        font_kills  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    except Exception:
        font_title = font_rank = font_name = font_sub = font_kills = ImageFont.load_default()

    if season_ended:
        header_color = (120, 40, 180, 255)
        title_text   = f'\U0001f3c6 FIN DE TEMPORADA {season_number} \u2014 TOP 10'
    else:
        header_color = (30, 40, 100, 255)
        title_text   = f'\u2694 LADDER TOP 10 \u2014 TEMPORADA {season_number}'

    draw.rectangle([0, 0, W, HEADER], fill=header_color)
    draw.rectangle([0, HEADER - 3, W, HEADER], fill=(200, 160, 50, 220) if season_ended else (80, 100, 220, 220))
    draw.text((PAD, 24), title_text, font=font_title, fill=(255, 245, 200, 255) if season_ended else (210, 220, 255, 255))

    RANK_COLORS = {
        1: (255, 215, 0),
        2: (192, 192, 192),
        3: (205, 127, 50),
    }
    AVATAR_S = 44

    for i, p in enumerate(players):
        rank   = i + 1
        y      = HEADER + i * ROW_H
        row_bg = (20, 20, 38, 240) if i % 2 == 0 else (26, 26, 46, 240)
        if rank == 1 and season_ended:
            row_bg = (40, 20, 60, 250)
        draw.rectangle([0, y, W, y + ROW_H - 1], fill=row_bg)

        rank_col = RANK_COLORS.get(rank, (140, 140, 180))
        draw.text((PAD + 2, y + ROW_H // 2), f'#{rank}', font=font_rank,
                  fill=rank_col + (255,), anchor='lm')

        char     = p.get('character', 'neoSpaz') if isinstance(p.get('character'), str) else 'neoSpaz'
        color    = p.get('color', [1.0, 1.0, 1.0])
        highlight= p.get('highlight', [1.0, 1.0, 1.0])
        char_png = os.path.join(CHARS_DIR, f'{char}.png')
        if not os.path.exists(char_png):
            char_png = os.path.join(CHARS_DIR, 'neoSpaz.png')
        av_x = 52
        av_y = y + (ROW_H - AVATAR_S) // 2
        if os.path.exists(char_png):
            avatar = Image.open(char_png).convert('RGBA').resize((AVATAR_S, AVATAR_S))
            try:
                if isinstance(color, list) and len(color) >= 3:
                    avatar = _tint_image(avatar, color, highlight if isinstance(highlight, list) else [1,1,1], char=char)
            except Exception:
                pass
            canvas.alpha_composite(avatar, (av_x, av_y))

        text_x = av_x + AVATAR_S + 8
        name   = p.get('name', '???')
        clean_name = ''.join(c for c in name if not (0xe000 <= ord(c) <= 0xf8ff)).strip() or name
        draw.text((text_x, y + 10), clean_name[:22], font=font_name, fill=(220, 220, 255, 255))

        kills  = p.get('kills', 0)
        deaths = p.get('deaths', 0)
        wins   = p.get('wins', 0)
        ns     = p.get('ns', 0)
        div    = p.get('division', '---')
        kd     = round(kills / max(deaths, 1), 2)

        draw.text((text_x, y + 28), f'\u2694 {kills} kills  |  KD {kd}  |  {wins} wins', font=font_sub, fill=(170, 180, 220, 220))
        draw.text((text_x, y + 42), f'{div}  \u2022  {ns} NS', font=font_sub, fill=(140, 140, 180, 180))

        bar_col = RANK_COLORS.get(rank, (60, 60, 120))
        draw.rectangle([0, y, 4, y + ROW_H - 1], fill=bar_col + (255,))

        if rank == 1 and season_ended:
            code = f'{ord(chr(0xe043)):04x}'
            icon_path = os.path.join(ICONS_DIR, f'{code}.png')
            if os.path.exists(icon_path):
                crown = Image.open(icon_path).convert('RGBA').resize((20, 20))
                canvas.alpha_composite(crown, (W - 28, y + (ROW_H - 20) // 2))

    buf = io.BytesIO()
    canvas.save(buf, 'PNG')
    buf.seek(0)
    return buf

_ladder_msg_id   = None
_last_season_num = None
SNAPSHOT_JSON    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nexus_data', 'season_snapshot.json')

def _read_season_snapshot() -> list:
    try:
        snap = os.path.normpath(SNAPSHOT_JSON)
        if os.path.exists(snap):
            with open(snap, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

async def _announce_season_end(channel, ended_season: int, players: list) -> None:
    buf1 = await asyncio.get_event_loop().run_in_executor(
        None, _render_ladder_top10, players, ended_season, True
    )
    file1 = discord.File(buf1, filename='season_end.png')
    embed1 = discord.Embed(
        title=f'\U0001f3c6 \u00a1FIN DE TEMPORADA {ended_season}!',
        description='La temporada ha concluido. \u00a1Gracias a todos los que participaron!',
        color=0x8B00FF
    )
    embed1.set_image(url='attachment://season_end.png')
    await channel.send(embed=embed1, file=file1)
    await asyncio.sleep(1)

    medals = ['\U0001f947', '\U0001f948', '\U0001f949', '4\ufe0f\u20e3', '5\ufe0f\u20e3', '6\ufe0f\u20e3', '7\ufe0f\u20e3', '8\ufe0f\u20e3', '9\ufe0f\u20e3', '\U0001f51f']
    lines = []
    for i, p in enumerate(players[:10]):
        name  = ''.join(c for c in p.get('name','???') if not (0xe000 <= ord(c) <= 0xf8ff)).strip() or p.get('name','???')
        kills = p.get('kills', 0)
        wins  = p.get('wins', 0)
        ns    = p.get('ns', 0)
        div   = p.get('division', '---')
        medal = medals[i] if i < len(medals) else f'#{i+1}'
        if i == 0:
            lines.append(f'{medal} **{name}** \u2014 {kills} kills | {wins} wins | {ns} NS | {div}  \u2190 \U0001f451 Premio especial')
        else:
            lines.append(f'{medal} **{name}** \u2014 {kills} kills | {wins} wins | {ns} NS | {div}  \u2190 \U0001f396 ALTpha')

    embed2 = discord.Embed(
        title=f'\U0001f396 Resultados Temporada {ended_season}',
        description='\n'.join(lines) if lines else 'Sin jugadores registrados.',
        color=0xFFD700
    )
    embed2.set_footer(text='Top 1 recibir\u00e1 un premio especial \u2022 Top 2-10 obtienen rol ALTpha en el juego')
    await channel.send(embed=embed2)
    await asyncio.sleep(1)
    print(f'[ladder] anuncio temporada {ended_season} enviado')

async def _ladder_watcher() -> None:
    global _ladder_msg_id, _last_season_num
    import asyncio

    await asyncio.sleep(8)
    channel = bot.get_channel(LADDER_CHANNEL)
    if not channel:
        print('[ladder] canal no encontrado')
        return

    async for msg in channel.history(limit=20):
        if msg.author.id == bot.user.id:
            _ladder_msg_id = msg.id
            break

    _last_season_num = _read_season_number()

    while True:
        try:
            season_number = _read_season_number()
            season_ended  = False

            if _last_season_num is not None and season_number != _last_season_num:
                season_ended     = True
                ended_season_num = _last_season_num
                _last_season_num = season_number

            players = _read_stats_top10()

            if season_ended:
                if _ladder_msg_id:
                    try:
                        old_msg = await channel.fetch_message(_ladder_msg_id)
                        await old_msg.delete()
                    except Exception:
                        pass
                    _ladder_msg_id = None

                snap = _read_season_snapshot()
                final_players = snap if snap else players

                await _announce_season_end(channel, ended_season_num, final_players)

            buf = await asyncio.get_event_loop().run_in_executor(
                None, _render_ladder_top10, players, season_number, False
            )
            file = discord.File(buf, filename='ladder.png')
            embed = discord.Embed(color=0x1a1d4e)
            embed.set_image(url='attachment://ladder.png')
            embed.set_footer(text=f'Actualizado cada 60s  \u2022  Temporada {season_number}')

            if _ladder_msg_id:
                try:
                    msg = await channel.fetch_message(_ladder_msg_id)
                    await msg.edit(embed=embed, attachments=[file])
                except discord.NotFound:
                    _ladder_msg_id = None
                except Exception as edit_err:
                    print(f'[ladder] edit fallido (sin crear nuevo): {edit_err}')

            if not _ladder_msg_id:
                buf2 = await asyncio.get_event_loop().run_in_executor(
                    None, _render_ladder_top10, players, season_number, False
                )
                file2 = discord.File(buf2, filename='ladder.png')
                new_msg = await channel.send(embed=embed, file=file2)
                _ladder_msg_id = new_msg.id

        except Exception as e:
            print(f'[ladder] error: {e}')

        await asyncio.sleep(60)

@tree.command(name='verificar', description='Verific\u00e1 tu cuenta de BombSquad')
@app_commands.describe(token='Tu c\u00f3digo de verificaci\u00f3n del juego')
async def cmd_verificar(interaction: discord.Interaction, token: str):
    import time as _t
    await interaction.response.defer(ephemeral=True)
    token = token.strip().upper()
    if not os.path.exists(PENDING_VERIFY):
        await interaction.followup.send('\u274c Token inv\u00e1lido o expirado.', ephemeral=True)
        return
    try:
        with open(PENDING_VERIFY, 'r', encoding='utf-8') as f:
            pending = json.load(f)
    except Exception:
        await interaction.followup.send('\u274c Error al leer tokens.', ephemeral=True)
        return
    entry = pending.get(token)
    if not entry:
        await interaction.followup.send('\u274c Token inv\u00e1lido o expirado.', ephemeral=True)
        return
    if entry.get('expires', 0) < _t.time():
        pending.pop(token, None)
        with open(PENDING_VERIFY, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)
        await interaction.followup.send('\u23f0 Token expirado. Us\u00e1 /discord en el juego de nuevo.', ephemeral=True)
        return
    acc = entry.get('acc')
    if os.path.exists(VERIFIED_PATH):
        try:
            with open(VERIFIED_PATH, 'r', encoding='utf-8') as f:
                verified = json.load(f)
            if acc in verified:
                await interaction.followup.send('\u26a0\ufe0f Esta cuenta ya est\u00e1 verificada.', ephemeral=True)
                return
            for data in verified.values():
                if data.get('discord_id') == interaction.user.id:
                    await interaction.followup.send('\u26a0\ufe0f Tu Discord ya est\u00e1 vinculado a otra cuenta.', ephemeral=True)
                    return
        except Exception:
            pass
    player = _get_player_from_roster(acc)
    if not player:
        player = {'aid': acc, 'name': acc, 'character': 'neoSpaz', 'color': [1.0, 1.0, 1.0], 'highlight': [1.0, 1.0, 1.0]}
    buf  = await asyncio.get_event_loop().run_in_executor(None, _render_verify_card, player)
    file = discord.File(buf, filename='verify.png')
    r = int(min(1, player['color'][0]) * 255)
    g = int(min(1, player['color'][1]) * 255)
    b = int(min(1, player['color'][2]) * 255)
    embed = discord.Embed(
        title='\U0001f3ae Verificaci\u00f3n de cuenta',
        color=(r << 16) + (g << 8) + b
    )
    embed.set_image(url='attachment://verify.png')
    embed.set_footer(text='Este mensaje expira en 2 horas')
    view = VerifyView(token, acc, player, interaction.user.id)
    await interaction.followup.send(embed=embed, file=file, view=view, ephemeral=True)

_ALLOWED_UNVERIFY: dict = {
    'owner': [1504729014051410011],
    'admin': [],
    'mod':   [],
}

@tree.command(name='unverify', description='Quitar verificaci\u00f3n de una cuenta de BombSquad')
@app_commands.describe(acc='Account ID del jugador (ej: pb-IF4xxx==)')
async def cmd_unverify(interaction: discord.Interaction, acc: str):
    if not _has_perm(interaction.user):
        await interaction.response.send_message('\u26d4 Sin permisos.', ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    raw = acc.strip()
    if raw.startswith('<@') and raw.endswith('>'):
        raw = raw[2:-1].lstrip('!')
    acc = raw
    if not acc.startswith('pb-'):
        found = None
        if os.path.exists(VERIFIED_PATH):
            try:
                with open(VERIFIED_PATH, 'r', encoding='utf-8') as f:
                    verified = json.load(f)
                for pb_id, data in verified.items():
                    if acc.isdigit():
                        if str(data.get('discord_id', '')) == acc:
                            found = pb_id
                            break
                    else:
                        if data.get('discord_name', '').lower() == acc.lower():
                            found = pb_id
                            break
            except Exception as e:
                print(f'[unverify] lookup error: {e}')
        if not found:
            await interaction.followup.send(f'\u274c No se encontr\u00f3 `{acc}` en verified.', ephemeral=True)
            return
        acc = found
    removed_verified = False
    if os.path.exists(VERIFIED_PATH):
        try:
            with open(VERIFIED_PATH, 'r', encoding='utf-8') as f:
                verified = json.load(f)
            if acc in verified:
                entry = verified[acc]
                unverify_discord_id = entry.get('discord_id')
                del verified[acc]
                with open(VERIFIED_PATH, 'w', encoding='utf-8') as f:
                    json.dump(verified, f, indent=2)
                removed_verified = True
                if unverify_discord_id:
                    try:
                        guild = bot.get_guild(_CFG['guild_id'])
                        try:
                            umember = await guild.fetch_member(unverify_discord_id)
                        except Exception:
                            umember = guild.get_member(unverify_discord_id)
                        if umember:
                            for rid in (_CFG['roles']['uzc'], _CFG['roles']['alt']):
                                r = guild.get_role(rid)
                                if r and r in umember.roles:
                                    await umember.remove_roles(r)
                                    print(f'[unverify] rol {rid} removido de Discord')
                        else:
                            print(f'[unverify] umember es None para discord_id={unverify_discord_id}')
                    except Exception as e:
                        print(f'[unverify] remove_role error: {e}')
        except Exception as e:
            print(f'[unverify] verified error: {e}')
    try:
        pending_roles_path = os.path.join(_DATA_BASE, 'pending_bs_roles.json')
        pr = {}
        if os.path.exists(pending_roles_path):
            with open(pending_roles_path, 'r', encoding='utf-8') as f:
                pr = json.load(f)
        pr[acc] = None  # None = quitar rol
        with open(pending_roles_path, 'w', encoding='utf-8') as f:
            json.dump(pr, f, indent=2)
    except Exception as e:
        print(f'[unverify] bs_role error: {e}')
    msg = f'\u2705 `{acc}` desverificado.'
    if not removed_verified:
        msg += ' (no estaba en verified.json)'
    await interaction.followup.send(msg, ephemeral=True)

async def _verify_watcher():
    import time
    seen = None
    await asyncio.sleep(3)
    while True:
        try:
            if os.path.exists(VERIFY_NOTIFY):
                with open(VERIFY_NOTIFY, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                token = data.get('token')
                acc   = data.get('acc')
                if token and token != seen:
                    seen = token
                    os.remove(VERIFY_NOTIFY)
                    if os.path.exists(PENDING_VERIFY):
                        with open(PENDING_VERIFY, 'r', encoding='utf-8') as f:
                            pending = json.load(f)
                        entry = pending.get(token)
                        if entry:
                            entry['acc'] = acc
                            pending[token] = entry
                            with open(PENDING_VERIFY, 'w', encoding='utf-8') as f:
                                json.dump(pending, f, indent=2)
                            discord_id = entry.get('discord_id', 0)
                            channel_id = entry.get('channel_id')
                            ticket_ch  = bot.get_channel(channel_id) if channel_id else None
                            ticket_ch  = bot.get_channel(channel_id) if channel_id else None
                            roster_player = _get_player_from_roster(acc) or {}
                            player = {
                                'aid':          acc,
                                'name':         entry.get('name', roster_player.get('name', acc)),
                                'account_name': entry.get('account_name', roster_player.get('account_name', '')),
                                'character':    entry.get('character', roster_player.get('character', 'neoSpaz')),
                                'color':        entry.get('color', roster_player.get('color', [1,1,1])),
                                'highlight':    entry.get('highlight', roster_player.get('highlight', [1,1,1])),
                            }
                            buf  = await asyncio.get_event_loop().run_in_executor(None, _render_verify_card, player)
                            file = discord.File(buf, filename='verify.png')
                            r = int(min(1, player['color'][0]) * 255)
                            g = int(min(1, player['color'][1]) * 255)
                            b = int(min(1, player['color'][2]) * 255)
                            embed = discord.Embed(
                                title='\U0001f3ae Verificaci\u00f3n de cuenta',
                                color=(r << 16) + (g << 8) + b
                            )
                            embed.set_image(url='attachment://verify.png')
                            embed.set_footer(text='Confirm\u00e1 si esta es tu cuenta')
                            view = VerifyConfirmView(token, acc, player, discord_id, ticket_ch)
                            target_ch = ticket_ch or bot.get_channel(VERIFY_CHANNEL)
                            if target_ch:
                                await target_ch.send(embed=embed, file=file, view=view)
        except Exception as e:
            print(f'[verify_watcher] error: {e}')
        await asyncio.sleep(2)

@tree.command(name='setup_verify', description='Postea el embed de verificacion en el canal')
@app_commands.checks.has_role(ALLOWED_ROLE)
async def setup_verify(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    channel = bot.get_channel(VERIFY_CHANNEL)
    if not channel:
        await interaction.followup.send('\u274c Canal no encontrado.', ephemeral=True)
        return
    embed = discord.Embed(
        title='\U0001f3ae Verificaci\u00f3n de cuenta',
        description=(
            'Para vincular tu cuenta de BombSquad con Discord segu\u00ed estos pasos:\n\n'
            '**1.** Apret\u00e1 el bot\u00f3n de abajo\n'
            '**2.** Se va a crear un canal privado para vos\n'
            '**3.** Ah\u00ed vas a recibir un token \u2014 cop\u00e1lo\n'
            '**4.** Entr\u00e1 al servidor de BombSquad y escrib\u00ed:\n'
            '```/v TU_TOKEN```\n'
            '**5.** Confirm\u00e1 tu cuenta en Discord\n\n'
            '\u23f0 El token dura **2 horas**.\n'
            '\u2139\ufe0f Si ten\u00e9s problemas un admin puede ayudarte en tu canal privado.'
        ),
        color=0x5865f2
    )
    embed.set_footer(text='Umbral Zero Community \u2014 Sistema de verificaci\u00f3n')
    await channel.send(embed=embed, view=StartVerifyView())
    await interaction.followup.send('\u2705 Embed posteado.', ephemeral=True)

@tree.error
async def on_tree_error(interaction: discord.Interaction, error: Exception):
    print(f'[tree_error] {type(error).__name__}: {error}')

@bot.event
async def on_ready():
    await tree.sync()
    print(f'[tag_bot] conectado como {bot.user}')
    bot.add_view(StartVerifyView())
    asyncio.ensure_future(_start_chat_watcher())
    asyncio.ensure_future(_start_report_watcher())
    asyncio.ensure_future(_live_players_watcher())
    asyncio.ensure_future(_ladder_watcher())
    asyncio.ensure_future(_verify_watcher())

async def _start_chat_watcher():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await _chat_watcher(session)

async def _start_report_watcher():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await _report_watcher(session)

if not BOT_TOKEN or BOT_TOKEN == 'TU_TOKEN':
    print('[tag_bot] sin token configurado, bot desactivado.')
else:
    bot.run(BOT_TOKEN)
'''

_BOT_PATH  = os.path.join(os.path.dirname(__file__), '_bot_runner.py')
_SELF_PATH = os.path.abspath(__file__)
_proc: 'subprocess.Popen | None' = None
_last_mtime: float = 0.0

def _kill_bot() -> None:
    global _proc
    if _proc and _proc.poll() is None:
        try:
            import signal
            os.killpg(os.getpgid(_proc.pid), signal.SIGTERM)
        except Exception:
            _proc.terminate()
        try:
            _proc.wait(timeout=5)
        except Exception:
            try:
                import signal
                os.killpg(os.getpgid(_proc.pid), signal.SIGKILL)
            except Exception:
                _proc.kill()
    _proc = None

def _kill_orphans() -> None:
    import signal
    try:
        result = subprocess.run(
            ['pgrep', '-f', '_bot_runner.py'],
            capture_output=True, text=True
        )
        for pid_str in result.stdout.strip().splitlines():
            try:
                pid = int(pid_str)
                os.kill(pid, signal.SIGKILL)
                print(f'[tag_bot] orphan killed: {pid}')
            except Exception:
                pass
    except Exception as e:
        print(f'[tag_bot] _kill_orphans error: {e}')

def _write_and_start() -> None:
    global _proc, _last_mtime
    _kill_orphans()
    _kill_bot()
    with open(_BOT_PATH, 'w', encoding='utf-8') as f:
        f.write(_BOT_SCRIPT)
    _last_mtime = os.path.getmtime(_SELF_PATH)
    _proc = subprocess.Popen(
        [sys.executable, _BOT_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    print('[tag_bot] bot de Discord iniciado')

    def _pipe():
        for line in iter(_proc.stdout.readline, b''):
            print('[tag_bot]', line.decode('utf-8', errors='replace').rstrip())
    threading.Thread(target=_pipe, daemon=True).start()

def _watchdog() -> None:
    import time
    global _BOT_SCRIPT
    while True:
        time.sleep(3)
        try:
            mtime = os.path.getmtime(_SELF_PATH)
            if mtime != _last_mtime:
                print('[tag_bot] cambio detectado - relanzando bot...')
                with open(_SELF_PATH, 'r', encoding='utf-8') as f:
                    src = f.read()
                start = src.find("_BOT_SCRIPT = r'''") + len("_BOT_SCRIPT = r'''")
                end   = src.find("\n'''", start)
                if start > 0 and end > 0:
                    _BOT_SCRIPT = src[start:end]
                _write_and_start()
        except Exception as e:
            print(f'[tag_bot] watchdog error: {e}')

def enable() -> None:
    threading.Thread(target=_write_and_start, daemon=True).start()
    threading.Thread(target=_watchdog, daemon=True).start()
    try:
        import babase
        async def _async_kill():
            _kill_bot()
    except Exception:
        pass
    print('[tag_bot] plugin cargado')
