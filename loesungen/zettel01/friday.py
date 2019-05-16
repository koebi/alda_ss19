###############
# Aufgabe 2a) #
###############
# Der 1.1. kann auf jeden Wochentag fallen, hier gibt es also 7 Möglichkeiten. Außerdem kann
# der Februar 28 oder 29 Tage haben (Schaltjahr). Es gibt somit insgesamt 14 Möglichkeiten.

days = [31,28,31,30,31,30,31,31,30,31,30,31]

# Zur einfachereren Ausgabe :)
yearNames = ["normal-year", "leap-year"]
dayNames = ["Mon.","Tue.","Wed.","Thu.","Fri.","Sat.","Sun."]

###############
# Aufgabe 2b) #
###############
def friday13th():
    for leap in range(2): #Schaltjahr: 0=False, 1=True
        for firstDay in range(7): #Tage nummerieren: 0=Monday, ..., 6=Sunday
            day, count = firstDay, 0
            for month in range(12):
                if (day+(13-1))%7 == 4:	 # Anmerkung: Man kann
                                         # "if (day+(13-1))%7 == 4:" durch
                                         # "if day%7 == 6:" ersetzen, da
                                         # Freitag der 13. <=> Sonntag der 1.
                    count += 1
                day += days[month]+(leap if month==1 else 0)
            print("# Friday 13th's [Jan 1st: {} | {}]: {}".format(dayNames[firstDay], yearNames[leap], count))

###############
# Aufgabe 2c) #
###############
# Import ok, da die Information, welcher Wochentag der 01.01. war, irgendwoher
# kommen muss, und man sich nicht mords einen abbrechen muss um das irgendwie
# zu berechnen
from datetime import datetime

def friday13thSince(day, month, year):
    #Initial checks
    if not 0 < day <= days[month-1]:
        raise RuntimeError("Wrong day argument")
    if month-1 not in range(12):
        raise RuntimeError("Wrong month argument")

    now, count = datetime.now(), 0
    for y in range(year, now.year+1):
        for m in range(12):
            if (y==year and (m+1<month or (m+1==month and 13<day)) or\
                y==now.year and (m+1>now.month or (m+1==now.month and 13>now.day))):
                continue
            if datetime(y, m+1, 13).strftime("%A") == "Friday":
                count += 1
    return count

if __name__ == "__main__":
    friday13th()
    print ("since birth:", friday13thSince(1,1,1970))
