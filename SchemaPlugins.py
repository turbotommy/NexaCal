import sqlite3
import datetime

__author__ = 'tommy'

class SchemaPlugin:
    name = ''
    eventType = ''
    eventRule = ''
    command = ''
    setAtStartTime=0
    cursor = ''

    def __init__(self,plugin):
        print "Why am I here"
        raise NotImplementedError

    def SchemaPluginFactory(plugin):
        eventRule=''
        sunadjust=''
        parts = plugin.split(':')
        for part in parts:
            if (part == 'Sunrise'):
                name = part
                sunadjust = 'UP'
            elif (part == 'Sunset'):
                name = part
                sunadjust = 'DOWN'
            elif (part == 'TempCheck'):
                name = part
            elif (part == 'On'):
                # Affecting when on-status is triggered
                colName = 'TSFROM'
                eventType = part
            elif (part == 'Off'):
                # Affecting when off-status is triggered
                eventType = part
                colName = 'TSTO'
            elif (part == 'Latest'):
                eventRule = part
            elif (part == 'Earliest'):
                eventRule = part
            else:
                command=part

        if (sunadjust):
            return SunTimesPlugin(name, eventType, eventRule,command)

        if (parts[0] == 'TempCheck'):
            return TemperaturePlugin(name, eventType, eventRule,command)

    SchemaPluginFactory=staticmethod(SchemaPluginFactory)

    def storeInDB(self,cursor, eventId):
        self.cursor=cursor
        cursor.execute("INSERT OR REPLACE INTO NexaPlugins (eventId , name, updated, eventType, eventRule) VALUES (?,?,?,?,?)",
                       (eventId,self.name,datetime.datetime.now(),self.eventType,self.eventRule))

    def setParams(self,name, eventType, eventRule,command):
        """Sets parameters to the parent class"""
        self.name=name
        self.eventType=eventType
        self.eventRule=eventRule
        self.command=command

class SunTimesPlugin(SchemaPlugin):
    sunadjust = ''
    __doc__ = 'Dokumentationstest'

    def __init__(self, name, eventType, eventRule,command):
        self.setParams(name, eventType, eventRule,command)

        #if (self.sunadjust):
         #   print self.sunadjust
            # Get sunrise or sunset
            # tsdate=self.SunAdjust(sunadjust,tsdate, eventRule)
            # if(eventRule=='Latest' and tsdate>):

def calcPluginTime(self,orgTimeStamp):

    timeStamp=orgTimeStamp[0:10]+'%'

    if(self.name=='Sunrise'):
        sunColName = 'UP'
    if(self.name=='Sunrise'):
        sunColName = 'DOWN'

    dbselect="SELECT {0} FROM suntimes WHERE {0} LIKE ?".format(sunColName)

    #The comma-sign after timeStamp makes it a tuple.
    self.cursor.execute(dbselect, (timeStamp,))

    stats = self.cursor.fetchone()
    sunTimeStamp=stats[0]
    if(self.eventRule=='Latest' and timeStamp>sunTimeStamp):
        sunTimeStamp=timeStamp
    if(self.eventRule=='Earliest' and timeStamp<sunTimeStamp):
        sunTimeStamp=timeStamp
    return sunTimeStamp

class TemperaturePlugin(SchemaPlugin):
    def __init__(self, name, eventType, eventRule,command):
        self.setParams(name, eventType, eventRule,command)
        return
