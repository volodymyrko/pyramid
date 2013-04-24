import time
from datetime import datetime


def time_diff_in_second(time1, time2):
    if not isinstance(time1, datetime):
        return -1
    if not isinstance(time2, datetime):
        return -1
    if time2 > time1:
        return -1
    t1 = time.mktime(time1.timetuple())
    t2 = time.mktime(time2.timetuple())
    return int(t1-t2)
