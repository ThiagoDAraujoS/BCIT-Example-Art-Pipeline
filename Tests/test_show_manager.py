from unittest import TestCase

from ShowSafari import JsonString
from ShowSafari.asset_library import AssetLibrary
from ShowSafari.data import Show
from ShowSafari.show_manager import ShowManager
from test_setup import TestSetup
import os


class TestShowManager(TestSetup):
    def setUp(self) -> None:
        self.show_name = "test_show"
        self.shot_name = "shot_name"
        self.library = AssetLibrary(self.main_folder_path)
        self.manager = ShowManager(self.main_folder_path, self.library)
        self.folder = self.manager._folder
        self.manager.create_show(self.show_name)
        self.shot_id = self.manager.create_shot(self.show_name, self.shot_name)

    def tearDown(self) -> None:
        self.manager._folder.delete()
        self.library._folder.delete()

    def test_create_show(self):
        show_name = "create_test_show"
        self.manager.create_show(show_name)
        self.assertIn(show_name, self.manager._shows.data,
                      "After show creation, show has not been added to data_structure")
        self.assertTrue(os.path.exists(self.folder.get_absolute_path(show_name)),
                        "After show creation, a new folder for the show has not been generated")

    def test_delete_show(self):
        self.manager.delete_show(self.show_name)
        self.assertNotIn(self.show_name, self.manager._shows.data,
                         "After show deletion, show has not been removed to data_structure")
        self.assertFalse(os.path.exists(self.folder.get_absolute_path(self.show_name)),
                         "After show deletion, the show folder has not been removed")

    def test_set_show_data(self):
        self.manager.set_show_data(self.show_name, JsonString('{ "rating": 100, "description": "TEST TEST"}'))
        self.assertTrue(
            self.manager[self.show_name].rating == 100 and
            self.manager[self.show_name].description == "TEST TEST",
            "Data has not been set correctly after set")

    def test_create_shot(self):
        shot = self.manager.create_shot(self.show_name, "New_Show2")
        self.assertIn(shot, self.library._assets.data, "New shot has not been added to the library")
        self.assertIn(shot, self.manager[self.show_name].shots, "new shot has not been bound to the show")

    def test_get_show_data(self):
        new_description = "TEST TEST TEST"
        self.manager._shows.data[self.show_name].description = new_description
        data = self.manager.get_show_data(self.show_name)
        self.assertTrue(f'"description": "{new_description}"' in data, "Get show data does not return accurate data")

    def test_get_show_folder(self):
        manager_path = self.manager.get_show_folder(self.show_name)
        folder_path = self.folder.get_absolute_path(self.show_name)
        self.assertTrue(os.path.exists(manager_path), "")
        self.assertEqual(manager_path, folder_path, "Get show folder does not return the right folder")

    def test_get_show(self):
        show = self.manager[self.show_name]
        self.assertEqual(show, self.manager._shows.data[self.show_name], "Get show does not return the right object")
        self.assertIsInstance(show, Show, "Get show does not return a show")

    def test_get_show_names(self):
        show_names = self.manager.get_show_names()
        self.assertEqual({"test_show"}, show_names, "Get show names did not return an accurate set of shows names")

    def test_remove_add_shot(self):
        self.manager.remove_shot(self.show_name, self.shot_id)
        self.assertNotIn(self.shot_id, self.manager[self.show_name].shots,
                         "Asset has not been removed properly from show")
        self.manager.add_shot(self.show_name, self.shot_id)
        self.assertIn(self.shot_id, self.manager[self.show_name].shots,
                      "Asset has not been added properly from show")

    def test_delete_shot(self):
        self.manager.delete_shot(self.shot_id)
        self.assertNotIn(self.shot_id, self.manager[self.show_name].shots)
        self.assertNotIn(self.shot_id, self.library._assets.data)
