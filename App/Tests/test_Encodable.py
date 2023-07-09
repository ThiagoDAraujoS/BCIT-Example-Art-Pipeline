import json
from datetime import date, time

from unittest import TestCase
from App.ShowManager.Serializable.Encodable import Encodable, NON_SERIALIZABLE_PREFIX


class TestClass(Encodable):
    def __init__(self):
        self._pr: int   = 0
        self.int: int   = 0
        self.flt: float = 0.0
        self.str: str   = ""
        self.dte: date  = date(1, 1, 1)
        self.tme: time  = time(1, 1, 1)
        self.lst: list  = []
        self.set: set   = set()
        self.dct: dict  = dict()


class TestEncodable(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.instance = TestClass()
        self.instance._pr = 100
        self.instance.int = 23
        self.instance.flt = 453.304
        self.instance.str = "NAME NAME NAME"
        self.instance.dte = date(2020, 7, 23)
        self.instance.tme = time(18, 40, 24)
        self.instance.lst = [0, 1, 2, 3, 4]
        self.instance.set = {5, 6, 7, 8, 9}
        self.instance.dct = {"key1": 3872, "key2": 1727, "key3": 7945}

        # Filter out any private field and save all fields in a self.data dictionary
        self.data = {data: value for data, value in self.instance.__dict__.items()}

        # cast any unfriendly json type to a friendly json type
        cast_data = {data: value for data, value in self.data.items() if not data.startswith(NON_SERIALIZABLE_PREFIX)}
        cast_data["dte"] = self.instance.dte.isoformat()
        cast_data["tme"] = self.instance.tme.isoformat()
        cast_data["set"] = list(self.instance.set)

        # convert the friendly data to json string in self.json
        self.json = json.dumps(cast_data, indent=4)

    def tearDown(self) -> None:
        super().tearDown()

    def test_decode(self):
        instance = TestClass()
        instance.decode(self.json)

        private_result, public_result = True, True
        for key, value in instance.__dict__.items():
            if key.startswith(NON_SERIALIZABLE_PREFIX):
                if self.data[key] == value:
                    private_result = False
            else:
                if self.data[key] != value:
                    public_result = False

        self.assertTrue(private_result, "Decode changed a private field")
        self.assertTrue(public_result, "Decode did not update a public field")

    def test_encode(self):
        result = self.instance.encode()
        self.assertEqual(result, self.json, "Encoded instance, is not equal to file json")
