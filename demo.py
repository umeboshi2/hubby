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
    dburl = "postgresql://dbadmin@bard/hubby"
    


here = os.getcwd()
settings = {'sqlalchemy.url' : 'sqlite:///%s/hubby.sqlite' % here}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
mm = ModelManager(s)
pc = PickleCollector()

people = s.query(Person).all()
depts = s.query(Department).all()
