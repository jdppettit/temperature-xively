import os
import glob
import time
import datetime
import json
import subprocess

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def read_temp():
    lines = read_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_raw():
        f = open('/sys/bus/w1/devices/28-00000560af11/w1_slave','r')
        lines = f.readlines()
        f.close()
        return lines

while True:
        temperature = read_temp()
        temperature = str(temperature)
        data = json.dumps({"version":"1.0.0","datastreams":[{"id":"YOURFEEDNAMEHERE","current_value":temperature}]})
        with open("temp.tmp","w") as f:
                f.write(data)
        subprocess.call(['curl --request PUT --data-binary @temp.tmp --header "X-ApiKey: YOURAPIKEYHERE" https://api.xively.com/v2/feeds/YOURFEEDIDHERE'], shell=True)
        os.remove("temp.tmp")

        time.sleep(60)


