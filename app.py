#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import requests
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import emoji
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
    json_params1= req.get("queryResult").get("intent").get("displayName")
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
    if(json_params1=='Real Time Cases'):
        searchResults=maps_search()
    elif(json_params1=='Real Time Cases - custom'):
        searchResults=maps_search1(searchString)
    elif(json_params1=='Bored'):
        searchResults=bored()
    elif(json_params1=='News'):
        searchResults=news()
    else:
        searchResults = google_search(searchString, my_api_key, my_cse_id, num=3, dateRestrict="d1")    # search for the topic
    print("Search results are")
    print(searchResults)
    print("DONE RESULTS")
    if searchResults is None:
        return{}

    res = makeWebhookResult(searchResults, searchstring)
    return res

def news():
    global r2
    r2=''
    r1=''
    tcopy1='123#*'
    tcopy2='789#*'
    if(r1==''):
        r1=''
        textsearch="Coronavirus India"
        sitesearch='https://www.bing.com/news/search?q='+textsearch
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        source_code = requests.get(sitesearch,headers=headers)
        plain_text = source_code.text
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
        #print(plain_text)
        soup1 = BeautifulSoup(plain_text, "html.parser")
#         [s.extract() for s in soup1('div' { "class" : "t_s" })]
#         unwantedTags = ['strong', 'cite']
#         for tag in unwantedTags:
#             for match in soup1.findAll(tag):
#                 match.replaceWithChildren()
            
        results = soup1.findAll('div',{ "class" : "t_s" })
        print("FREEEEEEEEEEEEEE2")
        a=1
        b=1
        c=1
        test_list = [1, 2, 3, 4, 5]
        text1=''
        text2=''
        text3=''
        ran=random.choice(test_list)
        
        for result in results:
            if(a==ran):
                ch=(result.find('div',{ "class" : "t_t" })).find('a')
                text2=ch['href']
                print("LINK: "+ch['href']+"\n#")
                print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                ch1=result.find('div',{ "class" : "snippet" })
                text1=ch1['title']
                print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                print("# ___________________________________________________________\n#")
                break
            a=a+1
        tcopy1=text1
            
        print(text1)    
        print(text2)
        if(text2!=''):
            r1=r1+emoji.emojize(':in:', use_aliases=True)+" *India*"+text1+" ("
            r1=r1+text2+")"
        else:
            r1=r1+text1
        tcopy2=text2
        print("FREEEEEEEEEEEEEE2")
        
        tcopy3='123#*'
        tcopy4='789#*'
        textsearch="Coronavirus Global"
        sitesearch='https://www.bing.com/news/search?q='+textsearch
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        source_code = requests.get(sitesearch,headers=headers)
        plain_text = source_code.text
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
        #print(plain_text)
        soup1 = BeautifulSoup(plain_text, "html.parser")
        #         [s.extract() for s in soup1('div' { "class" : "t_s" })]
        #         unwantedTags = ['strong', 'cite']
        #         for tag in unwantedTags:
        #             for match in soup1.findAll(tag):
        #                 match.replaceWithChildren()
        results = soup1.findAll('div',{ "class" : "t_s" })
        print("FREEEEEEEEEEEEEE2")
        a=1
        b=1
        c=1
        test_list = [1, 2, 3, 4, 5]
        text1=''
        text2=''
        text3=''
        ran=random.choice(test_list)
        for result in results:
            if(a==ran):
                ch=(result.find('div',{ "class" : "t_t" })).find('a')
                text2=ch['href']
                print("LINK: "+ch['href']+"\n#")
                print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                ch1=result.find('div',{ "class" : "snippet" })
                text1=ch1['title']
                print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                print("# ___________________________________________________________\n#")
                break
            a=a+1
        print(text1)
        
        tcopy3=text1
        print(text2)
        if(r1!=''):
            r1=r1+"\n\n"
        if(text2!=''):
            r1=r1+emoji.emojize('::globe_with_meridians::', use_aliases=True)+" *Globa*"text1+" ("
            r1=r1+text2+")"
        else:
            r1=r1+text1
        tcopy4=text2
        
        
        if(1==1):
            if(tcopy1=='' and tcopy2=='' and tcopy3=='' and tcopy4==''):
                r1='Oops, I found 0 results for your search'
            
        r1=r1+"\n\nReply *4* for more News\nReply *0* for Main Menu"
        return r1
    
    
    
    
    

