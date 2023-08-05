import shutil

from test_setup import TestSetup
from ShowSafari.folder import Folder
import os


class TestFolder(TestSetup):
    def setUp(self) -> None:
        self.test_folder_name = "test_folder"
        self.test_folder_path = os.path.join(self.main_folder_path, self.test_folder_name)

        self.test_subfolder_name = "test_subfolder"
        self.test_subfolder_path = os.path.join(self.test_folder_path, self.test_subfolder_name)

        self.folder = Folder(self.main_folder_path, self.test_folder_name)
        self.folder.setup_subfolder("test_subfolder")

        # folders can only be packed if they have something inside of them
        with open(f"{self.test_subfolder_path}\\test", 'w') as file: pass

    def tearDown(self) -> None:
        if self.folder.exists():
            self.folder.delete()

    def test_path(self):
        folder_path = os.path.join(self.main_folder_path, self.test_folder_name)
        self.assertEqual(self.folder.path, folder_path, "Path does not return the folder path")

    def test_setup(self):
        new_folder_name = "new_folder"
        new_folder = Folder(self.main_folder_path, new_folder_name)
        path = os.path.join(self.main_folder_path, new_folder_name)
        self.assertTrue(os.path.exists(path), "Folder was not created after setup")
        self.assertEqual(new_folder.path, path, "Folder path has not been updated properly on setup")

    def test_delete(self):
        self.folder.delete()
        self.assertFalse(os.path.exists(self.test_folder_path), "Folder has not been deleted")

    def test_exists(self):
        self.assertTrue(self.folder.exists(), "Exists returns False even though folder exists")
        shutil.rmtree(self.test_folder_path)
        self.assertFalse(self.folder.exists(), "Exists returns True even though folder does not exist")

    def test_setup_subfolder(self):
        new_subfolder_name = "new_folder"
        new_subfolder = self.folder.setup_subfolder(new_subfolder_name)
        path = os.path.join(self.folder.path, new_subfolder_name)

        self.assertTrue(os.path.exists(path), "Subfolder has not been created")
        self.assertIsNotNone(new_subfolder, "Setup subfolder has not returned the subfolder path")

    def test_get_absolute_path(self):
        path = self.folder.get_absolute_path(self.test_subfolder_name)
        self.assertEqual(path, self.test_subfolder_path, "Get Absolute has not returned the subfolder absolute path")

    def test_delete_subfolder(self):
        self.folder.delete_subfolder(self.test_subfolder_name)
        self.assertFalse(os.path.exists(self.test_subfolder_path), "After deletion subfolder still exists")

    def test_subfolder_exists(self):
        self.assertTrue(self.folder.subfolder_exists(self.test_subfolder_name),
                        "Exists returns False even though folder exists")
        shutil.rmtree(self.test_subfolder_path)
        self.assertFalse(self.folder.subfolder_exists(self.test_subfolder_name),
                         "Exists returns True even though folder does not exist")

    def test_archive_unpack_subfolder(self):
        self.folder.archive_subfolder(self.test_subfolder_name)
        self.assertTrue(os.path.exists(f"{self.test_subfolder_path}.zip"), "Missing .zip after archiving")
        self.assertFalse(os.path.exists(self.test_subfolder_path), "Subfolder still exists after archiving")

        self.folder.unpack_subfolder(self.test_subfolder_name)
        self.assertFalse(os.path.exists(f"{self.test_subfolder_path}.zip"), ".zip still exists after unpacking")
        self.assertTrue(os.path.exists(self.test_subfolder_path), "Missing Subfolder after unpacking")
