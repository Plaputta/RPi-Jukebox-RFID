#!/usr/bin/python3

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from time import sleep
import sys
import signal
import pigpio
import threading

from subprocess import check_output, check_call, DEVNULL

def show_num(num,color,pixels):
  pixels.set_pixel(2, Adafruit_WS2801.RGB_to_color(0, 20, 0))
  for i in range(9):
    pixels.set_pixel(3+i, color if num > i else Adafruit_WS2801.RGB_to_color(0, 0, 0))
  pixels.show()

PIXEL_COUNT = 12

SPI_PORT = 0
SPI_DEVICE = 0

def display_ip(pixels):
  ip = check_output("hostname -I", shell=True).decode(sys.stdout.encoding).strip(' \t\n\r').split(" ")

  if pixels is None:
    print("IP", ip)
    return

  if len(ip[0]):
    for c in ip[0]:
      if c == ".":
        color = Adafruit_WS2801.RGB_to_color(0, 30, 0)
        num = 9
      else:
        color = Adafruit_WS2801.RGB_to_color(0, 30, 30)
        num = int(c)
      show_num(num, color, pixels)
      sleep(2)
      pixels.clear()
      pixels.show()
      sleep(0.5)

    sleep(3)

def spin(pixels):
  pos = 0
  while spinner_running:
    pixels.clear()
    pixels.set_pixel(2 + pos, Adafruit_WS2801.RGB_to_color(0, 0, 20))
    pixels.show()
    pos += 1
    if (pos > 9):
      pos = 0
    sleep(0.2)

def display_info(pixels, msg, color):
  if (pixels is None):
    print(msg)
    return
  pixels.clear()
  for i in range(10):
    pixels.set_pixel(2 + i, color)
  pixels.show()
  sleep(3)

def check_wifi_wps(gpio, level, tick):
  global spinner_running
  print("WiFi config triggered.")

  try:
    rgb_service_status = check_call("service phoniebox-rgb-leds status",shell=True, stdout=DEVNULL)
  except:
    rgb_service_status = 1

  pixels = None
  spi_dev = None

  if rgb_service_status == 0:
    check_call("service phoniebox-rgb-leds stop", shell=True)

    spi_dev = SPI.SpiDev(SPI_PORT, SPI_DEVICE)
    pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=spi_dev)

    pixels.clear()
    pixels.show()

    spinner_running = True
    spinner_thread = threading.Thread(target=spin, args=[pixels])
    spinner_thread.start()

  try:
    wifi_result = check_output("./scripts/wifi-wps.sh", shell=True).decode(sys.stdout.encoding).strip(' \t\n\r')
    spinner_running = False
    sleep(0.2)
  except:
    wifi_result = "ERR"

  if wifi_result.split('\n')[-1] != "OK":
    display_info(pixels, wifi_result, Adafruit_WS2801.RGB_to_color(20, 0, 0))
  else:
    display_info(pixels, wifi_result, Adafruit_WS2801.RGB_to_color(0, 20, 0))
    sleep(2)
    display_ip(pixels)

  if spi_dev is not None:
    spi_dev.close()

  if rgb_service_status == 0:
    check_call("service phoniebox-rgb-leds start", shell=True)

spinner_running = False

pi = pigpio.pi()

pi.set_mode(13, pigpio.INPUT)
pi.set_pull_up_down(13, pigpio.PUD_UP)
pi.set_glitch_filter(13, 300)

pi.callback(13, pigpio.FALLING_EDGE, check_wifi_wps)

while True:
  signal.pause()