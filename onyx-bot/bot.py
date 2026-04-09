import os
import sqlite3
import json
import logging
import tempfile
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from anthropic import Anthropic
from openai import OpenAI
from system_prompt import ONYX_SYSTEM_PROMPT
from notion_client import save_linkedin_post, save_substack_article
from drive_client import save_to_drive

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

# ─── Conversation history (SQLite para persistencia entre reinicios) ───────────

DB_PATH = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS last_draft (
            chat_id INTEGER PRIMARY KEY,
            content TEXT,
            title TEXT,
            draft_type TEXT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_history(chat_id: int, limit: int = 20) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM conversations WHERE chat_id=? ORDER BY ts DESC LIMIT ?",
        (chat_id, limit)
    ).fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def add_message(chat_id: int, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO conversations (chat_id, role, content) VALUES (?, ?, ?)",
        (chat_id, role, content)
    )
    conn.commit()
    conn.close()

def clear_history(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM conversations WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()

def save_draft(chat_id: int, content: str, title: str, draft_type: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO last_draft (chat_id, content, title, draft_type) VALUES (?, ?, ?, ?)",
        (chat_id, content, title, draft_type)
    )
    conn.commit()
    conn.close()

def get_draft(chat_id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT content, title, draft_type FROM last_draft WHERE chat_id=?",
        (chat_id,)
    ).fetchone()
    conn.close()
    if row:
        return {"content": row[0], "title": row[1], "type": row[2]}
    return None


# ─── Claude call ──────────────────────────────────────────────────────────────

def ask_onyx(chat_id: int, user_message: str) -> str:
    history = get_history(chat_id)
    messages = history + [{"role": "user", "content": user_message}]

    try:
        response = anthropic.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=ONYX_SYSTEM_PROMPT,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error en Claude API: {e}")
        raise


# ─── Handlers ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Hola Lucía, soy Onyx.\n\n"
        "Podés usarme con comandos o hablarme directamente.\n\n"
        "*/post* [contexto] — draft de post LinkedIn\n"
        "*/substack* [contexto] — outline o artículo Substack\n"
        "*/roadmap* — tareas de la semana\n"
        "*/save* — guarda el último draft en Drive + Notion\n"
        "*/new* — nueva conversación\n\n"
        "O escribime lo que necesites y te respondo."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = " ".join(context.args) if context.args else ""
    prompt = f"Generá un post de LinkedIn. {args}" if args else "Generá un post de LinkedIn sobre P1 (AP Reconciliation App)."

    await update.message.reply_text("⏳ Generando post...")
    add_message(chat_id, "user", prompt)

    response = ask_onyx(chat_id, prompt)
    add_message(chat_id, "assistant", response)

    # Guardar como draft activo
    title = f"Post LinkedIn {datetime.now().strftime('%Y-%m-%d')}"
    save_draft(chat_id, response, title, "linkedin")

    await update.message.reply_text(response)
    await update.message.reply_text(
        "💾 Si el draft te gusta, respondé /save para guardarlo en Drive y Notion."
    )


async def cmd_substack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = " ".join(context.args) if context.args else ""
    prompt = f"Generá un artículo de Substack. {args}" if args else "Generá el artículo de Substack sobre P1 (AP Reconciliation App)."

    await update.message.reply_text("⏳ Generando artículo...")
    add_message(chat_id, "user", prompt)

    response = ask_onyx(chat_id, prompt)
    add_message(chat_id, "assistant", response)

    title = f"Artículo Substack {datetime.now().strftime('%Y-%m-%d')}"
    save_draft(chat_id, response, title, "substack")

    # Telegram tiene límite de 4096 chars por mensaje
    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)

    await update.message.reply_text(
        "💾 Si el artículo te gusta, respondé /save para guardarlo."
    )


