def gen():
    a = yield 1
    b = yield 2 + a
    c = yield 3 + b
    d = yield 4 + c
    e = yield 5 + d
    return 0


def delegator(subgen):
    i = iter(subgen)
    try:
        y = next(i)
        print(y)
    except StopIteration as exc:
        r = exc.value
    else:
        while True:
            s = yield y

            try:
                y = i.send(s)
                print(y)
            except StopIteration as e:
                r = e.value
                break

    return r

def grouper():
    deleg = delegator(gen())
    res = next(deleg)
    while True:
        user = yield res
        res = yield deleg.send(user)
        print(res)


def main():
    result = []
    group = grouper()
    result.append(next(group))
    for i in range(1, 5):
        res = group.send(i)
        group.send(0)
        #print(res)
        result.append(res)
        #print('i e', i)
    print(result)



if __name__ == '__main__':
    main()
