class Quantity:

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class QuantityInvsbl:

    _counter = 0

    def __init__(self):
        cls = self.__class__
        cls_name = cls.__name__
        cls._counter += 1
        self.storage_name = '{}#{}'.format(cls_name, cls._counter)

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')

    def __get__(self, instance, owner):
        if instance:
            return instance.__dict__[self.storage_name]
        else:
            return self


def quantity():
    try:
        quantity._counter += 1
    except AttributeError:
        quantity._counter = 0

    storage_name = '{}#{}'.format('quantity', quantity._counter)

    def get_value(instance):
        return instance.__dict__[storage_name]

    def set_value(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(get_value, set_value)


class LineItem:

    #weight = Quantity('weight')
    #price = Quantity('price')
    weight = QuantityInvsbl()
    price = QuantityInvsbl()
    #weight = quantity()
    #price = quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.price * self.weight
