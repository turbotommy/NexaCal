#!/usr/local/bin/python
# -*- coding: utf-8 -*-

__author__ = 'tommy'

import sys
import tellcore.telldus as td
import tellcore.constants as const

class Device:
    name='N/A'
    id=999
    state='off'

    def __init__(self,devid,devname):
        assert isinstance(devname, str)
        self.name=devname
        self.id=devid

    def turn_on(self):
        print("Fake dev "+ self.name +" on")
        self.state=const.TELLSTICK_TURNON

    def turn_off(self):
        print("Fake dev "+ self.name +" off")
        self.state=const.TELLSTICK_TURNOFF

    def last_sent_command(self,supported):
        return self.state

class TelldusFakeCore:
    test=0

    def devices(self):
        return {Device(1,'DarkLamp'),Device(2,'NightLamp'),Device(3,'ChildLamps'),Device(4,'EngineHeater')}


class TelldusCtrl:
    global core
    global isStickPresent

    devs={}
    isStickPresent=1

    if(isStickPresent==1):
        core = td.TelldusCore()

    else:
        core = TelldusFakeCore()

    cdevs=core.devices()
    for dev in cdevs:
        devs[dev.name]=dev

    def turn_on(self, dev):
        name=dev.name
        try:
            if(dev.last_sent_command(-1)==const.TELLSTICK_TURNON):
                print name + " redan påslagen"
            else:
                print "Slår på " +name+ ", id="+str(dev.id)
                dev.turn_on()
        except td.TelldusError as e:
            print e


    def turn_off(self, dev):
        name=dev.name
        try:
            if(dev.last_sent_command(-1)==const.TELLSTICK_TURNOFF):
                print name + " redan avslagen"
            else:
                print "Slår av " +name+ ", id="+str(dev.id)
                dev.turn_off()
        except td.TelldusError as e:
            print e


    def notused(self):
        try:
            devices=core.devices()
            dev=devices[0]
            print dev.name
            print dev.turn_on()
            print dev.turn_off()

            for device in devices:
                print device.name
            print device.parameters()
            print device.protocol

        #    dev2=devices['Motorväarmare']
        #    print dev2.name

        except td.TelldusError as e:
            print("Could not list devices")
            print(e)
            print(e.message)
            print(e.error)

