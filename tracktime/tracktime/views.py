import transaction
from datetime import datetime, date, timedelta

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    TrackTimeEntry,
)
from .utils import time_diff_in_second

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


@view_config(route_name='main', renderer='templates/main.pt')
def main(request):
    return {'entries': get_entries('today')}


@view_config(route_name='counter_status', renderer='json')
def counter_status(request):
    response = {
        'status': 'new',
    }
    last = DBSession.query(TrackTimeEntry).order_by('-id').first()
    if last and last.stop_time is None:
        response['status'] = 'continue'
        response['sec'] = time_diff_in_second(datetime.now(), last.start_time)
        response['id'] = last.id

    return response


@view_config(route_name='counter_start', renderer='json')
def counter_start(request):
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
    if entry:
        msg = request.POST.get('data', '')
        entry.msg = msg
        DBSession.add(entry)
        transaction.commit()
        response['status'] = 1
    return response


@view_config(route_name='entry_list', renderer='json')
def entry_list(request):
    period = request.matchdict['period']
    return {'entries': get_entries(period)}


@view_config(route_name='entry_remove', renderer='json')
def entry_remove(request):
    response = {'status':  0}
    pk = request.matchdict['pk']
    entry = DBSession.query(TrackTimeEntry).get(pk)
    if entry:
        DBSession.delete(entry)
        transaction.commit()
        response['status'] = 1

    return response


def get_entries(period):
    entries = []
    today = date.today()
    if period == 'today':
        query = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= today).all()
    if period == 'yesterday':
        yesterday = today - timedelta(days=1)
        query = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= yesterday,
            TrackTimeEntry.start_time < today).all()
    if period == 'week':
        week = today - timedelta(days=7)
        query = DBSession.query(TrackTimeEntry).filter(
            TrackTimeEntry.start_time >= week).all()
    for obj in query:
        entries.append({
            'id': obj.id,
            'time': time_diff_in_second(obj.stop_time, obj.start_time),
            'msg': obj.msg if obj.msg else '-',
        })
    return entries