async def cmd_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    prompt = "Mostrá las tareas de la semana actual del roadmap de 16 semanas. Hoy es " + datetime.now().strftime("%d/%m/%Y") + ". Formatealo de forma clara para Telegram."

    await update.message.reply_text("⏳ Buscando tareas...")
    add_message(chat_id, "user", prompt)

    response = ask_onyx(chat_id, prompt)
    add_message(chat_id, "assistant", response)

    await update.message.reply_text(response)


async def cmd_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    draft = get_draft(chat_id)

    if not draft:
        await update.message.reply_text("No hay ningún draft activo. Generá un post o artículo primero.")
        return

    await update.message.reply_text("💾 Guardando...")

    results = []

    # Google Drive
    drive_result = save_to_drive(draft["content"], draft["title"], draft["type"])
    results.append(f"📁 Drive: {drive_result}")

    # Notion
    if draft["type"] == "linkedin":
        notion_result = save_linkedin_post(draft["title"], draft["content"])
    else:
        notion_result = save_substack_article(draft["title"], draft["content"])
    results.append(f"📋 Notion: {notion_result}")

    await update.message.reply_text("\n".join(results))


async def cmd_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    clear_history(chat_id)
    await update.message.reply_text(
        "🔄 Conversación reiniciada. ¿En qué trabajamos?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Modo conversacional — cualquier mensaje de texto libre."""
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Atajos para guardar sin usar /save
    if user_text.lower().strip() in ["guardar", "save", "guardá", "ok guardá", "sí guardá"]:
        await cmd_save(update, context)
        return

    await update.message.chat.send_action("typing")
    add_message(chat_id, "user", user_text)

    try:
        response = ask_onyx(chat_id, user_text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error al contactar Claude: {e}")
        return

    add_message(chat_id, "assistant", response)

    # Si la respuesta parece un draft (más de 200 chars), guardarlo automáticamente
    if len(response) > 200:
        title = f"Draft {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        draft_type = "substack" if any(w in user_text.lower() for w in ["substack", "artículo", "articulo"]) else "linkedin"
        save_draft(chat_id, response, title, draft_type)

    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)


# ─── Voice handler ────────────────────────────────────────────────────────────

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transcribe voice message with Whisper, then pass to Onyx as text."""
    chat_id = update.effective_chat.id
    await update.message.chat.send_action("typing")

    # Download OGG from Telegram
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        await voice_file.download_to_drive(tmp.name)
        tmp_path = tmp.name

    # Transcribe with Whisper
    if not openai_client:
        os.unlink(tmp_path)
        await update.message.reply_text("Transcripción de audio no disponible — configurá OPENAI_API_KEY para usarla.")
        return
    try:
        with open(tmp_path, "rb") as audio:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="es"
            )
        user_text = transcription.text.strip()
    except Exception as e:
        await update.message.reply_text(f"No pude transcribir el audio: {e}")
        return
    finally:
        os.unlink(tmp_path)

    if not user_text:
        await update.message.reply_text("No entendí el audio. ¿Podés repetirlo o escribirlo?")
        return

    # Show transcription so Lucía sabe qué entendió
    await update.message.reply_text(f"🎤 _{user_text}_", parse_mode="Markdown")

    # Process exactly like a text message
    add_message(chat_id, "user", user_text)
    try:
        response = ask_onyx(chat_id, user_text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error al contactar Claude: {e}")
        return
    add_message(chat_id, "assistant", response)

    if len(response) > 200:
        title = f"Draft {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        draft_type = "substack" if any(w in user_text.lower() for w in ["substack", "artículo", "articulo"]) else "linkedin"
        save_draft(chat_id, response, title, draft_type)

    if len(response) > 4000:
        for chunk in [response[i:i+4000] for i in range(0, len(response), 4000)]:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    init_db()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN no configurado")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", cmd_post))
    app.add_handler(CommandHandler("substack", cmd_substack))
    app.add_handler(CommandHandler("roadmap", cmd_roadmap))
    app.add_handler(CommandHandler("save", cmd_save))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("Onyx Bot iniciado")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
