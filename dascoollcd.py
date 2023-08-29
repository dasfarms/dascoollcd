#!/usr/bin/env python

import os
import glob
import time
import lib4relind
import liquidcrystal_i2c
lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20


def readf(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    fahrenheit = (temperature / 1000) * 1.8 + 32
    fahstr = str(round(fahrenheit, 1))
    return fahrenheit, fahstr


def readc(ds18b20):

    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = int(temperature) / 1000
    celstr = str(round(celsius, 1))
    return celsius, celstr

def lcddisplay(ds18b20):
    lcd.printline(0,"Temp: " + readc()[1] + unichr(223) + "C")
    lcd.printline(1,"Temp: " + readf()[1] + unichr(223) + "F")

def loop(ds18b20):

    while True:

        lcddisplay(ds18b20)

        if readf(ds18b20)[0] < 45.0 or readc(ds18b20)[0] < 7.2:

            print(readf(ds18b20)[1])
            print(readc(ds18b20)[1])

            time.sleep(3)


        elif readf(ds18b20)[0] < 60.0 or readc(ds18b20)[0] < 15.5:

            lib4relind.set_relay(0, 1, 0)
            print(readf(ds18b20)[1])
            print(readc(ds18b20)[1])
            time.sleep(30)
            lib4relind.set_relay(0, 1, 1)

        else:
            print("WARNING FREEZER OVERTEMP")
            lcd.clear()
            lcd.printline(0,"!!! WARNING  !!!")
            lcd.printline(1,"!!! OVERTEMP !!!")
            lcd.printline(2,"Temp: " + readf()[1] + unichr(223) + "F")





def kill():
    quit()


if __name__ == '__main__':

    try:
        serialNum = sensor()

        loop(serialNum)

    except KeyboardInterrupt:

        kill()
