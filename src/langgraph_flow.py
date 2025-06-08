from langgraph.graph import StateGraph, END, START
from src.scraper.scraper_agent import ScraperAgent
from src.extractor.extractor_agent import ExtractorAgent
from src.extractor.normalizer import NormalizerAgent
from src.database_consultant.database_consultant_agent import DatabaseConsultantAgent
from src.telegram_connector.telegram_question import TelegramGetQuestionAgent
from src.telegram_connector.telegram_answer import TelegramSendAnswerAgent
from src.reasoner.reasoner import ReeasonerAgent
from typing import TypedDict
import time


class GlobalState(TypedDict):
    query: str
    respuesta: str


receptor = TelegramGetQuestionAgent()
reasoner = ReeasonerAgent()
scraper = ScraperAgent()
extractor = ExtractorAgent()
normalizer = NormalizerAgent()
consultor = DatabaseConsultantAgent()
emisor = TelegramSendAnswerAgent()


builder = StateGraph(GlobalState)


def router(input):
    pregunta = input.get("query").strip().upper()
    if pregunta == "ACTUALIZAR":
        return "scraper"
    else:
        return "reasoner"



builder.add_node("receptor", receptor.invoke)
builder.add_node("reasoner", reasoner.invoke)
builder.add_node("router", router)
builder.add_node("scraper",    scraper.invoke)
builder.add_node("extractor",  extractor.invoke)
builder.add_node("normalizer", normalizer.invoke)
builder.add_node("consultor",  consultor.invoke)
builder.add_node("emisor",   emisor.invoke)


builder.set_entry_point("receptor")


# Condicional
builder.add_conditional_edges("receptor",
                              router)

# Flujo ACTUALIZACION DE LA BASE DE DATOS
builder.add_edge("scraper", "extractor")
builder.add_edge("extractor", "normalizer")
builder.add_edge("normalizer", "emisor")
builder.add_edge("emisor", END)


# Flujo CONSULTA USUARIO
builder.add_edge("reasoner", "consultor")
builder.add_edge("consultor", "emisor")
builder.add_edge("emisor", END)


flow = builder.compile()

while True:
    output = flow.invoke({})
    print("Consulta resuelta:", output.get("respuesta"))
    time.sleep(1)