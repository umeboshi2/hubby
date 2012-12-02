import transaction

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

from leaflet.hubby.legistar import legistar_host
from leaflet.hubby.util import legistar_id_guid

from leaflet.models.base import DBSession
from leaflet.models.rssdata import Feed, FeedData
from leaflet.models.hubby import Department, Person
from leaflet.models.hubby import Meeting, Item, Action


from leaflet.hubby.collector import MainCollector



class ModelManager(object):
    def __init__(self, session):
        self.session = session

    def set_session(self, session):
        self.session = session

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
        

    
        
    
