import time
import datetime
import csv
import sys


def nuke_me(): 
    with open('mycsv.csv','w',newline='') as f:
        thewriter = csv.writer(f)
     
        thewriter.writerow(['','2','10','30','100','500','2000','>2000'])
 
todays_date = datetime.datetime.now()
print_date  = time.strftime("%B %m, %Y")
 
career    = []
creation  = []
education = []
health    = []
chores    = []
net       = [] 
 
categories = (career,creation,education,health,chores,net)
 
# Takes today's date in yyyymmdd format, adds x, and eliminates
# rollover error from changing month/year
def date_adder(x):
    today = datetime.datetime.now()
    today = today + datetime.timedelta(days=x)
    print(today.date())
    return(today.date())
     
 
class TwoDays:
    def __init__(self,category,date):
        self.cat  = category
        self.date = date
 
class TenDays:
    def __init__(self,category='Chores', date=todays_date):
        self.cat  = category
        self.date = date
 
 
if len(sys.argv) == 1:
    raise Exception('Expected at least one input to command line. Zero were given')
 
elif len(sys.argv) == 2:
    goal = sys.argv[1]
    chores.append(goal)
    column = 1 # columns numbered starting from 0
    due = str(date_adder(2))
    with open('mycsv.csv','a') as f:
        mywriter = csv.writer(f)
        mywriter.writerow(['',goal+'('+due+')','','','','','',''])

elif len(sys.argv) == 3:
    if sys.argv[-1][0] == '2':
        due = sys.argv[-1][0:4] + '-' + sys.argv[-1][4:6] + '-' + sys.argv[-1][-2:]
        entry = sys.argv[1] + '(' + due + ')'

    elif sys.argv[1][0] == '2':
        due = sys.argv[-1][0:4] + '-' + sys.argv[-1][4:6] + '-' + sys.argv[-1][-2:]
        entry = sys.argv[1] + '(' + due + ')'        

        



print(chores)

