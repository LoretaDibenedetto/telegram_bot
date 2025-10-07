import requests
import logging
from typing import List
import config  # Make sure config.py exists and contains GEMINI_API_URL

logger = logging.getLogger(__name__)

def ask_gemini(context_text: str) -> str:
    payload = {
        "contents": [
            {"parts": [{"text": context_text}]}
        ]
    }

    try:
        response = requests.post(config.GEMINI_API_URL, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Errore API Gemini: {e}")
        return "🚨 Errore di connessione con Gemini."

    if "candidates" in data:
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "⚠️ Risposta Gemini in formato inatteso."
    elif "error" in data:
        return f"❌ Errore Gemini: {data['error'].get('message', 'Errore sconosciuto')}"
    else:
        return "😅 Risposta Gemini non valida."
