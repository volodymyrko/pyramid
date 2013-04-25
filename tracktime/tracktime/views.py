import transaction
from datetime import datetime, date, timedelta

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    TrackTimeEntry,
    )
from .utils import time_diff_in_second

DATETIME_FORMAT = "%Y-%m-%d %H:%M"

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'tracktime'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tracktime_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='test', renderer='templates/test.pt')
def test_view(request):
    return {'one': 'one', 'project': 'tracktime'}


@view_config(route_name='counter_status', renderer='json')
def counter_status(request):
    #import pdb; pdb.set_trace()
    response = {
        'status': 'new',
        }
    last = DBSession.query(TrackTimeEntry).order_by('-id').first()
    if last and last.stop_time is None:
        response['status'] = 'continue'
        response['sec'] = time_diff_in_second(datetime.now(), last.start_time)
        response['id'] = last.id
    

    return response

#session = DBSession()

@view_config(route_name='counter_start', renderer='json')
def counter_start(request):
    #import pdb; pdb.set_trace()
    
    last = DBSession.query(TrackTimeEntry).order_by('-id').first()
    if last and last.stop_time is None:
        response = {'status': 0}
    else:
        entry = TrackTimeEntry()
        DBSession.add(entry)
        transaction.commit()

        response = {
            'status': 1,
            'id': entry.id
            }

    return response

    
@view_config(route_name='counter_stop', renderer='json')
def counter_stop(request):
    response = {
        'status': 0,
    }
    pk = request.matchdict['pk']
    entry = DBSession.query(TrackTimeEntry).get(pk)
    if entry:
        entry.stop_time = datetime.now()
        DBSession.add(entry)
        transaction.commit()
        response['status'] = 1
    return response

    
@view_config(route_name='counter_msg', renderer='json')
def counter_msg(request):
    response = {
        'status': 0,
    }
    pk = request.matchdict['pk']
    entry = DBSession.query(TrackTimeEntry).get(pk)
    #import pdb; pdb.set_trace()
    if entry:
        msg = request.POST.get('data')
        if msg:
            entry.msg = msg
            DBSession.add(entry)
            transaction.commit()
            response['status'] = 1
    return response


@view_config(route_name='entry_list', renderer='json')
def entry_list(request):

    response = {
        'entries': []
    }
    entries = []
    period = request.matchdict['period']
    #import pdb; pdb.set_trace()
    today = date.today()
    if period == 'today':
        entries = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= today).all()
    if period == 'yesterday':
        yesterday = today - timedelta(days=1)
        entries = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= yesterday,
            TrackTimeEntry.start_time < today).all()
    if period == 'week':
        week = today - timedelta(days=7)
        entries = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= week).all()
    for obj in entries:
        response['entries'].append({
            'id': obj.id,
            'start_time': obj.start_time.strftime(DATETIME_FORMAT),
            'stop_time': obj.stop_time.strftime(DATETIME_FORMAT),
            'msg': obj.msg,
        })
    return response

