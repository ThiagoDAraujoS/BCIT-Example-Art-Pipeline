import os
import shutil
from unittest import TestCase


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
