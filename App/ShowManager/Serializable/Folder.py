import os
import shutil
from os import path


class Folder:
    """ Represents a folder on the file system.

    Attributes:
        _path (str): The normalized path of the folder.
    """

    def __init__(self, folder_path: str):
        """ Initializes a new Folder instance.

        Args:
            folder_path (str): The path of the folder.
        """
        self._path = path.normpath(folder_path)
        self.create()

    def get_path(self):
        """ Get the path of the folder.

        Returns:
            str: The normalized path of the folder.
        """
        return self._path

    def set_path(self, folder_path):
        """ Set the path of the folder.

        Args:
            folder_path (str): The new path of the folder.
        """
        self._path = path.normpath(folder_path)

    def create(self):
        """ Creates the folder if it doesn't exist. """
        if not self.exists():
            os.mkdir(self._path)

    def delete(self):
        """ Deletes the folder and all its contents if it exists. """
        if self.exists():
            shutil.rmtree(self._path)

    def exists(self):
        """ Checks if the folder exists.

        Returns:
            bool: True if the folder exists, False otherwise.
        """
        return path.exists(self._path)

    def __repr__(self):
        """ Returns the string representation of the Folder object.

        Returns:
            str: The folder's path.
        """
        return self._path

    def __str__(self):
        """ Returns a user-friendly string representation of the Folder object.

        Returns:
            str: A formatted string indicating the folder's path.
        """
        return f"Folder path: {self._path}"
