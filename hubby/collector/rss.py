import feedparser
import requests

from hubby.util import get_rss_feed


class RssCollector(object):
    def __init__(self):
        self.rss = None
        self.info = None
        self.entries = []

    def get_rss(self, url):
        r = requests.get(url)
        self.content = r.content
        self.info = r.headers
        self.rss = feedparser.parse(r.content)
        self.entries = self.rss.entries
