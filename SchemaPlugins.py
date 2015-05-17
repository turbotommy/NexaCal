import sqlite3

__author__ = 'tommy'

class SchemaPlugin:
    name = ''
    eventType = ''
    eventRule = ''
    setsAtStartTime=0

    def __init__(self,plugin):
        print "Why am I here"
        raise NotImplementedError

    def SchemaPluginFactory(plugin):
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

        if (parts[0] == 'SunRise' or parts[0] == 'SunSet'):
            return SunTimesPlugin()

        if (parts[0] == 'TempCheck'):
            return TemperaturePlugin(name, eventType, eventRule)

    SchemaPluginFactory=staticmethod(SchemaPluginFactory)

    def storeInDB(self,cursor, eventId):
        cursor.execute("INSERT OR REPLACE INTO NexaPlugins (eventId TEXT not null, name TEXT, eventType TEXT, eventRule TEXT")

        cursor.commit()

class SunTimesPlugin(SchemaPlugin):
    sunadjust = ''
    __doc__ = 'Dokumentationstest'

    def __init__(self, params):
        if (self.sunadjust):
            print self.sunadjust
            # Get sunrise or sunset
            # tsdate=self.SunAdjust(sunadjust,tsdate, eventRule)
            # if(eventRule=='Latest' and tsdate>):


class TemperaturePlugin(SchemaPlugin):
    def __init__(self, params):
        return
