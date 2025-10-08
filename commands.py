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
    await send_long_message(update, reply)


    
    

  
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Comandi disponibili:\n"
        "/start - Avvia il bot\n"
        "/help - Mostra questo messaggio di aiuto\n"
        "/history - Mostra gli ultimi messaggi della chat\n\n"
        "Scrivi qualsiasi messaggio per chattare con l'AI."
    )
    await update.message.reply_text(help_text)


MAX_TELEGRAM_MSG_LENGTH = 4096

async def send_long_message(update, text):
    if len(text) <= MAX_TELEGRAM_MSG_LENGTH:
        await update.message.reply_text(text)
    else:
        for i in range(0, len(text), MAX_TELEGRAM_MSG_LENGTH):
            await update.message.reply_text(text[i:i+MAX_TELEGRAM_MSG_LENGTH])


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id

        # Recupera ultimo storico (ad esempio ultimi 10 messaggi)
        messages = get_recent_messages(chat_id, limit=10)
        
        if not messages:
            await update.message.reply_text("📭 Nessuna cronologia disponibile per questa chat.")
            return

        # Prepara testo da inviare
        history_lines = []
        for sender, message in messages:
            prefix = "🤖 AI" if sender == "bot" else "👤 Utente"
            history_lines.append(f"{prefix}: {message}")

        history_text = "\n".join(history_lines)

        await update.message.reply_text(f"📜 Storico ultimi messaggi:\n\n{history_text}")
 