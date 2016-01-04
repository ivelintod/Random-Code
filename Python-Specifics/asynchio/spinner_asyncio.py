import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    for char in itertools.cycle('\|/-'):
        status = char + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        sys.stdout.write('\x08' * len(status))
        try:
            yield from asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    sys.stdout.write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    yield from asyncio.sleep(3)
    return 42


@asyncio.coroutine
def supervisor():
    spinner = asyncio.async(spin('loading...'))
    print('spinner obj: ', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result


def main():
    #loop = asyncio.get_event_loop()
    #result = loop.run_until_complete(supervisor())
    #loop.close()
    result = supervisor()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
