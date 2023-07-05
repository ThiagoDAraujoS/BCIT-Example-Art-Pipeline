from __future__ import annotations

from .Serializable import serializable
from datetime import date, time
from .Shot import Shot
from .SerializableDict import SerializableDict

FILE_NAME: str = "show"
FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show information."""


@serializable(FILE_HEADER, FILE_NAME)
class Show(SerializableDict):
    """ A class representing a show """
    def __init__(self):
        super().__init__(Shot)

        self.name: str = ""
        self.rating: int = 0
        self.popularity_score: int = 0
        self.type: str = "tv_series"
        self.cast: set[str] = set()
        self.third_party_services: set[str] = set()
        self.description: str = ""
        self.certification: dict[str, str] = {}
        self.release: date = date(1, 1, 1)
        self.countries_of_origin: set[str] = set()


