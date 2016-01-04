def deco(func):
    def inner():
        print('running inner')
    return inner


@deco
def target():
    print('running target()')


registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


#@register
def f1():
    print('running f1()')
f1 = register(f1)

#@register
def f2():
    print('running f2()')
f2 = register(f2)


def f3():
    print('running f3()')


if __name__ == '__main__':
    print('running main()')
    print('registry ->', registry)

