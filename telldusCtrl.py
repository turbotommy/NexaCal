#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'tommy'

#import sys
import tellcore.telldus as td
import tellcore.constants as const
import logging

class Device:
    name='N/A'
    id=999
    state='off'

    def __init__(self,devid,devname):
        assert isinstance(devname, str)
        self.name=devname
        self.id=devid

    def turn_on(self):
        logger.info("Fake dev "+ self.name +" on")
        self.state=const.TELLSTICK_TURNON

    def turn_off(self):
        logger.info("Fake dev "+ self.name +" off")
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
    global logger

    devs={}
    isStickPresent=1

    logging.config.fileConfig('logging.conf')
    #logging.basicConfig(filename='NexaCal.log',level=logging.DEBUG)
    logger = logging.getLogger(__name__)

#    logging.basicConfig(filename='tellduswrapper.log',level=logging.DEBUG)
#    logger = logging.getLogger('werkzeug')

    try:
        logger.info("Starting tellduswrapper")
        core = td.TelldusCore()
    except Exception as e:
        logger.warning(e.message)
        core = TelldusFakeCore()
        isStickPresent=0

    cdevs=core.devices()
    for dev in cdevs:
        devs[dev.name]=dev

    def turn_on(self, dev):
        name=dev.name
        try:
            if(dev.last_sent_command(-1)==const.TELLSTICK_TURNON):
                logger.info(name + " already on")
            else:
                logger.info("Turns on " +name+ ", id="+str(dev.id))
                dev.turn_on()
        except td.TelldusError as e:
            logger.error(e)


    def turn_off(self, dev):
        name=dev.name
        try:
            if(dev.last_sent_command(-1)==const.TELLSTICK_TURNOFF):
                logger.info(name + " already off")
            else:
                logger.info("Turns off " +name+ ", id="+str(dev.id))
                dev.turn_off()
        except td.TelldusError as e:
            logger.error(e)


    def notused(self):
        try:
            devices=core.devices()
            dev=devices[0]
            logger.info(dev.name)
            logger.info(dev.turn_on())
            logger.info(dev.turn_off())

            for device in devices:
                logger.info(device.name)
            logger.info(device.parameters())
            logger.info(device.protocol)

        #    dev2=devices['Motorväarmare']
        #    print dev2.name

        except td.TelldusError as e:
            logger.error("Could not list devices")
            logger.error(e)
            logger.error(e.message)
            logger.error(e.error)

