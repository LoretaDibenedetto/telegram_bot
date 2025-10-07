from telegram import Update
from telegram.ext import ContextTypes
from memory import add_message, build_context
from api_gemini import ask_gemini

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.chat_data["memory"] = []
    await update.message.reply_text("Ciao! 👋 Sono il tuo bot AI. Scrivimi qualcosa e ti risponderò!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_message = update.message.text

    memory = context.chat_data.get("memory", [])
    memory = add_message(memory, f"Utente: {user_message}")

    context_text = build_context(memory)
    reply = ask_gemini(context_text)

    memory = add_message(memory, f"AI: {reply}")
    context.chat_data["memory"] = memory

    await update.message.reply_text(reply)
