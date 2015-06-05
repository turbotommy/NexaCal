__author__ = 'tommy'

from NexaCal import *
from flask import Flask

app = Flask(__name__)

@app.route('/init')
def init():
    CalComm=NexaCalWorker()

    #timeStamp = datetime.datetime('2015-06-01T16:00:00+0200')

    #CalComm.dbtest()

#    CalComm.login()
#    CalComm.getsunrisenset()
    CalComm.getbookings(1)

    return 'Ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

