# -*- coding: utf-8 -*-
import datetime
import configs


def GetTimeAsString(_time):
    time = _time
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    return "%s/%s/%s %s:%s:%s" % (year, month, day, hour, minute, second)


def GetTimestamp():
    return GetTimeAsString(datetime.datetime.now())


def IsValidFrequency(_frequency):
    _split = _frequency.split(':')
    if len(_split) != 3:
        return False
    _h, _m, _s = _split
    if (int(_h) > 0) or (int(_m) > 0) or (int(_s) > 0):
        if (int(_h) < 24) or (int(_m) < 60) or (int(_s) < 60):
            return True
    return False


def TimeUntilNextDownload(_id):
    _next_download_time = configs.GetValue(_id, 'next_download_time')
    _hours_Now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    _hours_Next = datetime.datetime.strptime(_next_download_time, "%Y/%m/%d %H:%M:%S")
    return _hours_Next-_hours_Now


def ShouldDownload(_id):
    _next_download_time = TimeUntilNextDownload(_id)
    if _next_download_time.total_seconds() < 0:
        return True
    else:
        return False


def SetNewDownloadTime(_id):
    _hours_Now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    # determine which scheduling type this download is:
    _download_type = configs.GetValue(_id, 'download_type')
    if _download_type == 'frequency':
        _frequency = configs.GetValue(_id, 'frequency')
        _hour, _minute, _second = _frequency.split(':')
        _td = datetime.timedelta(seconds=int(_second), minutes=int(_minute), hours=int(_hour))
        _new_time = GetTimeAsString(_hours_Now+_td)
        configs.SetValue(_id, 'next_download_time', _new_time)
    elif _download_type == 'hour':
        _day_today = GetTimestamp().split(' ')[0]
        _download_on_hour = configs.GetValue(_id, 'frequency')
        _hour, _minute, _second = _download_on_hour.split(':')
        _monday = configs.GetValue(_id, 'monday')
        _tuesday = configs.GetValue(_id, 'tuesday')
        _wednesday = configs.GetValue(_id, 'wednesday')
        _thursday = configs.GetValue(_id, 'thursday')
        _friday = configs.GetValue(_id, 'friday')
        _saturday = configs.GetValue(_id, 'saturday')
        _sunday = configs.GetValue(_id, 'sunday')
        _weekdayToday = datetime.datetime.now().weekday()
        _f_days = [_monday, _tuesday, _wednesday, _thursday, _friday, _saturday, _sunday]
        # Wrap weekdays so today is element 0
        _f_days_wrapped = []
        for i in _f_days[_weekdayToday:]:
            _f_days_wrapped.append(i)
        for i in _f_days[:_weekdayToday]:
            _f_days_wrapped.append(i)
        # check how many days until next set day:
        _days_to_add = 1
        for _d in _f_days_wrapped[1:]:  # [1:] to ignore today
            if _d == 'False':
                _days_to_add += 1
            else:
                break
        # Set new:
        _new_time = '%s %s:%s:%s' % (_day_today, _hour, _minute, _second)
        _new_time = datetime.datetime.strptime(_new_time, "%Y/%m/%d %H:%M:%S")
        _new_time = _new_time + datetime.timedelta(days=_days_to_add)
        _new_time = GetTimeAsString(_new_time)
        configs.SetValue(_id, 'next_download_time', _new_time)
    else:
        raise Exception('Invalid "download_type" in configs for id: %s' % _id)
