'''class LineItem:

    def __init__(self, description, price, weight):
        self.description = description
        self.price = price
        self.weight = weight

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be above 0')'''


def quantity(storage_name):

    def qty_getter(instance):
        #return instance.__class__.storage_name
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            #instance.__class__.storage_name = value
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:

    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, price, weight):
        self.description = description
        self.price = price
        self.weight = weight

    def subtotal(self):
        return self.weight * self.price


