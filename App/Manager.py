from __future__ import annotations
from os import path
import os
from Show import Show
from typing import Callable

class Manager:
    """ The Manager class handles the management of shows and their associated files """
    def __init__(self):
        self.shows: dict[str, Show] = {}
        self.main_folder: str = ""

    def install(self, folder_path: str, on_overwrite_callback: Callable[[str], None] | None = None, on_folder_exists_callback: Callable[[str], None] | None = None) -> None:
        """ Sets the main folder path for tracking show files

        This method sets the main folder path to the specified `folder_path`
        for tracking show files. Optionally, you can provide callbacks to be
        executed in certain scenarios, such as when inadvertently overwriting
        a previous installation or when the new folder already exists.

        Parameters:
            folder_path (str): The path to the main folder.

            on_overwrite_callback (Optional[Callable[[str], None]]):
                A callback function to be executed when inadvertently
                overwriting a previous installation. The callback function
                should take a single argument, which is the path of the
                existing main folder. Defaults to None.

            on_folder_exists_callback (Optional[Callable[[str], None]]):
                A callback function to be executed when the folder already
                exists. The callback function should take a single argument,
                which is the path of the new folder that already exists.
                Defaults to None. """
        if self.main_folder and on_overwrite_callback:
            on_overwrite_callback(self.main_folder)
            return

        normalized_folder_path = path.normpath(folder_path)
        if not os.path.exists(normalized_folder_path) and on_folder_exists_callback:
            on_folder_exists_callback(normalized_folder_path)
            return

        self.main_folder = normalized_folder_path
        os.mkdir(self.main_folder)

    def load_shows(self) -> None:
        """ Loads shows by scanning the main folder and deserializing their metafiles

        This method populates the `shows` list with instances of the Show class
        by searching for folders within the main folder and checking for the existence
        of metafiles associated with each folder. If a metafile is found, it is deserialized
        to retrieve the show's information. """
        self.shows = []
        for folder in os.listdir(self.main_folder):
            if path.isfile(folder):
                continue

            show_metafile = path.join(folder, Show.FILE_NAME)
            if not path.exists(show_metafile):
                continue
            show = Show.deserialize(show_metafile)
            # TODO Maybe I need to try deserialize and treat errors that if the metafile is broken
            self.shows[show.name] = show

    def create_show(self, name: str) -> Show | None:
        """ Creates a new show with the given name

        This method creates a new instance of the Show class, sets its name
        attribute to the specified name, and returns the created show object.

        Parameters:
            name (str): The name of the new show.

        Returns:
            Show: The newly created show object.
        """
        show_folder = path.normpath(path.join(self.main_folder, name))
        if path.exists(show_folder):
            # TODO Warn the user this show already exists
            return

        os.mkdir(show_folder)
        new_show:Show = Show(show_folder)
        new_show.name = name
        new_show.serialize()

    def print_shows(self) -> list[str]:
        """ Print the list of archived shows and return their name as a list """
        show_list = list(self.shows.keys())
        print(*show_list)
        return show_list


if __name__ == '__main__':
    FOLDER = path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')
    manager = Manager()
    manager.install(FOLDER)
    manager.create_show("Super Raptors")



