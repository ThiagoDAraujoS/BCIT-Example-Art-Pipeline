from unittest import TestCase
import os
import shutil
from App.ShowManager.Manager import Manager


class TestManager(TestCase):
    COMPANY_NAME: str = "COMPANY"
    """ Constant with generic test company name """

    test_folder_path: str = ""
    """ The folder path containing the test folder """

    test_company_path: str = ""
    """ The folder path containing the company folder """

    @classmethod
    def setUpClass(cls) -> None:
        parent_directory = os.path.dirname(os.getcwd())
        iteration = 0
        while not cls.test_folder_path or os.path.exists(cls.test_folder_path):
            cls.test_folder_path = os.path.normpath(os.path.join(parent_directory, f"test_folder_{iteration}"))
        os.mkdir(cls.test_folder_path)

        cls.test_company_path = os.path.normpath(os.path.join(cls.test_folder_path, cls.COMPANY_NAME))

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_folder_path):
            shutil.rmtree(cls.test_folder_path)

    def setUp(self):
        self.manager: Manager = Manager()
        """ Default managed obj used for testing """

        self.was_overwrite_cb_triggered = False
        """ Assertion variable used to check if install overwrite callback was performed """

        self.was_folder_exists_cb_triggered = False
        """ Assertion variable used to check if install folder exists callback was performed """

    def tearDown(self):
        if os.path.exists(self.test_company_path):
            shutil.rmtree(self.test_company_path)


class TestInstall(TestManager):

    def on_install_overwrite(self, original_folder, *_):
        self.assertEqual(TestInstall.test_company_path, original_folder, "On Overwrite argument is different than installed folder")
        self.was_overwrite_cb_triggered = True

    def on_install_folder_collision(self, collision_folder, *_):
        self.assertEqual(TestInstall.test_company_path, collision_folder, "On Folder Collision argument is different than existing folder")
        self.was_folder_exists_cb_triggered = True

    def test_install_overwrite(self):
        self.manager.install(TestInstall.test_company_path)
        result = self.manager.install(TestInstall.test_company_path, self.on_install_overwrite, self.on_install_folder_collision)
        self.assertTrue(self.was_overwrite_cb_triggered, "On overwrite callback not called when trying to install on a previously installed folder")
        self.assertFalse(self.was_folder_exists_cb_triggered, "On folder collision called when installation overwrite was the problem")
        self.assertEqual(result, 1, "Return code not 1 when installation met an overwrite case")

    def test_install_collision(self):
        os.mkdir(TestInstall.test_company_path)
        result = self.manager.install(TestInstall.test_company_path, self.on_install_overwrite, self.on_install_folder_collision)
        self.assertFalse(self.was_overwrite_cb_triggered, "On overwrite called when installation folder collision was the problem")
        self.assertTrue(self.was_folder_exists_cb_triggered, "On folder collision callback not called when a folder was identified in the installation path")
        self.assertEqual(result, 2, "Return code not 1 when installation met an overwrite case")

    def test_install_success(self):
        self.manager.install(TestInstall.test_company_path, self.on_install_overwrite, self.on_install_folder_collision)
        self.assertFalse(self.was_overwrite_cb_triggered, "On Overwrite called when installation was successful")
        self.assertFalse(self.was_folder_exists_cb_triggered, "On folder collision called when installation was successful")
        self.assertEqual(self.manager._folder_path, TestInstall.test_company_path, "The folder required was not the same as targeted by the installation")
        self.assertTrue(os.path.exists(self.manager._folder_path), "The installation folder does not exists")
        self.assertTrue(self.manager.has_serialized_file(), "The manager's meta file does not exist")
