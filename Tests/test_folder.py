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
        self.assertEqual(self.folder.path, folder_path)

    def test_setup(self):
        new_folder_name = "new_folder"
        new_folder = Folder(self.main_folder_path, new_folder_name)
        path = os.path.join(self.main_folder_path, new_folder_name)
        self.assertTrue(os.path.exists(path))
        self.assertIsNotNone(new_folder)
        self.assertEqual(new_folder.path, path)

    def test_delete(self):
        self.folder.delete()
        self.assertFalse(os.path.exists(self.test_folder_path))

    def test_exists(self):
        self.assertTrue(self.folder.exists())
        shutil.rmtree(self.test_folder_path)
        self.assertFalse(self.folder.exists())

    def test_setup_subfolder(self):
        new_subfolder_name = "new_folder"
        new_subfolder = self.folder.setup_subfolder(new_subfolder_name)
        path = os.path.join(self.folder.path, new_subfolder_name)

        self.assertTrue(os.path.exists(path))
        self.assertIsNotNone(new_subfolder)

    def test_get_absolute_path(self):
        path = self.folder.get_absolute_path(self.test_subfolder_name)
        self.assertEqual(path, self.test_subfolder_path)

    def test_delete_subfolder(self):
        self.folder.delete_subfolder(self.test_subfolder_name)
        self.assertFalse(os.path.exists(self.test_subfolder_path))

    def test_subfolder_exists(self):
        self.assertTrue(self.folder.subfolder_exists(self.test_subfolder_name))
        shutil.rmtree(self.test_subfolder_path)
        self.assertFalse(self.folder.subfolder_exists(self.test_subfolder_name))

    def test_archive_unpack_subfolder(self):
        self.folder.archive_subfolder(self.test_subfolder_name)
        self.assertTrue(os.path.exists(f"{self.test_subfolder_path}.zip"))
        self.assertFalse(os.path.exists(self.test_subfolder_path))
        self.folder.unpack_subfolder(self.test_subfolder_name)
        self.assertFalse(os.path.exists(f"{self.test_subfolder_path}.zip"))
        self.assertTrue(os.path.exists(self.test_subfolder_path))
