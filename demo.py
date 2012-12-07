#!/usr/bin/env python
import os, sys

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from hubby.database import Base
from hubby.database import Meeting

from hubby.collector.main import MainCollector
from hubby.manager import ModelManager


here = os.getcwd()
settings = {'sqlalchemy.url' : 'sqlite:///%s/hubby.sqlite' % here}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
mm = ModelManager(s)

from hubby.legistar import RSS_THIS_MONTH, RSS_YEAR_2011, RSS_YEAR_2012

y1 = RSS_YEAR_2011
y2 = RSS_YEAR_2012
m1 = RSS_THIS_MONTH

rss = mm.get_rss(m1)
e = rss.entries[0]
mc = mm.remote_meeting(e.link)
mitem = mc['items'][0]

c = mm.remote_legislation_item(mitem['item_page'])

#link = i['item_page']
#c = mm.remote_legislation_item(link)

import cPickle as Pickle
if os.path.isfile('items.pickle'):
    items = Pickle.load(file('items.pickle'))
    
