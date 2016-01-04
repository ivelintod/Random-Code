from concurrent import futures

from flags import main, show, download_flag, get_img, FLAGS_GETTER_LINK

MAX_WORKERS = 20


def download_one(country):
    img = get_img(FLAGS_GETTER_LINK, country)
    show(country)
    download_flag(img, country)


def download_many(countries):
    workers = min(MAX_WORKERS, len(countries))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(list(countries)))
    return len(list(res))


if __name__ == '__main__':
    main(download_many)

