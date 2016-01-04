import abc
import random


class Tombola(abc.ABC):

    @abc.abstractmethod
    def pick(self):
        """Return random item without repetitions untill the end.
           Raise LookupError if no items are present."""

    @abc.abstractmethod
    def load(self, iterable):
        """Load iterable of items in a containter."""

    def loaded(self):
        return bool(self.inspect())

    def inspect(self):
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))

