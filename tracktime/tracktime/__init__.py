from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('main', '/')
    config.add_route('counter_status', '/counter/status/')
    config.add_route('counter_start', '/counter/start/')
    config.add_route('counter_stop', '/counter/stop/{pk}/')
    config.add_route('counter_msg', '/counter/msg/{pk}/')
    config.add_route('entry_list', '/entry/{period}/')
    config.add_route('entry_remove', '/entry/remove/{pk}/')
    config.scan()
    return config.make_wsgi_app()
