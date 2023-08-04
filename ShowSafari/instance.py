from __future__ import annotations

from .save_file import SaveFile, autosave
from .folder import Folder
from .data import Show
from .asset_library import AssetLibrary

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined
import os.path
from typing import Dict

DEBUG = True


@dataclass_json
@dataclass
class ShowsData:
    data: Dict[str, Show] = field(default_factory=dict)


class Instance:
    def __init__(self, main_folder_path: str):
        self._main_folder_path: str = os.path.normpath(main_folder_path)
        """ Main folder path """

        self._show_folder: Folder = Folder(self._main_folder_path, "Shows")
        """ Show folder representation """

        self._shows: ShowsData = ShowsData()
        """ Dictionary of Shows """

        self._show_file: SaveFile = SaveFile(self._show_folder, self._shows, "Shows")
        """ Save file for show dictionary """

        self.library: AssetLibrary = AssetLibrary(self._main_folder_path)
        """ Asset library reference """

        self.get_show = self._shows.data.get
        self._show_file.load()

    @autosave("_show_file")
    def create_show(self, show_name: str):
        if show_name in self._shows.data:
            if DEBUG:
                return
            else:
                raise KeyError(f"Show {show_name} already presented in shows collection")

        self._shows.data[show_name] = Show()
        self._show_folder.setup_subfolder(show_name)

    @autosave("_show_file")
    def delete_show(self, show_name: str):
        if show_name not in self._shows.data:
            if DEBUG:
                return
            else:
                raise KeyError(f"Show {show_name} not presented in shows collection")

        self._show_folder.delete_subfolder(show_name)
        self._shows.data.pop(show_name)

    @autosave("_show_file")
    def set_show_data(self, show_name: str, show_json: str):
        self._shows.data[show_name].from_json(show_json, undefine=Undefined.EXCLUDE)

    @autosave("_show_file")
    def create_shot(self, show_name, shot_name) -> str:
        uuid = self.library.create(shot_name, "Shot")
        self._shows.data[show_name].shots.append(uuid)
        return uuid

    def get_show_data(self, show_name: str) -> str:
        return self._shows.data[show_name].to_json()

    def get_show_folder(self, show_name) -> str | None:
        if show_name not in self._shows.data:
            if DEBUG:
                raise KeyError(f"Show {show_name} not presented in shows collection")
            else:
                return None
        return self._show_folder.get_subfolder_path(show_name)
