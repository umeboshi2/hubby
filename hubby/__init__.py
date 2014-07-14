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
    #config.add_static_view('static', 'client', cache_max_age=3600)
    #config.add_static_view(settings['static_assets'], 'hubby:client')
    config.add_static_view(name='client', path=settings['static_assets_path'])
    config.add_route('home', '/')
    config.add_view('hubby.views.client.ClientView',
                    route_name='home',)
    config.add_route('meeting_calendar', '/hubcal')
    config.add_view('hubby.views.main.MeetingCalendarViewer',
                    route_name='meeting_calendar',
                    renderer='json',)
    
    config.scan()
    return config.make_wsgi_app()
