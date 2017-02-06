"""
    Debugger Assistant module for AUHR-HUST
"""

import datetime

def printLog(content):
    currentTime = datetime.datetime.now().isoformat("-")
    print("[LOG] [ %s ]\t %s" % (currentTime, content))