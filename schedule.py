from calendar import Calendar, TextCalendar
from datetime import date
import re
import sys

class Day:
    def __init__(self, date):
        self.date = date
        self.minutes = 1440
        self.times = createTimes()
        self.deadlines = []
        self.todo = {}

    def getFreeTime(self):
        hours = int(self.minutes / 60)
        min = self.minutes % 60
        return f"{hours} Hours {min} Minutes"

    def addEvent(self, name, start, end):
        unitsStart = re.search("(^[1-9]{1}|1{1}[0-2]{1}):([0-5]{1}[0-9]{1}) (PM|AM)", start).groups()
        unitsEnd = re.search("(^[1-9]{1}|1{1}[0-2]{1}):([0-5]{1}[0-9]{1}) (PM|AM)", end).groups()

        if unitsStart[0] == '12': start0 = 0
        else: start0 = int(unitsStart[0])
        if unitsEnd[0] == '12': end0 = 0
        else: end0 = int(unitsEnd[0])


        checkRange = False
        for i in self.times:
                if self.times[i] == name:
                    print(f"Duplicate event {name} {self.date.month}/{self.date.day}")
                    return -1
                if i == start: checkRange = True
                if i == end: checkRange = False
                if checkRange:
                    if self.times[i] != None:
                        print(f"Conflicting times {name} {self.date.month}/{self.date.day}")
                        return -1
        if unitsStart[2] == unitsEnd[2]:
            if start0 > end0:
                print(f"Invalid time entry {name} {self.date.month}/{self.date.day}")
                return -1
            elif start0 == end0 and unitsStart[1] >= unitsEnd[1]:
                print(f"Invalid time entry {name} {self.date.month}/{self.date.day}")
                return -1

            breakOut = False
            for i in range(start0, 12):
                if i == 0:k = 12
                else: k = i
                if i == start0: l = int(unitsStart[1])
                else: l = 0
                
                for j in range(l, 60):
                    self.times[(str(k) + ":{:02d} ".format(j)) + unitsStart[2]] = name
                    self.minutes -= 1
                    if i == end0 and j == int(unitsEnd[1]):
                        breakOut = True
                        break
                if breakOut: break

        elif unitsStart[2] == 'AM' and unitsEnd[2] == 'PM':
            breakOut = False
            for i in range(start0, 12):
                if i == start0: l = int(unitsStart[1])
                else: l = 0
                for j in range(l, 60):
                    self.times[(str(i) + ":{:02d} ".format(j) + unitsStart[2])] = name
                    self.minutes -= 1
            # 12 to end
            for i in range(0, 12):
                if i == 0: k = '12'
                else: k = i

                for j in range(0, 60):
                    self.times[(str(k) + ":{:02d} ".format(j)+ unitsEnd[2])] = name
                    self.minutes -= 1
                    if i == int(end0) and j == int(unitsEnd[1]):
                        breakOut = True
                        break
                if breakOut: break
        else:
            print("Invalid time " + name + self.date)
            return -1

    def addTodo(self, name, time):
        self.todo[name] = time
        self.minutes -= time

    def addDeadline(self, name):
        self.deadlines.append(name)

    def showEvents(self):
        eventsHash = {}
        freeIdx = 0
        freeTime = [['12:00 AM']]
        previousTime = '12:00 AM'
        for time in self.times:
            if self.times[time] != None:
                if self.times[time] in eventsHash:
                    eventsHash[self.times[time]].append(time)
                else:
                    eventsHash[self.times[time]] = [time]
            else:
                if previousTime in freeTime[freeIdx]:
                    freeTime[freeIdx].append(time)
                else:
                    freeTime.append([time])
                    freeIdx += 1

            previousTime = time

        for event in eventsHash:
            print(f"event: {event} {eventsHash[event][0]} - {eventsHash[event][len(eventsHash[event]) - 1]}")
        print("Free Time:")
        for interval in freeTime:
            if interval[0] == interval[len(interval) - 1]: continue
            print(interval[0] + " - " + interval[len(interval) - 1 ])
        print("Total free time: " + self.getFreeTime())
        print("Deadlines: ")
        for task in self.deadlines:
            print(task)
        # print("Todo list: ")
        # for task in self.todo:
        #     if self.todo[task] >= 60: print(f"{task}, {int(self.todo[task]/60)} Hrs {self.todo[task] % 60} minutes")
        #     elif self.todo[task] == 0: print(task)
        #     else: print(f"{task}, {self.todo[task]} minutes")
    
    def clear(self):
        for time in self.times:
            self.times[time] = None

def getDay(date, cal):
    for week in cal:
        for day in week:
            if day.date == date:
                return day
    return -1

def createTimes():
    times = {}
    for i in range(12):
        if i == 0:
            j = 12
        else:
            j = i
        for k in range(60):
            times[(str(j) + ":{:02d} AM".format(k))] = None
    for i in range(12):
        if i == 0:
            j = 12
        else:
            j = i
        for k in range(60):
            times[(str(j) + ":{:02d} PM".format(k))] = None
    return times

def createCalendar():
    times = createTimes()
    cal = Calendar(firstweekday=0)
    badDates = cal.yeardatescalendar(2022, width=12)[0]
    idx = 0
    dates = [[]]
    daysCheck = set()
    for month in badDates:
        for week in month:
            for day in week:
                if day not in daysCheck:
                    if len(dates[idx]) == 7:
                        dates.append([])
                        idx += 1
                    dates[idx].append(Day(day))
                    daysCheck.add(day)
    return dates

