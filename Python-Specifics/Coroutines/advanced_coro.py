data = {
 'girls;kg':
 [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
 'girls;m':
 [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
 'boys;kg':
 [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
 'boys;m':
 [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    average = None
    total = 0.0
    count = 0
    while True:
        item = yield average
        if item is None:
            break
        total += item
        count += 1
        average = total / count
    return Result(count, average)


def grouper(result):
    while True:
        key = yield
        result[key] = yield from averager()


from inspect import getgeneratorstate

def main(data):
    result = {}
    group = grouper(result)
    group.send(None)
    for key, values in data.items():
        #group = grouper(result, key)
        print(group)

        group.send(key)
        for value in values:
            group.send(value)
        group.send(None)

    print(result)
    report(result)
#following commented lines are changes to the original code from FluentPython book
'''        try:
            group.send(None)                #I nested group.send(None) in try/except in order to catch StopIteration
        except StopIteration:               #and thus did not need while in delegegating generator(grouper) and also could
            del group                       #immediately(or so i think) garbage collect the grouper generator, four of whose instances were
    print(result)                           #concecutively stuck in GEN_SUSPENDED condition, by calling del on group and removing
    report(result)                          #the last(and only) reference to the according delegating generator.
                                            #every new delegating generator immediately positioned itself in place of the garbage collected previous one.
'''


def report(result):
    for key, value in sorted(result.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            value.count, group, value.average, unit))


if __name__ == '__main__':
    main(data)
