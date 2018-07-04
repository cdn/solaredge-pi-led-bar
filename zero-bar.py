#!/usr/bin/env python3

from gpiozero import LEDBarGraph
import requests
import simplejson as json
import sys
import time

#sudo pip3 install tenacity

#from tenacity import retry, stop_after_attempt
#from tenacity import wait_combine, wait_fixed, wait_jitter

# Cross-strip outputs; via omission of
#  I2C, GND pins (on subsequent physical implementation)

BAR_R1 = 26
BAR_R2 = 19
BAR_R3 = 13
BAR_Y1 = 6
BAR_Y2 = 5
BAR_G1 = 7
BAR_G2 = 8
BAR_G3 = 11
BAR_G4 = 25
BAR_G5 = 10

# SolarEdge API docs:
# https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

# SolarEdge inverter identifier/API key

SE_SITE = 'nnnnnn'
SE_AKEY = 'ALPHANUMERIC0123456789ABCEDFGHIJ'

# array/tuple pin layout
graph = LEDBarGraph(26, 19, 13, 6, 5, 7, 8, 11, 25, 10, pwm=True)

#@retry(wait=wait_combine(wait_fixed(10), wait_jitter(30)),
# stop=stop_after_attempt(5))
r = requests.session()

# URL to SolarEdge API
u = 'https://monitoringapi.solaredge.com/site/' + SE_SITE
u += '/currentPowerFlow?api_key=' + SE_AKEY

while 1:
    try:
        j = r.get(u, timeout=10)
        if 'STORAGE' not in j.text:
            print('no data')
            time.sleep(900)
            j = r.get(u, timeout=10)
#      sys.exit()

# STORAGE key in j.json()['siteCurrentPowerFlow']
#    if 'STORAGE' in j.text:
        t = j.json()['siteCurrentPowerFlow']['STORAGE']

        c = int(t['chargeLevel'])

# output selection control structure, tuple addressing

        graph.value = c/100

        wait = 900
        while wait > 0:
            print(wait)
            time.sleep(1)
            wait -= 1
    except ConnectionError:
        print('-error-')
    except ConnectionResetError:
        print('Reset')
    except KeyboardInterrupt:
        graph.close()
#        gpiozero.Factory.close()
        sys.exit()
