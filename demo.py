#!/usr/bin/env python
import os, sys
import cPickle as Pickle

from sqlalchemy import engine_from_config
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from hubby.database import Base
from hubby.database import Meeting, Item
from hubby.database import Person, Department

from hubby.collector.main import MainCollector
from hubby.manager import ModelManager
from hubby.util import legistar_id_guid


here = os.getcwd()
settings = {'sqlalchemy.url' : 'sqlite:///%s/hubby.sqlite' % here}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
mm = ModelManager(s)

people = s.query(Person).all()
if not len(people):
    print "adding people...."
    mm.add_people()
    s.commit()
    
depts = s.query(Department).all()
if not len(depts):
    print "adding departments....."
    mm.add_departments()
    s.commit()

from hubby.legistar import RSS_THIS_MONTH, RSS_YEAR_2011, RSS_YEAR_2012

y1 = RSS_YEAR_2011, 'y1.rss'
y2 = RSS_YEAR_2012, 'y2.rss'
m1 = RSS_THIS_MONTH, 'm1.rss'

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
            print "adding", entry.link
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
###meetings = qmeetings.all()
meetings = []
for meeting in meetings:
    print "Merging %d from legistar" % meeting.id
    mm.merge_meeting_from_legistar(meeting.id)
    s.commit()
    


            


items = {}
filename = 'items.pickle'
if os.path.isfile(filename):
    items = Pickle.load(file(filename))
else:
    for meeting in s.query(Meeting).all():
        print "Getting items for meeting", meeting.id
        print "link", meeting.link
        items[meeting.id] = mm.remote_legislation_items(meeting.link)
    Pickle.dump(items, file(filename, 'w'))
