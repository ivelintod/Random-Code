import functools
import time


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        atr_list = []
        if args:
            atr_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%s' % (k, v) for k, v in sorted(kwargs.items())]
            atr_list.append(', '.join(pairs))
        atr_str = ', '.join(atr_list)
        print(('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, atr_str, result)))
        return result
    return clocked


@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == '__main__':
    import timeit
    setup = 'from __main__ import fibonacci'
    print(timeit.timeit('fibonacci(30)', setup=setup))
    time.sleep(5)
    fibonacci = clock(fibonacci)
    print(timeit.timeit('fibonacci(30)', setup=setup))
