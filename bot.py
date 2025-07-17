from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = '7755895733:AAGqzDhti3hx8sTl93T0QrUmyZsfE3TY42I'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    if username:
        username = '@' + username
    else:
        username = ''
    await update.message.reply_text(
        f"سلام!\nخوش آمدی {username}\n"
        "برای ساخت استیکر، عکس بفرست.\n"
        "برای دیدن عکس یا ویدیوی استیکر، استیکر بفرست."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive('photo.jpg')
    with open('photo.jpg', 'rb') as f:
        await update.message.reply_sticker(InputFile(f))

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    file = await context.bot.get_file(sticker.file_id)

    if sticker.is_animated:
        filename = 'sticker.tgs'
    elif sticker.is_video:
        filename = 'sticker.webm'
    else:
        filename = 'sticker.webp'

    await file.download_to_drive(filename)

    with open(filename, 'rb') as f:
        if sticker.is_animated or sticker.is_video:
            await update.message.reply_document(InputFile(f, filename=filename))
        else:
            await update.message.reply_photo(InputFile(f))

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.STICKER, handle_sticker))

    print("ربات روشن شد!")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
