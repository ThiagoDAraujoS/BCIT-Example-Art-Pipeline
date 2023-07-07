import os
import shutil
from App.ShowManager.SerializableDict import SerializableDict
from App.Tests.test_setup import SetupBaseDirectory, SerializableTestClass


class TestSerializableDict(SetupBaseDirectory):
    def setUp(self):
        super().setUp()
        self.case_folder = os.path.join(self.test_folder_path, "SerializableDictTest")
        os.mkdir(self.case_folder)

        self.names = ["one", "two", "three"]
        self.count = len(self.names)
        self.sdict: SerializableDict = SerializableDict(SerializableTestClass, self.case_folder)

        for name in self.names:
            self.sdict.create_element(name)

    def tearDown(self):
        super().tearDown()
        if os.path.exists(self.case_folder):
            shutil.rmtree(self.case_folder)

    def test_create_element(self):
        new_name = "new"
        self.sdict.create_element(new_name)
        self.assertTrue(new_name in self.sdict, "Created Element does not add its name to the SerializableDict")
        self.assertFalse(self.sdict[new_name] is None, "Create element does not map newly created objects to their names")

    def test_load_folder(self):
        new_sdict: SerializableDict = SerializableDict(SerializableTestClass)
        new_sdict.load_folder(self.case_folder)
        self.assertListEqual(sorted(new_sdict.keys()), sorted(self.sdict.keys()), "After Test_Load_Folder, the dictionary has different keys")

    def test_print_names(self):
        names = self.sdict.get_element_names()
        self.assertListEqual(names, self.names, "Print Names does not return an accurate element names")

    def test_get_element_count(self):
        count = self.sdict.get_element_count()
        self.assertEqual(self.count, count, "Get Element Count does not return an accurate element count")
