from __future__ import annotations

from .save_file import SaveFile
from .folder import Folder
from .data import Show
from .library import Library

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined
import os.path
from typing import Dict


@dataclass_json
@dataclass
class ShowsData:
    data: Dict[str, Show] = field(default_factory=dict)


class Instance:
    def __init__(self, main_folder_path: str):
        self.main_folder_path: str = os.path.normpath(main_folder_path)
        """ Main folder path """

        self.show_folder: Folder = Folder(self.main_folder_path, "Shows")
        """ Show folder representation """

        self.show_folder.create()
        self.shows: ShowsData = ShowsData()
        """ Dictionary of Shows """

        self.show_file: SaveFile = SaveFile(self.show_folder, self.shows, "Shows")
        """ Save file for show dictionary """

        self.library: Library = Library(self.main_folder_path)
        """ Asset library reference """

        self.save_shows = self.show_file.save
        self.load_shows = self.show_file.load

    def create_show(self, show_name: str) -> bool:
        if show_name in self.shows.data:
            return False
        self.shows.data[show_name] = Show()
        self.show_folder.create_subfolder(show_name)
        self.save_shows()
        return True

    def delete_show(self, show_name: str) -> bool:
        if show_name not in self.shows.data:
            return False
        self.show_folder.delete_subfolder(show_name)
        self.shows.data.pop(show_name)
        self.save_shows()
        return True

    def set_show_data(self, show_name: str, show_json: str):
        self.shows.data[show_name].from_json(show_json, undefine=Undefined.EXCLUDE)

    def get_show_data(self, show_name: str) -> str:
        return self.shows.data[show_name].to_json()

    def create_shot(self, show_name, shot_name):
        uuid = self.library.create(shot_name, "Shot")
        self.shows.data[show_name].shots.append(uuid)

    def get_asset_data(self, asset_id):
        return self.library.get(asset_id).to_json()

    def set_asset_data(self, asset_id: str, asset_json: str):
        self.library.get(asset_id).from_json(asset_json, undefine=Undefined.EXCLUDE)

    def get_show_folder(self, show_name) -> str | None:
        if show_name not in self.shows.data:
            return None
        return self.show_folder.get_subfolder_path(show_name)
