from __future__ import annotations
from .Show import Show
from .Serializable.SerializableDecorator import serializable
from App.ShowManager.Serializable.SerializableDict import SerializableDict

FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show manager information."""


@serializable(FILE_HEADER)
class Manager(SerializableDict):
    """ The Manager class handles the management of shows and their associated files """
    def __init__(self, folder=""):
        super().__init__(Show, folder)