def bored():
    arr=["recreational", "social", "diy", "charity", "cooking", "relaxation", "music"]
    act=random.choice(arr)
    url = "http://www.boredapi.com/api/activity?type="+act
    respo = requests.request("GET", url)
    respo=respo.json()
    activity=respo.get("activity")
    
    headers={'User-Agent':'My Library (https://github.com/Dev-solutions100/google-search-webhook)'}
    url = "https://icanhazdadjoke.com/slack"
    respo = requests.request("GET", url, headers=headers)
    respo=respo.json()
    joke=respo.get("attachments")[0].get("text")
    
#     test_list = [1, 2]
#     ran=random.choice(test_list)
#     if(ran==1):
    fact=random.choice(facts.useless_facts)
#     else:
#         url = "numbersapi.com/random/trivia"
#         respo = requests.request("GET", url)
#         respo=respo.json()
#         act=respo.get("activity")
      
    f = open('quotes.json',) 
    datas = json.load(f)
    n=random.randint(0, 498)
    quote=datas[n].get("content")
    author=datas[n].get("author")
    
    print("JOKE")
    print(joke)
    print(activity)
    print(fact)
    print(quote)
    print(author)
        
    


def maps_search():
    global r2
    url = "https://api.covid19api.com/summary"
    respo = requests.request("GET", url)
    print("FREEEEEEEEEEEEEE")
    respo=respo.json()
    print(respo.get("Global").get("TotalConfirmed"))
    print("FREEEEEEEEEEEEEE")
    g1=respo.get("Global").get("TotalConfirmed")
    g2=respo.get("Global").get("TotalRecovered")
    g3=respo.get("Global").get("TotalDeaths")
    url = "https://api.covid19api.com/live/country/india/status/confirmed"
    respo = requests.request("GET", url)
    #print("FREEEEEEEEEEEEEE")
    respo=respo.json()
    #print("FREEEEEEEEEEEEEE")
    l=len(respo)
    i1=respo[l-1].get("Confirmed")
    i2=respo[l-1].get("Recovered")
    i3=respo[l-1].get("Deaths")
    r1=" *India (Real Time)*\n\n Total cases: "+str(i1)+"\n Total recovery: "+str(i2)+"\n Total deaths: "+str(i3)+"\n\n"+" *Globally (Updated Daily)*\n\n Total cases: "+str(g1)+"\n Total recovery: "+str(g2)+"\n Total deaths: "+str(g3)
    r2="Reply with any country's name to see its cases (Example: *'Italy'*)\n\nReply with *0* for Main Menu"
    return r1

def maps_search1(data):
    global r2
#     url = "https://api.covid19api.com/summary"
#     respo = requests.request("GET", url)
#     print("FREEEEEEEEEEEEEE")
#     respo=respo.json()
#     print(respo.get("Global").get("TotalConfirmed"))
#     print("FREEEEEEEEEEEEEE")
#     g1=respo.get("Global").get("TotalConfirmed")
#     g2=respo.get("Global").get("TotalRecovered")
#     g3=respo.get("Global").get("TotalDeaths")
    text1=''
    for ele in data:
        if(ele!=' '):
            text1=text1+ele.lower()
        else:
            text1=text1+'-'
    data1=''
    a=0
    b=0
    for ele in data:
        if(a==0):
            data1=data1+ele.upper()
            a=1
        else:
            if(ele==' '):
                b=1
                data1=data1+ele
            else:
                if(b==0):
                    data1=data1+ele
                else:
                    data1=data1+ele.upper()
                    b=0
    url = "https://api.covid19api.com/live/country/"+text1+"/status/confirmed"
    respo = requests.request("GET", url)
    #print("FREEEEEEEEEEEEEE")
    respo=respo.json()
    #print("FREEEEEEEEEEEEEE")
    l=len(respo)
    i1=respo[l-1].get("Confirmed")
    i2=respo[l-1].get("Recovered")
    i3=respo[l-1].get("Deaths")
    r1=" *"+data1+" (Real Time)*\n\n Total cases: "+str(i1)+"\n Total recovery: "+str(i2)+"\n Total deaths: "+str(i3)
    r2="Reply with any country's name to see its cases (Example: *'Italy'*)\n\nReply with *0* for Main Menu"
    return r1

