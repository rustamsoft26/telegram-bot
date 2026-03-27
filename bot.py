import sqlite3
import imagehash
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# baza ochamiz
conn = sqlite3.connect("hashes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS hashes (hash TEXT)")
conn.commit()

TOKEN = "8656669768:AAGEtCyW-qL5qanXwb2X4iGEGcl3uotBJSg"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive("temp.jpg")

    img = Image.open("temp.jpg")
    img_hash = str(imagehash.phash(img))

    cursor.execute("SELECT hash FROM hashes WHERE hash=?", (img_hash,))
    result = cursor.fetchone()

    if result:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Bu rasm ilgari yuborilgan, iltimos hiyla qilmang!"
        )
    else:
        cursor.execute("INSERT INTO hashes (hash) VALUES (?)", (img_hash,))
        conn.commit()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="✅ Yangi rasm saqlandi"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
