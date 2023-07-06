import os
import shutil
from datetime import date, time
from unittest import TestCase

from App.ShowManager.Serializable import serializable

HEADER = "HEADER"
FILE = "test"


@serializable(HEADER, FILE)
class SerializableTestClass:
    def __init__(self):
        self.i: int = 1
        self.f: float = 1.0
        self.s: str = "string"
        self.d: date = date(1, 1, 1)
        self.t: time = time(1, 1, 1)
        self.li: list = [1, 2, 3]
        self.se: set = {1, 2, 3}
        self.di: dict = {"1": 1, "2": 2, "3": 3}


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
