from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7755895733:AAGqzDhti3hx8sTl93T0QrUmyZsfE3TY42I'

def start(update: Update, context: CallbackContext):
    username = update.effective_user.username
    if username:
        username = '@' + username
    else:
        username = ''
    update.message.reply_text(
        f"سلام!\nخوش آمدی {username}\n"
        "برای ساخت استیکر، عکس بفرست.\n"
        "برای دیدن عکس یا ویدیوی استیکر، استیکر بفرست."
    )

def handle_photo(update: Update, context: CallbackContext):
    file = update.message.photo[-1].get_file()
    file.download('photo.jpg')
    with open('photo.jpg', 'rb') as f:
        update.message.reply_sticker(f)

def handle_sticker(update: Update, context: CallbackContext):
    sticker = update.message.sticker
    if sticker.is_animated or sticker.is_video:
        file = context.bot.get_file(sticker.file_id)
        filename = 'sticker.tgs' if sticker.is_animated else 'sticker.webm'
        file.download(filename)
        with open(filename, 'rb') as f:
            update.message.reply_document(f, filename=filename)
    else:
        file = context.bot.get_file(sticker.file_id)
        file.download('sticker.webp')
        with open('sticker.webp', 'rb') as f:
            update.message.reply_photo(f)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.sticker, handle_sticker))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
