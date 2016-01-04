class Factory:

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __iter__(self):
        return (x for _, x in self.__dict__.items())


def record_factory(cls_name, *args):
    if len(args) == 1:
        details = args[0].split()
    else:
        details = args
    fields = tuple(details)
    counter = len(fields)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __init__(self, *args, **kwargs):
        actual_len = len(args) + len(kwargs.items())
        if actual_len > self.counter:
            err_msg = '__init__ takes {} positional arguments but {} were given'
            raise TypeError(err_msg.format(self.counter, actual_len))
        attrs = dict(zip(self.fields, args))
        print(attrs)
        attrs.update(kwargs)
        for name, value in attrs.items():
            self.__setattr__(name, value)


    def __iter__(self):
        for name in self.fields:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.fields, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(fields=fields,
                     counter=counter,
                     __setattr__=__setattr__,
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)

    return type(cls_name, (object,), cls_attrs)

