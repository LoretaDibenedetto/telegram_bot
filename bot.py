from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import config
from commands import start, chat

def main():
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot avviato!")
    app.run_polling()

if __name__ == "__main__":
    main()
