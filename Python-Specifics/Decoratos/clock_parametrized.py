import time
import functools
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        @functools.wraps(func)
        def clocked(*_args, **kwargs):
            t0 = time.time()
            _result = func(*_args, **kwargs)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate


@clock('{name}: {elapsed}s')
def snoozing(t):
    print('Sleeping for %s' % t)
    time.sleep(t)


if __name__ == '__main__':
    snoozing(.123)
    snoozing(2)
    snoozing(5)
