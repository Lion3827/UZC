#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sed -i '/babase.app.add_shutdown_task/d' "$DIR/dist/ba_root/mods/plugins/tag_bot/tag_bot.py"
touch "$DIR/dist/ba_root/mods/plugins/tag_bot/tag_bot.py"
exec "$DIR/bombsquad_server" "$@"
