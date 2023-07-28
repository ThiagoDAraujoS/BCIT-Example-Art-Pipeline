from __future__ import annotations

from ShowSafari import *

import os.path
from typing import Dict


class Instance:
    def __init__(self, main_folder_path: str):
        self.main_folder_path: str = os.path.normpath(main_folder_path)
        """ Main folder path """

        self.show_folder: Folder = Folder(self.main_folder_path, "Shows")
        """ Show folder representation """

        self.show_folder.create()
        self.shows: Dict[str, Show] = {}
        """ Dictionary of Shows """

        self.show_file = SaveFile(self.show_folder, self.shows, "Shows")
        """ Save file for show dictionary """

        self.asset_library: Library = Library(self.main_folder_path)
        """ Asset library reference """

        self.save_shows = self.show_file.save
        self.load_shows = self.show_file.load

    def create_show(self, show_name: str) -> bool:
        if show_name in self.shows:
            return False
        self.shows[show_name] = Show()
        self.show_folder.create_subfolder(show_name)
        self.save_shows()
        return True

    def delete_show(self, show_name: str) -> bool:
        if show_name not in self.shows:
            return False
        self.show_folder.delete_subfolder(show_name)
        self.shows.pop(show_name)
        self.save_shows()
        return True

    def get_show_folder(self, show_name) -> str | None:
        if show_name not in self.shows:
            return None
        return self.show_folder.get_subfolder_path(show_name)


