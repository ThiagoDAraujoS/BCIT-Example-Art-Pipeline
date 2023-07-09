import json
import os
from datetime import date, time

from App.ShowManager.Serializable.Serializable import Serializable, FILE_DATA_BULLET, BuildExitCode
from App.Tests.test_setup import SetupBaseDirectory

HEADER = "HEADER"
FILE = "test"


class SerializableTest(Serializable):
    def __init__(self, folder, file_name, header):
        super().__init__(folder, file_name, header)
        self.a = 5
        self.b = "name"


class TestSerializable(SetupBaseDirectory):
    def setUp(self) -> None:
        super().setUp()
        self.folder_path = os.path.join(self.test_folder_path, "manager")
        self.file_path = os.path.join(self.folder_path, f"{FILE}.meta")
        self.instance = SerializableTest(self.folder_path, FILE, HEADER)

        self.data = SerializableTest(self.folder_path, FILE, HEADER)
        self.data.a = 10
        self.data.b = "name2"

        self.json = json.dumps({"a": 10, "b": "name2"}, indent=4)
        self.file = f"{HEADER}{FILE_DATA_BULLET}{self.json}"

    def tearDown(self) -> None:
        self.instance.delete_folder()
        super().tearDown()

    def test_build_success(self):
        self.assertEqual(self.instance.build(), BuildExitCode.SUCCESS, "Result from a successful installation was not 0")
        self.assertEqual(self.instance.get_folder(), self.folder_path, "The folder required was not the same as targeted by the installation")
        self.assertTrue(self.instance.folder_exists(), "The installation folder does not exists")
        self.assertTrue(self.instance.file_exists(), "The manager's meta file does not exist")

    def test_build_overwrite(self):
        self.instance.build()
        self.assertEqual(self.instance.build(), BuildExitCode.PROJECT_OVERRIDE, "Return code not 1 when installation met an overwrite case")

    def test_build_collision(self):
        os.mkdir(self.folder_path)
        self.assertEqual(self.instance.build(), BuildExitCode.FOLDER_COLLISION, "Return code not 1 when installation met an overwrite case")

    def test_build_path_broken(self):
        self.instance.set_folder("ERROR_1234567890_ERROR/ERROR_1234567890_ERROR")
        self.assertEqual(self.instance.build(), BuildExitCode.PATH_BROKEN, "Returned code on install/path broken is not equal to InstallExitCode.PATH_BROKEN")

    def test_serialize_deserialize(self):
        self.instance.build()
        self.instance.a = self.data.a
        self.instance.b = self.data.b

        self.instance.serialize()
        self.assertTrue(self.instance.file_exists(), "Serialized file does not exist")

        with open(self.instance.get_file(), "r") as file:
            file_string = file.read()

        self.assertEqual(self.file, file_string, "file string is not equal to predictive file contents")
        test = SerializableTest(self.folder_path, FILE, HEADER)
        test.deserialize()
        self.assertDictEqual(self.instance.__dict__, test.__dict__, "Deserialized object is not identical to original instance")

    def test_incorporate_file_data(self):
        self.instance.incorporate_file_data(self.json)
        self.assertDictEqual(self.instance.__dict__, self.data.__dict__, "Deserialized object is not identical to original instance")

    def test_compose_file_data(self):
        json_string = self.data.compose_file_data()
        self.assertEqual(json_string, self.file)

    def test_get_file(self):
        self.instance.build()
        self.instance.serialize()
        self.assertEqual(self.instance.get_file(), self.file_path)

    def test_file_exists_built(self):
        self.assertFalse(self.instance.file_exists())
        self.assertFalse(self.instance.is_built())
        self.instance.build()
        self.assertTrue(self.instance.is_built())
        self.assertTrue(self.instance.file_exists())
