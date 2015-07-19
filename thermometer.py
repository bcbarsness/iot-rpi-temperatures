import sys
import os
import glob
import time
import urllib2
from urllib import urlopen
import json
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'
device_temp1 = glob.glob(base_dir + '28-000006dd6544/w1_slave') [0]
device_temp2 = glob.glob(base_dir + '28-000006dc7b83/w1_slave') [0]
url="http://api.openweathermap.org/data/2.5/weather?zip=23507,us"
 
def read_temp_raw():
    f1 = open(device_temp1, 'r')
    lines1 = f1.readlines()
    f1.close()
    
    f2 = open(device_temp2, 'r')
    lines2 = f2.readlines()
    f2.close()

    return (lines1, lines2)
 
def read_temp():
    lines1, lines2 = read_temp_raw()
    while (lines1[0].strip()[-3:] != 'YES') and (lines2[0].strip()[-3:] != 'YES') :
        time.sleep(0.2)
        lines1, lines2 = read_temp_raw()
    equals_pos1 = lines1[1].find('t=')
    equals_pos2 = lines2[1].find('t=')
    if (equals_pos1 != -1) and (equals_pos2 != -1) :
        temp_string = lines1[1][equals_pos1+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f1 = temp_c * 9.0 / 5.0 + 32.0

        temp_string = lines2[1][equals_pos2+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f2 = temp_c * 9.0 / 5.0 + 32.0

        return (temp_f1, temp_f2)

def getOutsideTemp():

    meteo=urlopen(url).read()
    meteo = meteo.decode('utf-8')
    weather = json.loads(meteo)
    temp_f = (float(weather['main']['temp']) - 273.15) * 1.8 + 32
    urlopen(url).close()
    return (temp_f)

	
def main():
    if len(sys.argv) < 2:
        print('Usage: python temperature.py PRIVATE_KEY')
        exit(0)
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]

    while True:
        try:
            myTemp1, myTemp2 = read_temp()
            outsideTemp = getOutsideTemp()
            print 'Temp1: %s Temp2: %s Outside: %s' % (myTemp1, myTemp2, outsideTemp)
            f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s" % (myTemp1, myTemp2, outsideTemp))
            print f.read()
            f.close()	
	    time.sleep(60)
        except:
            print 'exiting.'
            break

if __name__ == '__main__':
    main()

