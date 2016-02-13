#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'tommy'

import tellcore.telldus as td
import tellcore.constants as const

core = td.TelldusCore()
devices=core.devices()
dev=devices[0]
dev.type

sensor=core.sensors()[1]
sensor.temperature().value
dir(sensor)



assert isinstance(dev, object)

