from datetime import time
from .Serializable.SerializableDecorator import serializable

FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized shot information."""


@serializable(FILE_HEADER)
class Shot:
    def __init__(self):
        self.clip_number: int
        self.length: time
        self.characters: set[str] = set()
        self.environments: set[str] = set()
