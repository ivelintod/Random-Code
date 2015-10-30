from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
import sys
#LINK_REGEX = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")


class LinkCollector:

    def __init__(self, url):
        self.url = "http://" + urlparse(url).netloc
        self.visited_links = set()
        self.collected_links = {}

    def collect_links(self, path='/'):
        full_url = self.url + path
        self.visited_links.add(full_url)
        page = str(requests.get(full_url).text)
        soup = BeautifulSoup(page)
        links = [link.get('href') for link in soup.find_all('a')]
        links = {self.normalize_link(path, link) for link in links}
        unvisited_links = links.difference(self.visited_links)
        self.collected_links[full_url] = links
        for link in links:
            self.collected_links.setdefault(link, set())
        #print(links, self.visited_links, self.collected_links, unvisited_links)
        for link in unvisited_links:
            if link.startswith(self.url):
                self.collect_links(urlparse(link).path)

    def normalize_link(self, path, link):
        if link.startswith('http://'):
            return link
        elif link.startswith('/'):
            return self.url + link
        else:
            return self.url + path.rpartition('/')[0] + '/' + link

if __name__ == '__main__':
    collector = LinkCollector(sys.argv[1])
    collector.collect_links()
    for link, item in collector.collected_links.items():
        print('{}:{}\n'.format(link, item))

print(urlparse('http://localhost:8000/blog.html'))
