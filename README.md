# OpositIA

**OpositIA** es un sistema modular e inteligente para la **recolección, análisis y publicación diaria** de convocatorias de oposiciones en España. Automatiza todo el flujo, desde el scraping hasta la consulta en lenguaje natural, utilizando tecnologías avanzadas como **LangGraph** y **GPT-4o**.

---

## Estructura del proyecto

```text
src/
├── Agent/                     # Clase padre de agente
├── database_consultant/       # Consultas sobre la base de datos con llama-index y llms
├── extractor/                 # Extracción y normalización de información
├── reasoner/                  # Razonamiento para reformular la pregunta del usuario
├── scraper/                   # Scraping de portales oficiales
├── telegram_connector/        # Interacción a través de Telegram
├── utils/                     # Utilidades auxiliares
└── langgraph_flow.py          # Flujo principal definido con LangGraph
```

---

##  Características destacadas

-  Scraping automatizado de fuentes oficiales.
-  Procesamiento de lenguaje natural para normalizar y estructurar datos.
-  Agentes especializados en un flujo orquestado por LangGraph.
-  Consultas conversacionales sobre la base de datos.
-  Integración con Telegram para interacción directa.

---

##  Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/opositia.git
cd opositia
```

2. Crea un entorno virtual y actívalo:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución

Lanza el flujo principal:

```bash
python src/langgraph_flow.py
```
*IMPORTANTE: no se podrá ejecutar correctamente a no ser que esté configurado el fichero .env en la raíz del proyecto*
---

##  Interfaz por Telegram

- Para interactuar con el Opositia_bot es necesario configurar el fichero .env con TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID.
- TELEGRAM_BOT_TOKEN es única y privada, y será facilitada en la demo del proyecto
- TELEGRAM_CHAT_ID es el ID de una conversación de cualquier usuario con opositia_bot, y puede ser obtenida buscando *opositia* en el buscador de Telegram, iniciando una conversación con él, y luego obteniendo el chat_id

---

##  OpenAI

- Para poder ejecutar el paquete, es necesario tener un token para conectarse con OpenAI e incluirlo en un fichero .env con el nombre OPENAI_API_KEY

---

##  Agentes principales

| Módulo                   | Descripción                                               |
|--------------------------|-----------------------------------------------------------|
| `scraper_agent.py`       | Obtiene convocatorias desde sitios web oficiales.         |
| `extractor_agent.py`     | Extrae y estructura información relevante.                |
| `normalizer.py`          | Homogeneiza datos usando LLMs.                            |
| `reasoner.py`            | Aplica lógica para mejorar la consulta del usuario.       |
| `database_consultant.py` | Responde preguntas sobre la base de datos utilizando LLMs |
| `telegram_connector/`    | Gestiona la comunicación mediante Telegram.               |

---

##  Casos de uso

- Seguimiento actualizado de convocatorias de empleo público.
- Automatización de informes y alertas personalizadas.
- Consulta avanzada por fecha, categoría, ubicación o institución.

---

