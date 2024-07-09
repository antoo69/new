from YukkiMusic import app
from pyrogram import Client, filters
from YukkiMusic.utils.groups import get_group_names
from YukkiMusic.misc import SUDOERS

@app.on_message(filters.command("listgroups") & SUDOERS)
async def handle_message(client, message):
        group_names = await get_group_names(app)
        if group_names:
            await message.reply_text("\n".join(group_names))
        else:
            await message.reply_text("Bot belum ditambahkan ke grup mana pun.")
