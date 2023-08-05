from datetime import date, time, datetime
from typing import NewType, Type

import dataclasses_json.cfg

dataclasses_json.cfg.global_config.encoders[date] = date.isoformat
dataclasses_json.cfg.global_config.decoders[date] = date.fromisoformat

dataclasses_json.cfg.global_config.encoders[time] = time.isoformat
dataclasses_json.cfg.global_config.decoders[time] = time.fromisoformat

dataclasses_json.cfg.global_config.encoders[datetime] = datetime.isoformat
dataclasses_json.cfg.global_config.decoders[datetime] = datetime.fromisoformat

UUIDString = NewType('UUIDString', str)
JsonString = NewType('JsonString', str)
TypeString = NewType('TypeString', str)
PathString = NewType('PathString', str)

IGNORE_ERRORS = False


def error(error_type: Type[Exception], message: str):
    if IGNORE_ERRORS:
        print(message)
    else:
        error_type(message)


class AssetArchiveError(Exception):
    """Exception raised when an operation is not allowed for an archived asset."""
    pass


class EmptyFolderError(Exception):
    """Custom exception for handling empty folders during archiving."""
    pass


class ConnectToSelfError(Exception):
    """ Custom Exception for handling assets connecting to themselves"""
    pass
