import functools

def encrypt(integer=2):
    if type(integer) != int:
        func = integer
        return encrypt(2)(func)

    def decorate(func):
        @functools.wraps(func)
        def dummy(*args, **kwargs):
            func_result = list(func(*args, **kwargs))
            desired_result = ''.join([chr(ord(x) + integer) if x != ' ' else x for x in func_result])
            return desired_result
        return dummy
    return decorate


@encrypt
def get_low():
    return 'Get get get low'
#get_low = encrypt(get_low)


def encrypt2(wrapped=None, integer=2):
    if not wrapped:
        return functools.partial(encrypt2, integer=integer)

    @functools.wraps(wrapped)
    def dummy(*args, **kwargs):
        func_result = list(wrapped(*args, **kwargs))
        desired_result = ''.join([chr(ord(x) + integer) if x != ' ' else x for x in func_result])
        return desired_result
    return dummy


@encrypt2
def get_low2():
    return 'Get get get low'

if __name__ == '__main__':
    print(get_low2())

