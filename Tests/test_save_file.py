import os

from test_setup import TestSetup
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from ShowSafari.save_file import SaveFile
from ShowSafari.folder import Folder


@dataclass_json
@dataclass
class TestData:
    data: int = 0


class TestSaveFile(TestSetup):
    def setUp(self) -> None:
        test_file_name = "test"
        self.folder = Folder(self.main_folder_path, "SaveFileTest")

        self.data = TestData()
        self.save_file = SaveFile(self.folder, self.data, test_file_name)

    def tearDown(self) -> None:
        self.folder.delete()

    def test_save(self):
        self.data.data = 30
        self.save_file.save()

        with open(self.save_file._file_path, 'r') as file:
            data_string = file.read()
        loaded_data = self.data.from_json(data_string)

        self.assertEqual(loaded_data.data, self.data.data, "Saved data does not match object data")

    def test_load(self):
        new_data: dataclass_json = TestData()
        new_data.data = 100

        json_string = new_data.to_json()
        with open(self.save_file._file_path, 'w') as file:
            file.write(json_string)

        self.save_file.load()
        self.assertEqual(self.data.data, new_data.data, "Loaded data does not match object data")

    def test_exists(self):
        self.assertTrue(self.save_file.exists(), "save_file_exists returns False even though the file exists")
        os.remove(self.save_file._file_path)
        self.assertFalse(self.save_file.exists(), "save_file_exists returns True even though the file does not exists")
