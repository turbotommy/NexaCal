#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'tommy'

from flask import Flask
from flask import request, current_app
from NexaCal import *

app = Flask(__name__)
CalComm=NexaCalWorker()
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)

# Also add the handler to Flask's logger for cases
#  where Werkzeug isn't used as the underlying WSGI server.
app.logger.addHandler(handler)

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
            var addr='http://192.168.222.43:5000';
            addr += '/'+$(lampa).attr('value');
            addr += '/'+$(lampa).attr('id');
            $.get(addr, function(response){
                alert(response);
            });
        }
        </script>
    </head>
    <body>
    <title>Misteln13</title>
    <h1 width="50%">Kontrollpanel</h1>
    <div width="50%" class="content" data-role="content">
        <h2 width="50%">
            <button class="lampknapp" id="1" value="off" height="80%">F�nsterlampor av</button>
            <button width="40%" class="lampknapp" id="1" value="on">F�nsterlampor p�</button>
        </h2>
        <h2 width="50%">
            <button class="lampknapp" id="2" value="off">Motorv%C3%A4rmare av</button><button class="lampknapp" id="2" value="on">Motorv%C3%A4rmare p�</button>
        </h2>
        <h2 width="50%">
            <button class="lampknapp" id="3" value="off">Barnlampor av</button><button class="lampknapp" id="3" value="on">Barnlampor p�</button>
        </h2>
        <h2 width="50%">
            <button class="lampknapp" id="5" value="off">Garage av</button><button class="lampknapp" id="5" value="on">Garage p�</button>
        </h2>
    </div>
    </body>
    '''

@app.route('/test')
def test():
    return '''Cool'''

@app.before_request
def log_request():

    if current_app.config.get('LOG_REQUESTS'):
        current_app.logger.debug('whatever')
        # Or if you dont want to use a logger, implement
        # whatever system you prefer here
        # print request.headers
        # open(current_app.config['REQUEST_LOG_FILE'], 'w').write('...')

@app.route('/on')
def on():
    return '''Switching on'''

@app.route('/off')
def off():
    return '''Switching off'''

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
