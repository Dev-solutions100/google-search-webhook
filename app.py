#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import requests
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from bs4 import BeautifulSoup
import urllib
import re

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
import pprint
import duckduckgo

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
    searchString = searchstring

    # KEYS SHOULDNT BE DISPLAYED
    my_api_key = "AIzaSyCdGOE_FUNxilcAd4hge330m5qr6p9K0Rc"
    my_cse_id = "005871159096424944872:s8zbwrmva57"
    searchResults = google_search(searchString, my_api_key, my_cse_id, num=3, dateRestrict="d1")    # search for the topic
    print("Search results are")
    print(searchResults)
    print("DONE RESULTS")
    if searchResults is None:
        return{}

    res = makeWebhookResult(searchResults, searchstring)
    return res


def google_search(search_term, api_key, cse_id, **kwargs):
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    
#     url = "https://duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com/"
#     querystring = {"no_redirect":"1","no_html":"1","callback":"process_duckduckgo","skip_disambig":"1","q":search_term,"format":"undefined"}
#     headers = {
#     'x-rapidapi-host': "duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com",
#     'x-rapidapi-key': "1ddaa42a65mshea3707d18590b92p19f14ejsn10f668df0edc"
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     print("FREEEEEEEEEEEEEE")
#     print(response.text)
#     print("FREEEEEEEEEEEEEE")
    
#     url="https://api.duckduckgo.com/"
#     querystring = {"no_redirect":"1","no_html":"1","skip_disambig":"1","q":search_term,"format":"json"}
#     headers={}
#     response = requests.request("GET", url, headers=headers, params=querystring)

    r1 = duckduckgo.get_zci(search_term)
#     r = duckduckgo.query(search_term)
    print("FREEEEEEEEEEEEEE1")
#     print(r.results)
#     print(r.related)
#     print(r.answer)
    print(r1)
    print("FREEEEEEEEEEEEEE1")


    sitesearch='http://www.google.com/?q='+search_term
    site = urllib.request.urlopen(sitesearch)
    data = site.read()

    parsed = BeautifulSoup(data)
    print("OK")
    print(parsed)
    soup = BeautifulSoup(parsed, 'html.parser')
#     topics = parsed.findAll('div', {'id': 'zero_click_topics'})[0]
#     results = topics.findAll('div', {'class': re.compile('results_*')})
    print("FREEEEEEEEEEEEEE2")
    print(parsed)
    a=soup.find_all("span", class_="f")[0]
    b=soup.find_all("span", class_="st")[0]
    c=soup.find_all("div", class_="r")[0]
    print(a)
    print(b)
    print(c)
    print("FREEEEEEEEEEEEEE2")
    
    return r1


def makeWebhookResult(data, searchstring):
    if (data is None):
        return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [{"text": {"text": ["Oops, unable to find anything on the web!"]}}],
        # "data": data,
        # "contextOut": [],
        "source": "google-search-webhook"
    }

#     articleUrl1 = data[0].get('formattedUrl')
#     articleSnippet1 = data[0].get('snippet')
    
#     articleUrl2 = data[1].get('formattedUrl')
#     articleSnippet2 = data[1].get('snippet')
    
#     articleUrl3 = data[0].get('formattedUrl')
#     articleSnippet3 = data[0].get('snippet')
    # print(json.dumps(item, indent=4))

   # speech = "*Please view these articles for latest information on " + searchstring + ":* " + "\n\n" + "1) "+ articleSnippet1+ "\n"+articleUrl1+ "\n\n" + "2) "+ articleSnippet2+ "\n"+articleUrl2
    speech=data
    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [{"text": {"text": [speech]}}],
        # "data": data,
        # "contextOut": [],
        "source": "google-search-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
