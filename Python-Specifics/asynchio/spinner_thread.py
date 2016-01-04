import sys
import itertools
import time
import threading


class Signal:
    go = True


def spin(msg, signal):
    for char in itertools.cycle('\|/-'):
        status = char + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        sys.stdout.write('\x08' * len(status))
        signal = yield
        if not signal.go:
            break

    sys.stdout.write(' ' * len(status) + '\x08' * len(status))


def slow_func_resembler():
    seconds = 0
    while seconds < 3:
        time.sleep(.1)
        yield None
        seconds += .1
    return 42


def commander():
    res = yield from slow_func_resembler()
    yield res

def supervisor():
    signal = Signal()
    #spinner = threading.Thread(target=spin, args=('loading...', signal))
    #spinner.start()
    coroutine = spin('loading...', signal)
    next(coroutine)
    com = commander()
    result = next(com)
    while not result:
        coroutine.send(signal)
        result = com.send(None)

    signal.go = False
    try:
        coroutine.send(signal)
    except StopIteration:
        del coroutine
        del commander
    finally:
        return result


if __name__ == '__main__':
    result = supervisor()
    print('Answer: ', result)

