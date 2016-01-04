from encrypt_deco import *
import datetime


def log(filename):
    def decorate(func):
        with open(filename, 'a') as fp:
            line = '%s was called at %s\n' % (func.__name__, datetime.datetime.now())
            fp.write(line)
        return func
    return decorate

get_low = log('log.txt')(get_low)
print(get_low())


