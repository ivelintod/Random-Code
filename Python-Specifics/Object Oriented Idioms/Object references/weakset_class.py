import weakref


class InstCount:

    live_instances = weakref.WeakSet()

    def __init__(self, name):
        self.name = name
        InstCount.live_instances.add(self)

    def __eq__(self, other):
        return self.__dict__.keys() == other.__dict__.keys()

    def __hash__(self):
        return hash(tuple(self.__dict__.keys()))

    def repr(self):
        return 'InstCount(%r)' % self.name

