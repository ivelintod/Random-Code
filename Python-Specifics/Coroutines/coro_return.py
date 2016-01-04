from collections import namedtuple
Result = namedtuple('Result', 'count average')

def coro_returner():
    average = None
    count = 0
    total = 0.0
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

