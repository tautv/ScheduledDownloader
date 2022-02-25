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
        print(_fr)
        print(type(_fr))
        if(_fr > datetime.timedelta(seconds=59)):
            return True
        else:
            return False
    except Exception as e:
        return False

def TimeUntilNextDownload(_last_download_time, _frequency):
    now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    last = datetime.datetime.strptime(_last_download_time, "%Y/%m/%d %H:%M:%S")
    diff = now-last
    freq_td = FrequencyTimeDelta(_frequency)
    if (freq_td>diff):
        return freq_td-diff
    else:
        return '00:00:00'

def ShouldDownload(_last_download_time, _frequency):
    now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    last = datetime.datetime.strptime(_last_download_time, "%Y/%m/%d %H:%M:%S")
    diff = now-last
    freq_td = FrequencyTimeDelta(_frequency)
    if(diff>freq_td):
        return True
    else:
        return False
