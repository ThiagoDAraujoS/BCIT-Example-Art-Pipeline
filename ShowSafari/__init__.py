import uuid
from dataclasses_json import config


def uuid_encoder(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def uuid_decoder(obj):
    if isinstance(obj, str):
        return uuid.UUID(obj)
    return obj


# Set up the custom encoder and decoder globally for dataclasses_json
config(encoder=uuid_encoder, decoder=uuid_decoder)

print("x")
