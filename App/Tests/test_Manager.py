import os
import shutil
from App.ShowManager.Manager import Manager
from App.Tests.test_setup import SetupBaseDirectory


class TestManager(SetupBaseDirectory):
    """ this setup class builds a manager object and sets a company folder for it """

    COMPANY_NAME: str = "COMPANY"
    """ Constant with generic test company name """

    test_company_path: str = ""
    """ The folder path containing the company folder """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_company_path = os.path.normpath(os.path.join(cls.test_folder_path, cls.COMPANY_NAME))

    def tearDown(self):
        if os.path.exists(self.test_company_path):
            shutil.rmtree(self.test_company_path)

    def setUp(self):
        super().setUp()
        self.manager: Manager = Manager()
        self.was_overwrite_cb_triggered = False
        """ Assertion variable used to check if install overwrite callback was performed """

        self.was_folder_exists_cb_triggered = False
        """ Assertion variable used to check if install folder exists callback was performed """

    def on_overwrite(self, original_folder, *_):
        self.assertEqual(self.test_company_path, original_folder, "On Overwrite argument is different than installed folder")
        self.was_overwrite_cb_triggered = True

    def on_folder_collision(self, collision_folder, *_):
        self.assertEqual(self.test_company_path, collision_folder, "On Folder Collision argument is different than existing folder")
        self.was_folder_exists_cb_triggered = True

    def test_overwrite(self):
        self.manager.install(self.test_company_path)
        result = self.manager.install(self.test_company_path, self.on_overwrite, self.on_folder_collision)
        self.assertTrue(self.was_overwrite_cb_triggered, "On overwrite callback not called when trying to install on a previously installed folder")
        self.assertFalse(self.was_folder_exists_cb_triggered, "On folder collision called when installation overwrite was the problem")
        self.assertEqual(result, 1, "Return code not 1 when installation met an overwrite case")

    def test_collision(self):
        os.mkdir(self.test_company_path)
        result = self.manager.install(self.test_company_path, self.on_overwrite, self.on_folder_collision)
        self.assertFalse(self.was_overwrite_cb_triggered, "On overwrite called when installation folder collision was the problem")
        self.assertTrue(self.was_folder_exists_cb_triggered, "On folder collision callback not called when a folder was identified in the installation path")
        self.assertEqual(result, 2, "Return code not 1 when installation met an overwrite case")

    def test_success(self):
        self.manager.install(self.test_company_path, self.on_overwrite, self.on_folder_collision)
        self.assertFalse(self.was_overwrite_cb_triggered, "On Overwrite called when installation was successful")
        self.assertFalse(self.was_folder_exists_cb_triggered, "On folder collision called when installation was successful")
        self.assertEqual(self.manager._folder, self.test_company_path, "The folder required was not the same as targeted by the installation")
        self.assertTrue(os.path.exists(self.manager._folder), "The installation folder does not exists")
        self.assertTrue(self.manager.has_serialized_file(), "The manager's meta file does not exist")

    def test_was_not_installed(self):
        self.assertFalse(self.manager.is_installed(), "is_installed returned true when the manager was not installed")

    def test_was_installed(self):
        self.manager.install(self.test_company_path)
        self.assertTrue(self.manager.is_installed(), "is_installed returned false when the manager was installed")
