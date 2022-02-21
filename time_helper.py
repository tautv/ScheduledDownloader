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



strptime_string = "%Y/%m/%d %H:%M:%S"

now = datetime.datetime.strptime(GetTimestamp(), "%Y/%m/%d %H:%M:%S")
later = now + datetime.timedelta(hours=5)

print(now)
print(later)

#https://www.w3schools.com/python/python_datetime.asp

#
#
# print('------------')
# today = datetime.datetime.now()
# tomorrow = today + datetime.timedelta(days=1)
# print('Today:    %s' % today)
# print('Tomorrow: %s' % tomorrow)
#
# print('------------')
# now = datetime.datetime.now()
# hourFromNow = now + datetime.timedelta(hours=1)
# print('Today:    %s' % now)
# print('Tomorrow: %s' % hourFromNow)
#
# print('------------')
# time = datetime.datetime.now()
# year = time.strftime("%Y")
# month = time.strftime("%m")
# day = time.strftime("%d")
# hour = time.strftime("%H")
# minute = time.strftime("%M")
# second = time.strftime("%S")
#
# print("Time Right now: %s" %time)
# print("Year:\t%s" % year)
# print("Month:\t%s" % month)
# print("Day:\t%s" % day)
# print("Hour:\t%s" % hour)
# print("Minute:\t%s" % minute)
# print("Second:\t%s" % second)
#
# print('------------')
# custom = datetime.datetime(2020, 12, 31, 23, 59, 59) # making a custom date
# print(custom)
# custom2 = custom+datetime.timedelta(seconds=1) # custom date with 1 second added
# print(custom2)
# print('custom2-custom: %s' % (custom2-custom)) # time difference between custom2 and custom
# print('custom>custom2: %s' % (custom>custom2)) # is custom greater than custom2
# print('custom2>custom: %s' % (custom2>custom)) # is custom2 greater than custom
# print('custom==custom2: %s' % (custom==custom2)) # is custom the same as custom2
# print('custom2-custom == datetime.timedelta(seconds=1): %s' % (custom2-custom == datetime.timedelta(seconds=1))) # is the difference between custom and custom2 equal to 1 second
#
# print('------------')
# '''
#
# '''
#https://www.w3schools.com/python/python_datetime.asp
