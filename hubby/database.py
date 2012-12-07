from sqlalchemy import Sequence, Column, ForeignKey

# column types
from sqlalchemy import Integer, String, Unicode
from sqlalchemy import Boolean, Date, LargeBinary
from sqlalchemy import PickleType
from sqlalchemy import Enum
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

####################################
## Data Types                     ##
####################################



FileType = Enum('agenda', 'minutes', 'attachment',
                name='file_type')

AgendaItemType = Enum('presentation', 'policy', 'routine', 'unknown',
                      name='agenda_item_type')

VoteType = Enum('Yea', 'Nay', 'Abstain', 'Absent', 'Present',
                name='vote_type')

AgendaItemTypeMap = dict(V='presentation', VI='policy',
                         VII='routine')

####################################
## Tables                         ##
####################################

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    guid = Column(String)
    name = Column(String)
    
    def __init__(self, id, guid):
        self.id = id
        self.guid = guid
        self.name = None

    def __repr__(self):
        return '<Dept: %d - %s>' % (self.id, self.name)

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    website = Column(String)
    photo_link = Column(String)
    notes = Column(String)

    def __init__(self):
        self.id = None
        self.guid = None
        self.firstname = None
        self.lastname = None
        self.website = None
        self.photo_link = None
        self.notes = None

    def __repr__(self):
        msg = '<Person: %d (%s %s)>'
        return msg  % (self.id, self.firstname, self.lastname)
    

class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    title = Column(String)
    date = Column(Date)
    time = Column(String)
    link = Column(String)
    dept_id = Column(Integer, ForeignKey('departments.id'))
    agenda_status = Column(String)
    minutes_status = Column(String)
    rss = Column(PickleType)
    updated = Column(DateTime)
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.title = None
        self.date = None
        self.time = None
        self.link = None
        self.dept_id = None
        self.agenda_link = None
        self.agenda_status = None
        self.minutes_link = None
        self.minutes_status = None
        self.rss = None
        self.updated = None
        
    def __repr__(self):
        return "<Meeting(%d): '%s'>" % (self.id, self.title)
    
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    file_id = Column(String)
    filetype = Column(String)
    name = Column(Unicode)
    title = Column(Unicode)
    status = Column(String)
    passed = Column(Date)
    on_agenda = Column(Date)
    introduced = Column(Date)
    acted_on = Column(Boolean)
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.file_id = None
        self.filetype = None
        self.name = None
        self.title = None
        self.status = None
        self.passed = None
        self.on_agenda = None
        self.introduced = None
        self.acted_on = False

    def __repr__(self):
        return "<Item: %s, id: %d>" % (self.file_id, self.id)
    
class MeetingItem(Base):
    __tablename__ = 'meeting_item'

    meeting_id = Column('meeting_id', Integer,
                        ForeignKey('meetings.id'),
                        primary_key=True)
    item_id = Column('item_id', Integer,
                     ForeignKey('items.id'),
                     primary_key=True)

    type = Column('type', AgendaItemType)
    order = Column('order', Integer)
    # I decided to consider keeping track of item
    # versions, and it probably should go in the
    # items table, but for now it is here.
    version = Column('version', Integer)
    
    def __init__(self, meeting_id, item_id):
        self.meeting_id = meeting_id
        self.item_id = item_id
        self.type = None
        self.order = None
        

    def __repr__(self):
        return "<MeetingItem %d:%d>" % (self.meeting_id, self.item_id)
    
    
class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    file_id = Column(String)
    filetype = Column(String)
    mover = Column(String)
    seconder = Column(String)
    result = Column(String)
    agenda_note = Column(String)
    minutes_note = Column(String)
    action = Column(String)
    action_text = Column(Unicode)
    #item_id = Column(Integer, ForeignKey('items.id'))
    
    # related
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.file_id = None
        self.filetype = None
        self.mover = None
        self.seconder = None
        self.result = None
        self.agenda_note = None
        self.minutes_note = None
        self.action = None
        self.action_text = None
        
    def __repr__(self):
        return "<Action: %s, id: %d>" % (self.file_id, self.id)
    

