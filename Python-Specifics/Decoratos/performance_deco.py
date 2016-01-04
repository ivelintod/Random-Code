import time
import functools

def performance(filename):
    def decorate(func):
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - t0
            name = func.__name__
            log_str = '{} was called and took {:.2f} seconds to complete\n'.format(name, elapsed)
            with open(filename, 'a') as fp:
                fp.write(log_str)
            return result
        return clocked
    return decorate


@performance('performance_log.txt')
def something_heavy():
    time.sleep(2.1)
    return 'I am done!'


@performance('performance_log.txt')
def countdown(n):
    while n > 0:
        n -= 1
    return 'I am done too'

print(something_heavy())
print(countdown(10000000))

