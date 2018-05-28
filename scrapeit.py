#!/usr/bin/env python
# from hubby.legistar import RSS_THIS_MONTH
from hubby.legistar import RSS_YEARLY_FEEDS

import os

import requests
import feedparser
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from hubby.database import Base

# from hubby.collector.main import MainCollector
from hubby.collector.main import PickleCollector
from hubby.dbmanager import DatabaseManager


runtimedir_varname = 'XDG_RUNTIME_DIR'
if 'TMPHUBBYDB' in os.environ and runtimedir_varname in os.environ:
    runtimedir = os.environ[runtimedir_varname]
    hubbydir = os.path.join(runtimedir, 'hubby')
    if not os.path.isdir(hubbydir):
        os.makedirs(hubbydir)
    dburl = "sqlite:///%(hubbydir)s/hubby.sqlite"
    dburl = dburl % dict(hubbydir=hubbydir)

else:
    dburl = "sqlite:///%(here)s/hubby.sqlite" % dict(here=os.getcwd())
    dburl = "postgresql://dbadmin@localhost/hubbytest"

here = os.getcwd()
print("dburl", dburl)
settings = {'sqlalchemy.url': dburl}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
pc = PickleCollector()
if not os.path.isdir(pc.dir):
    os.makedirs(pc.dir)

manager = DatabaseManager(s, pc)
manager.add_people()
manager.add_departments()


def get_rss_content(year, url):
    filename = "data/rss-{}.rss".format(year)
    if os.path.isfile(filename):
        content = open(filename).read()
    else:
        with open(filename, 'wb') as outfile:
            req = requests.get(url)
            if req.ok:
                outfile.write(req.content)
            else:
                msg = "Bad response from server {}".format(req.status)
                raise RuntimeError(msg)
        print("Saved {}".format(filename))
        content = req.content
    return content


# FIXME: this may not be the proper 2014 url
# y4 = RSS_YEAR_2014, 'data/y4.rss'
years = list(RSS_YEARLY_FEEDS.keys())
years.sort()
for year in years:
    url = RSS_YEARLY_FEEDS[year]
    content = get_rss_content(year, url)
    print("Adding meetings for {}".format(year))
    manager.add_rss_meetings('ignore', rss=feedparser.parse(content))

manager.add_meetings()
