from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import config
from commands import start, chat, help_command, history_command
from db import create_db  # Assumes create_db is defined in db.py

def main():
    create_db()  # crea la tabella se non esiste
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(CommandHandler("help", help_command)) 
    app.add_handler(CommandHandler("history", history_command)) 
    print("🤖 Bot avviato!")
    app.run_polling()

if __name__ == "__main__":
    main()
