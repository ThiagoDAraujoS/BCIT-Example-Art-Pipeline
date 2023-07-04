from .Serializable import serializable
from datetime import date, time
from .Episode import Episode

FILE_NAME: str = "show"
FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show information."""


@serializable(FILE_HEADER, FILE_NAME)
class Show:
    """ A class representing a show """
    def __init__(self):
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

        self._episodes: set[Episode] = set()

    def get_episode_count(self):
        """ Returns the number of episodes in the show """
        return len(self._episodes)
