import json
import os
from datetime import date, time
from App.Tests.test_setup import SetupBaseDirectory, SerializableTestClass, HEADER
from App.ShowManager.Serializable import FILE_DATA_BULLET, NON_SERIALIZABLE_PREFIX


class TestSerializableClass(SetupBaseDirectory):
    def setUp(self) -> None:
        super().setUp()
        # build a serializable test object and fill it with non-default values
        self.instance = SerializableTestClass()
        self.instance.i = 2
        self.instance.f = 2.0
        self.instance.s = "string_2"
        self.instance.d = date(2, 2, 2)
        self.instance.t = time(2, 2, 2)
        self.instance.li = [4, 5, 5]
        self.instance.se = {4, 5, 5}
        self.instance.di = {"4": 4, "5": 5, "6": 6}

        self.instance.set_folder(os.path.join(self.test_folder_path, "instance"))
        self.instance.create_folder()

        # Filter out any private field and save all fields in a self.data dictionary
        self.data = {data: value for data, value in self.instance.__dict__.items() if not data.startswith(NON_SERIALIZABLE_PREFIX)}

        # cast any unfriendly json type to a friendly json type
        cast_data = self.data.copy()
        cast_data["d"] = self.instance.d.isoformat()
        cast_data["t"] = self.instance.t.isoformat()
        cast_data["se"] = list(self.instance.se)

        # convert the friendly data to json string in self.json
        self.json = json.dumps(cast_data, indent=4)

        # save the ideal full file string in self.file
        self.file = f"{HEADER}{FILE_DATA_BULLET}{self.json}"

    def tearDown(self) -> None:
        self.instance.delete_folder()
        super().tearDown()

    def test_decode(self):
        test_obj = SerializableTestClass()
        test_obj.decode(self.json)

        result = True
        for key, value in test_obj.__dict__.items():
            if key.startswith(NON_SERIALIZABLE_PREFIX) or self.data[key] == value:
                continue
            result = False
        self.assertTrue(result, "Not all fields set by decode are equal to the fields in original instance")

    def test_unpack(self):
        self.assertEqual(SerializableTestClass.unpack(self.file), self.json, "method did not return a json string containing the objs data")

    def test_encode(self):
        result = self.instance.encode()
        self.assertEqual(result, self.json, "Encoded dictionary, is not equal to file json")

    def test_serialize_deserialize(self):
        path = self.instance._folder
        self.instance.serialize()
        self.assertTrue(self.instance.file_exists(), "Serialized file does not exist")

        with open(self.instance.get_file(), "r") as file:
            file_string = file.read()

        self.assertEqual(self.file, file_string, "file string is not equal to predictive file contents")
        test = SerializableTestClass.deserialize(path)
        self.assertDictEqual(self.instance.__dict__, test.__dict__, "Deserialized object is not identical to original instance")

    def test_create_folder(self):
        path = self.instance._folder
        new_path = os.path.join(path, "test")
        self.instance.set_folder(new_path)
        self.instance.create_folder()
        self.assertTrue(os.path.exists(self.instance._folder), "Make directory did not create a directory")
        self.instance.set_folder(path)

