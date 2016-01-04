from abc import ABC, abstractmethod
from collections import namedtuple


Person = namedtuple('Person', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:

    def __init__(self, person, items, promotion=None):
        self.person = person
        self.items = list(items)
        self.promotion = promotion

    def total(self):
        return sum(item.total() for item in self.items)

    def due(self):
        if self.promotion is None:
            return self.total()
        else:
            return self.total() - self.promotion.promo(self)

    def __repr__(self):
        fmt = '<Order total {:.2f} --- due {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotions(ABC):

    @abstractmethod
    def promo(self, order):
        """Return discount as a positive dollar amount"""


class FidelityPromotion(Promotions):

    def promo(self, order):
        return order.total() * .05 if order.person.fidelity >= 1000 else 0


class BulkItemPromotion(Promotions):

    def promo(self, order):
        return sum(item.total() * .1 for item in order.items if item.quantity >= 20)


class LargeOrderPromotion(Promotions):

    def promo(self, order):
        if len({item for item in order.items}) >= 10:
            return order.total() * .07
        return 0
