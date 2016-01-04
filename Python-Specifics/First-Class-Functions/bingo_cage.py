import random


class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('picking from empty BingoCage')

    def __call__(self):
        return self.pick()

b = BingoCage({'kuc': 'kon', 'vtori': 'kuc_kon', 'i taka': 'natatak'})
