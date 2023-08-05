import os
import shutil
from unittest import TestCase


class TestSetup(TestCase):
    main_folder_path = ""

    @classmethod
    def setUpClass(cls):
        # Create the TestStage folder for testing
        relative_path = "../TestStage"
        if os.path.exists(relative_path):
            shutil.rmtree(relative_path)

        os.makedirs(relative_path)
        cls.main_folder_path = os.path.abspath(relative_path)

    @classmethod
    def tearDownClass(cls):
        # Remove the TestStage folder after all tests are done
        shutil.rmtree(cls.main_folder_path)
