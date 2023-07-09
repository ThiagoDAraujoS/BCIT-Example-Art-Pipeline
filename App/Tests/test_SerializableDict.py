import os

from App.ShowManager.Serializable.SerializableDict import SerializableDict
from App.ShowManager.Serializable.SerializableDecorator import serializable
from App.Tests.test_setup import SetupBaseDirectory

HEADER = "HEADER"


@serializable(HEADER)
class SerializableTest:
    def __init__(self):
        self.a = 5
        self.b = "name"


class TestSerializableDict(SetupBaseDirectory):
    def setUp(self):
        super().setUp()
        self.test_folder = os.path.join(self.test_folder_path, "serializableDict")
        self.instance: SerializableDict = SerializableDict(SerializableTest, self.test_folder)
        self.instance.create_folder()
        self.names = ["one", "two", "three"]
        for name in self.names:
            self.instance.create_element(name)

    def tearDown(self):
        self.instance.delete_folder()
        super().tearDown()

    def test_create_element(self):
        new_name = "new"
        self.instance.create_element(new_name)
        self.assertTrue(new_name in self.instance, "Created Element does not add its name to the SerializableDict")
        self.assertFalse(self.instance[new_name] is None, "Create element does not map newly created objects to their names")

    def test_delete(self):
        folder = self.instance[self.names[0]].get_folder()
        self.instance.delete(self.names[0])
        self.assertTrue(self.names[0] not in self.instance, "After deletion element still exists in dictionary")
        self.assertFalse(os.path.exists(folder), "Folder has not been deleted after element deletion")

    def test_load_from_folder(self):
        new_sdict: SerializableDict = SerializableDict(SerializableTest, self.instance.get_folder())
        new_sdict.load_from_folder()
        self.assertListEqual(sorted(new_sdict.keys()), sorted(self.instance.keys()), "After Test_Load_Folder, the dictionary has different keys")

    def test_get_names(self):
        names = self.instance.get_names()
        self.assertListEqual(names, self.names, "Print Names does not return an accurate element names")
