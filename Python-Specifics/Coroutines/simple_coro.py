import functools


def coroutine(a):
    print('Value of a is ', a)
    b = yield a
    print('Value of b is ', b)
    c = yield a + b
    print('Value of c is ', c)


def coro_activator(coro):
    @functools.wraps(coro)
    def wrapper(*args, **kwargs):
        result = coro(*args, **kwargs)
        result.send(None)
        return result
    return wrapper


def coro_averager():
    total = .0
    items = 0
    average = None
    while True:
        item = yield average
        total += item
        items += 1
        average = total / items


@coro_activator
def coro_displayer():
    numbers = []
    res = None
    while len(numbers) < 10:
        number = yield res
        numbers.append(number)
        res = ' '.join(numbers)


class DemoException(Exception):
    '''demo test'''


def coro_handling_errors():
    print('Coroutine started.')
    #x = 1
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('Invalid x handled. Continuing...')
            else:
                print('Value {!r} was received'.format(x))
    finally:
        print('Coroutine terminated.')

