from __future__ import annotations
from .data import *


class Manager:
    """ The Manager class handles the management of shows and their associated files """
    def __init__(self, folder=""):
        self.library = None

    def add_asset(self, asset_uuid: UUID, asset):
        self.library[asset_uuid] = asset

    def remove_asset(self, asset_uuid: UUID):
        if asset_uuid in self.library:
            del self.library[asset_uuid]

    def get_asset(self, asset_uuid: UUID):
        return self.library.get(asset_uuid, None)
