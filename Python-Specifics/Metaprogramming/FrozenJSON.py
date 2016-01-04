from collections import abc
import keyword

from loader import load


class FrozenJSON:

    def __init__(self, data):
        self.data = dict(data)

    def __getattr__(self, val):
        if hasattr(self.data, val):
            return getattr(self.data, val)
        try:
            return FrozenJSON.build(self.data[val])
        except KeyError as exc:
            msg = '{} object has no attribute {}'.format(type(self).__name__, exc.args[0])
            raise AttributeError(msg)

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class FJSON:

    def __init__(self, data):
        self.__data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, attr):
        if hasattr(self.__data, attr):
            return getattr(self.__data, attr)
        try:
            return FJSON.build(self.__data[attr])
        except KeyError as exc:
            cls = type(self).__name__
            msg = '{} object has no attribute {}'.format(cls, exc.args[0])
            raise AttributeError(msg)

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class NewFrozenJSON:

    def __new__(cls, data):
        if isinstance(data, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(data, abc.MutableSequence):
            return [cls(item) for item in data]
        else:
            return data

    def __init__(self, data):
        self.__data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, attr):
        if hasattr(self.__data, attr):
            return getattr(self.__data, attr)
        try:
            return NewFrozenJSON(self.__data[attr])
        except KeyError as exc:
            cls = type(self).__name__
            msg = '{} object has no attribute {}'.format(cls, exc.args[0])
            raise AttributeError(msg)
