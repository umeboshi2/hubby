#!/usr/bin/env python
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from hubby.database import Meeting, Item, Action
from hubby.database import Person, Department

from hubby.manager import ModelManager
from hubby.util import legistar_id_guid


def check_dupe_item(session, item):
    Dupe = True
    # FIXME straighten this out
    if 'id' not in item:
        print("Bad item", item)
        import pdb ; pdb.set_trace() # noqa
        return Dupe
    dbitem = session.query(Item).get(item['id'])
    if dbitem is None:
        return False
    filtered_keys = ['attachments', 'action_details']
    keys = [k for k in list(item.keys()) if k not in filtered_keys]
    for key in keys:
        if getattr(dbitem, key) != item[key]:
            Dupe = False
    return Dupe


class DatabaseManager(object):
    def __init__(self, session, collecter):
        self.session = session
        self.collecter = collecter
        self.manager = ModelManager(self.session)
        self.meeting = None
        self.parsed = None

    def add_people(self):
        people = self.session.query(Person).all()
        if not len(people):
            print("adding people........")
            people = self.collecter.collect('people')
            self.manager.add_collected_people(people)
            self.session.commit()

    def add_departments(self):
        depts = self.session.query(Department).all()
        if not len(depts):
            print("adding departments.....")
            depts = self.collecter.collect('depts')
            self.manager.add_collected_depts(depts)
            self.session.commit()

    def add_rss_meetings(self, url, rss=None):
        if rss is None:
            rss = self.manager.get_rss(url)
        for entry in rss.entries:
            id, guid = legistar_id_guid(entry.link)
            meeting = self.session.query(Meeting).get(id)
            if meeting is None:
                print("adding meeting {} from rss".format(id))
                try:
                    self.manager.add_meeting_from_rss(entry)
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
            else:
                print("Meeting {} already present.".format(id))

    def set_meeting(self, meeting):
        self.meeting = meeting
        self.parsed = self.collecter.collect('meeting', link=self.meeting.link)

    def add_meetings(self):
        meetings = self.session.query(Meeting).all()
        for meeting in meetings:
            self.set_meeting(meeting)
            self.add_meeting(meeting)
        self.session.commit()

    def add_meeting(self, meeting):
        for item in self.parsed['items']:
            self.add_meeting_item(item)
        self.manager._merge_collected_meeting_items(meeting, self.parsed)
        self.session.commit()

    def merge_nonfinal(self):
        filtered = or_(Meeting.minutes_status == None, # noqa
                       Meeting.minutes_status != 'Final')
        qmeetings = self.session.query(Meeting).filter(filtered)
        meetings = qmeetings.all()
        for meeting in meetings:
            collected = self.collecter.collect('meeting', link=meeting.link)
            self.manager._merge_collected_meeting(meeting, collected)
            print("Merging meeting %d" % meeting.id)
            self.session.commit()

    def add_meeting_item(self, parsed_item):
        item = self.collecter.collect('item', link=parsed_item['item_page'])
        if b'id' in item:
            sitem = {}
            for key in item:
                sitem[key.decode()] = item[key]
            item = sitem
        if not check_dupe_item(self.session, item):
            print("adding item %d to database." % item['id'])
            self.manager._add_collected_legislation_item(item)
        if 'action_details' not in item:
            action_details = []
        else:
            action_details = item['action_details']
        self.add_item_actions(item['id'], action_details)

    def add_item_actions(self, item_id, action_details):
        for link in action_details:
            action = self.collecter.collect('action', link=link)
            dbaction = self.session.query(Action).get(action['id'])
            if dbaction is None:
                print("adding action %d to database." % action['id'])
                self.manager.add_collected_action(item_id, action)
        self.session.commit()
