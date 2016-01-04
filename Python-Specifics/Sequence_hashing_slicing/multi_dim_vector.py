from array import array
import itertools
import functools
import operator
import reprlib
import math
from itertools import zip_longest
import numbers


class Vector:

    typecode = 'd'
    attrs = 'xyzt'

    def __init__(self, iterable):
        self._components = array(self.typecode, iterable)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        '''if len(self) != len(other):
            return False
        else:
            for a, b in zip(self, other):
                if a != b:
                    return False
        return True'''
        cls = type(self)
        if isinstance(other, cls):
            return (len(self) == len(other) and
                    all(a == b for a, b in zip(self, other)))
        return NotImplemented

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(self):
        return Vector(self)

    def __invert__(self):
        return Vector(-(x + 1) for x in self)

    def __add__(self, other):
        try:
            return Vector(x + y for x, y in zip_longest(self, other, fillvalue=0.0))
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, bytes_obj):
        typecode = chr(bytes_obj[0])
        memv = memoryview(bytes_obj[1:]).cast(typecode)
        return Vector(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        '''if type(index) is int:
            return self._components[index]
        arr = self._components[index]
        return Vector(arr)'''
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __getattr__(self, name):
        cls = type(self)
        pos = cls.attrs.find(name)
        if len(name) == 1:
            if 0 <= pos < len(self):
                return self._components[pos]
        msg = '{.__name__} object has no attribute {}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.attrs:
                error = 'readonly attribute {attr!r}'
            elif name.islower():
                error = 'cannot set attrubutes a-z for {cls.__name__}'
            else:
                error = ''
            if error:
                msg = error.format(attr=name, cls=cls)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        all_comps = False
        if fmt_spec.endswith('*'):
            all_comps = True
            fmt_spec = fmt_spec[:-1]
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())

            outer_fmt = '<{}>'

        else:
            coords = self
            outer_fmt = '({})'

        if all_comps:
            components = (format(c, fmt_spec) for c in coords)

        else:
            components = (format(c, fmt_spec) for i, c in enumerate(coords) if i < 30)
            outer_fmt = outer_fmt.replace(outer_fmt[-1], ', ...' + outer_fmt[-1])
        return outer_fmt.format(', '.join(components))
