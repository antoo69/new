from pyrogram import Client
from typing import List

# Import fungsi database yang telah Anda definisikan
from YukkiMusic.utils.database import get_served_chats  # Ganti dengan nama file database Anda jika berbeda

async def get_group_names(app: Client) -> List[str]:
  """
  Mengambil daftar nama grup yang menggunakan bot.

  Args:
    app: Objek klien Pyrogram.

  Returns:
    Sebuah list yang berisi nama-nama grup.
  """

  group_names = []
  served_chats = await get_served_chats()

  for chat in served_chats:
    try:
      chat_obj = await app.get_chat(chat["chat_id"])
      group_names.append(chat_obj.title)
    except Exception as e:
      print(f"Error mengambil informasi grup: {e}")

  return group_names
