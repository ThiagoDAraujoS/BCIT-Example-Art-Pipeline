import os
import shutil

from App.ShowManager.Manager import Manager, InstallExitCode
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

    def test_overwrite(self):
        self.manager.install(self.test_company_path)
        result = self.manager.install(self.test_company_path)
        self.assertEqual(result, InstallExitCode.PROJECT_OVERRIDE, "Return code not 1 when installation met an overwrite case")

    def test_collision(self):
        os.mkdir(self.test_company_path)
        result = self.manager.install(self.test_company_path)
        self.assertEqual(result, InstallExitCode.FOLDER_COLLISION, "Return code not 1 when installation met an overwrite case")

    def test_success(self):
        result_code = self.manager.install(self.test_company_path)
        self.assertEqual(result_code, InstallExitCode.SUCCESS, "Result from a successful installation was not 0")
        self.assertEqual(self.manager._folder, self.test_company_path, "The folder required was not the same as targeted by the installation")
        self.assertTrue(os.path.exists(self.manager._folder), "The installation folder does not exists")
        self.assertTrue(self.manager.file_exists(), "The manager's meta file does not exist")

    def test_path_broken(self):
        result_code = self.manager.install("ERROR_1234567890_ERROR/ERROR_1234567890_ERROR")
        self.assertEqual(result_code, InstallExitCode.PATH_BROKEN, "Returned code on install/path broken is not equal to InstallExitCode.PATH_BROKEN")

    def test_was_not_installed(self):
        self.assertFalse(self.manager.is_installed(), "is_installed returned true when the manager was not installed")

    def test_was_installed(self):
        self.manager.install(self.test_company_path)
        self.assertTrue(self.manager.is_installed(), "is_installed returned false when the manager was installed")
