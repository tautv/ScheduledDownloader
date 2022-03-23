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

def FrequencyTimeDelta(_frequency):
    _day = int(_frequency.split(' ')[0])
    _time = _frequency.split(' ')[1]
    _hour = int(_time.split(':')[0])
    _minute = int(_time.split(':')[1])
    _second = int(_time.split(':')[2])
    if(_hour > 23):
        raise Exception("23 is max for hours")
    if(_minute > 59):
        raise Exception("59 is max for minutes")
    if(_second > 59):
        raise Exception("59 is max for seconds")
    return datetime.timedelta(days=_day, seconds=_second, minutes=_minute, hours=_hour)

def IsValidFrequency(_frequency):
    try:
        _fr = FrequencyTimeDelta(_frequency)
        if(_fr > datetime.timedelta(seconds=59)):
            return True
        else:
            return False
    except Exception as e:
        return False

def TimeUntilNextDownload(_last_download_time, _frequency):
    print('=============================')
    _weekdayToday = datetime.datetime.now().weekday()
    _f_days = _frequency.split(' ')[0].split(',') # gets weekday freq: [1,1,1,1,1,1,1,1]
    _f_hour = _frequency.split(' ')[1] # gets the hour: 08:00:00
    _todaysDownload = '%s %s' % (GetTimestamp().split(' ')[0], _f_hour)
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
    for i in range(7):
        if(_f_days_wrapped[i] == '1'):
            # if we're looking at the past, ignore today and add one day to delta
            if(_hours_Now>_hours_Last):
                _addToDelta +=1
            break
        else:
            _addToDelta+=1

    # split timedelta:
    _res = _hours_Last-_hours_Now
    _res_hours, _res_remainder = divmod(_res.seconds, 3600)
    _res_minutes, _res_seconds = divmod(_res_remainder, 60)

    # If hour passed already
    if(_hours_Now<_hours_Last):
        _dt_td = datetime.timedelta(days=_addToDelta, seconds=_res_seconds, minutes=_res_minutes, hours=_res_hours)
        return _dt_td
    else:
        if(_addToDelta>0):
            _dt_td = datetime.timedelta(days=_addToDelta, seconds=_res_seconds, minutes=_res_minutes, hours=_res_hours)
        else:
            _dt_td = datetime.timedelta(days=_addToDelta, seconds=0, minutes=0, hours=0)
        return _dt_td

def ShouldDownload(_last_download_time, _frequency):
    now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    last = datetime.datetime.strptime(_last_download_time, "%Y/%m/%d %H:%M:%S")
    diff = now-last
    freq_td = FrequencyTimeDelta(_frequency)
    if(diff>freq_td):
        return True
    else:
        return False




# these should all work:
# print(TimeUntilNextDownload('2022/03/22 08:00:00', '1,0,0,0,0,0,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,1,0,0,0,0,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,1,0,0,0,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,1,0,0,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,1,0,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,0,1,0 14:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,0,0,1 14:00:00'))
# print('-')
# print(TimeUntilNextDownload('2022/03/22 08:00:00', '1,0,0,0,0,0,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,1,0,0,0,0,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,1,0,0,0,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,1,0,0,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,1,0,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,0,1,0 08:00:00'))
# print(TimeUntilNextDownload('2089/01/01 08:00:00', '0,0,0,0,0,0,1 08:00:00'))