class ItemAction(Base):
    __tablename__ = 'item_action'

    item_id = Column('item_id', Integer,
                     ForeignKey('items.id'),
                     primary_key=True)
    action_id = Column('action_id', Integer,
                        ForeignKey('actions.id'),
                        primary_key=True)

    def __init__(self, item_id, action_id):
        self.item_id = item_id
        self.action_id = action_id
        

    def __repr__(self):
        return "<ItemAction %d:%d>" % (self.item_id, self.action_id)
    

class ActionVote(Base):
    __tablename__ = 'action_vote'

    action_id = Column('action_id', Integer,
                       ForeignKey('actions.id'),
                       primary_key=True)
    person_id = Column('person_id', Integer,
                       ForeignKey('people.id'),
                       primary_key=True)
    vote = Column('vote', VoteType)

    def __init__(self, action_id, person_id, vote):
        self.action_id = action_id
        self.person_id = person_id
        self.vote = vote

    def __repr__(self):
        infotuple = self.action_id, self.person_id, self.vote
        return "<ActionVote %d:%d  %s>" % infotuple


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer,
                primary_key=True)
    http_info = Column(PickleType)
    content = Column(LargeBinary)
    link = Column(String)

    def __init__(self):
        self.id = None
        self.http_info = None
        self.content = None
        self.link = None
        
    def __repr__(self):
        return "<File:  id: %d>" % self.id
    
    
    
class Agenda(Base):
    __tablename__ = 'agendas'

    id = Column(Integer, ForeignKey('meetings.id'),
                primary_key=True)
    guid = Column(String)
    http_info = Column(PickleType)
    content = Column(LargeBinary)
    link = Column(String)
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.http_info = None
        self.content = None
        self.link = None
        
    def __repr__(self):
        return "<Agenda:  id: %d>" % self.id
    
    
class Minutes(Base):
    __tablename__ = 'minutes'

    id = Column(Integer, ForeignKey('meetings.id'),
                primary_key=True)
    guid = Column(String)
    http_info = Column(PickleType)
    content = Column(LargeBinary)
    link = Column(String)
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.http_info = None
        self.content = None
        self.link = None
        
    def __repr__(self):
        return "<Minutes:  id: %d>" % self.id
    
    
class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    name = Column(String)
    http_info = Column(PickleType)
    content = Column(LargeBinary)
    link = Column(String)
    item_id = Column(Integer, ForeignKey('items.id'))
    
    def __init__(self):
        self.id = None
        self.guid = None
        self.name = None
        self.http_info = None
        self.content = None
        self.link = None
        self.item_id = None
        
    def __repr__(self):
        return "<Attachment:  id: %d>" % self.id


class Tag(Base):
    __tablename__ = 'tagnames'

    name = Column(String, primary_key=True)

    def __init__(self):
        self.name = None

    def __repr__(self):
        return "<Tag: %s>" % self.name
    

class ItemTag(Base):
    __tablename__ = 'item_tags'

    id = Column(Integer, ForeignKey('items.id'),
                primary_key=True)
    tag = Column(String, ForeignKey('tagnames.name'),
                 primary_key=True)

    def __init__(self):
        self.id = None
        self.tag = None

    def __repr__(self):
        return "<ItemTag: %s:%s>" % (self.id, self.tag)
    
    
#######################################################
#######################################################

# Meeting relationships
meeting_backref = backref('meeting', uselist=False)

Meeting.dept = relationship(Department,
                            backref=meeting_backref)

Meeting.items = relationship(Item, backref='meetings',
                             order_by=Item.id,
                             secondary='meeting_item')

Meeting.meeting_items = relationship(MeetingItem)

Meeting.agenda = relationship(Agenda, uselist=False,
                              backref=meeting_backref)
Meeting.minutes = relationship(Minutes, uselist=False,
                               backref=meeting_backref)



# MeetingItem relationships
MeetingItem.meeting = relationship(Meeting)
MeetingItem.item = relationship(Item)


# Item relationships
Item.actions =  relationship(Action, backref='items',
                             order_by=Action.id,
                             secondary='item_action')

Item.attachments = relationship(Attachment, backref='item',
                                order_by=Attachment.id)


# Action relationships
Action.item = relationship(Item, backref='items',
                           secondary='item_action')

