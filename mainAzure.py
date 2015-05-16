__author__ = 'tommy'

from NexaCal import *
from AzureTest import *

import proton

if __name__ == "__main__":
    print "Starting"

    #azureComm=AzureTestQ()
    #azureComm.SendMsg()

    CalComm=NexaCalWorker()

    CalComm.dbtest()

#    CalComm.login()
#    CalComm.getsunrisenset()
    CalComm.getbookings()
    print "Klar"
