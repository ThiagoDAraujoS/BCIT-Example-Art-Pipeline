import json
import os
from datetime import date, time
from App.ShowManager.Serializable import serializable

from App.Tests.test import SetupBaseDirectory

HEADER = "HEADER"
FILE = "test"


@serializable(HEADER, FILE)
class TestSubject:
    def __init__(self):
        self.i: int = 1
        self.f: float = 1.0
        self.s: str = "string"
        self.d: date = date(1, 1, 1)
        self.t: time = time(1, 1, 1)
        self.li: list = [1, 2, 3]
        self.se: set = {1, 2, 3}
        self.di: dict = {"1": 1, "2": 2, "3": 3}


class TestSerializableClass(SetupBaseDirectory):
    json = ""
    data = {}
    instance = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = TestSubject()
        cls.instance.set_folder_path(cls.test_folder_path)
        data = {}
        for key, value in cls.instance.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, (date, time)):
                value = value.isoformat()
            if isinstance(value, set):
                value = list(value)
            data[key] = value
        cls.json = json.dumps(data, indent=4)
        cls.file = f"{HEADER}\nDATA>>>\n{cls.json}"
        cls.data = cls.instance.__dict__

    def test_decode(self):
        data = self.instance.decode(self.file)
        result = True
        for key, value in data.items():
            if self.data[key] == value:
                continue
            result = False
        self.assertTrue(result, "Not all fields returned by decode are equal to the fields in original instance")

    def test_encode(self):
        result = self.instance.encode()
        self.assertEqual(result, self.json, "Encoded dictionary, is not equal to file json")

    def test_serialize_deserialize(self):
        path = self.instance._folder_path
        self.instance.serialize()
        self.assertTrue(self.instance.has_serialized_file(), "Serialized file does not exist")
        test = TestSubject.deserialize(path)
        self.assertDictEqual(self.instance.__dict__, test.__dict__, "Deserialized object is not identical to original instance")

    def test_make_directory(self):
        path = self.instance._folder_path
        new_path = os.path.join(path, "test")
        self.instance.set_folder_path(new_path)
        self.instance.make_directory()
        self.assertTrue(os.path.exists(self.instance._folder_path), "Make directory did not create a directory")
        self.instance.set_folder_path(path)

