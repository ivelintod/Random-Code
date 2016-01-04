from custom_abc import Tombola
import random


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self.containter = []
        self.load(iterable)

    def load(self, iterable):
        self.containter.extend(x for x in iterable)

    def pick(self):
        '''if len(self.containter) > 0:
            random_pos = random.randrange(len(self.containter))
            item = self.containter.pop(random_pos)
            return item
        else:
            raise LookupError("Empty seq")'''
        try:
            random_pos = random.randrange(len(self.containter))
        except ValueError:
            raise LookupError("Can't pick from an empty sequence")
        return self.containter.pop(random_pos)

    def loaded(self):
        return bool(self.containter)

    def inspect(self):
        return tuple(sorted(self.containter))
