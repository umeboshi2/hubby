from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from .database import (
    Base,
    )



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession = sessionmaker()
    settings['db.sessionmaker'] = DBSession
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    request_factory = 'hubby.request.AlchemyRequest'
    config = Configurator(settings=settings,
                          request_factory=request_factory,)
    config.include('cornice')
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
