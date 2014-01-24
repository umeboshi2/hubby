import os
import cPickle as Pickle
from datetime import datetime

from hubby.util import legistar_id_guid

from base import BaseCollector

from people import PeopleCollector
from departments import DeptCollector
from meeting import MeetingCollector
from item import ItemCollector
from action import ActionCollector


class PickleCollector(object):
    def __init__(self):
        self.people = PeopleCollector()
        self.depts = DeptCollector()
        self.meeting = MeetingCollector()
        self.item = ItemCollector()
        self.action = ActionCollector()
        self.dir = 'data'

        self._collectors = dict(people=self.people,
                                depts=self.depts,
                                meeting=self.meeting,
                                item=self.item,
                                action=self.action)

    def _collector(self, type):
        return self._collectors[type]

    def _filename(self, type, id=None):
        if type == 'people':
            filename = 'people.pickle'
        elif type == 'depts':
            filename = 'departments.pickle'
        elif type == 'meeting':
            filename = 'meeting-%d.pickle' % id
        elif type == 'item':
            filename = 'item-%d.pickle' % id
        elif type == 'action':
            filename = 'action-%d.pickle' % id
        else:
            raise RuntimeError('unknown type')
        return os.path.join(self.dir, filename)

    def _dbname(self, type, id=None):
        if type == 'people':
            dbname = 'people'
        elif type == 'depts':
            dbname = 'departments'
        elif type == 'meeting':
            dbname = 'meeting-%d' % id
        elif type == 'item':
            dbname = 'item-%d' % id
        elif type == 'action':
            dbname = 'action-%d' % id
        else:
            raise RuntimeError('unknown type')
        return dbname

    def make_cache_object(self, type, link=None):
        from hubby.database import MainCache
        id = None
        if type in ['meeting', 'item', 'action']:
            id, guid = legistar_id_guid(link)
        filename = self._filename(type, id)
        dbname = self._dbname(type, id)
        if os.path.isfile(filename):
            content = Pickle.load(file(filename))
            now = datetime.now()
            mc = MainCache()
            mc.name = dbname
            mc.retrieved = now
            mc.updated = now
            mc.content = content
        else:
            raise RuntimeError, "No file present %s" % filename
        return mc
    
        
    def collect(self, type, link=None):
        id = None
        if type in ['meeting', 'item', 'action']:
            id, guid = legistar_id_guid(link)
        filename = self._filename(type, id)
        if not os.path.isfile(filename):
            print "Retrieving %s from legistar..." % filename
            collector = self._collector(type)
            if link is not None:
                print 'link is', link, type
                if not link.startswith('http'):
                    link = collector.url_prefix + link
                print "Retrieving", link
                collector.set_url(link)
            collector.collect()
            Pickle.dump(collector.result, file(filename, 'w'))
        return Pickle.load(file(filename))


class _MainCollector(PeopleCollector, DeptCollector,
                     MeetingCollector, ItemCollector,
                     ActionCollector):
    pass


class MainCollector(_MainCollector):
    def __init__(self):
        _MainCollector.__init__(self)
        self.dept_url = 'http://hattiesburg.legistar.com/Departments.aspx'
        self.people_url = 'http://hattiesburg.legistar.com/People.aspx'
        self.url_prefix = 'http://hattiesburg.legistar.com/'
        self._map = dict(people=PeopleCollector,
                         dept=DeptCollector,
                         meeting=MeetingCollector,
                         item=ItemCollector,
                         action=ActionCollector)

    def collect(self, ctype):
        self._map[ctype].collect(self)


if __name__ == "__main__":
    murl = 'http://hattiesburg.legistar.com/MeetingDetail.aspx?From=RSS&ID=209045&GUID=6F113835-7E47-432D-B3BA-2140AC586A6C'
    iurl = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1221728&GUID=9CC815CB-387A-42BF-B442-B80F953CB51E&Options=&Search='
    iurl2 = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1195041&GUID=8DB3A9EB-569C-477C-9F3B-B04EFD8AA955&Options=&Search='
    aurl = 'http://hattiesburg.legistar.com/HistoryDetail.aspx?ID=6153632&GUID=1376DD13-58E1-443A-9A2E-F218CE70C4B6'
    mc = MainCollector()
    mc.set_url(murl)
