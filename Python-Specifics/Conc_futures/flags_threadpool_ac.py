from concurrent import futures

from flags_threadpool import download_one, main


def download_many(countries):
    futures_list = []
    with futures.ThreadPoolExecutor(10) as executor:
        for c in countries:
            fut = executor.submit(download_one, c)
            futures_list.append(fut)
            msg = '{} scheduled for execution'
            print(msg.format(fut))

        for future in futures.as_completed(futures_list):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
    return len(futures_list)


if __name__ == '__main__':
    main(download_many)
