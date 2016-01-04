import asyncio

import aiohttp
from flags import FLAGS_GETTER_LINK, show, main, download_flag


@asyncio.coroutine
def get_img(name):
    url = FLAGS_GETTER_LINK.format(name)
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image


@asyncio.coroutine
def download_one(name):
    image = yield from get_img(name)
    show(name)
    download_flag(image, name)
    return name


def download_many(names_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(name) for name in sorted(names_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
