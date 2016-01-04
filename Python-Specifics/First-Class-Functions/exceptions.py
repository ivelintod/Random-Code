class TestException(Exception):
    def __init__(self, balance):
        #super().__init__(balance)
        self.balance = balance

    def calc_overhead(self):
        return self.amount - self.balance

    def __call__(self):
        return self.calc_overhead()

    def withdraw(self, amount):
        #super().__init__(amount)
        if amount > self.balance:
            self.amount = amount
            raise self
        self.balance -= amount


try:
    t = TestException(35)
    t.withdraw(40)
except TestException as e:
    print(e())


from collections import OrderedDict, Counter


class OrderedCounter(Counter, OrderedDict):
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))


class SortedCounterOrdered(Counter, OrderedDict):
    def __init__(self, seq):
        super().__init__(sorted(seq))


a = OrderedCounter('dabcdwadaf')
c = SortedCounterOrdered('dabcdwadaf')
b = Counter('dabcdwadaf')
d = OrderedDict({1: 'a', 2: 'b', 3: 'c'})



class Singleton:

    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, name, surname):
        if not hasattr(self, 'name'): #optional if first ever state is wanted permanent
            self.name = name
            self.surname = surname


s = Singleton('Ivo', 'Tod')
d = Singleton('Stef', 'Tod')


class FixedList(list):

    def __new__(cls, *args, **kwargs):
        fixed_list = super().__new__(cls)
        fixed_list.extend([None] * kwargs['size'])
        return fixed_list

    def _expand(self, num):
        self.extend([None] * num)

    def __init__(self, *args, size=5):
        index = 0
        if len(args) > size:
            self._expand(len(args) - size)
        for item in args:
            self[index] = item
            index += 1


def test_clipper(text: str, max_len: 'int > 0'=80) -> str:
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after

    if end is None:
        end = len(text)

    return text[:end].rstrip()
