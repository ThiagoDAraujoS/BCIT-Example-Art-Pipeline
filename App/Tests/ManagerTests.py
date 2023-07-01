import unittest
import os
from App.Manager import Manager
from App.Show import Show


class ManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.test_folder_path: str = ""
        """ The folder where the tests are going to happen"""

        self.manager: Manager = Manager()
        """ Default managed obj used for testing """

        parent_directory = os.path.dirname(os.getcwd())
        iteration = 0
        while not self.test_folder_path or os.path.exists(self.test_folder_path):
            self.test_folder_path = os.path.normpath(os.path.join(parent_directory, f"test_folder_{iteration}"))
        os.mkdir(self.test_folder_path)

        self.company_name = "COMPANY"
        """ Company name used for testing """

        self.test_company_path: str = os.path.normpath(os.path.join(self.test_folder_path, self.company_name))
        """ Company path used for testing """

        self.was_overwrite_cb_triggered = False
        """ Assertion variable used to check if install overwrite callback was performed """

        self.was_folder_exists_cb_triggered = False
        """ Assertion variable used to check if install folder exists callback was performed """

    def _on_overwrite(self, _): self.was_overwrite_cb_triggered = True
    def _on_folder_exists(self, _): self.was_folder_exists_cb_triggered = True

    def _reset(self):
        self.was_folder_exists_cb_triggered = False
        self.was_overwrite_cb_triggered = False
        self.manager.main_folder = ""
        if os.path.exists(self.test_company_path):
            os.rmdir(self.test_company_path)

    def tearDown(self):
        if os.path.exists(self.test_folder_path):
            os.rmdir(self.test_folder_path)

    def test_install_overwrite(self):
        self.manager.main_folder = "ERROR_ERROR_ERROR"
        self.manager.install(self.test_company_path, on_overwrite_callback=self._on_overwrite, on_folder_exists_callback=self._on_folder_exists)
        self.assertTrue(self.was_overwrite_cb_triggered)
        self.assertFalse(self.was_folder_exists_cb_triggered)
        self._reset()

    def test_install_folder_exist(self):
        os.mkdir(self.test_company_path)
        self.manager.install(self.test_company_path, on_overwrite_callback=self._on_overwrite, on_folder_exists_callback=self._on_folder_exists)
        self.assertFalse(self.was_overwrite_cb_triggered)
        self.assertTrue(self.was_folder_exists_cb_triggered)
        self._reset()

    def test_install(self):
        self.manager.install(self.test_company_path, on_overwrite_callback=self._on_overwrite, on_folder_exists_callback=self._on_folder_exists)
        self.assertEqual(self.manager.main_folder, self.test_company_path)
        self.assertTrue(os.path.exists(self.manager.main_folder))
        self.assertFalse(self.was_overwrite_cb_triggered)
        self.assertFalse(self.was_folder_exists_cb_triggered)

    def test_create_show(self):
        show_name = "Test Show"
        show = self.manager.create_show(show_name)

        # Assert that a Show object is returned
        self.assertIsInstance(show, Show)

        # Assert that the show object has the correct name
        self.assertEqual(show.name, show_name)

        # Assert that the show folder was created
        show_folder = os.path.join(self.manager.main_folder, show_name)
        self.assertTrue(os.path.exists(show_folder))

        # Assert that the show was serialized
        show_file = os.path.join(show_folder, Show.FILE_NAME)
        self.assertTrue(os.path.exists(show_file))


if __name__ == '__main__':
    unittest.main()