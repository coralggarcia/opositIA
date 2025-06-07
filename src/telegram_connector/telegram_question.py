from telegram import Bot
from loguru import logger
from src.Agent.Agent import Agent
import os
import time

class TelegramGetQuestionAgent(Agent):
    """
    Tool que espera un mensaje del usuario por Telegram y lo devuelve como 'query'.
    Compatible con LangGraph.
    """

    def __init__(self):
        super().__init__()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token:
            raise ValueError("Falta TELEGRAM_BOT_TOKEN en .env")

        self.bot = Bot(token=self.token)
        self.last_update_id = None

    def get_latest_message(self):
        updates = self.bot.get_updates(offset=self.last_update_id, timeout=10)
        for update in updates:
            if update.message and update.message.text:
                self.last_update_id = update.update_id + 1
                return update.message.text
        return None

    def invoke(self, input):
        """
        Espera un nuevo mensaje de Telegram. Devuelve {'query': <texto>}.
        Bloquea hasta que se recibe algo.
        """
        logger.info("Esperando pregunta del usuario por Telegram...")
        while True:
            msg = self.get_latest_message()
            if msg:
                logger.info(f"Mensaje recibido: {msg}")
                input["query"]=msg
                return input
            time.sleep(1)
