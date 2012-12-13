#!/usr/bin/env python
import os, sys
import cPickle as Pickle

from sqlalchemy import engine_from_config
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from hubby.database import Base
from hubby.database import Meeting, Item, Action, Attachment
from hubby.database import Person, Department

from hubby.collector.main import MainCollector
from hubby.collector.main import PickleCollector
from hubby.manager import ModelManager
from hubby.util import legistar_id_guid


if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    dbhost = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    dbport = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    dbuser = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
    dbpass = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    dburl = "postgresql://%s:%s@%s:%s/leaflet"
    dburl = dburl % (dbuser, dbpass, dbhost, dbport)
else:
    dburl = "postgresql://dbadmin@bard/leaflet"
    


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
    os.makedirs(pc.dir)
    
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

people = s.query(Person).all()
if not len(people):
    print "adding people........"
    people = pc.collect('people')
    mm.add_collected_people(people)
    s.commit()
    
depts = s.query(Department).all()
if not len(depts):
    print "adding departments....."
    depts = pc.collect('depts')
    mm.add_collected_depts(depts)
    s.commit()

from hubby.legistar import RSS_THIS_MONTH, RSS_YEAR_2011, RSS_YEAR_2012

y1 = RSS_YEAR_2011, 'data/y1.rss'
y2 = RSS_YEAR_2012, 'data/y2.rss'
m1 = RSS_THIS_MONTH, 'data/m1.rss'

ulist = [y1, y2, m1]
rsslist = []
for url, filename in ulist:
    if os.path.exists(filename):
        rss = Pickle.load(file(filename))
    else:
        rss = mm.get_rss(url)
        Pickle.dump(rss, file(filename, 'w'))
    rsslist.append(rss)
    
# add all meetings
for rss in rsslist:
    for entry in rss.entries:
        id, guid = legistar_id_guid(entry.link)
        meeting = s.query(Meeting).get(id)
        if meeting is None:
            print "adding meeting %d from rss" % id
            try:
                mm.add_meeting_from_rss(entry)
                s.commit()
            except IntegrityError:
                s.rollback()
        else:
            print "Meeting %d already present." % id
            
# merge all meeting info
filtered = or_(Meeting.minutes_status == None,
               Meeting.minutes_status != 'Final')
qmeetings = s.query(Meeting).filter(filtered)
meetings = qmeetings.all()
for meeting in meetings:
    collected = pc.collect('meeting', link=meeting.link)
    mm._merge_collected_meeting(meeting, collected)
    print "Merging meeting %d" % meeting.id
    s.commit()
    


meetings = s.query(Meeting).all()
for meeting in meetings:
    pmeeting = pc.collect('meeting', link=meeting.link)
    for mitem in pmeeting['items']:
        item = pc.collect('item', link=mitem['item_page'])
        if not check_dupe_item(item):
            print "adding item %d to database." % item['id']
            mm._add_collected_legislation_item(item)
        for link in item['action_details']:
            action = pc.collect('action', link=link)
            dbaction = s.query(Action).get(action['id'])
            if dbaction is None:
                print "adding action %d to database." % action['id']
                mm.add_collected_action(item['id'], action)
        s.commit()
    s.commit()
    mm._merge_collected_meeting_items(meeting, pmeeting)
    
# next we tie the items to the meetings
# todo
