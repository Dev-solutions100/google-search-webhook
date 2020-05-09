#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import requests
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import emoji
import flag
from bs4 import BeautifulSoup
import urllib
import re
import random

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
import pprint
import duckduckgo
import facts

# Flask app should start in global layout
app = Flask(__name__)

r2=''

@app.route('/hook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# construct search query from result.parameters
def processRequest(req):

#     if req.get("result").get("action") != "googleSearch":
#         return {}
    if (req.get("sourcechatfuel")):
        if(req.get("task")=="news"):
            resp=news()
            return {
            "messages": [{"text": resp,
            "quick_replies": [
            {
            "title":"Mask Guidelines",
            "block_names": ["Avoid_English"]
            },
            {
            "title":"Surface",
            "block_names": ["Symptoms_English"]
            },
            {
            "title":"More",
            "block_names": ["More_English"]
            }]}]
            }
        if(req.get("task")=="cases"):
            locat=req.get("loc")
            resp=risk(locat)
            return {
            "messages": [{"text": resp,
            "quick_replies": [
            {
            "title":"Mask Guidelines",
            "block_names": ["Avoid_English"]
            },
            {
            "title":"Surface",
            "block_names": ["Symptoms_English"]
            },
            {
            "title":"More",
            "block_names": ["More_English"]
            }]}]
            }
    else:
        json_params1= req.get("queryResult").get("intent").get("displayName")
        json_params = req.get("queryResult").get("queryText")
        searchstring = ''    # this creates the overall topic which covers user's raw query
    
    #print("JSON params is")
    #print(json_params)
    #print("DONE")
#     for value in json_params.values():
#         searchstring += value
#         searchstring += " "
        searchstring=json_params
    #print(searchstring)
        searchString = searchstring

    # KEYS SHOULDNT BE DISPLAYED
        my_api_key = "AIzaSyCdGOE_FUNxilcAd4hge330m5qr6p9K0Rc"
        my_cse_id = "005871159096424944872:s8zbwrmva57"
        num=1
        if(json_params1=='Real Time Cases'):
            searchResults=maps_search(num)
        elif(json_params1=='Real Time Cases-Hindi'):
            num=2
            searchResults=maps_search(num)
        elif(json_params1=='Real Time Cases - custom' or json_params1=='Country' or json_params1=='Country1'):
            if(req.get("queryResult").get("parameters").get("geo-country")):
                if(req.get("queryResult").get("parameters").get("geo-country")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-country")
            searchResults=maps_search1(searchString,num)
        elif(json_params1=='Real Time Cases - custom-Hindi'):
            if(req.get("queryResult").get("parameters").get("geo-country")):
                if(req.get("queryResult").get("parameters").get("geo-country")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-country")
            num=2
            searchResults=maps_search1(searchString,num)
        elif(json_params1=='Bored'):
            searchResults=bored()
#         elif(json_params1=='Bored-Hindi'):
#             searchResults=boredh()
        elif(json_params1=='Suggestions'):
            searchResults=suggestions()
        elif(json_params1=='News'):
            searchResults=news(num)
        elif(json_params1=='News-Hindi'):
            num=2
            searchResults=news(num)
        elif(json_params1=='Risk - custom' or json_params1=='City1' or json_params1=='Start - no - custom' or json_params1=='Start - yes - custom'):
            if(req.get("queryResult").get("parameters").get("geo-city")):
                if(req.get("queryResult").get("parameters").get("geo-city")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-city")
            searchResults=risk(searchString,num)
        elif(json_params1=='Risk - custom-Hindi' or json_params1=='City1-Hindi' or json_params1=='LocYes' or json_params1=='LocNo'):
            if(req.get("queryResult").get("parameters").get("geo-city")):
                if(req.get("queryResult").get("parameters").get("geo-city")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-city")
            num=2
            searchResults=risk(searchString,num)
        elif(json_params1=='State - custom' or json_params1=='State1' or json_params1=='State4 - custom'):
            if(req.get("queryResult").get("parameters").get("geo-state")):
                if(req.get("queryResult").get("parameters").get("geo-state")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-state")
            searchResults=state(searchString,num)
        elif(json_params1=='State1-Hindi' or json_params1=='State2-Hindi' or json_params1=='State5-Hindi'):
            if(req.get("queryResult").get("parameters").get("geo-state")):
                if(req.get("queryResult").get("parameters").get("geo-state")!=''):
                    searchString=req.get("queryResult").get("parameters").get("geo-state")
            num=2
            searchResults=state(searchString,num)
        elif(json_params1=='Default-Hindi'):
            num=2
            searchResults=google_search(searchString,num)
        else:
            searchResults = google_search(searchString,num)    # search for the topic
    #print("Search results are")
    #print(searchResults)
    #print("DONE RESULTS")
        if searchResults is None:
            return{}

        res = makeWebhookResult(searchResults, searchstring)
        return res

# def chatfuel():
#     return {
#             "messages": [{"text": "Got it"}]
#         }
    
    
def risk(data,num):
    r6="\n\n"+emoji.emojize(':point_right:', use_aliases=True)+" Reply with *20* to change to *Hindi*"+"\n\n"
    chng=0
    if(data.lower()=="murgo"):
        data="ladakh"
        r1=state("ladakh",num)
        return r1
    if(data.lower()=="kanpur"):
        data="Kanpur Nagar"
    if(data.lower()=="madras"):
        data="chennai"
    if(data.lower()=="noida" or data.lower()=="greater noida"):
        data="Gautam Buddha Nagar"
    if(data.lower()=="bombay"):
        data="Mumbai"
    if(data.lower()=="bangalore" or data.lower()=="bengaluru"):
        data="Bengaluru Urban"
    if(data.lower()=="bangalore urban"):
        data="Bengaluru Urban"
    if(data.lower()=="bangalore rural"):
        data="Bengaluru Rural"
    if(data.lower()=="gurgaon"):
        data="Gurugram"
    if(data.lower()=="delhi"):
        r1=state("Delhi",num)
        return r1
    if(data.lower()=="allahabad"):
        data="Prayagraj"
    if(data.lower()=="calcutta"):
        data="Kolkata"
    url = "https://api.covid19india.org/v2/state_district_wise.json"
    err=0
    try:
        respo = requests.request("GET", url)
#         print("FREEEEEEEEEEEEEE")
#         print(respo.status_code)
    except:
        err=1
    finally:
        if(err==0):
            ##print("FREEEEEEEEEEEEEE")
            respo=respo.json()
            ##print("FREEEEEEEEEEEEEE")
            #l=len(respo)
            i1=''
            i2=''
            i3=''
            i4=''
            brk=0
            for itm in respo:
                if(brk==1):
                    break
                itm1=itm.get("districtData")
                for itm2 in itm1:
                    if(itm2.get("district").lower()==data.lower()):
                        i1=itm2.get("confirmed")
                        i2=itm2.get("recovered")
                        i3=itm2.get("deceased")
                        i4=itm2.get("district")
                        brk=1
                        break
            if(not(i1=='' and i2=='' and i3=='' and i4=='')):
                if(i4=='Gautam Buddha Nagar'):
                    i4='Gautam Buddha Nagar (Noida)'
                if(num==1):
                    if(chng==0):
                        r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+str(i3)
                    else:
                        r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+str(i3)+"\n\n"+emoji.emojize(':point_right:', use_aliases=True)+" Reply *Delhi* for total cases in Delhi"
                
                if(num==2):
                    if(chng==0):
                        r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+str(i3)
                    else:
                        r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+str(i3)+"\n\n"+emoji.emojize(':point_right:', use_aliases=True)+" दिल्ली के सारे मामले जानने के लिए *दिल्ली* लिखकर सेंड करे"
                
                urll = "https://api.covid19india.org/zones.json"
                err1=0
                try:
                    respo1 = requests.request("GET", urll)
                except:
                    err1=1
                finally:
                    if(err1==0):
                        respo1=respo1.json()
                        i5=''
                        itm5=respo1.get("zones")
                        for itm6 in itm5:
                            if(itm6.get("district").lower()==data.lower()):
                                i5=itm6.get("zone")
                                break
                        if(i5!=''):
                            if(i5=='Red'):
                                if(num==1):
                                    r1=r1+"\n\n"+emoji.emojize(':red_circle:', use_aliases=True)+" This district is in *"+i5+"* zone"
                                else:
                                    r1=r1+"\n\n"+emoji.emojize(':red_circle:', use_aliases=True)+" यह जिला रेड जोन में हैं"
                            if(i5=='Orange'):
                                if(num==1):
                                    r1=r1+"\n\n"+emoji.emojize(':large_orange_diamond:', use_aliases=True)+" This district is in *"+i5+"* zone"
                                else:
                                    r1=r1+"\n\n"+emoji.emojize(':large_orange_diamond:', use_aliases=True)+" यह जिला ऑरेंज जोन में हैं"
                            if(i5=='Green'):
                                if(num==1):
                                    r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" This district is in *"+i5+"* zone"
                                else:
                                    r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" यह जिला ग्रीन क्षेत्र में हैं"
                    if(num==1):
                        r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" Share this bot - https://wa.me/917380648641?text=Hi"+r6+emoji.emojize(':dart:', use_aliases=True)+" Want to see what more I can do? Reply with *0*!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with a *District/City/State/Country* to see its cases"+"\n"
                    else:
                        r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" शेयर करें - https://wa.me/917380648641?text=नमस्ते"+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" देखना चाहते है कि मैं और क्या-क्या कर सकता हूं? *0* लिखकर भेजें!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"और मामले देखने के लिए *जिला/शहर/राज्य/देश* का नाम लिख के भेजें (उदाहरण: *नोएडा*)"
                    return r1
            else:
                urll = "https://api.covid19india.org/zones.json"
                err1=0
                try:
                    respo1 = requests.request("GET", urll)
                except:
                    err1=1
                finally:
                    if(err1==0):
                        respo1=respo1.json()
                        i5=''
                        itm5=respo1.get("zones")
                        for itm6 in itm5:
                            if(itm6.get("district").lower()==data.lower()):
                                i5=itm6.get("zone")
                                i6=itm6.get("district")
                                break
                        if(i5!=''):
                            if(num==1):
                                r1=flag.flagize(":IN:")+" *"+i6+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+"0"+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+"0"+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+"0"
                                r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" This district is in *"+i5+"* zone"
                                r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" Share this bot - https://wa.me/917380648641?text=Hi"+r6+emoji.emojize(':dart:', use_aliases=True)+" Want to see what more I can do? Reply with *0*!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with a *District/City/State/Country* to see its cases"
                            else:
                                r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+"0"+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+"0"+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+"0"
                                r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" यह जिला ग्रीन क्षेत्र में हैं"
                                r1=r1+"\n\n"+emoji.emojize(':white_check_mark:', use_aliases=True)+" शेयर करें - https://wa.me/917380648641?text=नमस्ते"+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" देखना चाहते है कि मैं और क्या-क्या कर सकता हूं? *0* लिखकर भेजें!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"और मामले देखने के लिए *जिला/शहर/राज्य/देश* के नाम को लिखकर भेजें (उदाहरण: *नोएडा*)"
                        else:
                            if(num==1):
                                r1="Oops, *"+data+"* is *not a district!* You can *Google* up your district or check the district's name and try again (Ex: *Gautam Buddha Nagar*)."+r6+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with another *District/City/State/Country* to see its cases\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
                            else:
                                r1="माफ़ करें, *"+data+"* जिला नहीं हैं! कृपया जिले का नाम सर्च करें या जिले का नाम चेक करें और पुन: प्रयास करें (उदाहरण: *नोएडा*).\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"और मामले देखने के लिए *जिला/शहर/राज्य/देश* के नाम को लिखकर भेजें (उदाहरण: *नोएडा*)\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
                    return r1
        else:
            if(num==1):
                r1="Oops, there was an error! Please try again."+r6+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
            else:
                r1="कृपया पुन: प्रयास करें\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
            return r1        
        
def state(data,num):
    r6="\n\n"+emoji.emojize(':point_right:', use_aliases=True)+" Reply with *20* to change to *Hindi*"+"\n\n"
    if(data.lower()=="surat"):
        r1=risk("Surat",num)
        return r1
    url = "https://api.covid19india.org/data.json"
    err=0
    try:
        respo = requests.request("GET", url)
#         print("FREEEEEEEEEEEEEE")
#         print(respo.status_code)
    except:
        err=1
    finally:
        if(err==0):
            ##print("FREEEEEEEEEEEEEE")
            respo=respo.json()
            ##print("FREEEEEEEEEEEEEE")
            #l=len(respo)
            i1=''
            i2=''
            i3=''
            i4=''
            itm=respo.get("statewise")
            for itm1 in itm:
                if(itm1.get("state").lower()==data.lower()):
                    i1=itm1.get("confirmed")
                    i2=itm1.get("recovered")
                    i3=itm1.get("deaths")
                    i4=itm1.get("state")
                    break
            if(not(i1=='' and i2=='' and i3=='' and i4=='')):
                
                urlsec="https://api.covid19india.org/states_daily.json"
                respo = requests.request("GET", urlsec)
                respo=respo.json()
                respo1=respo.get("states_daily")
                l=len(respo1)
                if(i4.lower()=='uttar pradesh'):
                    stt='up'
                
                if(i4.lower()=='west bengal'):
                    stt='wb'
                
                if(i4.lower()=='maharashtra'):
                    stt='mh'
                
                if(i4.lower()=='gujarat'):
                    stt='gj'
                
                if(i4.lower()=='tamil nadu'):
                    stt='tn'
                
                if(i4.lower()=='delhi'):
                    stt='dl'
                
                if(i4.lower()=='rajasthan'):
                    stt='rj'
                
                if(i4.lower()=='madhya pradesh'):
                    stt='mp'
                
                if(i4.lower()=='andhra pradesh'):
                    stt='ap'
                
                if(i4.lower()=='punjab'):
                    stt='pb'
                
                if(i4.lower()=='telangana'):
                    stt='tg'
                
                if(i4.lower()=='jammu and kashmir'):
                    stt='jk'
                
                if(i4.lower()=='karnataka'):
                    stt='ka'
                
                if(i4.lower()=='haryana'):
                    stt='hr'
                
                if(i4.lower()=='kerala'):
                    stt='kl'
                
                if(i4.lower()=='bihar'):
                    stt='br'
                
                if(i4.lower()=='odisha'):
                    stt='or'
                
                if(i4.lower()=='chandigarh'):
                    stt='ch'
                
                if(i4.lower()=='jharkhand'):
                    stt='jh'
                
                if(i4.lower()=='tripura'):
                    stt='tr'
                
                if(i4.lower()=='uttarakhand'):
                    stt='ut'
                
                if(i4.lower()=='chhattisgarh'):
                    stt='ct'
                
                if(i4.lower()=='assam'):
                    stt='as'
                
                if(i4.lower()=='himachal pradesh'):
                    stt='hp'
                
                if(i4.lower()=='ladakh'):
                    stt='la'
                
                if(i4.lower()=='andaman and nicobar islands'):
                    stt='an'
                
                if(i4.lower()=='meghalaya'):
                    stt='ml'
                
                if(i4.lower()=='puducherry'):
                    stt='py'
                
                if(i4.lower()=='goa'):
                    stt='ga'
                
                if(i4.lower()=='manipur'):
                    stt='mn'
                
                if(i4.lower()=='mizoram'):
                    stt='mz'
                
                if(i4.lower()=='arunachal pradesh'):
                    stt='ar'
                
                if(i4.lower()=='dadra and nagar haveli and daman and diu'):
                    stt='dn'
                
                if(i4.lower()=='nagaland'):
                    stt='nl'
                
                if(i4.lower()=='daman and diu'):
                    stt='dd'
                
                if(i4.lower()=='lakshadweep'):
                    stt='ld'
                
                if(i4.lower()=='sikkim'):
                    stt='sk'
                
                
                infod=respo1[l-1]
                infod=infod[stt]
                infor=respo1[l-2]
                infor=infor[stt]
                infoc=respo1[l-3]
                infoc=infoc[stt]
                
                
                
                if(num==1):
                    r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+str(i3)+"\n\n"+"*In last 24 hours:*\n\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" Cases: "+str(infoc)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" Recovered: "+str(infor)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" Deaths: "+str(infod)+r6+emoji.emojize(':dart:', use_aliases=True)+" Want to see what more I can do? Reply with *0*!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with a *State* to see its cases\n"
                else:
                    r1=flag.flagize(":IN:")+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+str(i3)+"\n\n"+"*पिछले 24 घंटों में:*\n\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" मामले: "+str(infoc)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" ठीक हुए: "+str(infor)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" मौतें: "+str(infod)+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" देखना चाहते है कि मैं और क्या-क्या कर सकता हूं? *0* लिखकर भेजें!\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"किसी भी राज्य के मामले देखने के लिए उसका नाम लिख कर सेंड करे (उदाहरण: *उत्तर प्रदेश*)\n\n"
                return r1
            else:
                if(num==1):
                    r1="Please check the state's name (Ex: *Uttar Pradesh*) and try again."+r6+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
                else:
                    r1="कृपया राज्य का नाम चेक करें (उदाहरण: *उत्तर प्रदेश*) और पुन: प्रयास करें.\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
                return r1
        else:
            if(num==1):
                r1="Oops, there was an error! Please try again."+r6+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
            else:
                r1="कृपया पुन: प्रयास करें\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
            return r1
        
def news(num):
    global r2
    r2=''
    r1=''
    tcopy1='123#*'
    tcopy2='789#*'
    if(r1==''):
        r1=''
        if(num==1):
            textsearch="Coronavirus India"
        else:
            textsearch="Coronavirus India"
        sitesearch='https://www.bing.com/news/search?q='+textsearch
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
        if(num==1):
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        else:
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        err=0
        try:
            source_code = requests.get(sitesearch,headers=headers)
        except:
            err=1
            tcopy1=''
            tcopy2=''
        finally:
            if(err==0):
                plain_text = source_code.text
                #print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
        ##print(plain_text)
                soup1 = BeautifulSoup(plain_text, "html.parser")
#         [s.extract() for s in soup1('div' { "class" : "t_s" })]
#         unwantedTags = ['strong', 'cite']
#         for tag in unwantedTags:
#             for match in soup1.findAll(tag):
#                 match.replaceWithChildren()
            
                results = soup1.findAll('div',{ "class" : "t_s" })
                #print("FREEEEEEEEEEEEEE2")
                a=1
                b=1
                c=1
                test_list = [1, 2, 3, 4, 5, 6, 7]
                text1=''
                text2=''
                text3=''
                ran=random.choice(test_list)
        
                for result in results:
                    if(a==ran):
                        ch=(result.find('div',{ "class" : "t_t" })).find('a')
                        text2=ch['href']
                        #print("LINK: "+ch['href']+"\n#")
                        #print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                        ch1=result.find('div',{ "class" : "snippet" })
                        text1=ch1['title']
                        #print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                        #print("# ___________________________________________________________\n#")
                        break
                    a=a+1
                tcopy1=text1
            
                #print(text1)    
                #print(text2)
                if(text2!=''):
                    if(text1!=''):
                        if(num==1):
                            r1=r1+flag.flagize(":IN:")+" *India:* "+text1+" ("
                        else:
                            r1=r1+flag.flagize(":IN:")+" *भारत:* "+text1+" ("
                        r1=r1+text2+")"
                    else:
                        if(num==1):
                            r1=r1+flag.flagize(":IN:")+" *India:* "+text2
                        else:
                            r1=r1+flag.flagize(":IN:")+" *भारत:* "+text2
                else:
                    if(num==1):
                        r1=r1+flag.flagize(":IN:")+" *India:* "+text1
                    else:
                        r1=r1+flag.flagize(":IN:")+" *भारत:* "+text1
                tcopy2=text2
                #print("FREEEEEEEEEEEEEE2")
            
                tcopy3='123#*'
                tcopy4='789#*'
                if(num==1):
                    textsearch="Coronavirus Global"
                else:
                    textsearch="Coronavirus Global"
                sitesearch='https://www.bing.com/news/search?q='+textsearch
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
                if(num==1):
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
                else:
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
                err1=0
                try:
                    source_code = requests.get(sitesearch,headers=headers)
                except:
                    err1=1
                    tcopy3=''
                    tcopy4=''
                finally:
                    if(err1==0):
                        plain_text = source_code.text
                        #print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
        ##print(plain_text)
                        soup1 = BeautifulSoup(plain_text, "html.parser")
        #         [s.extract() for s in soup1('div' { "class" : "t_s" })]
        #         unwantedTags = ['strong', 'cite']
        #         for tag in unwantedTags:
        #             for match in soup1.findAll(tag):
        #                 match.replaceWithChildren()
                        results = soup1.findAll('div',{ "class" : "t_s" })
                        #print("FREEEEEEEEEEEEEE2")
                        a=1
                        b=1
                        c=1
                        test_list = [1, 2, 3, 4, 5, 6, 7]
                        text1=''
                        text2=''
                        text3=''
                        ran=random.choice(test_list)
                        for result in results:
                            if(a==ran):
                                ch=(result.find('div',{ "class" : "t_t" })).find('a')
                                text2=ch['href']
                                #print("LINK: "+ch['href']+"\n#")
                                #print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                                ch1=result.find('div',{ "class" : "snippet" })
                                text1=ch1['title']
                                #print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                                #print("# ___________________________________________________________\n#")
                                break
                            a=a+1
                        #print(text1)
        
                        tcopy3=text1
                        #print(text2)
                        if(r1!=''):
                            r1=r1+"\n\n"
                        if(text2!=''):
                            if(text1!=''):
                                if(num==1):
                                    r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *Global:* "+text1+" ("
                                else:
                                    r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *दुनिया:* "+text1+" ("
                                r1=r1+text2+")"
                            else:
                                if(num==1):
                                    r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *Global:* "+text2
                                else:
                                    r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *दुनिया:* "+text2
                        else:
                            if(num==1):
                                r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *Global:* "+text1
                            else:
                                r1=r1+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *दुनिया:* "+text1
                        tcopy4=text2
        
        
                        if(1==1):
                            if(tcopy1=='' and tcopy2=='' and tcopy3=='' and tcopy4==''):
                                if(num==1):
                                    r1=emoji.emojize(':mag_right:', use_aliases=True)+' Oops, I found zero results for your search. You can always try again!\n\n'+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
                                else:
                                    r1=emoji.emojize(':mag_right:', use_aliases=True)+' कृपया पुन: प्रयास करें\n\n'+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
                        if(num==1):
                            r1=r1+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *6* for more News\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
                        else:
                            r1=r1+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"और खबरों के लिए *6* लिख के भेजें\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
                        return r1


def bored():
#     arr=["recreational", "social", "diy", "charity", "cooking", "relaxation", "music"]
#     act=random.choice(arr)
#     url = "http://www.boredapi.com/api/activity?type="+act
#     respo = requests.request("GET", url)
#     respo=respo.json()
#     activity=respo.get("activity")

    f = open('activities.json') 
    datas = json.load(f)
    n=random.randint(0, 99)
    activity=datas[n].get("activity")
    
    test_list = [1, 2]
    ran=random.choice(test_list)
    if(ran==1):
        fact=random.choice(facts.useless_facts)
    else:
        trivia=random.choice(facts.triviaa)
        triv=trivia[0]
        if(trivia[1]=='false'):
            vl='This is a myth! Hence, not true.'
        else:
            vl='This is actually true!'
#         url = "numbersapi.com/random/trivia"
#         respo = requests.request("GET", url)
#         respo=respo.json()
#         act=respo.get("activity")
      
    f = open('quotes.json') 
    datas = json.load(f)
    n=random.randint(0, 497)
    quote=datas[n].get("content")
    author=datas[n].get("author")

#     #print("JOKE")
#     #print(joke)
#     #print(activity)
#     #print(fact)
#     #print(quote)
#     #print(author)
    
    headers={'User-Agent':'My Library (https://github.com/Dev-solutions100/google-search-webhook)'}
    url = "https://icanhazdadjoke.com/slack"
    err=0
    try:
        respo = requests.request("GET", url, headers=headers)
    except:
        err=1
    finally:
        if(err==0):
            respo=respo.json()
            joke=respo.get("attachments")[0].get("text")
        else:
            ar=["What doy call an alligator in a vest? An in-vest-igator!","An apple a day keeps the bullies away. If you throw it hard enough.","Did you hear about the two thieves who stole a calendar? They each got six months.","What has ears but cannot hear? A field of corn."]
            joke=random.choice(ar)
    
        if(ran==1):
            r1=emoji.emojize(':sunglasses:', use_aliases=True)+" *What you can do:* "+activity+"\n"+emoji.emojize(':hushed:', use_aliases=True)+" *Fact:* "+fact+"\n"+emoji.emojize(':relieved:', use_aliases=True)+" *Quote:* "+quote+" (By - "+author+")"+"\n"+emoji.emojize(':joy:', use_aliases=True)+" *Joke:* "+joke+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" *Want to play quiz? Reply 11*\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *5* to get more Ideas\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
        else:
            r1=emoji.emojize(':sunglasses:', use_aliases=True)+" *What you can do:* "+activity+"\n"+emoji.emojize(':hushed:', use_aliases=True)+" *Trivia:* "+triv+" *("+vl+")*"+"\n"+emoji.emojize(':relieved:', use_aliases=True)+" *Quote:* "+quote+" (By - "+author+")"+"\n"+emoji.emojize(':joy:', use_aliases=True)+" *Joke:* "+joke+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" *Want to play quiz? Reply 11*\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *5* to get more Ideas\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
        return r1
    
    #emoji.emojize(':clapper:', use_aliases=True)" *Suggested Movie:* "+movie+"\n\n"+emoji.emojize(':musical_note:', use_aliases=True)+"*Suggested Song:* "+song

def suggestions():
    
    f = open('movies.json') 
    datas = json.load(f)
    n=random.randint(0, 3430)
    movie=datas[n].get("title")
    yr=datas[n].get("year")
    genre=datas[n].get("genres")
    gen=", ".join(genre)
    
    test_list = [1, 2]
    ran=random.choice(test_list)
    if(ran==1):
        f = open('games.json') 
        datas = json.load(f)
        n=random.randint(0, 547)
        game=datas[n].get("title")
    else:
        f = open('books.json') 
        datas = json.load(f)
        n=random.randint(0, 5980)
        book=datas[n].get("title")
        author=datas[n].get("authors")
        rating=datas[n].get("average_rating")
    
    tvseries=random.choice(facts.tv_series)
    
    f = open('songs.json') 
    datas = json.load(f)
    n=random.randint(0, 9000)
    song=datas[n].get("title")
    artist=datas[n].get("artist")
    yrsongs=datas[n].get("date")
    arr=song.split()
    arr1=artist.split()
    arr2=arr+arr1
    qr="+".join(arr2)
    link='https://www.youtube.com/results?search_query='+qr
    
    if(ran==1):
        r1="*Here are your suggestions:*\n\n"+emoji.emojize(':clapper:', use_aliases=True)+" *Movie:* "+movie+" ("+str(yr)+", "+gen+")"+"\n"+emoji.emojize(':notes:', use_aliases=True)+" *Song:* "+song+" - By "+artist+"\n"+emoji.emojize(':video_game:', use_aliases=True)+" *Game:* "+game+" (PC Game)\n"+emoji.emojize(':tv:', use_aliases=True)+" *Tv-Series:* "+tvseries+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" *Want to play quiz? Reply 11*\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *6* to get more Suggestions\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
    else:
        r1="*Here are your suggestions:*\n\n"+emoji.emojize(':clapper:', use_aliases=True)+" *Movie:* "+movie+" ("+str(yr)+", "+gen+")"+"\n"+emoji.emojize(':notes:', use_aliases=True)+" *Song:* "+song+" - By "+artist+"\n"+emoji.emojize(':blue_book:', use_aliases=True)+" *Book:* "+book+" (By - "+author+", Rating - "+str(rating)+")\n"+emoji.emojize(':tv:', use_aliases=True)+" *Tv-Series:* "+tvseries+"\n\n"+emoji.emojize(':dart:', use_aliases=True)+" *Want to play quiz? Reply 11*\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *6* to get more Suggestions\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
    return r1
    
def maps_search(num):
    global r2
    err=0
#     url = "https://api.covid19api.com/summary"
    url="https://corona.lmao.ninja/v2/continents"
    try:
        respo = requests.request("GET", url)
    except:
        err=1
        g1="3,000,000+"
        g2="1,000,000+"
        g3="200,000+"
    finally:
        if(err==0):
            #print("FREEEEEEEEEEEEEE")
            respo=respo.json()
            #print(respo.get("Global").get("TotalConfirmed"))
            #print("FREEEEEEEEEEEEEE")
            g1=0
            g2=0
            g3=0
            for itm in respo:
                g1=int(g1)+int(itm.get("cases"))
                g2=int(g2)+int(itm.get("recovered"))
                g3=int(g3)+int(itm.get("deaths"))
#             g1=respo.get("Global").get("TotalConfirmed")
#             g2=respo.get("Global").get("TotalRecovered")
#             g3=respo.get("Global").get("TotalDeaths")
        err1=0
        #url="https://api.covid19api.com/total/dayone/country/india"
        url = "https://corona.lmao.ninja/v2/countries/india"
        try:
            respo = requests.request("GET", url)
        except:
            err1=1
            i1="40,000+"
            i2="10,000+"
            i3="1000+"
        finally:
            if(err1==0):
#                 respo = requests.request("GET", url)
                ##print("FREEEEEEEEEEEEEE")
                respo=respo.json()
                ##print("FREEEEEEEEEEEEEE")
#                 l=len(respo)
#                 i1=respo[l-1].get("Confirmed")
#                 i2=respo[l-1].get("Recovered")
#                 i3=respo[l-1].get("Deaths")
                i1=respo.get("cases")
                i2=respo.get("recovered")
                i3=respo.get("deaths")
            if(num==1):
                r1=flag.flagize(":IN:")+" *India*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+"Total cases: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+str(i3)+"\n\n"+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *Globally*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+str(g1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(g2)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total deaths: "+str(g3)+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with a country's name to see its cases (Example: *Italy*)\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* for Main Menu"
            else:
                r1=flag.flagize(":IN:")+" *भारत*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+str(i3)+"\n\n"+emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *दुनिया*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(g1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(g2)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" कुल मौतें: "+str(g3)+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"किसी भी देश के मामले देखने के लिए उसका नाम लिख कर भेजें (उदाहरण: *इटली*)\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
            return r1

def maps_search1(data,num):
    global r2
    if(data.lower()=="england" or data.lower()=="uk" or data.lower()=="britain" or data.lower()=="great britain" or data.lower()=="scotland"):
#         data="United Kingdom"
        data="uk"
    if(data.lower()=="america" or data.lower()=="us" or data.lower()=="usa" or data.lower()=="united states of america" or data.lower()=="united states"):
        #data="United States"
        data="usa"
#     url = "https://api.covid19api.com/summary"
#     respo = requests.request("GET", url)
#     #print("FREEEEEEEEEEEEEE")
#     respo=respo.json()
#     #print(respo.get("Global").get("TotalConfirmed"))
#     #print("FREEEEEEEEEEEEEE")
#     g1=respo.get("Global").get("TotalConfirmed")
#     g2=respo.get("Global").get("TotalRecovered")
#     g3=respo.get("Global").get("TotalDeaths")

#     text1=''
#     for ele in data:
#         if(ele!=' '):
#             text1=text1+ele.lower()
#         else:
#             text1=text1+'-'
            
#     data1=''
#     a=0
#     b=0
#     for ele in data:
#         if(a==0):
#             data1=data1+ele.upper()
#             a=1
#         else:
#             if(ele==' '):
#                 b=1
#                 data1=data1+ele
#             else:
#                 if(b==0):
#                     data1=data1+ele
#                 else:
#                     data1=data1+ele.upper()
#                     b=0

#     url = "https://api.covid19api.com/total/dayone/country/"+text1
    url="https://corona.lmao.ninja/v2/countries"
    err=0
    try:
        respo = requests.request("GET", url)
#         print("FREEEEEEEEEEEEEE")
#         print(respo.status_code)
    except:
        err=1
    finally:
        if(err==0):
            ##print("FREEEEEEEEEEEEEE")
            respo=respo.json()
            ##print("FREEEEEEEEEEEEEE")
            l=len(respo)
            i1=''
            i2=''
            i3=''
            i4=''
            for itm in respo:
                if(itm.get("country").lower()==data.lower()):
                    i1=itm.get("cases")
                    i2=itm.get("recovered")
                    i3=itm.get("deaths")
                    i4=itm.get("country")
                    infot=itm.get("tests")
                    break
            if(not(i1=='' and i2=='' and i3=='' and i4=='')):
#                 i1=respo[l-1].get("Confirmed")
#                 i2=respo[l-1].get("Recovered")
#                 i3=respo[l-1].get("Deaths")
#                 i4=respo[l-1].get("Country")
             
                urlc="https://disease.sh/v2/countries"
                headers={'yesterday':'true'}
                respos = requests.request("GET",urlc)
                print("FFFFFFFFFFFFFFFFFFFFFF")
                print(respos)
                respos=respos.json()
                for itmt in respos:
                    if(itmt.get("country").lower()==data.lower()):
                        print(itmt)
                        infoc=itmt.get("todayCases")
                        infod=itmt.get("todayDeaths")
    
                if(num==1):
                    r1=emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" Total cases: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" Total recovery: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" Total deaths: "+str(i3)+"\n\n"+"*In last 24 hours:*\n\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" Cases: "+str(infoc)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" Deaths: "+str(infod)+"\n\n"+emoji.emojize(':syringe:', use_aliases=True)+" *Total tests done:* "+str(infot)+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply with any country's name to see its cases (Example: *Spain*)\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* to see more options"
                else:
                    r1=emoji.emojize(':globe_with_meridians:', use_aliases=True)+" *"+i4+"*\n\n"+emoji.emojize(':bar_chart:', use_aliases=True)+" कुल मामले: "+str(i1)+"\n"+emoji.emojize(':chart_with_upwards_trend:', use_aliases=True)+" ठीक हुए: "+str(i2)+"\n"+emoji.emojize(':chart_with_downwards_trend:', use_aliases=True)+" कुल मौतें: "+str(i3)+"\n\n"+"*पिछले 24 घंटों में:*\n\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" मामले: "+str(infoc)+"\n"+emoji.emojize(':arrow_up:', use_aliases=True)+" मौतें: "+str(infod)+"\n\n"+emoji.emojize(':syringe:', use_aliases=True)+" *कुल टेस्ट्स:* "+str(infot)+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"किसी भी देश के मामले देखने के लिए उसका नाम लिख कर भेजें (उदाहरण: *इटली*)\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
            else:
                if(num==1):
                    r1="Please check the country's name (Ex: *New Zealand*) and try again.\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* to see more options"
                else:
                    r1="कृपया देश का नाम चेक करें (उदाहरण: *इटली*) और पुन: प्रयास करें.\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
        else:
            if(num==1):
                r1="Oops, there was an error! Please try again.\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"Reply *0* to see more options"
            else:
                r1=emoji.emojize(':mag_right:', use_aliases=True)+' कृपया पुन: प्रयास करें\n\n'+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
        return r1

def google_search(search_term, num):
    global r2
    r2=''
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    
#     url = "https://duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com/"
#     querystring = {"no_redirect":"1","no_html":"1","callback":"process_duckduckgo","skip_disambig":"1","q":search_term,"format":"undefined"}
#     headers = {
#     'x-rapidapi-host': "duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com",
#     'x-rapidapi-key': "1ddaa42a65mshea3707d18590b92p19f14ejsn10f668df0edc"
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     #print("FREEEEEEEEEEEEEE")
#     #print(response.text)
#     #print("FREEEEEEEEEEEEEE")
    
#     url="https://api.duckduckgo.com/"
#     querystring = {"no_redirect":"1","no_html":"1","skip_disambig":"1","q":search_term,"format":"json"}
#     headers={}
#     response = requests.request("GET", url, headers=headers, params=querystring)

    #r1 = duckduckgo.get_zci(search_term)
#     r = duckduckgo.query(search_term)
#    #print("FREEEEEEEEEEEEEE1")
#     #print(r.results)
#     #print(r.related)
#     #print(r.answer)

#     #print(r1)
#     #print("FREEEEEEEEEEEEEE1")
#     rcopy=r1
    r1=''
    tcopy1='123#*'
    tcopy2='789#*'
    #if(r1=='' or r1[:4]=='http'):
    if(r1==''):
        r1=''
        
        #sitesearch='https://www.google.com/search?q='+search_term
        
#     site = urllib.request.urlopen(sitesearch)
#     data = site.read()

#     parsed = BeautifulSoup(data)


#         headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
#         source_code = requests.get(sitesearch,headers=headers)
#         plain_text = source_code.text
#         #print("OK")
#         ##print(plain_text)
#         soup = BeautifulSoup(plain_text, "html.parser")
        
        
        if(num==2):
            search_term=search_term
        sitesearch='https://www.bing.com/search?q='+search_term
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
        if(num==1):
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        else:
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}

        err=0
        try:
            source_code = requests.get(sitesearch,headers=headers)
        except:
            err=1
        finally:
            if(err==0):
                plain_text = source_code.text
                #print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
            ##print(plain_text)
                soup1 = BeautifulSoup(plain_text, "html.parser")
                [s.extract() for s in soup1('span')]
                unwantedTags = ['strong', 'cite']
                for tag in unwantedTags:
                    for match in soup1.findAll(tag):
                        match.replaceWithChildren()
            
                results = soup1.findAll('li', { "class" : "b_algo" })
#         for result in results:
#             ch=(result.find('h2')).find('a')
#             #print("LINK: "+ch['href']+"\n#")
#             #print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
#             #print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
#             #print("# ___________________________________________________________\n#")
        
        
#     topics = parsed.findAll('div', {'id': 'zero_click_topics'})[0]
#     results = topics.findAll('div', {'class': re.compile('results_*')})
                #print("FREEEEEEEEEEEEEE2")
    ##print(parsed)
                a=1
                b=1
                c=1
                test_list = [1, 2, 3, 4]
                text1=''
                text2=''
                text3=''
                ran=random.choice(test_list)
        
#         for desc in soup.find_all("span",{"class":"st"}):
#             if(a==ran):
#                 text1=desc.text
#                 break
#             a=a+1
#         #print(text1)
        
                for result in results:
                    if(a==ran):
                        ch=(result.find('h2')).find('a')
                        text2=ch['href']
                        #print("LINK: "+ch['href']+"\n#")
                        #print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                        txts=result.find('p')
                        text1=txts.text
                        #print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                        #print("# ___________________________________________________________\n#")
                        break
                    a=a+1
        
        
        
#         d=0
#         if(text3==''):
#             text1=''
#         else:
#             for elem in text3:
#                 if(d==20):
#                     break
#                 if(elem!=' '):
#                     text1=text1+elem
#                 else:
#                     text1=text1+elem
#                     d=d+1
                
                tcopy1=text1
                if(text1!=''):
                    text1=altertext(text1)
    
#         for descc in soup.find_all("div",{"class":"r"}):
#             if(b==ran):
#                 children = descc.findChildren("a" , recursive=False)
#                 for child in children:
#                     text2= child['href']
#                     break
#             if(b==ran):
#                 break
#             b=b+1
            
                #print(text1)    
                #print(text2)
                if(text2!=''):
                    if(text1!=''):
                        r1=r1+text1+"\n\n"
                        r1=r1+text2
                    else:
                        r1=r1+text2
#             r1=r1+text1+" ("
#             r1=r1+text2+")"
                else:
                    r1=r1+text1
                tcopy2=text2
    
#     for desccc in soup.find_all("h3",{"class":"r"}):
#         if(c==ran):
#             text3=desccc.text
#             break
#         c=c+1
#     #print(text3)
#     a=soup.find_all("span", class_="f")[0]
#     b=soup.find_all("span", class_="st")[0]
#     c=soup.find_all("div", class_="r")[0]
#     #print(a)
#     #print(b)
#     #print(c)
            #print("FREEEEEEEEEEEEEE2")
    #if(rcopy=='' or rcopy[:4]=='http'):
            if(num==1):
                r1=emoji.emojize(':mag_right:', use_aliases=True)+" *I found this:* "+r1
            else:
                r1=emoji.emojize(':mag_right:', use_aliases=True)+" *मुझे यह मिला:* "+r1+"\n\n"+emoji.emojize(':round_pushpin:', use_aliases=True)+"मुख्य मैन्यू के लिए *0* लिख के भेजें"
            if(1==1):
                if(tcopy1=='' and tcopy2==''):
                    if(num==1):
                        r1='Oops, I found zero results for your search. You can always try again!'
                    else:
                        r1='मुझे इससे सम्बंधित कुछ नहीं मिला.कृपया पुन: प्रयास करें.'
    else:
        if(num==1):
            r1='Oops, I found zero results for your search. You can always try again!'
        else:
            r1='कृपया पुन: प्रयास करें'
    return r1

def altertext(text):
    splitted=text.split()
    l=len(splitted)
    c=0
    d=0
    str=''
    wr='...'
    for w in splitted:
        c=c+1
        if(c>59):
            d=1
            if(w=='...'):
                str+w
            else:
                wr=w
                str=str+w+" "
            break
        str=str+w+" "
    
    if(wr!='...'):
        str=str+"..."
        return str
    else:
        if(d==0):
            if(splitted[l-1]!='...'):
                str=str+'...'
            else:
                str=str.strip()
        return str

def makeWebhookResult(data, searchstring):
    global r2
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
    # #print(json.dumps(item, indent=4))

   # speech = "*Please view these articles for latest information on " + searchstring + ":* " + "\n\n" + "1) "+ articleSnippet1+ "\n"+articleUrl1+ "\n\n" + "2) "+ articleSnippet2+ "\n"+articleUrl2
    speech=data
    #print("Response:")
    #print(speech)
    if(r2==''):
        return {
            "fulfillmentText": speech,
            "fulfillmentMessages": [{"text": {"text": [speech]}}],
            # "data": data,
            # "contextOut": [],
            "source": "google-search-webhook"
        }
    else:
        return {
            "fulfillmentText": speech,
            "fulfillmentMessages": [{"text": {"text": [speech]}},{"text": {"text": [r2]}}],
            # "data": data,
            # "contextOut": [],
            "source": "google-search-webhook"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
