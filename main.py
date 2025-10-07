



from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes









# 🔹 Memoria breve per conversazione (ultimi 5 messaggi)
chat_memory = {}



# 🔹 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    chat_memory[chat_id] = []  # inizializza memoria
    await update.message.reply_text(
        "Ciao! 👋 Sono il tuo bot AI. Scrivimi qualcosa e ti risponderò!"
    )




# 🔹 Gestione messaggi
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_message = update.message.text
    reply = ask_gemini(chat_id, user_message, chat_memory)
    await update.message.reply_text(reply)

# 🔹 Avvio bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Bot Gemini Telegram attivo! Scrivi qualcosa al bot...")
app.run_polling()