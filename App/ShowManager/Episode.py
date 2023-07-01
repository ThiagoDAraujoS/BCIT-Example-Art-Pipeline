from .Shot import Shot
from datetime import time, date, timedelta
from .Serializable import serializable

ACT_ONE, ACT_TWO, ACT_THREE = 0, 1, 2

FILE_HEADER: str = "FILE CREATED BY: THIAGO dA. SILVA\nBCIT - British Columbia Institute of Technology\nTechnical Arts Advanced Course\n"


@serializable(FILE_HEADER)
class Episode:
    def __init__(self, number: int, release_date: date = date(1, 1, 1)):
        self._acts: list[set[Shot]] = [[], [], []]

        self.number: int = -1
        self.release_date: date = date.now()

    def duration(self) -> timedelta:
        """ Return the episode's total duration by summing its shots' lengths """
        total_duration = timedelta()

        for shot in self.get_shots_itr():
            duration = timedelta(
                hours=shot.length.hour,
                minutes=shot.length.minute,
                seconds=shot.length.seconds,
                milliseconds=shot.length.milliseconds)
            total_duration += duration
        return total_duration

    def create_shot(self, clip_number: int, act: int, length: time, characters: set = set(), environments: set = set()):
        """ Create a new shot and add it to an act collection """
        shot = Shot(clip_number, act, length, characters, environments)
        shot.create()
        return shot

    def get_shots_itr(self):
        """ Get an iterator that iterate through shots """
        for act in self._acts:
            yield from act
