from telegram import Update
from telegram.ext import ContextTypes

from api_gemini import ask_gemini
from memory import add_message, build_context     # per la memoria temporanea

from db import get_recent_messages, save_message  # per la memoria persistente


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.chat_data["memory"] = []
    await update.message.reply_text("Ciao! 👋 Sono il tuo bot AI. Scrivimi qualcosa e ti risponderò!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_message = update.message.text
    # Recupera la memoria temporanea della chat (lista)
    memory = context.chat_data.get("memory", [])

    # Aggiorna la memoria aggiungendo il messaggio dell'utente
    memory = add_message(memory, f"Utente: {user_message}")

    # Salva la memoria aggiornata nel contesto della chat
    context.chat_data["memory"] = memory

    # Costruisci il contesto da inviare a Gemini (puoi usare build_context)
    context_text = build_context(memory)

    # Chiama Gemini per la risposta
    reply = ask_gemini(context_text)

    # Aggiorna la memoria con la risposta della AI
    memory = add_message(memory, f"AI: {reply}")
    context.chat_data["memory"] = memory

    # Invia la risposta all'utente
    await update.message.reply_text(reply)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Comandi disponibili:\n"
        "/start - Avvia il bot\n"
        "/help - Mostra questo messaggio di aiuto\n"
        "Scrivi qualsiasi messaggio per chattare con l'AI."
    )
    await update.message.reply_text(help_text)