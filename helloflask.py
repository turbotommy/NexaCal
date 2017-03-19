#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'tommy'

from flask import Flask
from flask import request, current_app
import logging
import logging.config
import socket

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
#logging.basicConfig(filename='NexaCal.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
#handler = logger.handlers.pop()
#logger.addHandler(handler)

app = Flask(__name__)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80)) #Google's DNS
myip=s.getsockname()[0]
s.close()

logger.info("Starting flaskd, baseaddr " + myip)
from NexaCal import *

CalComm=NexaCalWorker()

# Also add the handler to Flask's logger for cases
#  where Werkzeug isn't used as the underlying WSGI server.
#app.logger.addHandler()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css" />
        <script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
        <script type="text/javascript">
        $(document).ready(function(){
            //Starta saker
            $('.lampknapp').click(function(){
                toggleLampa(this);
            });
        });
        function toggleLampa(lampa){
            //var addr='http://192.168.222.60:5000';
            var addr='http://127.0.0.1:5000';
            var addr='http://''' + myip +''':5000';
            addr += '/'+$(lampa).attr('value');
            addr += '/'+$(lampa).attr('id');
            $.get(addr, function(response){
                alert(response);
            });
        }
        </script>
    </head>
    <body>
    <title>Misteln 13</title>
    <h1 width="50%">Kontrollpanel</h1>
    <div width="50%" class="content" data-role="content">
        <h2 width="50%">
            <button class="lampknapp" id="DarkLamp" value="off" height="80%">Fönsterlampor av</button>
            <button width="40%" class="lampknapp" id="DarkLamp" value="on">Fönsterlampor på</button>
        </h2>
        <h2 width="50%">
            <button width="50%" class="lampknapp" id="EngineHeater" value="off">Motorvärmare av</button><button class="lampknapp" id="EngineHeater" value="on">Motorvärmare på</button>
        </h2>
        <h2 width="50%">
            <button class="lampknapp" id="NightLamp" value="off">Barnlampor av</button><button class="lampknapp" id="NightLamp" value="on">Barnlampor på</button>
        </h2>
        <h2 width="50%">
            <button class="lampknapp" id="GarageLamp" value="off">Garage av</button><button class="lampknapp" id="GarageLamp" value="on">Garage på</button>
        </h2>
    </div>
    </body>
    '''
@app.route('/lab')
def lab():
    CalComm.lab()
    return '''Ready'''

@app.before_request
def log_request():

    if current_app.config.get('LOG_REQUESTS'):
        logger.debug('whatever')
        # Or if you dont want to use a logger, implement
        # whatever system you prefer here
        # print request.headers
        # open(current_app.config['REQUEST_LOG_FILE'], 'w').write('...')

@app.route('/on/<nexa_id>')
def on(nexa_id):
    CalComm.on(nexa_id)
    return 'Switched on %s' % nexa_id

@app.route('/off/<nexa_id>')
def off(nexa_id):
    CalComm.off(nexa_id)
    return 'Switched off %s' % nexa_id

@app.route('/init')
def init():
    try:


        #timeStamp = datetime.datetime('2015-06-01T16:00:00+0200')

        #CalComm.dbtest()

    #    CalComm.login()
        CalComm.getsunrisenset()
        return CalComm.getbookings(1)

    except Exception as e:
        return e.__str__()


@app.route('/fireTelldus')
def fireTelldus():
    CalComm.getbookings(1)
    return CalComm.fireTelldus()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

