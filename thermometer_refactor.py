import sys
import os
import glob
import time
import urllib2
from urllib import urlopen
import json
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

update_rate_secs = 60 
base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'
device_temp1 = glob.glob(base_dir + '28-000006dd6544/w1_slave') [0]
device_temp2 = glob.glob(base_dir + '28-000006dc7b83/w1_slave') [0]
url="http://api.openweathermap.org/data/2.5/weather?zip=23507,us"
 
def read_temp(device):
    lines = device.readlines()
    while (lines[0].strip()[-3:] != 'YES') :
        time.sleep(0.2)
        lines = read_temp_raw(device_id)
    equals_pos = lines[1].find('t=')
    if (equals_pos != -1) :
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return (temp_f)

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
    temp_file1 = open(device_temp1, 'r')
    temp_file2 = open(device_temp2, 'r')
    while True:
        try:
            temp_sensor1 = read_temp(temp_file1)
            temp_sensor2 = read_temp(temp_file2)            
            outsideTemp = getOutsideTemp()
            print 'Temp1: %s Temp2: %s Outside: %s' % (temp_sensor1, temp_sensor2, outsideTemp)
            f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s" % (temp_sensor1, temp_sensor2, outsideTemp))
            print f.read()
            f.close()
            time.sleep(update_rate_secs)
#        except:
#            print 'exiting.'
#            break

        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    temp_file1.close()
    temp_file2.close()

if __name__ == '__main__':
    main()

