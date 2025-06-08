from pathlib import Path
from dotenv import load_dotenv
class Agent():
    def __init__(self):
        self.parent_dir = Path(__file__).resolve().parent.parent.parent
        load_dotenv()
