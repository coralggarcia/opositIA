from pathlib import Path
class Agent():
    def __init__(self):
        self.parent_dir = Path(__file__).resolve().parent.parent.parent  # En scripts