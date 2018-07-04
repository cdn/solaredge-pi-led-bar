#!/usr/bin/env python3

#import RPi.GPIO as GPIO
from gpiozero import LEDBarGraph
import requests
import simplejson as json
import sys
import time

#sudo pip3 install tenacity

#from tenacity import retry, stop_after_attempt
#from tenacity import wait_combine, wait_fixed, wait_jitter

# Suppress output pertaining to use of SPI pins as general GPIO (tautology)
#GPIO.setwarnings(False)
# Broadcom GPIO pin numbering scheme
#GPIO.setmode(GPIO.BCM)

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
BAR_G4 = 9  # no apparent output
BAR_G4 = 25
BAR_G5 = 10

# SolarEdge API docs:
# https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

# SolarEdge inverter identifier/API key

SE_SITE = 'nnnnnn'
SE_AKEY = 'VE94E5S3PJKL0CXIEA0ZYRI45PF03PRY'

# array/tuple pin layout
bar = [26, 19, 13, 6, 5, 7, 8, 11, 25, 10]
bar = {26, 19, 13, 6, 5, 7, 8, 11, 25, 10}
bar = (26, 19, 13, 6, 5, 7, 8, 11, 25, 10)
#GPIO.setup(bar, GPIO.OUT)

graph = LEDBarGraph(26, 19, 13, 6, 5, 7, 8, 11, 25, 10)

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

# remainder from division
        d = c % 10

# index to pinout array for LED PWM
        e = int(c / 10)

#    print(e)

        if e < 10:
            print(bar[e])

# output selection control structure, tuple addressing

        graph.value = c/100

 #       if c == 100:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
 #       elif c >= 90:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 1, 1, 1, 1, 0))
 #       elif c >= 80:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 1, 1, 1, 0, 0))
 #       elif c >= 70:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 1, 1, 0, 0, 0))
 #       elif c >= 60:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 1, 0, 0, 0, 0))
 #       elif c >= 50:
 #           GPIO.output(bar, (1, 1, 1, 1, 1, 0, 0, 0, 0, 0))
 #       elif c >= 40:
 #           GPIO.output(bar, (1, 1, 1, 1, 0, 0, 0, 0, 0, 0))
 #       elif c >= 30:
 #           GPIO.output(bar, (1, 1, 1, 0, 0, 0, 0, 0, 0, 0))
 #       elif c >= 20:
 #           GPIO.output(bar, (1, 1, 0, 0, 0, 0, 0, 0, 0, 0))
 #       elif c >= 10:
 #           GPIO.output(bar, (1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
 #       else:
 #           GPIO.output(bar, 0)

# apply PWM with d*10 duty cycle on next level above (c - d)%

 #       if d > 0:
 #           p = GPIO.PWM(bar[e], 100)
 #           p.start(int(d*10))

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
#        GPIO.cleanup()
        graph.close()
#        gpiozero.Factory.close()
        sys.exit()
