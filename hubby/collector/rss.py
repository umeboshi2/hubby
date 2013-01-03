import feedparser

from hubby.util import get_rss_feed


class RssCollector(object):
    def __init__(self):
        self.rss = None
        self.info = None
        self.entries = []

    def get_rss(self, url):
        content, info = get_rss_feed(url)
        self.info = info
        self.rss = feedparser.parse(content)
        self.entries = self.rss.entries
