string_float = 1.2342313
print(format(string_float, '0.2f'))

a = '{size:.2f}'
print(a.format(size=1.234242))


string = 'xyztq'
string2 = 'xyaf'

print(1 ^ 4)


def sum_of_digits(n):
    import functools
    res = functools.reduce(lambda x, y: x+y, [int(x) for x in str(n)])
    print(res)
sum_of_digits(131414)

from array import array
from functools import reduce
from operator import xor


class Pythonic:

    typecode = 'd'

    def __init__(self, iterable):
        self._components = array(self.typecode, iterable)

    def __iter__(self):
        return (x for x in self._components)

    def __str__(self):
        return str(self._components)

    def __repr__(self):
        cls = type(self)
        iterable = ', '.join(str(x) for x in iter(self))
        cls_repr = '{.__name__}([{}])'.format(cls, iterable)
        return cls_repr

    def __len__(self):
        return len(self._components)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        return reduce(xor, (hash(x) for x in self))

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        else:
            return self._components[index]

    def __getattr__(self, attr):
        cls = type(self)
        attrs = 'xyzt'
        if len(attr) == 1:
            pos = attrs.find(attr)
            if 0 <= pos <= len(self):
                return self._components[pos]
        msg = '{} object has no attribute {}'.format(cls.__name__, repr(attr))
        raise AttributeError(msg)

    def __setattr__(self, attr, val):
        if len(attr) == 1:
            if attr in 'xyzt':
                raise AttributeError("Can't assign values to read-only attribute {}". format(repr(attr)))
            else:
                raise AttributeError("Can't assign a-z attributes")

        super().__setattr__(attr, val)


def power_to(num, power):
    if power == 0:
        return 1
    if power == 1:
        return num

    return temp(power_to(num, power - 1), num)


def temp(num, times):
    if times == 1:
        return num
    return num + temp(num, times - 1)


print(power_to(3, 0))


a = [1, 2, 3, 4]
a += (1, 2, 3)
print(a)
