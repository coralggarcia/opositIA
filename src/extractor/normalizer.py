import re
from openai import OpenAI
import pandas as pd
import sqlite3
from dotenv import load_dotenv

import os
from loguru import logger
from src.Agent.Agent import Agent
from src.utils.regex_utils import extraer_referencia, extraer_via, extraer_titulo, extraer_plazas, extraer_fecha_fin, extraer_fecha_apertura


class NormalizerAgent(Agent):
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
    def create_output_dir(self):
        """
        Crea el directorio de salida si no existe.
        """
        self.outputs_dir.mkdir(parents=True, exist_ok=True)


    def get_files_to_process(self):
        log_path = os.path.join(self.log_dir, "execution_log.txt")

        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        return lines

    def get_openai_client(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        self.open_ai_client = client


    def get_text_block(self, text):
        texto = text.split('PROCESOS  CONVOCADOS  EN LA ÚLTIMA  SEMANA')[2].replace('Referencia : ', 'Referencia: ')
        pattern = r"(.*?Referencia:\s+\d+)"
        bloques = re.findall(pattern, texto, re.DOTALL)
        diccionario = {}
        for i, bloque in enumerate(bloques, 1):
            diccionario[i] = {'texto_original': bloque}
        return diccionario

    def get_information_regex(self, diccionario):
        for key, value in diccionario.items():
            texto = value['texto_original']
            diccionario[key] = value | {
                "título": extraer_titulo(texto),
                "vía": extraer_via(texto),
                "plazas_convocadas": extraer_plazas(texto)[0],
                "plazas_libres": extraer_plazas(texto)[1],
                "fecha_apertura": extraer_fecha_apertura(texto),
                "fecha_fin": extraer_fecha_fin(texto),
                "referencia": extraer_referencia(texto),
            }
        return diccionario
    def call_llm(self, texto):
        system_prompt = "Necesito que extraigas la información de estos textos." \
                        "-Los campos obligatorios que hay que extraer son:" \
                        "  * titulo: aquí tiene que venir el título de la oposición. Por ejemplo: MÉDICO, INGENIERO NAVAL, ENFERMEROS" \
                        "  * organismo_que_convoca: por ejemplo: AYUNTAMIENTO DE MADRID" \
                        "  * titulacion_requerida" \
                        "  * via" \
                        "  * plazas_convocadas" \
                        "  * plazas_libres" \
                        "  * otras_plazas: aquí, devuelve la suma de todas las plazas que no sean plazas libres o convocadas" \
                        "  * fecha_de_publicacion" \
                        "  * fecha_de_cierre" \
                        "  * referencia" \
                        "-Si alguno de estos campos no aparece en el texto, devuelve 'no aplica' para ese campo." \
                        "-Devuelve todo en minúscula." \
                        "-Devuelve todo como string"\
                        "-Devuelve los campos marcados como fecha con este formato: 2025-06-05" \
                        "-Limpia texto mal formateado. Hazlo con todos los casos en los que tenga más sentido si hay que eliminar algún espacio. Por ejemplo, si aparece la palabra 'auxilia r' o 'no investigado r', conviértelo en 'auxiliar' y 'no investigador'"  \
                        ""

        response = self.open_ai_client.chat.completions.create(model="gpt-4.1-nano",
                                                  messages=[{"role": "system", "content": system_prompt},
                                                            {"role": "user", "content": texto},
                                                            ])
        try:
            result = eval(response.choices[0].message.content)
            print(result)
        except Exception as e:
            print(e)
            return [None]*10
        try:
            result = (result['titulo'], result['organismo_que_convoca'], result['titulacion_requerida'], result['via'],
                     result['plazas_convocadas'], result['plazas_libres'], result['otras_plazas'],
                     result['fecha_de_publicacion'],
                     result['fecha_de_cierre'], result['referencia'])
        except Exception as e:
            print(e)
            return [None] * 10
        return result

    def get_information_llm(self, diccionario):
        self.get_openai_client()
        df = pd.DataFrame(diccionario).T
        campos = ['titulo', 'organismo_que_convoca',
                    'titulacion_requerida', 'via',
                    'plazas_convocadas', 'plazas_libres',
                    'otras_plazas', 'fecha_de_publicacion',
                    'fecha_de_cierre', 'referencia']
        df[campos] = df["texto_original"].apply(lambda x: pd.Series(self.call_llm(x)))
        return df

    def save_in_sql(self, df):
        conn = sqlite3.connect(f"{self.outputs_dir}/oposiciones.db")
        df.to_sql("oposiciones", conn, if_exists="append", index=False)
        conn.close()

    def invoke(self, input):
        if input.get("respuesta").startswith("Sin ficheros"):
            return input
        else:
            files_to_process = self.get_files_to_process()
            result = pd.DataFrame({})
            for file in files_to_process:
                logger.info(f"Leyendo el contenido del texto {file}")
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()
                diccionario = self.get_text_block(text)
                df = self.get_information_llm(diccionario)
                result = pd.concat([result, df])
            self.save_in_sql(result)
            input["respuesta"]=f"Se ha almacenado con éxito el nuevo boletín, correspondiente a los ficheros: {files_to_process}"
            return input




