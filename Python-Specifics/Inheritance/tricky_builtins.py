class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

d = DoppelDict(one=1)


class AnswerDict(dict):
    def __getitem__(self, key):
        return 42

ad = AnswerDict(a='foo')


import collections


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

dd = DoppelDict2(one=1)


class AnswerDict2(collections.UserDict):
    def __getitem__(self, key):
        return 42


a = AnswerDict2(a='foo')


def print_mro(cls):
    print(', '.join(c.__name__ for c in cls.__mro__))
