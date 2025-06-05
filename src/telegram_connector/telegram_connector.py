from telegram import Bot
from loguru import logger
from src.Agent.Agent import Agent
import os
import asyncio

class TelegramNotifierAgent(Agent):
    """
    Tool que recibe una respuesta generada (texto) y la envía por Telegram.
    Compatible con LangGraph (modo async).
    """

    def __init__(self):
        super().__init__()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")

        self.bot = Bot(token=self.token)

    def invoke(self, input: dict) -> dict:
        """
        Espera un dict con la clave 'respuesta'. Enviará ese contenido por Telegram.
        Ejecuta el envío de manera asíncrona, compatible con notebooks o LangGraph sync.
        """
        mensaje = input.get("respuesta", "").strip()
        if not mensaje:
            return {"error": "No se proporcionó ningún mensaje para enviar por Telegram."}

        try:
            asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=mensaje))
            logger.info("Mensaje enviado por Telegram.")
            return {"status": "enviado"}
        except Exception as e:
            logger.error(f"Error enviando mensaje por Telegram: {e}")
            return {"error": str(e)}
