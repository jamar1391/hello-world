#!usr/bin/env

import sys
import time
import datetime

today = datetime.datetime.now()

def date_stripper(date):
    date = str(date)
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    newdate = year + month + date

    return newdate

if len(sys.argv) == 1:
    raise Exception('At least one command line argument required.')


goal = sys.argv[1].title()

if len(sys.argv) == 2:
    due = today + datetime.timedelta(2)
    due = due.date()


print(date_stripper(due))