def google_search(search_term, api_key, cse_id, **kwargs):
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
#     print("FREEEEEEEEEEEEEE")
#     print(response.text)
#     print("FREEEEEEEEEEEEEE")
    
#     url="https://api.duckduckgo.com/"
#     querystring = {"no_redirect":"1","no_html":"1","skip_disambig":"1","q":search_term,"format":"json"}
#     headers={}
#     response = requests.request("GET", url, headers=headers, params=querystring)

    #r1 = duckduckgo.get_zci(search_term)
#     r = duckduckgo.query(search_term)
#    print("FREEEEEEEEEEEEEE1")
#     print(r.results)
#     print(r.related)
#     print(r.answer)

#     print(r1)
#     print("FREEEEEEEEEEEEEE1")
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
#         print("OK")
#         #print(plain_text)
#         soup = BeautifulSoup(plain_text, "html.parser")
        
        
        
        sitesearch='https://www.bing.com/search?q='+search_term
        #headers={'User-Agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        source_code = requests.get(sitesearch,headers=headers)
        plain_text = source_code.text
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKK")
        #print(plain_text)
        soup1 = BeautifulSoup(plain_text, "html.parser")
        [s.extract() for s in soup1('span')]
        unwantedTags = ['strong', 'cite']
        for tag in unwantedTags:
            for match in soup1.findAll(tag):
                match.replaceWithChildren()
            
        results = soup1.findAll('li', { "class" : "b_algo" })
#         for result in results:
#             ch=(result.find('h2')).find('a')
#             print("LINK: "+ch['href']+"\n#")
#             print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
#             print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
#             print("# ___________________________________________________________\n#")
        
        
#     topics = parsed.findAll('div', {'id': 'zero_click_topics'})[0]
#     results = topics.findAll('div', {'class': re.compile('results_*')})
        print("FREEEEEEEEEEEEEE2")
    #print(parsed)
        a=1
        b=1
        c=1
        test_list = [1, 2, 3]
        text1=''
        text2=''
        text3=''
        ran=random.choice(test_list)
        
#         for desc in soup.find_all("span",{"class":"st"}):
#             if(a==ran):
#                 text1=desc.text
#                 break
#             a=a+1
#         print(text1)
        
        for result in results:
            if(a==ran):
                ch=(result.find('h2')).find('a')
                text2=ch['href']
                print("LINK: "+ch['href']+"\n#")
                print("# TITLE: " + str(result.find('h2')).replace(" ", " ") + "\n#")
                txts=result.find('p')
                text1=txts.text
                print("# DESCRIPTION: " + str(result.find('p')).replace(" ", " "))
                print("# ___________________________________________________________\n#")
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
    
#         for descc in soup.find_all("div",{"class":"r"}):
#             if(b==ran):
#                 children = descc.findChildren("a" , recursive=False)
#                 for child in children:
#                     text2= child['href']
#                     break
#             if(b==ran):
#                 break
#             b=b+1
            
        print(text1)    
        print(text2)
        if(text2!=''):
            r1=r1+text1+" ("
            r1=r1+text2+")"
        else:
            r1=r1+text1
        tcopy2=text2
    
#     for desccc in soup.find_all("h3",{"class":"r"}):
#         if(c==ran):
#             text3=desccc.text
#             break
#         c=c+1
#     print(text3)
#     a=soup.find_all("span", class_="f")[0]
#     b=soup.find_all("span", class_="st")[0]
#     c=soup.find_all("div", class_="r")[0]
#     print(a)
#     print(b)
#     print(c)
    print("FREEEEEEEEEEEEEE2")
    #if(rcopy=='' or rcopy[:4]=='http'):
    if(1==1):
        if(tcopy1=='' and tcopy2==''):
            r1='Oops, I found 0 results for your search'
    return r1


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
    # print(json.dumps(item, indent=4))

   # speech = "*Please view these articles for latest information on " + searchstring + ":* " + "\n\n" + "1) "+ articleSnippet1+ "\n"+articleUrl1+ "\n\n" + "2) "+ articleSnippet2+ "\n"+articleUrl2
    speech=data
    print("Response:")
    print(speech)
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

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
