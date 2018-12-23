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

import pigpio
import time
import signal
from subprocess import check_call

def trigger_held(signal, frame):
   check_call("./scripts/playout_controls.sh -c=shutdown", shell=True)

def check_rotation(gpio, level, tick):
   global encoder_rotate_time, encLevA, encLevB, lastEncPin
   if level > 1:
      return
   if gpio == encPinA:
      encLevA = level
   else:
      encLevB = level
   if gpio == lastEncPin: # debounce
      return
   lastEncPin = gpio
   signal.alarm(0)
   encoder_rotate_time = time.time()
   pressed = not bool(pi.read(3))
   if gpio == encPinA and level == 1:
      if encLevB == 1:
         if pressed:
            check_call("./scripts/playout_controls.sh -c=playernext", shell=True)
         else:
            check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)
   elif gpio == encPinB and level == 1:
      if encLevA == 1:
         if pressed:
            check_call("./scripts/playout_controls.sh -c=playerprev", shell=True)
         else:
            check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def trigger_released(gpio, level, tick):
   global trigger_press_time, encoder_rotate_time
   signal.alarm(0)
   if encoder_rotate_time < trigger_press_time:
      check_call("./scripts/playout_controls.sh -c=playerpause", shell=True)

def trigger_pressed(gpio, level, tick):
   global trigger_press_time
   trigger_press_time = time.time()
   signal.alarm(5)

def exit_handler(signal, frame):
  exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGALRM, trigger_held)

encoder_rotate_time = trigger_press_time = time.time()

pi = pigpio.pi()

encPinA = 5
encPinB = 6

if pi.get_mode(encPinA) != pigpio.INPUT:
  pi.set_mode(encPinA, pigpio.INPUT)
  pi.set_pull_up_down(encPinA, pigpio.PUD_UP)
  pi.set_glitch_filter(encPinA, 30)

if pi.get_mode(encPinB) != pigpio.INPUT:
  pi.set_mode(encPinB, pigpio.INPUT)
  pi.set_pull_up_down(encPinB, pigpio.PUD_UP)
  pi.set_glitch_filter(encPinB, 30)

if pi.get_mode(3) != pigpio.INPUT:
  pi.set_mode(3, pigpio.INPUT)
  pi.set_pull_up_down(3, pigpio.PUD_UP)
  pi.set_glitch_filter(3, 300)

encLevA = pi.read(encPinA)
encLevB = pi.read(encPinB)
lastEncPin = None


pi.callback(3, pigpio.FALLING_EDGE, trigger_pressed)
pi.callback(3, pigpio.RISING_EDGE, trigger_released)
pi.callback(5, pigpio.EITHER_EDGE, check_rotation)
pi.callback(6, pigpio.EITHER_EDGE, check_rotation)

while True:
   signal.pause()
