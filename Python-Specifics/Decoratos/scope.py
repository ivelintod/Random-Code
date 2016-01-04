b = 6

def f(a):
    global b
    print(a)
    print(b)
    b = 9


class Averager:

    def __init__(self):
        #self.series = []
        self.count = 0
        self.total = 0

    def __call__(self, number):
        self.total += number
        self.count += 1
        return self.total / self.count
        #return sum(self.series) / len(self.series)

avg = Averager()
#print(avg(10))
#print(avg(11))
#print(avg(12))


def _make_averager():

    series = []

    def average(number):
        series.append(number)
        total = len(series)
        return sum(series) / total

    return average


def make_averager():

    #count = 0
    #total = 0
    keeper = {'count': 0, 'total': 0}

    def average(new_value):
        #nonlocal count, total
        #count += 1
        #total += new_value
        keeper['count'] += 1
        keeper['total'] += new_value
        return keeper['total'] / keeper['count']

    return average

