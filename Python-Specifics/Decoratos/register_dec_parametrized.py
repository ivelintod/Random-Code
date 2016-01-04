registry = set()


def register(active=True):
    def decorate(func):
        print('Decorating func %s -> active is %s' % (func.__name__, active))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=False)
def f1():
    print('running %s' % f1.__name__)


@register()
def f2():
    print('running %s' % f2.__name__)


def f3():
    print('running %s' % f3.__name__)


if __name__ == '__main__':
    print('running main()')
    print('registry -> ', registry)
    f1()
    f2()
    f3()
