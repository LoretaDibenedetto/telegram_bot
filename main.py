
import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


# 🔑 Inserisci qui i tuoi token
load_dotenv()  # loads variables from .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY




# 🔹 Memoria breve per conversazione (ultimi 5 messaggi)
chat_memory = {}

MAX_MEMORY = 5  # numero di messaggi da ricordare



# 🔹 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    chat_memory[chat_id] = []  # inizializza memoria
    await update.message.reply_text(
        "Ciao! 👋 Sono il tuo bot AI. Scrivimi qualcosa e ti risponderò!"
    )

# 🔹 Funzione per generare risposta con Gemini
def ask_gemini(chat_id, user_message):
    if chat_id not in chat_memory:
        chat_memory[chat_id] = []

    # Aggiunge messaggio utente alla memoria
    chat_memory[chat_id].append(f"Utente: {user_message}")
    if len(chat_memory[chat_id]) > MAX_MEMORY:
        chat_memory[chat_id] = chat_memory[chat_id][-MAX_MEMORY:]

    context_text = "\n".join(chat_memory[chat_id]) + "\nAI:"

    payload = {
        "contents": [
            {
                "parts": [{"text": context_text}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=20)
        data = response.json()
    except Exception as e:
        return f"🚨 Errore di connessione con Gemini: {e}"

    # ✅ Controlla se Gemini ha risposto correttamente
    if "candidates" in data:
        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            reply = "⚠️ Gemini ha risposto in un formato inatteso."
    elif "error" in data:
        reply = f"❌ Errore Gemini: {data['error'].get('message', 'Errore sconosciuto')}"
    else:
        reply = f"😅 Risposta non valida di Gemini: {data}"

    chat_memory[chat_id].append(f"AI: {reply}")
    return reply


# 🔹 Gestione messaggi
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_message = update.message.text
    reply = ask_gemini(chat_id, user_message)
    await update.message.reply_text(reply)

# 🔹 Avvio bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Bot Gemini Telegram attivo! Scrivi qualcosa al bot...")
app.run_polling()