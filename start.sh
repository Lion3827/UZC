#!/bin/bash
sed -i '/babase.app.add_shutdown_task/d' /root/SalsaDiamond/dist/ba_root/mods/plugins/tag_bot/tag_bot.py
touch /root/SalsaDiamond/dist/ba_root/mods/plugins/tag_bot/tag_bot.py
exec /root/SalsaDiamond/bombsquad_server "$@"