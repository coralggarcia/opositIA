# OpositIA

OpositIA es un sistema modular e inteligente para la recolección, análisis y publicación diaria de convocatorias de oposiciones en España. Combina scraping, procesamiento de lenguaje natural (NLP) y generación de informes visuales. Diseñado con LangGraph y GPT-4o, ofrece un flujo flexible y eficiente para mantenerte siempre actualizado.

---

## ¿Qué hace OpositIA?

- Recolecta y descarga boletines oficiales de oposiciones (solo Gobierno de España, sin comunidades autónomas, por ahora).  
- Extrae y estructura los datos clave: plazas, fechas límite, requisitos y perfiles ideales.  
- Clasifica los perfiles más adecuados para cada convocatoria usando heurísticas y modelos de IA.  
- Genera un informe diario con todas las novedades.  
- Publica automáticamente en Instagram bajo el perfil OpositIA.

---

## Arquitectura general

- **ScraperAgent:** Descarga boletines (PDF/HTML) de fuentes oficiales.  
- **ExtractorAgent:** Limpia y convierte el contenido a texto estructurado.  
- **NormalizerAgent:** Homogeneiza fechas y campos clave.  
- **ProfileMatcherAgent:** Identifica perfiles recomendados (usando GPT-4o cuando es necesario).  
- **ReportGeneratorAgent:** Crea el informe diario en formato visual (Markdown, HTML o imagen).  
- **InstagramPosterAgent:** Publica el resumen en Instagram vía Meta Graph API.  
- **Orquestación:** LangGraph coordina todo el flujo con bifurcaciones dinámicas (OCR, errores, etc.).

---

## Tecnologías clave

- **Python:** Lenguaje principal.  
- **LangGraph:** Orquestación modular de agentes.  
- **Pandas, BeautifulSoup, pdfplumber, pytesseract:** Extracción y procesamiento de datos.  
- **OpenAI GPT-4o API:** Clasificación semántica de perfiles (opcional, según complejidad del texto).  
- **Pillow / Canva API:** Creación de imágenes para Instagram.  
- **Meta Graph API:** Publicación automática en Instagram.

---

## Instalación y uso

Proyecto en fase de desarrollo y aprendizaje, no apto todavía para producción.

```bash
# 1️⃣ Clona el repositorio
git clone https://github.com/tu-usuario/OpositIA.git
cd OpositIA

# 2️⃣ Crea entorno virtual
python -m venv .venv
source .venv/bin/activate

# 3️⃣ Instala dependencias principales
pip install -r requirements.txt

# 4️⃣ Configura variables de entorno (API keys, rutas de scraping)
cp .env.example .env
# Edita .env con tus credenciales de OpenAI e Instagram (Meta Graph API)

# 5️⃣ Ejecuta el flujo principal (ejemplo)
python main.py
