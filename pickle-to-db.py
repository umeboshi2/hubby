#!/usr/bin/env python
import os, sys
import cPickle as Pickle
from datetime import datetime

from sqlalchemy import engine_from_config
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from hubby.database import Base
from hubby.database import Meeting, Item, Action, Attachment
from hubby.database import Person, Department
from hubby.database import MainCache

from hubby.collector.main import MainCollector
from hubby.collector.main import PickleCollector
from hubby.manager import ModelManager
from hubby.util import legistar_id_guid

#dburl = "postgresql+psycopg2://dbadmin:dbadmin@cypress/hubby"
dburl = "sqlite:///%(here)s/hubby.sqlite" % dict(here=os.getcwd())


here = os.getcwd()
settings = {'sqlalchemy.url' : 'sqlite:///%s/hubby.sqlite' % here}
settings = {'sqlalchemy.url' : dburl}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
mm = ModelManager(s)
pc = PickleCollector()

if not os.path.isdir(pc.dir):
    raise RuntimeError, "We assume the pickled files exist."

    
def check_dupe_item(item):
    dbitem = s.query(Item).get(item['id'])
    if dbitem is None:
        return False
    filtered_keys = ['attachments', 'action_details']
    keys = [k for k in item.keys() if k not in filtered_keys]
    Dupe = True
    for key in keys:
        if getattr(dbitem, key) != item[key]:
            Dupe = False
    return Dupe

people = pc.make_cache_object('people')
depts = pc.make_cache_object('depts')

from hubby.legistar import RSS_THIS_MONTH, RSS_YEAR_2011, RSS_YEAR_2012
from hubby.legistar import RSS_YEAR_2013

y1 = 'rss-2011', 'data/y1.rss'
y2 = 'rss-2012', 'data/y2.rss'
y3 = 'rss-2013', 'data/y3.rss'
m1 = 'rss-this-month', 'data/m1.rss'

ulist = [y1, y2, y3, m1]

cached_rss = list()
for name, filename in ulist:
    now = datetime.now()
    rss = Pickle.load(file(filename))
    mc = MainCache()
    mc.name = name
    mc.retrieved = now
    mc.updated = now
    mc.content = rss
    cached_rss.append(mc)
    

cached_meetings = list()
cached_items = list()
cached_actions = list()

# merge all meeting info
filtered = or_(Meeting.minutes_status == None,
               Meeting.minutes_status != 'Final')
qmeetings = s.query(Meeting).filter(filtered)
meetings = qmeetings.all()

meetings = s.query(Meeting).all()
for meeting in meetings:
    cached = pc.make_cache_object('meeting', link=meeting.link)
    cached_meetings.append(cached)
    pmeeting = cached.content
    for mitem in pmeeting['items']:
        item = pc.make_cache_object('item', link=mitem['item_page'])
        name = item.name
        if name not in [i.name for i in cached_items]:
            #print "adding item %d to list." % item.content['id']
            cached_items.append(item)
        else:
            print "Ignoring item %d" % item.content['id']
        for link in item.content['action_details']:
            action = pc.make_cache_object('action', link=link)
            name = action.name
            if name not in [a.name for a in cached_actions]:
                #print "adding action %d to list." % action.content['id']
                cached_actions.append(action)
            else:
                print "Ignoring action %d" % action.content['id']

dbobjects = [people, depts] + cached_rss
dbobjects += cached_meetings + cached_items + cached_actions

for o in dbobjects:
    s.add(o)

s.commit()

