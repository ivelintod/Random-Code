class Attempt:

    def __init__(self, name, info):
        self.name = name
        self.info = info

    def repr(self):
        return self.name + ' ' + self.info

