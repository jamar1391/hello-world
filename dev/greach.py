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

# 1) I need to make it so that if I only input one argument, it gets
#    automatically scheduled for two days out:

if len(sys.argv) == 2:
    due = today + datetime.timedelta(2)
    due = due.date()

# unit test:
print(date_stripper(due))

# 2) I need to be able to input 2 arguments, and have the second one
#    be automatically understood as a date. This means a first input of
#    [goal] and a second input of [date]. The date can take three forms:
#
#    a) integer. A number like 14 means the program sets a due date 14 
#       days from today, and categorizes accordingly.
#    
#    b) yyyymmdd. Date format with year specified.
# 
#    c) mmdd. Date format without year. The current year is used as the 
#       default unless the date has already occurred, in which case next
#       year is used