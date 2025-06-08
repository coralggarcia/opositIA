
from src.scraper.scraper_agent import ScraperAgent
from src.extractor.extractor_agent import ExtractorAgent
from src.extractor.normalizer import NormalizerAgent
from loguru import logger

def main():
    logger.info("Inicializando ScrapperAgent...")
    #scraper = ScraperAgent()
    #scraper.scrape()
    logger.info("Scraping completado.")

    logger.info("Inicializando ExtractorAgent...")
    #extractor = ExtractorAgent()
    #extractor.extract()
    logger.info("Extracción completada.")

    logger.info("Inicializando NormalizerAgent...")
    #normalizer = NormalizerAgent()
    #normalizer.normalize_and_save()
    logger.info("Normalización completada.")

if __name__ == "__main__":
    main()