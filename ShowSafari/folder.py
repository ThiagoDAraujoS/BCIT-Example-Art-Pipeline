import os
import platform
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

    def open_folder_in_explorer(self, subfolder: str = ""):
        """ Open the specified folder or subfolder in the default file explorer.

            This method opens the specified folder or subfolder in the default file explorer of the user's operating system.
            The method automatically detects the operating system and uses the appropriate command to open the folder.

        Args:
            subfolder (str, optional): The name of the subfolder to be opened within the main folder.
                                       If not provided or empty, the main folder will be opened.
                                       The default is an empty string.

        Note:
            The `self.path` attribute should be set to the path of the main folder to be opened.

        Returns:
            bool: True if the folder or subfolder was opened successfully, False otherwise.

        Examples:
            # Assuming the main folder path is '/path/to/my_folder/'
            # Open the main folder
            if open_folder_in_explorer():
                print("Folder opened successfully.")
            else:
                print("Failed to open folder.")

            # Open a subfolder named 'images' within the main folder
            if open_folder_in_explorer("images"):
                print("Subfolder 'images' opened successfully.")
            else:
                print("Failed to open subfolder 'images'.")

            # Open a subfolder named 'documents' within the main folder
            if open_folder_in_explorer("documents"):
                print("Subfolder 'documents' opened successfully.")
            else:
                print("Failed to open subfolder 'documents'.")
        """
        subfolder = self.path if not subfolder else self.get_subfolder_path(subfolder)
        if not os.path.exists(subfolder):
            return False

        system = platform.system()
        if system == "Windows":
            os.startfile(subfolder)
        elif system == "Darwin":
            os.system(f"open {subfolder}")
        else:
            os.system(f"xdg-open {subfolder}")
        return True

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

    def delete_subfolder(self, subfolder_name: str):
        """ Delete a subfolder within the main folder.

            This method deletes the specified subfolder within the main folder and all its contents.
            If the subfolder doesn't exist, the method does nothing.

        Args:
            subfolder_name (str): The name of the subfolder to be deleted.

        Examples:
            # Assuming the main folder path is '/path/to/my_folder/'
            # Delete a subfolder named 'images' within the main folder
            delete_subfolder("images")

            # Try to delete a non-existent subfolder named 'docs'
            delete_subfolder("docs")
        """
        subfolder_path = self.get_subfolder_path(subfolder_name)
        if not self.subfolder_exists(subfolder_path):
            shutil.rmtree(subfolder_path)

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
