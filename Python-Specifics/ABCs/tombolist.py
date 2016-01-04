from custom_abc import Tombola
import random


@Tombola.register
class TomboList(list):

    def __bool__(self):
        return bool(len(self))

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty seq')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))
