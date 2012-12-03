#!/usr/bin/env python
import os, sys

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from hubby.database import Base
from hubby.database import Meeting

from hubby.manager import ModelManager


here = os.getcwd()
settings = {'sqlalchemy.url' : 'sqlite:///%s/hubby.sqlite' % here}
engine = engine_from_config(settings)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

s = Session()
mm = ModelManager(s)
