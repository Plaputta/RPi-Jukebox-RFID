#!/usr/bin/python3
# card presence sensor
# This script is compatible with any I2S DAC e.g. from Hifiberry, Justboom, ES9023, PCM5102A
# It is using GPIO Port 4 and is designed for the Neuftech RFID Reader
#
# Connect a 4.7kOhm resistor to the square diagnose pin on the outer left side of the pcb and connect it to GPIO 4
# Since the reader is connected directly to the RPi through USB there is no need to connect the GND lines
#
#                       ++++++++++++++++++++++++++++++++++++++++++++++
#                       |                          __       OOOO     |
#                       | ___        -+----+-     |Q |           ___ |
#                       ||   |       -|    |-     |U |          |   ||
#                       ||___|       -| CH |-     |A |          |___||
#                       |            -| IP |-     |R |               |
#                       |            -+----+-     |T |               |
#                       |                         |Z_|               |
#                       |                                            |
#    GPIO 4----(4k7)-----[o] o ___                           ___     |
#                        +    |   |           +||||+        |   |   +
#                         +   |___|           | U  |        |___|  +
#                          +                  | S  |              +
#                           +-----------------| B  |-------------+
#                                             +----+


import pigpio
import signal
from subprocess import check_call

def card_removed(gpio = None, level = None, tick = None):
  check_call("./scripts/playout_controls.sh -c=playerpausereal", shell=True)

def exit_handler(signal, frame):
  exit(0)

def update_handler(signal, frame):
  if (pi.read(4) == 0):
    card_removed()

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGALRM, update_handler)

pi = pigpio.pi()

if pi.get_mode(4) != pigpio.INPUT:
  pi.set_mode(4, pigpio.INPUT)
  pi.set_pull_up_down(4, pigpio.PUD_UP)
  pi.set_glitch_filter(4, 300)

pi.callback(4, pigpio.FALLING_EDGE, card_removed)

while True:
  signal.alarm(1)
  signal.pause()
