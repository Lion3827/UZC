# UZC - BombSquad Server

Servidor competitivo de BombSquad corriendo en Ballistica API 9.

## Requisitos

- VPS con Linux x86_64 (Ubuntu 22+ recomendado)
- Python 3.13
- tmux
- 1 GB RAM mínimo

## Instalación

### 1. Instalar dependencias del sistema

```bash
sudo apt install python3.13 python3.13-dev python3-pip tmux -y
```

### 2. Instalar dependencias de Python

```bash
pip3 install aiohttp discord.py pillow requests
```

### 3. Clonar el repositorio

```bash
git clone https://github.com/Lion3827/UZC
cd UZC
```

### 4. Dar permisos de ejecución

```bash
chmod +x start.sh
chmod +x dist/bombsquad_headless
```

### 5. Configurar el bot de Discord

Edita `dist/ba_root/mods/plugins/bot_config.json` con tu token y IDs de Discord.

### 6. Configurar permisos

Edita `dist/ba_root/mods/plugins/perms/perms_data.json` y agrega tu account ID como owner.

### 5. Configurar el bot de Discord

Edita dist/ba_root/mods/plugins/bot_config.json con tu token y IDs de Discord.

### 6. Configurar permisos

Edita dist/ba_root/mods/plugins/perms/perms_data.json y agrega tu account ID como owner.

### 7. Iniciar el servidor

```bash
tmux new -s uzc
./start.sh
