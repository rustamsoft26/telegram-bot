from telegram.ext import Application, MessageHandler, filters
import imagehash
from PIL import Image
import io

hashes = set()

async def handle_photo(update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    data = await file.download_as_bytearray()

    img = Image.open(io.BytesIO(data))
    h = str(imagehash.phash(img))

    if h in hashes:
        await update.message.reply_text(
            "Bu rasm oldin yuborilgan"
        )
    else:
        hashes.add(h)

app = Application.builder().token("8656669768:AAGEtCyW-qL5qanXwb2X4iGEGcl3uotBJSg").build()

app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()