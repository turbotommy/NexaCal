from apiclient.discovery import build
import httplib2
import datetime
from dateutil import tz, parser
import os
import time
import sqlite3
import logging
from SchemaPlugins import *
from oauth2client.client import SignedJwtAssertionCredentials, AccessTokenRefreshError, Error
from httplib2 import Http

__author__ = 'Tommy Ekh'

class NexaCalWorker:
    global db
    global calId
    global syncToken

    logging.basicConfig(filename='NexaCal.log',level=logging.DEBUG)
    db = sqlite3.connect('nexa.db')

    #Read config
    with open("NexaCal.cfg") as f:
        #Google email account for calendar
        client_email=f.readline().split('=')[1][:-1]

        #calendar id
        calId=f.readline().split('=')[1][:-1]

    #The certificate file from google dev
    with open("FlaskProv-9f61f8b38f53.p12") as f:
        private_key = f.read()

    credentials = SignedJwtAssertionCredentials(client_email,
                                                private_key,
                                                'https://www.googleapis.com/auth/calendar')
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build(serviceName='calendar', version='v3', http=http)

    def login(self):
        """

        :type self: object
        """
        return

    def dbtest(self):

        #connect to db
        # db = sqlite3.connect('/home/tommy/nexa.db')

        cursor=db.cursor()

        user_id = 3
        #cursor.execute('''SELECT * FROM test WHERE =?''', (user_id,))
        cursor.execute('''SELECT * FROM test''')

        stats = cursor.fetchone()

        return

    def callGoogleCalendar(self, calendarId, init):
        """

        :rtype : instancemethod
        """
        request=''

        try:
            # get the next 12 hours of events
            epoch_time = time.time()
            start_time = epoch_time - 3600  # 1 hour ago
            end_time = epoch_time + 30 * 24 * 3600  # 3 days in the future
            tz_offset = - time.altzone / 3600
            if tz_offset < 0:
                tz_offset_str = "-%02d00" % abs(tz_offset)
            else:
                tz_offset_str = "+%02d00" % abs(tz_offset)
            start_time = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str
            end_time = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str

            if(init==1):
                logging.info("Getting calendar events between: " + start_time + " and " + end_time)

                # The Calendar API's events().list method returns paginated results, so we
                # have to execute the request in a paging loop. First, build the
                # request object. The arguments provided are:
                #   primary calendar for user
                request = self.service.events().list(calendarId=calendarId,
                                                     timeMin=start_time,
                                                     timeMax=end_time,
    #                                                 pageToken='EjYKKzVjYzE4YmFuYTM1a3JpdG03dnNvZnNtNjQ4XzIwMTUwOTIyVDE0MDAwMFoYgIDTuIGLyAI=',
                                                     #orderBy='startTime',
                                                     maxResults=100,
                                                     singleEvents=True)
            else:
                logging.info("Getting updated calendar events")

                # The Calendar API's events().list method returns paginated results, so we
                # have to execute the request in a paging loop. First, build the
                # request object. The arguments provided are:
                #   primary calendar for user
                request = self.service.events().list(calendarId=calendarId,
                                                     #timeMin='2015-05-06T04:30:00.000Z',
                                                     #timeMax='2015-05-15T14:00:00.000Z',
    #                                                 pageToken='EjYKKzVjYzE4YmFuYTM1a3JpdG03dnNvZnNtNjQ4XzIwMTUwOTIyVDE0MDAwMFoYgIDTuIGLyAI=',
                                                     orderBy='startTime',
                                                     maxResults=100,
                                                     syncToken='CNiij-jEv8UCENiij-jEv8UCGAQ=',
                                                     singleEvents=True)

            #request = self.service.events().list(calendarId=calendarId,
            #                                     timeMin=start_time,
            #                                     timeMax=end_time,
                                                 #updatedMin='2015-05-08T00:00:00.000Z',
            #                                     singleEvents=True)
        except Error:
            print Error.message()
            # The AccessTokenRefreshError exception is raised if the credentials
            # have been revoked by the user or they have expired.
            print ('The credentials have been revoked or expired, please re-run'
                   'the application to re-authorize')

        return request

    def gettz(self):
        epoch_time = time.time()
        start_time = epoch_time - 3600  # 1 hour ago
        end_time = epoch_time + 12 * 3600  # 12 hours in the future
        tz_offset = - time.altzone / 3600
        if tz_offset < 0:
            tz_offset_str = "-%02d00" % abs(tz_offset)
        else:
            tz_offset_str = "+%02d00" % abs(tz_offset)

        return tz_offset_str

    def getsunrisenset(self):
      try:
        cursor=db.cursor()

      #db = sqlite3.connect('/home/tommy/nexa.db')
        request=self.callGoogleCalendar('i_78.69.212.216#sunrise@group.v.calendar.google.com')
        #request = self.service.events().list(calendarId='i_78.69.212.216#sunrise@group.v.calendar.google.com',
        #                                         timeMin=u'2015-04-26T20:54:26+0200',
        #                                         timeMax=u'2015-04-27T20:54:26+0200',
        #                                         singleEvents=True)
        #First get the timezones straight
        tzlocal=tz.tzlocal()
        tzUTC=tz.gettz('UTC')

        # Loop until all pages have been processed.
        while request != None:
          # Get the next page.
          response = request.execute()
          # Accessing the response like a dict object with an 'items' key
          # returns a list of item objects (events).
          logging.debug("Response: ")
          logging.debug(response)
          for event in response.get('items'):
            # The event object is a dict object with a 'summary' key.

            # Insert info about event
            summary=event.get('summary', 'Tomt')
            sunDate=event.get('start', 'Tomt')
            sunDate=sunDate.get('date')+' '

            logging.info(summary)
            tmpList=summary.split(",")

            tsfrom=parser.parse(sunDate+tmpList[0][-7:])
            tsfrom=tsfrom.replace(tzinfo=tzUTC)
            tsfrom=tsfrom.astimezone(tzlocal)

            tsto=parser.parse(sunDate+tmpList[1][-7:])
            tsto=tsto.replace(tzinfo=tzUTC)
            tsto=tsto.astimezone(tzlocal)

            rc=cursor.execute('''INSERT INTO suntimes(up, down)
                              VALUES(?,?)''', (tsfrom, tsto))
            db.commit()
            logging.info('First user inserted')
            #print repr(event.get('summary', 'NO SUMMARY')) + '\n'
          # Get the next request object by passing the previous request object to
          # the list_next method.
          #select up from suntimes where date(up) = date('now');
          request = self.service.events().list_next(request, response)

      except sqlite3.IntegrityError as sqlIE:
        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
        logging.debug(sqlIE.message)
      except Error:
        print Error.message()
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
        print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')

        print "Hello"

      #except Exception:
      #  print Exception.message

      db.commit()
      db.close

    def getbookings(self, init):

      cursor=db.cursor()

      try:

        request=self.callGoogleCalendar(calId, init)

        while request != None:
          # Get the next page.
          response = request.execute()
          logging.debug("Calresponse:")
          logging.debug(response)
          # Accessing the response like a dict object with an 'items' key
          # returns a list of item objects (events).
          print response
          for event in response.get('items'):
            # The event object is a dict object with a 'summary' key.

            # Insert info about event
            eventId=event['id']
            status=event['status']

            if(status=='cancelled'):
                cursor.execute('''DELETE from NexaControl where eventId=?''', (eventId))
                cursor.execute('''DELETE from NexaPlugins where eventId=?''', (eventId))
            else:
                summary=event.get('summary', 'Tomt')

                tsfrom=event.get('start', 'Tomt')
                tsfrom=tsfrom.get('dateTime') #QUE: What if it is not dateTime?

                tsto=event['end']
                tsto=tsto['dateTime']

                updated=event.get('updated', 'Tomt')

                #Check for plugins in description field
                descr=event['description']
                plugins=descr.split('\n')
                for pluginrow in plugins:
                    schemaPlugin=SchemaPlugin.SchemaPluginFactory(pluginrow)

                    schemaPlugin.storeInDB(cursor, eventId)

                cursor.execute('''INSERT OR REPLACE INTO NexaControl(eventId, name, updated, tsfrom, tsto, plugin)
                                  VALUES(?,?,?,?,?,?)''', ( eventId,
                                                            summary,
                                                            updated,
                                                            tsfrom,
                                                            tsto,
                                                            descr))




            logging.debug(event.get('summary', 'Tomt'))
            logging.debug(event.get('start', 'Tomt'))
            logging.debug(event.get('end', 'Tomt'))
            logging.debug(event.get('updated', 'Tomt'))
            #print repr(event.get('summary', 'NO SUMMARY')) + '\n'
          # Get the next request object by passing the previous request object to
          # the list_next method.
          request = self.service.events().list_next(request, response)

        #Store nextSyncToken
        print response['nextSyncToken']
        cursor.execute('''UPDATE CalConfig SET value=? where key=?''',(response['nextSyncToken'],'nextSyncToken'))
      except Error:
        print Error.message()
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
        print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')

        print "Hello"

      db.commit()
      db.close

    def SunAdjust(self, sunColName,timeStamp, eventRule):
        cursor=db.cursor()
        timeStampDB=timeStamp[0:10]+'%'

        dbselect="SELECT {0} FROM suntimes WHERE {0} LIKE ?".format(sunColName)

        #The comma-sign after timeStamp makes it a tuple.
        cursor.execute(dbselect, (timeStampDB,))

        stats = cursor.fetchone()
        sunTimeStamp=stats[0]
        if(eventRule=='Latest' and timeStamp>sunTimeStamp):
            sunTimeStamp=timeStamp
        if(eventRule=='Earliest' and timeStamp<sunTimeStamp):
            sunTimeStamp=timeStamp
        return sunTimeStamp
