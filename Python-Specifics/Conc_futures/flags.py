import os
import sys
import time

import requests
from bs4 import BeautifulSoup


NAME_GETTER_LINK = 'http://www.sciencekids.co.nz/pictures/flags.html'

FLAGS_GETTER_LINK = 'http://www.sciencekids.co.nz/images/pictures/flags680/{}.jpg'

DEF_NUM_OF_PROC_COUNTRIES = 40

country_names = []

DOWNL_DIR = 'downloads/'

def extract_country_names(link):
    html_body = requests.get(link).text
    soup = BeautifulSoup(html_body)
    pre_names = soup.select('a[href^="flags/"]')
    global country_names
    for i in range(1, DEF_NUM_OF_PROC_COUNTRIES, 2):
        country_names.append(pre_names[i].contents[0])
    return country_names


def download_flag(img, filename):
    path = os.path.join(DOWNL_DIR)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + filename, 'wb') as fp:
        fp.write(1000*img)


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def get_img(link, name):
    img = requests.get(link.format(name))
    if img.status_code != 200:
        img.raise_for_status()
    return img.content


def download_many(countries):
    for c in countries:
        img = get_img(FLAGS_GETTER_LINK, c)
        show(c)
        download_flag(img, c)
    return len(countries)


def main(download_many):
    extract_country_names(NAME_GETTER_LINK)
    t0 = time.time()
    length = download_many(country_names)
    elapsed = time.time() - t0
    print('{} flags were downloaded in {:.2f}s'.format(length, elapsed))


if __name__ == '__main__':
    main(download_many)
