from custom_abc import Tombola
import random


class BingoCage(Tombola):

    def __init__(self, iterable):
        self._shuffler = random.SystemRandom()
        self._items = []
        self.load(iterable)

    def load(self, iterable):
        self._items.extend(iterable)
        self._shuffler.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()
