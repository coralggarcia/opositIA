from bs4 import BeautifulSoup
import os
from loguru import logger
from src.Agent.Agent import Agent
import requests

class ScraperAgent(Agent):
    """
    Clase encargada de extraer y guardar el PDF de boletines de empleo público
    desde la web oficial. Hereda de Agent.
    """
    def __init__(self):
        """
        Inicializa el agente con la URL de la fuente y el directorio de salida.
        """
        super().__init__()
        self.url_source = "https://administracion.gob.es/pag_Home/empleoPublico/boletin.html"
        self.output_dir = self.parent_dir / "data" / "raw"

    def create_output_dir(self):
        """
        Crea el directorio de salida si no existe.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scrape(self):
        """
        Extrae el enlace al PDF desde la página, descarga el PDF
        y lo guarda en el directorio de salida.
        """
        logger.info("Extrayendo el boletín actualizado")

        # Cabeceras para simular un navegador real y evitar bloqueos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }

        # Realiza la petición GET para obtener el HTML de la página
        response = requests.get(self.url_source, headers=headers)

        if response.status_code == 200:
            # Parsear el HTML con BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_link = soup.find("a", href=lambda x: x and x.endswith(".pdf"))
            if pdf_link:
                pdf_url = f"{pdf_link['href']}"
                pdf_response = requests.get(pdf_url, headers=headers)
                output_path = os.path.join(self.output_dir, "boletines", pdf_link['href'].split('/')[-1])
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(pdf_response.content)
                logger.info(f"PDF guardado: \n {output_path}")
            else:
                logger.error("No se encontró enlace al PDF.")
        else:
            logger.error("Error al acceder a la página:", response.status_code)