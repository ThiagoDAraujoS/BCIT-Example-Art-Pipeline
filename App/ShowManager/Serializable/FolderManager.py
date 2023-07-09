import os
import shutil
from os import path


class FolderManager:
    """
    This class represents an object that manages a folder

    Attributes:
        _folder (str): The path to the managed folder.

    Methods:
        get_folder(): Get the path of the managed folder.
        set_folder(folder_path): Set the path of the managed folder.
        create_folder(): Create the managed folder.
        delete_folder(): Delete the managed folder.
        folder_exists(): Check if the managed folder exists.
    """

    def __init__(self, folder_path: str = ""):
        """Initialize a FolderManager object."""
        if not self._folder:
            self._folder = folder_path

    def get_folder(self):
        """Get the path of the managed folder."""
        return self._folder

    def set_folder(self, folder_path):
        """Set the path of the managed folder."""
        self._folder = path.normpath(folder_path)

    def create_folder(self):
        """Create the managed folder."""

        os.mkdir(self._folder)

    def delete_folder(self):
        """Delete the managed folder."""
        if self.folder_exists():
            shutil.rmtree(self._folder)

    def folder_exists(self):
        """Check if the managed folder exists."""
        return path.exists(self._folder)
