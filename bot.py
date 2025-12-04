#!/usr/bin/env python3
"""
🤖 МИНИМАЛЬНЫЙ РАБОЧИЙ БОТ БЕЗ Updater
"""

import os
import logging
from threading import Thread
from flask import Flask

# ========== НАСТРОЙКА ==========
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    print("❌ ОШИБКА: TELEGRAM_BOT_TOKEN не найден!")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== FLASK ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ========== TELEGRAM BOT ==========
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError as e:
    logger.error(f"❌ Ошибка импорта: {e}")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Используется Application API")

def main():
    logger.info("🚀 Запуск тестового бота...")
    
    # Запуск Flask
    Thread(target=run_flask, daemon=True).start()
    
    # Создание Application
    application = Application.builder().token(TOKEN).build()
    
    # Добавление команды
    application.add_handler(CommandHandler("start", start))
    
    logger.info("✅ Бот готов к работе")
    application.run_polling()

if __name__ == "__main__":
    main()
