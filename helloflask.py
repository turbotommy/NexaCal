__author__ = 'tommy'

from NexaCal import *
from flask import Flask

app = Flask(__name__)
CalComm=NexaCalWorker()

@app.route('/init')
def init():
    try:


        #timeStamp = datetime.datetime('2015-06-01T16:00:00+0200')

        #CalComm.dbtest()

    #    CalComm.login()
    #    CalComm.getsunrisenset()
        return CalComm.getbookings(1)

    except Exception as e:
        return e.__str__()


@app.route('/fireTelldus')
def fireTelldus():
    CalComm.getbookings(1)
    return CalComm.fireTelldus()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

