from datetime import datetime, time
from dataclasses import dataclass

@dataclass()
class Shot:
    folder: str = ""
    meta_file: str = ""
    clip_number: int
    length: time
    characters: characters = []
    environments: environments = []

    def load(self, file):
        pass

    def save(self, file):
        pass
