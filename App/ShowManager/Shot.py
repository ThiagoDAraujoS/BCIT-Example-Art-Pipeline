from datetime import datetime, time
from dataclasses import dataclass
from .Serializable import serializable


@serializable
class Shot:
    def __init__(self):
        self.folder: str = ""
        self.meta_file: str = ""
        self.clip_number: int
        self.length: time
        self.characters: set[str] = set()
        self.environments: set[str] = set()

    def load(self, file):
        pass

    def save(self, file):
        pass
