from __future__ import annotations
from os import path
import os
from Show import Show


class Manager:
    """ The Manager class handles the management of shows and their associated files """
    def __init__(self):
        self.shows: list[Show] = []
        self.main_folder: str = ""

    def install(self, folder_path: str) -> None:
        """ Sets the main folder path for tracking shows files

        Parameters:
            folder_path (str): The path to the main folder.
        """
        if self.main_folder:
            # TODO Warn the user theres a main folder being tracked before moving it
            pass

        normalized_folder_path = path.normpath(folder_path)
        if not os.path.exists(normalized_folder_path):
            # TODO Warn the user the new foder is inexistent
            pass

        self.main_folder = normalized_folder_path
        self.load()

    def load_shows(self) -> None:
        """ Loads shows by scanning the main folder and deserializing their metafiles

        This method populates the `shows` list with instances of the Show class
        by searching for folders within the main folder and checking for the existence
        of metafiles associated with each folder. If a metafile is found, it is deserialized
        to retrieve the show's information.
        """
        self.shows = []
        for folder in os.listdir(self.main_folder):
            if path.isfile(folder):
                continue

            show_metafile = path.join(folder, Show.FILE_NAME)
            if not path.exists(show_metafile):
                continue
            show = Show.deserialize(show_metafile)          # TODO Maybe I need to try deserialize and treat errors that if the metafile is broken
            self.shows.append(show)

    def create_show(self, name: str) -> Show:
        """ Creates a new show with the given name

        This method creates a new instance of the Show class, sets its name
        attribute to the specified name, and returns the created show object.

        Parameters:
            name (str): The name of the new show.

        Returns:
            Show: The newly created show object.
        """
        pass

    def print_shows(self) -> list(str):
        pass


if __name__ == '__main__':
    FOLDER =  path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')

    manager = Manager()
    manager.install(FOLDER)
    manager.load(FOLDER)



