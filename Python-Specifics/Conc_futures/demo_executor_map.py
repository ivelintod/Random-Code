from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {:.2f}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    display('Starting....')
    executor = futures.ThreadPoolExecutor(max_workers=1)
    results = executor.map(loiter, range(5))
    display('results: ', results)
    display('Waiting for individual results: ')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
