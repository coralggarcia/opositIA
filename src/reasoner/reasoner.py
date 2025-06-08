import re
from openai import OpenAI
import pandas as pd
import sqlite3
from dotenv import load_dotenv

import os
from loguru import logger
from src.Agent.Agent import Agent
from src.utils.regex_utils import extraer_referencia, extraer_via, extraer_titulo, extraer_plazas, extraer_fecha_fin, extraer_fecha_apertura


class ReeasonerAgent(Agent):
    """
    Clase convertir el texto en una base de datos que pueda ser consultada. Hereda de Agent.
    """
    def __init__(self):
        """
        Inicializa el agente con la URL de la fuente y el directorio de salida.
        """
        super().__init__()
        self.processed_dir = self.parent_dir / "data" / "processed"
        self.outputs_dir = self.parent_dir / "data" / "outputs"
        self.raw_dir = self.parent_dir / "data" / "raw"
        self.log_dir = self.parent_dir / "data" / "log"
        self.open_ai_client = None



    def get_openai_client(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        self.open_ai_client = client




    def call_llm(self, texto):
        self.get_openai_client()
        system_prompt = f"""Eres un experto en análisis de lenguaje natural y en generación de consultas estructuradas.

                        Tu tarea es analizar una pregunta ambigua o incompleta formulada por un usuario humano y convertirla en una consulta más clara, completa y precisa, que pueda ser utilizada por otro modelo de lenguaje para transformarla en una consulta SQL bien formada.
                        
                        ---
                        
                        Instrucciones:
                        
                        1. Piensa paso a paso qué información está pidiendo el usuario.
                        2. Si hay ambigüedades (fechas, cargos, organismos...), acláralas en la reformulación usando términos más técnicos o explícitos.
                        3. Si te preguntan por número de plazas, plazas u oposiciones, interprétalo por defecto como plazas convocadas, ten en cuenta que hay tres tipos de plazas para cada convocatoria: plazas convocadas, plazas libres y otras plazas. Si no se indica explícitamente lo contrario, el usuario estará preguntando por las tres.
                        4. Cuando se hable de fechas, razona el intervalo de fechas al que se están refiriendo teniendo en cuenta la fecha actual. Devuelve el intervalo en formato AÑO-MES-DIA
                        5. No hagas la consulta SQL tú mismo. Solo reformula la pregunta.
                        6. No inventes datos que no estén implícitos en la pregunta.
                        7. Mantén la reformulación en un solo bloque de texto.
                        
                        ---
                        
                        Ejemplo:
                        
                        Pregunta original:  
                        "¿Hay algo para técnicos en junio?"
                        
                        Reformulación:  
                        "¿Qué oposiciones vigentes existen para perfiles técnicos (por ejemplo, técnicos superiores o medios) cuya fecha de cierre de convocatoria sea entre el 1 y el 31 del 06 del 2025?"
                        
                        ---
                        
                        Pregunta original: {texto}
                        
                        Reformulación:
                        """

        response = self.open_ai_client.chat.completions.create(model="gpt-4.1-nano",
                                                  messages=[{"role": "system", "content": system_prompt},
                                                            {"role": "user", "content": texto},
                                                            ])
        return response.choices[0].message.content



    def invoke(self, input):
        query_inicial = input.get("query")
        logger.info(f"La query inicial del usuario es: {query_inicial}")
        query_reformulada = self.call_llm(query_inicial)
        logger.info(f"La query reformulada que se le enviará al llm es: {query_reformulada}")
        input["query"]=query_reformulada
        return input




