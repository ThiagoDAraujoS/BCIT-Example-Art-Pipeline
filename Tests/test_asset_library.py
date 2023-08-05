from datetime import time

from dataclasses_json import Undefined

from ShowSafari import TypeString, JsonString
from ShowSafari.asset_library import AssetLibrary
from ShowSafari.data import Asset
from test_setup import TestSetup
import os


class TestAssetLibrary(TestSetup):
    def setUp(self) -> None:
        self.test_folder_name = "test_library"
        self.library = AssetLibrary(self.main_folder_path)

        self.file = self.library._save_file
        self.folder = self.library._folder
        self.data = self.library._assets

        self.a_asset_name = "test_asset_a"
        self.a_asset_type = TypeString("Shot")
        self.a_asset_uuid = self.library.create(self.a_asset_name, self.a_asset_type)

        self.b_asset_name = "test_asset_b"
        self.b_asset_type = TypeString("Test")
        self.b_asset_uuid = self.library.create(self.b_asset_name, self.b_asset_type)

    def tearDown(self) -> None:
        self.library._folder.delete()

    def test_create_remove(self):
        asset_name = "test_asset1"
        asset_type = TypeString("Music")
        uuid = self.library.create(asset_name, asset_type)
        self.assertIn(uuid, self.data.data, "Asset has not been added to library")
        self.assertEqual(self.library[uuid].name, asset_name, "New asset entry does not match user defined name")
        self.assertEqual(self.library[uuid]._asset_type, asset_type, "New asset entry does match user defined type")
        self.assertTrue(self.folder.subfolder_exists(uuid), "Asset creation did not setup a new asset folder")

    def test_remove(self):
        self.library.remove(self.a_asset_uuid)
        self.assertNotIn(self.a_asset_uuid, self.data.data, "After remove asset has not been removed from library")
        self.assertFalse(self.folder.subfolder_exists(self.a_asset_uuid), "After remove asset folder still exists")

    def test_archive_unpack(self):
        folder_path = self.folder.get_absolute_path(self.a_asset_uuid)
        with open(f"{folder_path}\\test", 'w'): pass
        file_path = f"{folder_path}.zip"

        self.library.archive(self.a_asset_uuid)

        self.assertTrue(self.library[self.a_asset_uuid].archived, "Archived asset has its 'archived' flag set to False")
        self.assertTrue(os.path.exists(file_path), "After archiving .zip file hasn't been created")
        self.assertFalse(os.path.exists(folder_path), "After archiving asset folder hasn't been removed")

        self.library.unpack(self.a_asset_uuid)

        self.assertFalse(self.library[self.a_asset_uuid].archived, "Unpacking did not set asset's 'archived' to False")
        self.assertFalse(os.path.exists(file_path), "After unpacking .zip hasn't been removed")
        self.assertTrue(os.path.exists(folder_path), "After unpacking asset folder hasn't been restated")

    def test_connect_disconnect(self):
        self.library.connect(self.a_asset_uuid, self.b_asset_uuid)
        self.assertIn(self.b_asset_uuid, self.library[self.a_asset_uuid].assets_used,
                      "After connect, parent asset did not include child asset to its assets_used set")
        self.assertIn(self.a_asset_uuid, self.library[self.b_asset_uuid].asset_used_by,
                      "After connect, child asset did not include parent asset to its asset_used_by set")

        self.library.disconnect(self.a_asset_uuid, self.b_asset_uuid)
        self.assertNotIn(self.b_asset_uuid, self.library[self.a_asset_uuid].assets_used,
                         "After disconnect, parent asset did not remove child asset to its assets_used set")
        self.assertNotIn(self.a_asset_uuid, self.library[self.b_asset_uuid].asset_used_by,
                         "After disconnect, child asset did not remove parent asset to its asset_used_by set")

    def test_set_data(self):
        self.library.set_data(self.a_asset_uuid, JsonString('{"name": "renamed"}'))
        self.assertEqual("renamed", self.library[self.a_asset_uuid].name,
                         "After set_data data has not been updated correctly")

    def test_get_data(self):
        new_data = {
            "clip_number": 20,
            "length": time(10, 10, 10),
            "characters": {"Bob", "John"},
            "environments": {"Mountains"}
        }
        for key, value in new_data.items():
            setattr(self.library[self.a_asset_uuid], key, value)

        new_data = self.library[self.a_asset_uuid].to_json()
        get_data = self.library.get_data(self.a_asset_uuid)
        self.assertEqual(new_data, get_data, "Get Data has not returned asset data correctly")

    def test_get_by_name(self):
        uuid_set = self.library.get_by_name("test_asset_a")
        self.assertEqual(uuid_set, {self.a_asset_uuid},
                         "Get by name has not accurately returned the set of named items")

    def test_get_types(self):
        set_of_types = self.library.get_types()
        self.assertSetEqual(set_of_types, {"Shot", "Test"},
                            "Get types has not accurately returned the set of assets types")

    def test_get_all_assets(self):
        assets = self.library.get_all_assets()
        self.assertSetEqual(assets, {self.a_asset_uuid, self.b_asset_uuid},
                            "Get all assets has not returned all assets ids")

    def test_get_all_assets_of_type(self):
        test_assets = self.library.get_all_assets_of_type(TypeString("Test"))
        self.assertSetEqual(test_assets, {self.b_asset_uuid},
                            "Get types has not accurately returned the set of assets of same type")
