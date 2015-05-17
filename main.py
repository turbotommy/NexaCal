__author__ = 'tommy'

from NexaCal import *

if __name__ == "__main__":
    print "Starting"


    CalComm=NexaCalWorker()

    #timeStamp = datetime.datetime('2015-06-01T16:00:00+0200')

    #CalComm.dbtest()

#    CalComm.login()
#    CalComm.getsunrisenset()
    CalComm.getbookings(1)

    print "Klar"
