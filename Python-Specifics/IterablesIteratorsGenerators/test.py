class TS:
    def __init__(self):
        self.container = [1, 2, 3, 4, 5]
        self.index = -1

    def __next__(self):
        #while True:
        try:
            self.index += 1
            return self.container[self.index]
        except IndexError:
            raise StopIteration()

    def __iter__(self):
        return self



class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    def __iter__(self):
        return self


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


def grouper(results):
    while True:
        key = yield
        results[key] = yield from averager()


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        item = yield average
        if item is None:
            break
        total += item
        count += 1
        average = total / count
    return average


def client(data):
    results = {}
    group = grouper(results)
    group.send(None)
    for key, values in data.items():
        group.send(key)
        for value in values:
            a = group.send(value)
            print(a)
        group.send(None)
    print(results)


if __name__ == '__main__':
    client(data)
