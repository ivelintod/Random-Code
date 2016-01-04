from collections import abc

import keyword
from loader import load


class FrozenJSON:

    def __init__(self, data):
        self.data = dict(data)

    def __getattr__(self, value):
        if hasattr(self.data, value):
            return getattr(self.data, value)
        else:
            try:
                return FrozenJSON.build(self.data[value])
            except KeyError as exc:
                cls = self.__class__.__name__
                msg = '{} object has no attribute {}'
                raise AttributeError(msg.format(cls, exc.args[0]))


    @classmethod
    def build(cls, value):
        if isinstance(value, abc.Mapping):
            return cls(value)
        elif isinstance(value, abc.MutableMapping):
            return [cls(item) for item in value]
        else:
            return value


class FJSON:

    def __new__(cls, data):
        if isinstance(data, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(data, abc.MutableMapping):
            return [cls(item) for item in data]
        else:
            return data

    def __init__(self, data):
        self.__data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key = '_' + key
            self.__data[key] = value

    def __getattr__(self, value):
        if hasattr(self.__data, value):
            return getattr(self.__data, value)
        try:
            return FJSON(self.__data[value])
        except KeyError as exc:
            raise AttributeError
