import itertools


class AP:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin)
        iternity = self.end is None
        index = 0
        while iternity or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


def AP_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    iternity = end is None
    index = 0
    while iternity or result < end:
        yield result
        index += 1
        result = begin + step * index

def ap_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    ap = itertools.count(result, step)
    if end is not None:
        ap = itertools.takewhile(lambda n: n < end, ap)
    return ap