def insertEvent(name, date, start, end, cal):
    day = getDay(date, cal)
    if day == -1: 
        print(f"error adding {name}") 
        return -1
    day.addEvent(name, start, end)

def insertDeadline(name, date, cal):
    day = getDay(date, cal)
    if day == -1:
        print(f"error adding {name}")
        return -1
    day.addDeadline(name)

def insertTodo(name, date, time, cal):
    day = getDay(date, cal)
    if day == -1:
        print(f"error adding {name}")
        return -1
    week = None
    for w in cal:
        if day in w:
            week = w
    for w in cal[cal.index(week):]:
        if w == week:
            for d in w[w.index(day):]: d.addTodo(name, int(time))
        else: 
            for d in w: d.addTodo(name, int(time))

def upcomingDeadlines(date, cal):
    week = None
    day = getDay(date, cal)
    for w in cal:
        if day in w:
            week = w

    print('─' * 50)
    print("Upcoming deadlines")
    for w in cal[cal.index(week):]:
        if w == week:
            for d in w[w.index(day):]:               
                for dl in d.deadlines:
                    print(f"{d.date.month}/{d.date.day} {dl}")
        else:
            for d in w:
                for dl in d.deadlines:
                    print(f"{d.date.month}/{d.date.day} {dl}")
    print('─' * 50)

def showWeekEvents(date, cal):
    week = None
    day = getDay(date, cal)
    for w in cal:
        if day in w:
            week = w
    if week == None:
        return -1

    totalFreeTime = 0
    for d in week:
        totalFreeTime += d.minutes
        print('─' * 50)
        print(f"{daysOfWeek[week.index(d)].upper()} {d.date.month}/{d.date.day}")
        d.showEvents()
        print('─' * 50)
    upcomingDeadlines(date, cal)
    hours = int(totalFreeTime / 60)
    min = totalFreeTime % 60
    print(f"Total Free Time this week: {hours} Hours {min} Minutes")
    print('─' * 50 + '\nTodo: ')

    for task in day.todo:
        if day.todo[task] >= 60: print(f"{task}, {int(day.todo[task]/60)} Hrs {day.todo[task] % 60} minutes")
        elif day.todo[task] == 0: print(task)
        else: print(f"{task}, {day.todo[task]} minutes")
    print('─' * 50)




daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
calendar = {'January':None, 'February':None,'March':None,'April':None,'May':None,'June':None,
'July':None,'August':None,'September':None,'October':None,'November':None,'December':None,}
responsibilities = {}
f = open("/Users/jonas/python-workspace/Jonas/Calendar/events.txt", "r")

calendar = createCalendar()

today = date.today()

try:
    nextWeek = date(today.year, today.month, today.day + 7)
except:
    nextWeek = date(today.year, today.month + 1, today.day + 7 - 30)

if len(sys.argv) == 2:
    if sys.argv[1] == "1": pass
    elif sys.argv[1] == '2': sys.stdout = open('/Users/jonas/Library/Mobile Documents/com~apple~CloudDocs/schedule.txt', 'w')
    else: exit()

for line in f:
    type = re.search("^(event|reccurring|todo|deadline)", line)
    if not type: continue

    if type.group(0) == 'event':
        #  1. month 2. day 3. name 4. start time 5. trash 6. trash 7. end time 8. trash 9. trash
        groups = re.search("event ([1-9]{1}|10|11|12)\/([1-9]{1}|[1-3]{1}[0-9]{1}) \"(.+)\" (([1-9]{1}|1{1}[0-2]{1}):[0-5]{1}[0-9]{1} (PM|AM)) (([1-9]{1}|1{1}[0-2]{1}):[0-5]{1}[0-9]{1} (PM|AM))", line).groups()
        insertEvent(groups[2], date(2022, int(groups[0]), int(groups[1])), groups[3], groups[6], calendar)
    elif type.group(0) == 'reccurring':
        # 1. day of the week 2. name 3. start 4.trash 5. trash 6. end 7. trash 8. trash
        groups = re.search("reccurring (monday|tuesday|wednesday|thursday|friday|saturday|sunday) \"(.+)\" (([1-9]{1}|1{1}[0-2]{1}):[0-5]{1}[0-9]{1} (PM|AM)) (([1-9]{1}|1{1}[0-2]{1}):[0-5]{1}[0-9]{1} (PM|AM))", line).groups()
        idx = daysOfWeek.index(groups[0].capitalize())
        for week in calendar:
            week[idx].addEvent(groups[1], groups[2], groups[5])
    elif type.group(0) == 'deadline':
        # 1. month 2. day 3. name
        groups = re.search("deadline ([1-9]{1}|10|11|12)\/([1-9]{1}|[1-3]{1}[0-9]{1}) \"(.+)\"", line).groups()
        insertDeadline(groups[2], date(2022, int(groups[0]), int(groups[1])), calendar)
    elif type.group(0) == 'todo':
        # 1. name 2. time
        groups = re.search("todo \"(.+)\" (\d{1,4})", line).groups()
        insertTodo(groups[0], today, groups[1], calendar)


showWeekEvents(today, calendar)
