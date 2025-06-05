
from PyPDF2 import PdfReader
import os
from loguru import logger
from src.Agent.Agent import Agent


class ExtractorAgent(Agent):
    """
    Clase encargada de extraer y guardar el PDF de boletines de empleo público
    desde la web oficial. Hereda de Agent.
    """
    def __init__(self):
        """
        Inicializa el agente con la URL de la fuente y el directorio de salida.
        """
        super().__init__()
        self.raw_dir = self.parent_dir / "data" / "raw"
        self.processed_dir = self.parent_dir / "data" / "processed"
        self.log_dir = self.parent_dir / "data" / "log"

    def create_output_dir(self):
        """
        Crea el directorio de salida si no existe.
        """
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def get_files_to_process(self):
        self.create_output_dir()
        input_files = os.listdir(os.path.join(self.raw_dir, "boletines"))
        output_files = os.listdir(os.path.join(self.processed_dir, "boletines"))

        return {new_file+'.pdf': os.path.join(self.raw_dir, "boletines", new_file+'.pdf')
                for new_file
                in set([file.split('.')[0] for file in input_files])
                .difference(set([file.split('.')[0] for file in output_files]))}

    def extract(self):
        files_to_process = self.get_files_to_process()
        output_files = []
        for file_name, file_path in files_to_process.items():
            logger.info(f"Leyendo el contenido del pdf {file_name}")
            reader = PdfReader(file_path)
            result = []
            for page in reader.pages:
                text = page.extract_text()
                result = result + [text]
            result = ''.join(result)
            file_name = file_name.replace('pdf', 'txt')
            with open(os.path.join(self.processed_dir, "boletines", file_name), 'w', encoding='utf-8') as f:
                f.write(result)
                output_files.append(os.path.join(self.processed_dir, "boletines", file_name))
            logger.info(f'Almacenando texto en {os.path.join(self.processed_dir, "boletines", file_name)}')
        with open(os.path.join(self.log_dir, "execution_log.txt"), 'w', encoding='utf-8') as f:
            f.write("\n".join(output_files))

