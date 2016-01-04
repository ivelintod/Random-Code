#@accepts decorator
#Make a decorator accepts that takes as many arguments as the function takes.
#That decorator specify the types of the arguments that your function takes.
#If any of the arguments does not match the type in the decorator raise a TypeError
import functools


def accepts(*args):
    def decorate(func):
        @functools.wraps(func)
        def decider(*dargs):
            if len(args) != len(dargs):
                raise TypeError('''decorator arguments must be
                                of same length as func arguments''')
            else:
                for i in range(len(args)):
                    if args[i] != type(dargs[i]):
                        raise TypeError('Argument %s of %s is not %s' % (i + 1, func.__name__, args[i]))
            return func(*dargs)
        return decider
    return decorate


@accepts(str)
def say_hello(name):
    return 'Hello, I am {}'.format(name)


@accepts(str, int)
def deposit(name, money):
    print('{} sends {} $'.format(name, money))
    return True
