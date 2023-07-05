import os
import shutil
from unittest import TestCase
from App.ShowManager.Manager import Manager


class SetupBaseDirectory(TestCase):
    """ this setup class creates a base directory to receive test folders and metafiles """

    test_folder_path: str = ""
    """ The folder path containing the test folder """

    @classmethod
    def setUpClass(cls) -> None:
        parent_directory = os.path.dirname(os.getcwd())
        iteration = 0
        while not cls.test_folder_path or os.path.exists(cls.test_folder_path):
            cls.test_folder_path = os.path.normpath(os.path.join(parent_directory, f"test_folder_{iteration}"))
            iteration += 1
        os.mkdir(cls.test_folder_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_folder_path):
            shutil.rmtree(cls.test_folder_path)


class SetupManager(SetupBaseDirectory):
    """ this setup class builds a manager object and sets a company folder for it """

    COMPANY_NAME: str = "COMPANY"
    """ Constant with generic test company name """

    test_company_path: str = ""
    """ The folder path containing the company folder """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_company_path = os.path.normpath(os.path.join(cls.test_folder_path, cls.COMPANY_NAME))

    def setUp(self):
        self.manager: Manager = Manager()
        """ Default managed obj used for testing """

    def tearDown(self):
        if os.path.exists(self.test_company_path):
            shutil.rmtree(self.test_company_path)


class SetupInstallation(SetupManager):
    """ this setup class installs the manager """
    def setUp(self):
        super().setUp()
        self.manager.install(self.test_company_path)


class SetupSampleProject(SetupInstallation):
    """ this setup class builds a fake project """
    def setUp(self):
        super().setUp()
        self.show_names = ["Test1", "Test2", "Test3"]
        self.manager.create_show(self.show_names[0])
        self.manager.create_show(self.show_names[1])
        self.manager.create_show(self.show_names[2])
