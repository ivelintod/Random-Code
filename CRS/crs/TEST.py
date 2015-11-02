from __future__ import division
from math import *


def calc_sq_root(number, up=None, down=None):
    if not up and not down:
        up = number
        down = 0

    mid = (up - down) / 2 + down
    #print(mid)
    if mid ** 2 > number:
        up = mid
    elif mid ** 2 < number:
        down = mid
    if abs(round(mid ** 2, 5) - number) < 0.00001:
        return round(mid, 5)

    return calc_sq_root(number, up, down)

print(calc_sq_root(5))
print(calc_sq_root(4))
print(calc_sq_root(247359))
