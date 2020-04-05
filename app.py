#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
import pprint

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# construct search query from result.parameters
def processRequest(req):

#     if req.get("result").get("action") != "googleSearch":
#         return {}
    json_params = req.get("queryResult").get("queryText")
    searchstring = ''    # this creates the overall topic which covers user's raw query
    
    print("JSON params is")
    print(json_params)
    print("DONE")
#     for value in json_params.values():
#         searchstring += value
#         searchstring += " "
    searchstring=json_params
    print(searchstring)
    searchString = "robot %s" % searchstring

    # KEYS SHOULDNT BE DISPLAYED
    my_api_key = "AIzaSyCdGOE_FUNxilcAd4hge330m5qr6p9K0Rc"
    my_cse_id = "005871159096424944872:s8zbwrmva57"
    searchResults = google_search(searchString, my_api_key, my_cse_id, num=1)    # search for the topic
    print("Search results are")
    print(searchResults)
    print("DONE RESULTS")
    if searchResults is None:
        return{}

    res = makeWebhookResult(searchResults, searchstring)
    return res


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def makeWebhookResult(data, searchstring):
    if (data[0] is None):
        return {}

    articleUrl = data[0].get('formattedUrl')
    # print(json.dumps(item, indent=4))

    speech = "Please view this article for more information on " + searchstring + ": " \
             + articleUrl

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [{"text": [speech]}],
        # "data": data,
        # "contextOut": [],
        "source": "google-search-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
