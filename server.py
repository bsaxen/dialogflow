# Flask app should start in global layout
#from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()
try:
    from urllib.parse import urlparse, urlencode
except ImportError:
     from urlparse import urlparse
#from urllib.parse import urlparse, urlencode
from urllib2 import urlopen, Request,HTTPError
try:
    import urllib2 as urlreq # Python 2.x
except:
    import urllib.request as urlreq # Python 3.x

import json
import os
import thread

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

callback_function = None

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = callback_function(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def init_server(port, request_function):
    print("Starting app on port %d" % port)
    global callback_function
    callback_function = request_function
    app.run(debug=False, port=port, host='0.0.0.0')

#----------------------------------------------------
def intent_request(req):
#----------------------------------------------------
    intent = req.get("queryResult").get("intent").get("displayName")
    print("Dialogflow Intent:", intent)
    sc_url = "http://spacecollapse.simuino.com/"
#----------------------------------------------------
    if intent == "current_temperature":
#----------------------------------------------------
        place = req.get("queryResult").get("parameters").get("places")
        print("Place: " + place)
        comment = "Default " + place
        p_url = "astenas_hus_D10_0.single"
        #-----------------------
        # Nytomta
        #-----------------------
        if place == 'hus':
            p_url   = "astenas_hus_D10_0.single"
            comment = "Temperaturen (C) i huset: "
        #-----------------------
        if place == 'garage':
            p_url   = "astenas_nytomta_D2_0.single"
            comment = "Temperaturen (C) i garaget: No support "
        #-----------------------
        if place == 'labb':
            p_url   = "astenas_nytomta_D8_0.single"
            comment = "Temperaturen (C) i labbet: "
        #-----------------------
        if place == 'kontor':
            p_url   = "astena_mysrum_D11_0.single"
            comment = "Temperaturen (C) i kontoret: "
        #-----------------------
        if place == 'snickeri':
            p_url   = "astenas_nytomta_D2_0.single"
            comment = "Temperaturen (C) i snickeriet: No support"
        #-----------------------
        if place == 'pannrum':
            p_url   = "astenas_nytomta_D2_0.single"
            comment = "Temperaturen (C) i pannrummet: "
        #-----------------------
        if place == 'utomhus':
            p_url   = "astenas_nytomta_D8_1.single"
            comment = "Temperaturen (C) utomhus: "
        #-----------------------

        url = sc_url + p_url
        req = urlreq.Request(url)
        contents = urlreq.urlopen(req).read()
        result = comment + str(contents)
        print result
    elif intent == "current_power":
#----------------------------------------------------
        location = req.get("queryResult").get("parameters").get("location")
        print("Location: " + location)
        comment = "Default " + location
        p_url = "astenas_nytomta_nixie2_0.single"

        if location == 'kil':
            p_url   = "kil_kvv32_esp2_0.single"
            comment = "Elektrisk effekt (watt) just nu i Kil: "
        #-----------------------
        if location == 'nytomta':
            p_url   = "astenas_nytomta_nixie2_0.single"
            comment = "Elektrisk effekt (watt) just nu i Nytomta: "
        #-----------------------

        url = sc_url + p_url
        req = urlreq.Request(url)
        contents = urlreq.urlopen(req).read()
        result = comment + str(contents)
        print result
    else:
        result = "Hittade ingen data"


    # Dict that will be returned as JSON to Dialogflow
    return {
    # V1 API
        #"speech": "hej1",
        #"displayText": "hej2",
        #"data": data,
        #"contextOut": [],
        #"source": "benny"
    # V2 API
        "fulfillmentText": result,
        "fulfillmentMessages": [],
        #"payload": data,
        "outputContexts": [],
        "source": "benny"
    }

print 'Start Dialogflow Service...'
init_server(7777,intent_request)
print "...started"
