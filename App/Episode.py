import Shot
from datetime import datetime, time
from enum import Enum
from dataclasses import dataclass

class Act(Enum): one, two, tree = 0, 1, 2

@dataclass()
class Episode:
    acts: dict[Act, list[Shot]] = {Act.one: [], Act.two: [], Act.tree: []}
    number: int = -1
    release_date: date = date.now()
    duration = time(0,0,0)

    def create_shot(self, clip_number: int, act: Act, length = None, characters = None, environments = None):
        shot = Shot(clip_number, act, length, characters, environments)
        shot.create()
        return shot

