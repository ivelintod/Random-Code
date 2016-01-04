from collections import namedtuple


Customer = namedtuple('Person', 'name fidelity')


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
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.items)
        return self.__total

    def due(self):
        if self.promotion is None:
            return self.total()
        else:
            return self.total() - self.promotion(self)

    def __repr__(self):
        fmt = '<Order total {:.2f} --- due {:.2f}>'
        return fmt.format(self.total(), self.due())

'''
promos = []


def promotion(promo_func):
    promos.append(promo_func)
    return promo_func'''

from strategy_dec import promos, promotion

@promotion
def fidelity_promo(order):
    return order.total() * .05 if order.person.fidelity >= 1000 else 0


#@promotion
#def bulk_item_promo(order):
#    return sum(item.total() * .1 for item in order.items if item.quantity >= 20)
#from order_funcs import promos as p
#promos.extend(p)

from order_funcs import bulk_item_promo
bulk_item_promo = promotion(bulk_item_promo)


@promotion
def large_order_promo(order):
    if len({item for item in order.items}) >= 10:
        return order.total() * .07
    return 0

#def best_promo(order):
    '''first way'''
    #promos = [globals()[name] for name in globals()
    #          if name.endswith('_promo') and name != 'best_promo']
    '''second way'''
    #import order_funcs
    #import inspect
    #promos = [func for name, func in inspect.getmembers(order_funcs, inspect.isfunction)]
    #return max(promo(order) for promo in promos)


def best_promo(order):
    return max(promo(order) for promo in promos)


joe = Customer('Joe', 0)
ann = Customer('Ann', 1100)
cart = [LineItem('banana', 4, .5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]
banana_cart = [LineItem('banana', 30, .5),
               LineItem('apple', 10, 1.5)]
long_cart = [LineItem(str(item_code), 1, 1.0)
             for item_code in range(10)]
