def fidelity_promo(order):
    return order.total() * .05 if order.person.fidelity >= 1000 else 0


def bulk_item_promo(order):
    return sum(item.total() * .1 for item in order.items if item.quantity >= 20)


def large_order_promo(order):
    if len({item for item in order.items}) >= 10:
        return order.total() * .07
    return 0

