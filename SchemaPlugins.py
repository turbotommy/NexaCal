# -*- coding: iso-8859-15 -*-
from abc import ABCMeta, abstractmethod
import sqlite3
import datetime
from dateutil import tz, parser
from random import randint

__author__ = 'tommy'

class SchemaPlugin:
    name = ''
    eventType = ''
    eventRule = ''
    command = ''
    setAtRuntime=0 #If 1 the time is set when the telldus is to be called.
    cursor = ''
    isRuntime=0

    __metaclass__ = ABCMeta

    def __init__(self,plugin):
        print "Why am I here:"+plugin
        raise NotImplementedError

    def SchemaPluginFactory(plugin):
        __doc__="Creates SchemaPlugin classes. If incoming parameter is string this is called at schema time. If it is list, this is done by runtime"

        name=''
        eventtype=''
        eventrule=''
        sunadjust=''
        command=''

        #Handlies if call made from database or Google Calendar
        if(isinstance(plugin,list)):
            parts=plugin
            isruntime=1
        else:
            parts = plugin.split(':')
            isruntime=0

        for part in parts:
            if part == 'Sunrise':
                name = part
                sunadjust = 'UP'
            elif part == 'Sunset':
                name = part
                sunadjust = 'DOWN'
            elif part == 'TempCheck':
                name = part
            elif (part == 'Random'):
                name = part
            elif (part == 'On'):
                # Affecting when on-status is triggered
                colName = 'TSFROM'
                eventtype = part
            elif (part == 'Off'):
                # Affecting when off-status is triggered
                eventtype = part
                colName = 'TSTO'
            elif (part == 'Latest'):
                eventrule = part
            elif (part == 'Earliest'):
                eventrule = part
            else:
                command=part

        if (sunadjust):
            return SunTimesPlugin(name, eventtype, eventrule, command, isruntime)
        elif (parts[0] == 'Random'):
            return RandomPlugin(name, eventtype, eventrule, command, isruntime)
        elif (parts[0] == 'TempCheck'):
            return TemperaturePlugin(name, eventtype, eventrule, command, isruntime)

    SchemaPluginFactory=staticmethod(SchemaPluginFactory)

    def storeInDB(self,cursor, eventId):
        self.cursor=cursor
        cursor.execute("INSERT OR REPLACE INTO NexaPlugins (eventId , name, updated, eventType, eventRule) VALUES (?,?,?,?,?)",
                       (eventId,self.name,datetime.datetime.now(),self.eventType,self.eventRule))

    def setParams(self,name, eventType, eventRule, command,isRuntime):
        """Sets parameters to the parent class"""
        self.name=name
        self.eventType=eventType
        self.eventRule=eventRule
        self.command=command
        self.isRuntime=isRuntime

    @abstractmethod
    def calcPluginTime(self,orgTimeStamp):
        print 'calcPluginTime should always be overridden'
        raise NotImplementedError

class RandomPlugin(SchemaPlugin):
    resolution = ''
    time=0

    __doc__ = 'Dokumentationstest för Random'

    def __init__(self, name, eventtype, eventRule,command,isRuntime):
        self.setParams(name, eventtype, eventRule,command,isRuntime)

        tmpList=command.split(' ')
        if(tmpList[1]=='min'):
            self.resolution='Minutes'
            self.time=int(tmpList[0])

    def calcPluginTime(self,orgTimeStamp):
        timediff=datetime.timedelta(minutes=randint(0,self.time))

        rndTimeStamp=orgTimeStamp+timediff
        return rndTimeStamp

class SunTimesPlugin(SchemaPlugin):
    sunadjust = ''

    __doc__ = 'Dokumentationstest'

    def __init__(self, name, eventType, eventRule,command,isRuntime):
        self.setParams(name, eventType, eventRule,command,isRuntime)


    def calcPluginTime(self,orgTimeStamp, callType):
        return super(SunTimesPlugin, self).calcPluginTime(orgTimeStamp)


    def calcPluginTime(self,orgTimeStamp):

        if(self.name=='Sunrise'):
            sunColName = 'UP'
        if(self.name=='Sunset'):
            sunColName = 'DOWN'

        #Get the date
        timeStamp=str(orgTimeStamp)[0:10]+'%'

        dbselect="SELECT {0} FROM suntimes WHERE {0} LIKE ?".format(sunColName)

        #The comma-sign after timeStamp makes it a tuple.
        self.cursor.execute(dbselect, (timeStamp,))

        stats = self.cursor.fetchone()
        if stats==None:
            #Time for some archiving and filling of tables. Return None to make it happen

            return None
        sunTimeStamp=parser.parse(stats[0])
        if self.eventRule=='Latest' and sunTimeStamp<orgTimeStamp:
            sunTimeStamp=orgTimeStamp
        if self.eventRule=='Earliest' and sunTimeStamp>orgTimeStamp:
            sunTimeStamp=orgTimeStamp
        return sunTimeStamp


class TemperaturePlugin(SchemaPlugin):
    def __init__(self, name, eventType, eventRule,command,isRuntime):
        self.setParams(name, eventType, eventRule,command,isRuntime)

        self.setAtRuntime=1
        return

    def calcPluginTime(self,orgTimeStamp):
        return orgTimeStamp
