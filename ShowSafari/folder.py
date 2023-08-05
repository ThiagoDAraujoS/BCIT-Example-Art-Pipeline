from . import PathString, EmptyFolderError

import os
import platform
import shutil


class Folder:
    def __init__(self, location_path: PathString, folder_name: str):
        """ Initializes a Folder object representing a directory on the file system.
        Then create the folder if it needs to be created.

        Parameters:
            location_path (str): The parent directory where the folder will be created.
            folder_name (str): The name of the folder to be created.
        """
        self._name: str = folder_name
        """_name (str): The folder name"""

        self._path: PathString = PathString(os.path.join(location_path, folder_name))
        """_path (str): The path to the folder."""

        self.setup()

    @property
    def path(self) -> PathString:
        """ Get the full path to the folder.

        Returns:
            str: The full path to the folder.
        """
        return self._path

    @path.setter
    def path(self, folder_path: PathString) -> None:
        """ Set the full path to the folder.

        Parameters:
            folder_path (str): The new full path to the folder.
        """
        self._path: str = os.path.normpath(folder_path)

    def setup(self) -> PathString | None:
        """ Create the folder if it does not exist.

        Returns:
            bool: True if the folder was created, False if it already existed.
        """
        if self.exists():
            return None
        os.mkdir(self._path)
        return self._path

    def delete(self) -> None:
        """ Delete the folder and all its contents. """
        shutil.rmtree(self._path)

    def open_folder_in_explorer(self, subfolder: str = "") -> None:
        """ Open the folder (or subfolder) in the file explorer.

        Parameters:
            subfolder (str, optional): The name of the subfolder to open. Defaults to the main folder.
        """
        subfolder = self.path if not subfolder else self.get_absolute_path(subfolder)

        system = platform.system()
        if system == "Windows":
            os.startfile(subfolder)
        elif system == "Darwin":
            os.system(f"open {subfolder}")
        else:
            os.system(f"xdg-open {subfolder}")

    def exists(self) -> bool:
        """ Check if the folder exists.

        Returns:
            bool: True if the folder exists, False otherwise.
        """
        return os.path.exists(self._path)

    def setup_subfolder(self, subfolder_name: str) -> PathString | None:
        """ Create a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder to create.

        Returns:
            bool: True if the subfolder was created, False if it already existed.
        """
        if self.subfolder_exists(subfolder_name):
            return None
        path = self.get_absolute_path(subfolder_name)
        os.mkdir(path)
        return path

    def get_absolute_path(self, subfolder_name: str) -> PathString:
        """ Get the full path to a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder.

        Returns:
            str: The full path to the subfolder.
        """
        return PathString(os.path.join(self.path, subfolder_name))

    def delete_subfolder(self, subfolder_name: str) -> None:
        """ Delete a subfolder within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder to delete.
        """
        subfolder_path = self.get_absolute_path(subfolder_name)
        shutil.rmtree(subfolder_path)

    def subfolder_exists(self, subfolder_name: str) -> bool:
        """ Check if a subfolder exists within the main folder.

        Parameters:
            subfolder_name (str): The name of the subfolder.

        Returns:
            bool: True if the subfolder exists, False otherwise.
        """
        subfolder_path = self.get_absolute_path(subfolder_name)
        return os.path.exists(subfolder_path)

    def archive_subfolder(self, subfolder_name: str) -> PathString:
        """ Archive a subfolder within the main folder into a ZIP file.

        Parameters:
            subfolder_name (str): The name of the subfolder to be archived.

        Raises:
            FileNotFoundError: If the specified subfolder doesn't exist.
            FileExistsError: If an archive file with the same name as the subfolder already exists.

        Notes:
            - The method creates a ZIP archive of the subfolder contents with the same name as the subfolder.
            - The original subfolder will be removed after archiving.

        Returns:
            PathString or None: The path to the created archive file.
        """
        path = self.get_absolute_path(subfolder_name)
        archive_name = f"{subfolder_name}.zip"

        if os.path.exists(self.get_absolute_path(archive_name)):
            raise FileNotFoundError(f"Archive file '{archive_name}' already exists and cannot be archived again.")

        if not self.subfolder_exists(subfolder_name):
            raise FileExistsError(f"Subfolder '{subfolder_name}' does not exist.")

        if not os.listdir(path):
            raise EmptyFolderError(f"Error archiving {subfolder_name}, Cannot archive an empty folder.")

        shutil.make_archive(path, 'zip', path)
        shutil.rmtree(path)
        return PathString(archive_name)

    def unpack_subfolder(self, archive_name: str) -> str:
        """ Unpack an archived subfolder.

            This method extracts the contents of an archived subfolder, making it available for use.
            The subfolder must have been previously archived using the `archive_subfolder` method.

        Parameters:
            archive_name (str): The name of the archived subfolder to be unpacked.

        Returns:
            str: The name of the unpacked subfolder.

        Example usage:
            library = YourClassName("/path/to/asset/library")
            unpacked_subfolder = library.unpack_subfolder("my_archived_subfolder")

        Raises:
            FileNotFoundError: If the archive .zip file is not found.
            FileExistsError: If the subfolder to be unpacked already exists.

        Note:
            After unpacking, the subfolder's contents become accessible again and the archive will be deleted.
        """
        if not archive_name.endswith(".zip"):
            archive_name += ".zip"

        archive_path = self.get_absolute_path(archive_name)

        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive .zip file '{archive_name}' not found.")

        subfolder_name = os.path.splitext(archive_name)[0]
        subfolder_path = os.path.splitext(archive_path)[0]

        if os.path.exists(subfolder_path):
            raise FileExistsError(f"Subfolder '{subfolder_name}' already exists and cannot be unpacked again.")

        shutil.unpack_archive(archive_path, subfolder_path, 'zip')
        os.remove(archive_path)
        return subfolder_name

    def __repr__(self) -> PathString:
        return self.path

    def __str__(self) -> str:
        return f"Folder path: {self.path}"
