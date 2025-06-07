from telegram import Bot
from loguru import logger
from src.Agent.Agent import Agent
import os
import asyncio

class TelegramSendAnswerAgent(Agent):
    def __init__(self):
        super().__init__()

        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")

        self.bot = Bot(token=self.token)

    def invoke(self, input):
        mensaje = input.get("respuesta", "").strip()
        try:
            asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=mensaje))
            logger.info("Mensaje enviado por Telegram.")
        except Exception as e:
            logger.error(f"Error enviando mensaje por Telegram: {e}")

