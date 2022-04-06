# -*- coding: utf-8 -*-
import datetime

def GetTimestamp():
    time = datetime.datetime.now()
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    return "%s/%s/%s %s:%s:%s" % (year, month, day, hour, minute, second)

def IsValidFrequency(_frequency):
    try:
        _f_days = _frequency.split(' ')[0].split(',')
        _f_hours = _frequency.split(' ')[1]
        if('1' not in _f_days):
            return False
        _hour = int(_f_hours.split(':')[0])
        _minute = int(_f_hours.split(':')[1])
        _second = int(_f_hours.split(':')[2])
        if(_hour > 23):
            raise Exception("23 is max for hours")
        if(_minute > 59):
            raise Exception("59 is max for minutes")
        if(_second > 59):
            raise Exception("59 is max for seconds")
        return True
    except Exception as e:
        print(e)
        return False

def TimeUntilNextDownload(_last_download_time, _frequency):
    _weekdayToday = datetime.datetime.now().weekday()
    _f_days = _frequency.split(' ')[0].split(',')  # gets weekday freq: [1,1,1,1,1,1,1,1]
    _f_hour = _frequency.split(' ')[1]  # gets the hour: 08:00:00
    # Wrap the list around, so weekdaytoday is the first index
    _f_days_wrapped = []
    for i in _f_days[_weekdayToday:]:
        _f_days_wrapped.append(i)
    for i in _f_days[:_weekdayToday]:
        _f_days_wrapped.append(i)

    # to check if we're looking to the past, or future:
    _hours_Now = datetime.datetime.strptime(GetTimestamp().split(' ')[1], "%H:%M:%S")
    _hours_Last = datetime.datetime.strptime(_f_hour, "%H:%M:%S")

    # Calculate how many days until next match:
    _addToDelta = 0
    _today = False
    for i in range(7):
        if(_f_days_wrapped[i] == '1'):
            # if we're looking at the past, ignore today
            if(_hours_Now>_hours_Last):
                _today = True
            break
        else:
            _addToDelta += 1

    # split timedelta:
    _res = _hours_Last-_hours_Now
    _res_hours, _res_remainder = divmod(_res.seconds, 3600)
    _res_minutes, _res_seconds = divmod(_res_remainder, 60)

    # If hour passed already
    if(_hours_Now<_hours_Last):
        _dt_td = datetime.timedelta(days=_addToDelta, seconds=_res_seconds, minutes=_res_minutes, hours=_res_hours)
        return _dt_td
    else:
        if(_addToDelta > 0) or (_today):
            _dt_td = datetime.timedelta(days=_addToDelta, seconds=_res_seconds, minutes=_res_minutes, hours=_res_hours)
        else:
            _dt_td = datetime.timedelta(days=_addToDelta, seconds=0, minutes=0, hours=0)
        return _dt_td

def ShouldDownload(_last_download_time, _frequency):
    _weekdayToday = datetime.datetime.now().weekday()
    _f_days = _frequency.split(' ')[0].split(',')  # gets weekday freq: [1,1,1,1,1,1,1,1]
    _f_hour = _frequency.split(' ')[1]  # gets the hour: 08:00:00
    #
    _last_download_date = datetime.datetime.strptime(_last_download_time.split(' ')[0], "%Y/%m/%d")
    _today_download_date = datetime.datetime.strptime(GetTimestamp().split(' ')[0], "%Y/%m/%d")
    # Wrap the list around, so weekdaytoday is the first index
    _f_days_wrapped = []
    for i in _f_days[_weekdayToday:]:
        _f_days_wrapped.append(i)
    for i in _f_days[:_weekdayToday]:
        _f_days_wrapped.append(i)

    # to check if we're looking to the past, or future:
    _hours_Now = datetime.datetime.strptime(GetTimestamp().split(' ')[1], "%H:%M:%S")
    _hours_Last = datetime.datetime.strptime(_f_hour, "%H:%M:%S")

    # split timedelta:
    _res = _hours_Last-_hours_Now
    _res_hours, _res_remainder = divmod(_res.seconds, 3600)
    _res_minutes, _res_seconds = divmod(_res_remainder, 60)

    if(_f_days_wrapped[0] == '1'):
        # past
        if(_last_download_date<_today_download_date):
            return True
        # present
        elif(_last_download_date==_today_download_date):
            if(_hours_Now>_hours_Last):
                # this is supposed to download if we launch the app,
                #   and the download time is today,
                #   but we missed the hour, it would download, however:
                # If this condition is met, it'll keep downloading forever.
                # Not sure how to solve yet!
                # If this is not solved, if the app is not running,
                #   it will not download today's list if the time passed already.
                pass  # return True
            if(_hours_Now==_hours_Last):
                return True
        # future
        else:
            if(_hours_Now>_hours_Last):
                    return True
    return False
