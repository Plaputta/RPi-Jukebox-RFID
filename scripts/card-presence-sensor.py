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


from gpiozero import Button
from signal import pause
from subprocess import check_call

def card_presented():
   pass  # Here you could implement a procedure that is run when a card was read successfully, the recommended option
         # is to set the "Second Swipe" setting to "Toggle Pause and Play"

def card_removed():
   check_call("./scripts/playout_controls.sh -c=playerpause", shell=True)

sensor = Button(4,pull_up=False)

sensor.when_released = card_presented
sensor.when_pressed = card_removed

pause()
