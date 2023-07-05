from unittest import TestCase
import os
import shutil
from App.ShowManager.Manager import Manager, Show


class SetupBaseDirectory(TestCase):
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
            iteration += 1
        os.mkdir(cls.test_folder_path)

        cls.test_company_path = os.path.normpath(os.path.join(cls.test_folder_path, cls.COMPANY_NAME))

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_folder_path):
            shutil.rmtree(cls.test_folder_path)


class SetupManager(SetupBaseDirectory):
    def setUp(self):
        self.manager: Manager = Manager()
        """ Default managed obj used for testing """

    def tearDown(self):
        if os.path.exists(self.test_company_path):
            shutil.rmtree(self.test_company_path)


class SetupInstalledManager(SetupManager):
    def setUp(self):
        super().setUp()
        self.manager.install(self.test_company_path)


class SetupCompleteProject(SetupInstalledManager):
    def setUp(self):
        super().setUp()
        self.show_names = "Test1", "Test2", "Test3"
        self.manager.create_show(self.show_names[0])
        self.manager.create_show(self.show_names[1])
        self.manager.create_show(self.show_names[2])


class TestInstall(SetupManager):
    def setUp(self):
        super().setUp()

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
        self.assertEqual(self.manager._folder_path, self.test_company_path, "The folder required was not the same as targeted by the installation")
        self.assertTrue(os.path.exists(self.manager._folder_path), "The installation folder does not exists")
        self.assertTrue(self.manager.has_serialized_file(), "The manager's meta file does not exist")


class TestIsInstalled(SetupManager):
    def test_was_not_installed(self):
        self.assertFalse(self.manager.is_installed(), "is_installed returned true when the manager was not installed")

    def test_was_installed(self):
        self.manager.install(self.test_company_path)
        self.assertTrue(self.manager.is_installed(), "is_installed returned false when the manager was installed")


class TestCreateShow(SetupInstalledManager):
    SHOW_NAME: str = "SHOW"
    """ Constant test show name """

    def setUp(self):
        super().setUp()
        self.was_on_show_exists_triggered = False
        self.on_show_exists_argument_instance = None

    def on_show_exists(self, show, *_):
        self.was_on_show_exists_triggered = True
        self.on_show_exists_argument_instance = show

    def test_create_show(self):
        result = self.manager.create_show(self.SHOW_NAME, self.on_show_exists)
        self.assertFalse(self.was_on_show_exists_triggered, "on_show_exists triggered even when the show did not exist previously")
        self.assertIsInstance(result, Show, "Create Show does not return a show")
        self.assertIn(self.SHOW_NAME, self.manager._shows, "Show has not been added to manager._shows dictionary")
        self.assertIs(self.manager._shows[result.name], result, "Value in the newly created manager._shows[show_name:show_instance] pair, does not represent created show instance")

    def test_show_exists(self):
        self.manager.create_show(self.SHOW_NAME)
        result = self.manager.create_show(self.SHOW_NAME, self.on_show_exists)
        self.assertTrue(self.was_on_show_exists_triggered, "on_show_exists didn't trigger when the show existed previously")
        self.assertIs(result, self.on_show_exists_argument_instance, "Argument 'show' in on_show_exists callback is different than the existing show")
        self.assertIsInstance(result, Show, "Create Show does not return a show")
        self.assertIn(self.SHOW_NAME, self.manager._shows, "Show has not been added to manager._shows dictionary")
        self.assertIs(self.manager._shows[result.name], result, "Value in the newly created manager._shows[show_name:show_instance] pair, does not represent created show instance")


class TestLoad(SetupCompleteProject):
    def setUp(self):
        super().setUp()

        # Reset Manager object
        self.manager = Manager()

    def test_load(self):
        self.manager.load(self.test_company_path)
        created_shows = list(self.manager._shows.keys())
        self.assertListEqual(sorted(self.show_names), sorted(created_shows), "Not all shows have been loaded properly")
        are_values_filled = True
        for key, value in self.manager._shows.items():
            if not value:
                are_values_filled = False
        self.assertTrue(are_values_filled, "All shows have been read but not all show objects have been created")
        self.assertEqual(self.manager._folder_path, self.test_company_path, "Folder Path have not been updated properlly")
