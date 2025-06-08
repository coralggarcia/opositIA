from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.prompts import PromptTemplate
from pathlib import Path
import os
from loguru import logger
from src.Agent.Agent import Agent


class DatabaseConsultantAgent(Agent):
    """
    Clase convertir el texto en una base de datos que pueda ser consultada. Hereda de Agent.
    """
    def __init__(self):
        """
        Inicializa el agente con la URL de la fuente y el directorio de salida.
        """
        super().__init__()
        self.outputs_dir = self.parent_dir / "data" / "outputs"
        self.prompt_text = """You are an expert SQL assistant for a **SQLite database que contiene información oficial sobre oposiciones públicas**.

                                The database has one main table called `oposiciones` with exactly these columns (use them verbatim, case-sensitive):
                                
                                - titulo
                                - organismo_que_convoca
                                - titulacion_requerida
                                - via
                                - plazas_convocadas
                                - plazas_libres
                                - otras_plazas
                                - fecha_de_publicacion
                                - fecha_de_cierre
                                - referencia
                                
                                Your task is to transform a question written in natural Spanish into a syntactically correct SQLite query that retrieves data relevant to the question, and return the answer.
                                
                                ---
                                
                                ### Important rules
                                
                                1. **Plazas vigentes (obligatorio)**
                                   Every query must include a filter to return only current/open positions:
                                   fecha_de_cierre >= DATE('now')
                                2. **Fuzzy matching**
                                If the user uses synonyms or general terms (e.g. "investigador"), match loosely:
                                LOWER(titulo) LIKE '%investigador%'
                                OR LOWER(titulo) LIKE '%investigacion%'
                                3. **Retrieve all results (no LIMIT)**
                                Return the full result set. Do not use LIMIT unless the user explicitly asks for it.
                                
                                4. **No SELECT ***
                                Only query the specific columns needed to answer the question.
                                
                                5. **Output format (una línea por sección)**
                                Question: <pregunta original>
                                SQLQuery: <consulta SQL generada>
                                SQLResult: <resultado de la consulta>
                                Answer: <respuesta final explicativa>
                                6. **Use only columns listed**. Qualify names if needed. Dialect is SQLite (fechas en formato 'YYYY-MM-DD').
                                
                                Use only the following schema:
                                
                                {schema}
                                
                                ---
                                
                                Question: {query_str}
                                SQLQuery:"""
        self.custom_prompt = PromptTemplate(self.prompt_text)
        self.sql_database = self.get_database()
        self.llm = self.get_llm()
        self.query_engine = self.get_sql_query_engine(self.sql_database,
                                                      self.llm,
                                                      self.custom_prompt
                                                      )


    def get_database(self):
        db_path = Path(f"{self.outputs_dir}/oposiciones.db").resolve()
        sql_database = SQLDatabase.from_uri(f"sqlite:///{db_path.as_posix()}")
        return sql_database

    def get_llm(self):
        llm = OpenAI(model="o4-mini", temperature=0.1,
                     api_key=os.getenv("OPENAI_API_KEY"))
        return llm

    def get_custom_prompt(self):
        custom_prompt = self.custom_prompt
        return custom_prompt

    def get_sql_query_engine(self, sql_database, llm, custom_prompt):
        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database,
            llm=llm,
            text_to_sql_prompt=custom_prompt,
            synthesize_response=True,
            verbose=True
        )
        return query_engine

    def invoke(self, input):
        pregunta = input.get("query", "").strip()
        logger.info(f"Procesando consulta del usuario: {pregunta}")
        respuesta = self.query_engine.query(pregunta)

        return {
            "respuesta": str(respuesta.response),
            "sql": respuesta.metadata.get("sql_query", "No SQL captured")
        }



