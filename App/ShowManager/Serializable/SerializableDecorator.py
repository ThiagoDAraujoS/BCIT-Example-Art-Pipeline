from .Serializable import Serializable


def serializable(header_text: str = ""):
    """ Decorator that adds serialization and deserialization features to a class """

    def decorator(cls):
        class DecoratedClass(cls, Serializable):
            def __init__(self, folder="", *args, **kwargs):
                self._folder = folder
                Serializable.__init__(self,
                                      file_name=f"{cls.__name__}",
                                      header=header_text)
                cls.__init__(self, *args, **kwargs)

        return DecoratedClass

    return decorator
