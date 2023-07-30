import os
import platform
import shutil


class Folder:
    def __init__(self, location_path: str, folder_name: str):
        """
        Initializes a Folder object representing a directory on the file system.
        Then create the folder if it needs to be created.

        Parameters:
            location_path (str): The parent directory where the folder will be created.
            folder_name (str): The name of the folder to be created.
        """
        self._name: str = folder_name
        """_name (str): The folder name"""

        self._path: str = os.path.join(location_path, folder_name)
        """_path (str): The path to the folder."""

        self.setup()

    @property
    def path(self) -> str:
        """
        Get the full path to the folder.

        Returns:
            str: The full path to the folder.
        """
        return self._path

    @path.setter
    def path(self, folder_path: str):
        """
        Set the full path to the folder.

        Parameters:
            folder_path (str): The new full path to the folder.
        """
        self._path: str = os.path.normpath(folder_path)

    def setup(self) -> bool:
        """
        Create the folder if it does not exist.

        Returns:
            bool: True if the folder was created, False if it already existed.
        """
        if self.exists():
            return False
        os.mkdir(self._path)
        return True

    def delete(self):
        """
        Delete the folder and all its contents.
        """
        shutil.rmtree(self._path)

    def open_folder_in_explorer(self, subfolder: str = ""):
        """
        Open the folder (or subfolder) in the file explorer.

        Parameters:
            subfolder (str, optional): The name of the subfolder to open. Defaults to the main folder.
        """
        subfolder = self.path if not subfolder else self.get_subfolder_path(subfolder)

        system = platform.system()
        if system == "Windows":
            os.startfile(subfolder)
        elif system == "Darwin":
            os.system(f"open {subfolder}")
        else:
            os.system(f"xdg-open {subfolder}")

    def exists(self) -> bool:
        """
        Check if the folder exists.

        Returns:
            bool: True if the folder exists, False otherwise.
        """
        return os.path.exists(self._path)

    def setup_subfolder(self, subfolder_name: str):
        """
        Create a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder to create.

        Returns:
            bool: True if the subfolder was created, False if it already existed.
        """
        if self.subfolder_exists(subfolder_name):
            return False
        os.mkdir(self.get_subfolder_path(subfolder_name))
        return True

    def get_subfolder_path(self, subfolder_name: str) -> str:
        """
        Get the full path to a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder.

        Returns:
            str: The full path to the subfolder.
        """
        return os.path.join(self.path, subfolder_name)

    def delete_subfolder(self, subfolder_name: str):
        """
        Delete a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder to delete.
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        shutil.rmtree(subfolder_path)

    def subfolder_exists(self, subfolder_name: str) -> bool:
        """
        Check if a subfolder exists within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder.

        Returns:
            bool: True if the subfolder exists, False otherwise.
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        return os.path.exists(subfolder_path)

    def __repr__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return f"Folder path: {self.path}"
