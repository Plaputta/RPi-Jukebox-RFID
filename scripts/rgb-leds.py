#!/usr/bin/python3

import pigpio
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from time import sleep
import sys
import signal

from subprocess import check_output

# Configure the count of pixels, first 2 used for card/play status
PIXEL_COUNT = 12

SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def set_play_pixels(play = False, card_present = None):
  if card_present is None:
    card_present = bool(pi.read(4))
  if play:
    pixels.set_pixel(0, Adafruit_WS2801.RGB_to_color(0, 10, 0))
    pixels.set_pixel(1, Adafruit_WS2801.RGB_to_color(0, 10, 0))
  elif card_present:
    pixels.set_pixel(0, Adafruit_WS2801.RGB_to_color(0, 0, 10))
    pixels.set_pixel(1, Adafruit_WS2801.RGB_to_color(0, 0, 10))
  else:
    pixels.set_pixel(0, Adafruit_WS2801.RGB_to_color(20, 20, 0))
    pixels.set_pixel(1, Adafruit_WS2801.RGB_to_color(20, 20, 0))
  pixels.show()

def get_card_status(gpio = None, level = None, tick = None):
  if not level is None and level < 2:
    set_play_pixels(card_present=bool(level))
    get_play()

def get_play(gpio = None, level = None, tick = None, delayed=True):
  if (delayed):
    sleep(0.2)
  status = check_output("./scripts/playout_controls.sh -c=getplaystatus", shell=True).decode(sys.stdout.encoding).strip(' \t\n\r')
  set_play_pixels(play=status == "play")

def get_volume(gpio = None, level = None, tick = None):
  sleep(0.1)
  vol = 0
  vol_str = check_output("./scripts/playout_controls.sh -c=getvolume", shell=True).decode(sys.stdout.encoding).strip(' \t\n\r')
  if len(vol_str):
    vol = int(vol_str)
  print(str(vol))
  for i in range(10):
    pixels.set_pixel(2+i, Adafruit_WS2801.RGB_to_color(0, 20, 20) if vol > i*10 else Adafruit_WS2801.RGB_to_color(0, 0, 0))
  pixels.show()

def exit_handler(signal, frame):
  pixels.clear()
  pixels.show()
  exit(0)

def update_handler(signal, frame):
  get_volume()
  get_play(delayed=False)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGALRM, update_handler)

pixels.clear()
pixels.show()

pi = pigpio.pi()

if pi.get_mode(4) != pigpio.INPUT:
  pi.set_mode(4, pigpio.INPUT)
  pi.set_pull_up_down(4, pigpio.PUD_UP)
  pi.set_glitch_filter(4, 300)

if pi.get_mode(3) != pigpio.INPUT:
  pi.set_mode(3, pigpio.INPUT)
  pi.set_pull_up_down(3, pigpio.PUD_UP)
  pi.set_glitch_filter(3, 300)

if pi.get_mode(5) != pigpio.INPUT:
  pi.set_mode(5, pigpio.INPUT)
  pi.set_pull_up_down(5, pigpio.PUD_UP)
  pi.set_glitch_filter(5, 100)

pi.callback(4, pigpio.EITHER_EDGE, get_card_status)
pi.callback(3, pigpio.RISING_EDGE, get_play)
pi.callback(5, pigpio.RISING_EDGE, get_volume)

while True:
  signal.alarm(2)
  signal.pause()
