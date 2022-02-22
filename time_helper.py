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

def ShouldDownload(_last_download_time, _frequency):
    now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
    last = datetime.datetime.strptime(_last_download_time, "%Y/%m/%d %H:%M:%S")
    diff = now-last
    freq = datetime.datetime.strptime(_frequency, "%H:%M:%S")
    freq_td = datetime.timedelta(hours=freq.hour, minutes=freq.minute, seconds=freq.second)
    if(diff>freq_td):
        return True
    else:
        return False

def IsValidFrequency(_frequency):
    try:
        d = datetime.datetime.strptime(_frequency, "%H:%M:%S")
        return True
    except Exception as e:
        return False
