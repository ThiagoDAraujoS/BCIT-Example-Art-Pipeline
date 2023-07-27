import os
import shutil


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
        self._path: str = os.path.normpath(folder_path)
        self.create()

    @property
    def path(self) -> str:
        """ Get the path of the folder.

        Returns:
            str: The normalized path of the folder.
        """
        return self._path

    @path.setter
    def path(self, folder_path: str):
        """ Set the path of the folder.

        Args:
            folder_path (str): The new path of the folder.
        """
        self._path: str = os.path.normpath(folder_path)

    def create(self):
        """ Creates the folder if it doesn't exist. """
        if not self.exists():
            os.mkdir(self._path)

    def delete(self):
        """ Deletes the folder and all its contents if it exists. """
        if self.exists():
            shutil.rmtree(self._path)

    def exists(self) -> bool:
        """ Checks if the folder exists.

        Returns:
            bool: True if the folder exists, False otherwise.
        """
        return os.path.exists(self._path)

    def create_subfolder(self, subfolder_name: str):
        """ Creates a subfolder within the current folder.

        Args:
            subfolder_name (str): The name of the subfolder to create.
        """
        os.mkdir(self.get_subfolder_path(subfolder_name))

    def get_subfolder_path(self, subfolder_name: str) -> str:
        """ Returns the path of a subfolder within the current folder.

        Args:
            subfolder_name (str): The name of the subfolder.

        Returns:
            str: The normalized path of the subfolder.
        """
        return os.path.join(self.path, subfolder_name)

    def subfolder_exists(self, subfolder_name: str) -> bool:
        """ Checks if a subfolder exists within the current folder.

        Args:
            subfolder_name (str): The name of the subfolder to check.

        Returns:
            bool: True if the subfolder exists, False otherwise.
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        return os.path.exists(subfolder_path)

    def __repr__(self) -> str:
        """ Returns the string representation of the Folder object.

        Returns:
            str: The folder's path.
        """
        return self.path

    def __str__(self) -> str:
        """ Returns a user-friendly string representation of the Folder object.

        Returns:
            str: A formatted string indicating the folder's path.
        """
        return f"Folder path: {self.path}"
