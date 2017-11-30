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
    serve_static_assets = False
    if 'serve_static_assets' in settings and settings['serve_static_assets'].lower() == 'true':
        serve_static_assets = True
    if serve_static_assets:
        print "Serving static assets from pyramid.", serve_static_assets
        config.add_static_view(name='client',
                               path=settings['static_assets_path'])
    config.add_route('home', '/')
    config.add_view('hubby.views.client.ClientView',
                    route_name='home',)  
    config.add_route('meeting_calendar', '/hubcal')
    config.add_view('hubby.views.main.MeetingCalendarViewer',
                    route_name='meeting_calendar',
                    renderer='json',)
    
    config.add_route('meeting_calendar_ts', '/hubcal1')
    config.add_view('hubby.views.main.MeetingCalendarViewer',
                    route_name='meeting_calendar_ts',
                    renderer='json',)
    
    config.scan()
    return config.make_wsgi_app()
