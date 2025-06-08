import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID", "23212132"))
API_HASH = os.environ.get("API_HASH", "1c17efa86bdef8f806ed70e81b473c20")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7946471075:AAEMIKMxb6T5n5SwpOvf8XMBbiA6XpxOtec")

app = Client("string_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

START_TEXT = """
✨ **Welcome to MonarchX String Session Generator!** ✨

Choose your preferred library to generate a string session.
"""

ABOUT_TEXT = """
**MonarchX String Generator Bot**
- Supports: Pyrogram & Telethon
- Fast, Secure & Easy to use!
- Made with ❤️ by [︎ 𝙁𝙊𝙎 〤 𝙉𝙊𝙓 ♛](https://t.me/FOS_FOUNDER)
"""

HELP_TEXT = """
**How to use:**
1. Click a button below to select a library.
2. Send your `API_ID` and then `API_HASH` as prompted.
3. Follow the instructions to get your string session.

_Never share your string session with anyone!_
"""

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⚡ Pyrogram", callback_data="pyrogram"),
            InlineKeyboardButton("💫 Telethon", callback_data="telethon"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ]
    ]
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        START_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "about":
        await callback_query.message.edit_text(
            ABOUT_TEXT,
            reply_markup=BUTTONS,
            disable_web_page_preview=True
        )
        return


    if data == "help":
        await callback_query.message.edit_text(
            HELP_TEXT,
            reply_markup=BUTTONS,
            disable_web_page_preview=True
        )
        return

    if data == "pyrogram":
        await callback_query.message.edit_text(
            "🔑 **Pyrogram String Session**\n\nSend your `API_ID`:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
        )

        def check_id(client, message):
            return message.chat.id == callback_query.message.chat.id and message.text.isdigit()

        resp_id = await app.listen(callback_query.message.chat.id, filters=filters.text & filters.create(check_id))
        await callback_query.message.reply("Now, send your `API_HASH`:")

        def check_hash(client, message):
            return message.chat.id == callback_query.message.chat.id and len(message.text) == 32

        resp_hash = await app.listen(callback_query.message.chat.id, filters=filters.text & filters.create(check_hash))
        try:
            api_id = int(resp_id.text.strip())
            api_hash = resp_hash.text.strip()
            await callback_query.message.reply("📱 Now, send your phone number (with country code):")

            def check_phone(client, message):
                return message.chat.id == callback_query.message.chat.id and message.text.startswith("+")

            phone = (await app.listen(callback_query.message.chat.id, filters=filters.text & filters.create(check_phone))).text
            async with Client(":memory:", api_id=api_id, api_hash=api_hash) as user:
                await user.connect()
                await user.send_code(phone)
                def check_code(client, message):
                    return message.chat.id == callback_query.message.chat.id and message.text.isdigit()
                code = (await app.listen(callback_query.message.chat.id, filters=filters.text & filters.create(check_code))).text
                await user.sign_in(phone, code)
                string_session = await user.export_session_string()
                await callback_query.message.reply(
                    f"✅ **Pyrogram String Session:**\n\n`{string_session}`\n\n"
                    "_Keep this string safe and never share it!_"
                )
        except Exception as e:
            await callback_query.message.reply(f"❌ Error: `{e}`")

    elif data == "telethon":
        await callback_query.message.edit_text(
            "🔑 **Telethon String Session**\n\nSend your `API_ID`:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
        )
        resp_id = await app.listen(callback_query.message.chat.id)
        await callback_query.message.reply("Now, send your `API_HASH`:")
        resp_hash = await app.listen(callback_query.message.chat.id)
        try:
            api_id = int(resp_id.text.strip())
            api_hash = resp_hash.text.strip()
            await callback_query.message.reply("📱 Now, send your phone number (with country code):")
            phone = (await app.listen(callback_query.message.chat.id)).text
            with TelegramClient(StringSession(), api_id, api_hash) as user:
                user.start(phone=phone)
                string_session = user.session.save()
                await callback_query.message.reply(
                    f"✅ **Telethon String Session:**\n\n`{string_session}`\n\n"
                    "_Keep this string safe and never share it!_"
                )
        except Exception as e:
            await callback_query.message.reply(f"❌ Error: `{e}`")

    elif data == "start":
        await callback_query.message.edit_text(
            START_TEXT,
            reply_markup=BUTTONS,
            disable_web_page_preview=True
        )

if __name__ == "__main__":
    app.run()
