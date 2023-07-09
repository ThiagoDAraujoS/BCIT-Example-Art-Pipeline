import os
import shutil

from App.ShowManager.Serializable.FolderManager import FolderManager
from test_setup import SetupBaseDirectory


class TestFolderManager(SetupBaseDirectory):
    def setUp(self) -> None:
        self.folder_name = "test"
        self.folder_path = os.path.join(self.test_folder_path, self.folder_name)
        self.instance = FolderManager()

    def tearDown(self) -> None:
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)

    def test_get_folder(self):
        self.instance._folder = self.folder_path
        self.assertEqual(self.instance.get_folder(), self.folder_path)

    def test_set_folder(self):
        self.instance.set_folder(self.folder_path)
        self.assertEqual(self.instance._folder, self.folder_path)

    def test_create_exists_delete_folder(self):
        self.instance._folder = self.folder_path
        self.instance.create_folder()
        self.assertTrue(os.path.exists(self.folder_path))
        self.assertTrue(self.instance.folder_exists())
        self.instance.delete_folder()
        self.assertFalse(os.path.exists(self.folder_path))

