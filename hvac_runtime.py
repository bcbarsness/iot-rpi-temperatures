from dateutil.parser import parse
import csv


def min_to_hours(minutes):
    hours = minutes / 60
    minutes = minutes % 60
    len = "%d:%02d" % (hours, minutes)
    return len

def parse_time(timedate):
    b = parse(timedate)
    return b.time()

with open('chart.csv', 'rb') as f:
    reader = csv.reader(f)
    last = 0
    dir = "Rising"
    on_time = 0
    off_time = 0
 
    for row in reader:
        if (last < row[2]):
            dir = "Rising"
        else:
            if (last > row[2]):
                dir = " Falling"

        if (dir == "Rising"):
        	off_time += 1
        else:
        	on_time += 1

        last = row[2]
        print dir, row[2], parse_time(row[0])
    print "On: ", min_to_hours(on_time), " Off: ", min_to_hours(off_time)




#a = "18/07/2015 09:04:00 PM"
#b = parse(a)
#print(b.time())
#print(b.date())


