import os
import platform
import shutil


class Folder:
    def __init__(self, folder_path: str):
        """
        Initialize a Folder instance.

        Args:
            folder_path (str): The path to the folder.
        """
        self._path: str = os.path.normpath(folder_path)
        self.create()

    @property
    def path(self) -> str:
        """
        Get the path of the folder.

        Returns:
            str: The folder path.
        """
        return self._path

    @path.setter
    def path(self, folder_path: str):
        """
        Set the path of the folder.

        Args:
            folder_path (str): The new folder path.
        """
        self._path: str = os.path.normpath(folder_path)

    def create(self) -> bool:
        """
        Create the folder if it does not exist.

        Returns:
            bool: True if the folder was created, False if it already exists.
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
        Open the folder (or a subfolder) in the file explorer.

        Args:
            subfolder (str, optional): The name of the subfolder to open. Defaults to "".
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

    def create_subfolder(self, subfolder_name: str):
        """
        Create a subfolder inside the main folder.

        Args:
            subfolder_name (str): The name of the subfolder to create.
        """
        os.mkdir(self.get_subfolder_path(subfolder_name))

    def get_subfolder_path(self, subfolder_name: str) -> str:
        """
        Get the path of a subfolder inside the main folder.

        Args:
            subfolder_name (str): The name of the subfolder.

        Returns:
            str: The path of the subfolder.
        """
        return os.path.join(self.path, subfolder_name)

    def delete_subfolder(self, subfolder_name: str):
        """
        Delete a subfolder inside the main folder and all its contents.

        Args:
            subfolder_name (str): The name of the subfolder to delete.
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        shutil.rmtree(subfolder_path)

    def subfolder_exists(self, subfolder_name: str) -> bool:
        """
        Check if a subfolder exists inside the main folder.

        Args:
            subfolder_name (str): The name of the subfolder.

        Returns:
            bool: True if the subfolder exists, False otherwise.
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        return os.path.exists(subfolder_path)

    def __repr__(self) -> str:
        """
        Get the string representation of the Folder object.

        Returns:
            str: The folder path.
        """
        return self.path

    def __str__(self) -> str:
        """
        Get the string representation of the Folder object.

        Returns:
            str: The folder path.
        """
        return f"Folder path: {self.path}"
