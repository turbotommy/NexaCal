__author__ = 'tommy'

from NexaCal import *

if __name__ == "__main__":
    print "Starting"

    CalComm=NexaCalWorker()

    #CalComm.dbtest()

#    CalComm.login()
#    CalComm.getsunrisenset()
    CalComm.getbookings()
    print "Klar"
