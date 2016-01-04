from models_descriptor import Quantity, NonBlank, name_init, Validate


@name_init
class LineItem:

    description = NonBlank()
    weight = Quantity()
    price = Quantity()
    '''
    def __new__(cls, *args, **kwargs):
        for key, attr in cls.__dict__.items():
            if isinstance(attr, Validate):
                cls_name = type(attr).__name__
                new_storage_name = '_{}#{}'.format(cls_name, key)
                attr.storage_name = new_storage_name
        return super().__new__(cls)'''

    def __init__(self, descr, price, weight):
        self.description = descr
        self.price = price
        self.weight = weight

    def subtotal(self):
        return self.price * self.weight
