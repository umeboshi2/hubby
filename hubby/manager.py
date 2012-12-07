import transaction

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

from hubby.legistar import legistar_host
from hubby.util import legistar_id_guid
from hubby.util import make_true_date

from hubby.database import Department, Person
from hubby.database import Meeting, Item, Action

from hubby.collector import MainCollector
from hubby.collector.rss import RssCollector



class ModelManager(object):
    def __init__(self, session):
        self.session = session

    def set_session(self, session):
        self.session = session

    def collector(self):
        return MainCollector()
    
    # entry is rss entry
    def add_meeting_from_rss(self, entry):
        transaction.begin()
        meeting = Meeting()
        meeting.title = entry.title
        meeting.link = entry.link
        meeting.rss = entry
        meeting.id, meeting.guid = legistar_id_guid(entry.link)
        self.session.add(meeting)
        self.session.flush()
        transaction.commit()

    # retrieve basic meeting info from
    # meeting details page on legistar.
    # the link is from the rss entry
    def remote_meeting(self, link):
        collector = self.collector()
        collector.set_url(link)
        collector.collect('meeting')
        return collector.meeting

    def remote_meeting_info(self, link):
        meeting = self.remote_meeting(link)
        info = meeting['info']
        return info
    
    def remote_meeting_items(self, link):
        meeting = self.remote_meeting(link)
        items = meeting['items']
        return items

    
    # link is relative from legistar prefix
    def _remote_legislation_item(self, link):
        collector = self.collector()
        url = collector.url_prefix + link
        collector.set_url(url)
        collector.collect('item')
        return collector.item

    # link is relative url to item page
    def remote_legislation_item(self, link):
        item = self._remote_legislation_item(link)
        # add id, guid to item
        id, guid = legistar_id_guid(link)
        item['id'], item['guid'] = legistar_id_guid(link)
        for key in ['introduced', 'on_agenda', 'passed']:
            if key in item and item[key]:
                item[key] = make_true_date(item[key])
        return item

    # link is full url to meeting
    def remote_legislation_items(self, link):
        meeting_items = self.remote_meeting_items(link)
        leg_items = []
        for item in meeting_items:
            item_page = item['item_page']
            leg_item = self.remote_legislation_item(item_page)
            leg_items.append(leg_item)
        return leg_items
        
    
    def merge_meeting_from_legistar(self, id):
        collector = MainCollector()
        transaction.begin()
        meeting = self.session.query(Meeting).filter_by(id=id).one()
        collector.set_url(meeting.link)
        collector.collect('meeting')
        info = collector.result['info']
        for key in ['id', 'guid', 'date', 'time', 'link',
                    'dept_id', 'agenda_status', 'minutes_status']:
            value = info[key]
            setattr(meeting, key, value)
        self.session.merge(meeting)
        self.session.flush()
        transaction.commit()
    
    def add_departments(self):
        collector = MainCollector()
        collector.collect('dept')
        transaction.begin()
        for dept_info in collector.result:
            id, guid, name = dept_info
            dept = Department(id, guid)
            dept.name = name
            self.session.add(dept)
        self.session.flush()
        transaction.commit()

    def add_people(self):
        collector = MainCollector()
        collector.collect('people')
        transaction.begin()
        for pinfo in collector.result:
            person = Person()
            for key in pinfo:
                setattr(person, key, pinfo[key])
            self.session.add(person)
        self.session.flush()
        transaction.commit()
        

    def get_rss(self, url):
        collector = RssCollector()
        collector.get_rss(url)
        return collector
    
    # here item is an item collected from
    # legistar
    def add_new_legislation_item(self, item):
        transaction.begin()
        dbitem = Item()
        for key in item:
            setattr(dbitem, key, item[key])
        self.session.add(dbitem)
        self.session.flush()
        transaction.commit()
    
