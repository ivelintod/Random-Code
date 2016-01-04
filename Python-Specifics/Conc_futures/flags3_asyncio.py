import asyncio

import tqdm
import aiohttp
from aiohttp import web
from flags2_asyncio import download_coro, download_many, main, CustomError, download_flag, FLAGS_GETTER_LINK


json_countries_data = 'http://data.okfn.org/data/core/country-list/r/data.json'


@asyncio.coroutine
def unified_downloader(url):
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        cont_type = resp.headers.get('Content-type', '').lower()
        if 'json' in cont_type or url.endswith('json'):
            data = yield from resp.json()
        else:
            data = yield from resp.read()
        return data

    elif resp.status == 404:
        raise web.HTTPNotFound()

    else:
        raise aiohttp.errors.HttpProcessingError(
            code=resp.status, message=resp.reason,
            headers=resp.headers)


@asyncio.coroutine
def get_flag(url, name):
    print(url)
    url = url.format(name)
    return (yield from unified_downloader(url))


@asyncio.coroutine
def get_country(url, name): #url must provide json content
    metadata = yield from unified_downloader(url)
    for candidate in metadata:
        if candidate['Name'] == name:
            return candidate['Code']


@asyncio.coroutine
def download_one(country_name, urls, semaphore, verbose):
    image_url, country_url = urls
    print(image_url)
    try:
        with (yield from semaphore):
            image = yield from get_flag(image_url, country_name)

        with (yield from semaphore):
            country_code = yield from get_country(country_url, country_name)

    except web.HTTPNotFound:
        msg = 'not found'

    except Exception as exc:
        raise CustomError(country_name) from exc

    else:
        msg = 'OK'
        loop = asyncio.get_event_loop()
        save_name = '{}-{}.jpeg'.format(country_name, country_code)
        loop.run_in_executor(None,
            download_flag, image, save_name)

    if verbose and msg:
        print(country_name, msg)


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


def download_many(country_names):
    loop = asyncio.get_event_loop()
    coro = download_coro(country_names, (FLAGS_GETTER_LINK, json_countries_data), True, 500)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts


if __name__ == '__main__':
    main(download_many)


