#!/usr/bin/python3
# Advanced Rotary Control
#
# The idea is to replace all input buttons with just one KY-040.
#
# Rotate: Increase/Decrease volume
# Rotate while pressing: Next/Previous track
# Short press (without rotating): Pause/Play
# Long press (5s, without rotating): Shutdown
#
# Connect as follows:
#
# | KY-040 | RPi    |
# |========|========|
# | CLK    | GPIO 5 |
# | DT     | GPIO 6 |
# | SW     | GPIO 3 |
# | +      | 3.3V   |
# | GND    | GND    |
#

from gpiozero import Button, InputDevice
from signal import pause
import time
from subprocess import check_call

def trigger_held():
   check_call("./scripts/playout_controls.sh -c=shutdown", shell=True)

def check_rotation():
   global encoder_rotate_time
   encoder_rotate_time = time.time()
   if trigger.is_active and direction.is_active:
      check_call("./scripts/playout_controls.sh -c=playernext", shell=True)
   elif trigger.is_active and not direction.is_active:
      check_call("./scripts/playout_controls.sh -c=playerprev", shell=True)
   elif direction.is_active:
      check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)
   else:
      check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def trigger_released():
   global trigger_press_time, encoder_rotate_time
   if encoder_rotate_time < trigger_press_time:
      check_call("./scripts/playout_controls.sh -c=playerpause", shell=True)

def trigger_pressed():
   global trigger_press_time
   trigger_press_time = time.time()

encoder_rotate_time = trigger_press_time = time.time()

trigger = Button(3,pull_up=True,bounce_time=0.1,hold_time=5)
trigger.when_pressed = trigger_pressed
trigger.when_released = trigger_released
trigger.when_held = trigger_held

direction = InputDevice(6, pull_up=True)

encoder = Button(5,pull_up=True,bounce_time=0.01)
encoder.when_released = check_rotation

pause()
