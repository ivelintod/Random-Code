import abc


class Auto:

    __counter = 0

    def __init__(self):
        cls = self.__class__
        cls_name = cls.__name__
        self.storage_name = '__{}#{}'.format(cls_name, cls.__counter)
        cls.__counter += 1
        print(cls.__counter)

    def __get__(self, instance, owner):
        if instance:
            return getattr(instance, self.storage_name)
        else:
            return self

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validate(abc.ABC, Auto):

    def __set__(self, instance, value):
        value = self.validate(value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, value):
        '''return validated value or raise ValueError'''


class Quantity(Validate):

    def validate(self, value):
        if value > 0:
            return value
        raise ValueError('value must be > 0')


class NonBlank(Validate):

    def validate(self, value):
        value = value.strip()
        if len(value) == 0:
            return ValueError('description must not be empty/blank')
        return value


def name_init(cls):
    for attr, value in cls.__dict__.items():
        if isinstance(value, Validate):
            cls_name = type(value).__name__
            new_storage_name = '_{}#{}'.format(cls_name, attr)
            value.storage_name = new_storage_name
    return cls
