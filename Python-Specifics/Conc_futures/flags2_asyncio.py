import asyncio
import collections
import tqdm

import aiohttp
from aiohttp import web
from flags import FLAGS_GETTER_LINK, show, main, download_flag


class CustomError(Exception):
    def __init__(self, country):
        self.country = country


@asyncio.coroutine
def get_img(name, link):
    url = link.format(name)
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image

    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.error.HTTPProcessingError(
            code=resp.status, message=resp.reason,
            headers=resp.headers)


@asyncio.coroutine
def download_one(name, url, semaphore, verbose):
    try:
        with (yield from semaphore):
            image = yield from get_img(name, url)
    except web.HTTPNotFound:
        #status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise CustomError(name) from exc
    else:
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None,
                download_flag, image, name)
        #download_flag(image, name)
        msg = 'OK'

    if verbose and msg:
        print(name, msg)


@asyncio.coroutine
def download_coro(names, url, verbose, concur_req):
    semaphore = asyncio.Semaphore(concur_req)

    to_do = [download_one(name, url, semaphore, verbose)
             for name in sorted(names)]

    to_do_iter = asyncio.as_completed(to_do)
    if verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(names))

    for future in to_do_iter:
        try:
            yield from future
        except CustomError as exc:
            country = exc.country

            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__

            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country, error_msg))


    return len(names)


def download_many(names):
    loop = asyncio.get_event_loop()
    coro = download_coro(names, FLAGS_GETTER_LINK, True, 1000)
    counts = loop.run_until_complete(coro)
    loop.close()

    return counts


if __name__ == '__main__':
    main(download_many)
