# -*- coding: utf-8 -*-
"""
Created on Sat May  9 00:54:53 2020

@author: IVAALEX
"""
from datetime import datetime

class TimeUtility(object):
    NULL_TIME = "%d:%02d:%02d" % (0, 0, 0)
    def __init__(self):
        pass
    
    def addTimes(self, time1, time2):
        timeList = [ time1, time2]
        totalSecs = 0
        for tm in timeList:
            timeParts = [int(s) for s in str(tm).split(':')]
            #timeParts = [tm.hour, tm.minute, tm.second]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        return "%d:%02d:%02d" % (hr, min, sec)
    
    def convertToDecimal(self, time):
        timeParts = [int(s) for s in str(time).split(':')]
        totalSecs = (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        decimalTime = totalSecs / 3600
        return round(decimalTime,2)

if __name__ == '__main__':
    tu = TimeUtility()
    time1 = "01:15:00"
    print(tu.convertToDecimal(time1))