import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from crontabs import Cron, Tab
import time
import github
import re
import datetime

def my_job():
#     file1 = open("test.txt", "a")  # append mode 
#     file1.write("Today \n") 
#     file1.close()

#     with open("./test.txt", "w") as file1:  # append mode 
#         file1.write("Today") 
#     file1.close()
    
    g=github.Github(base_url="https://api.github.com/user",login_or_token="1c770ce741ada6a0852eca85b4ff59bae83c67e9")
    repo=g.get_user().get_repo("google-search-webhook")
    contents=repo.get_contents("test.txt")
    contents1=repo.get_contents("zone.txt")
    contents2=repo.get_contents("state.txt")
    contents3=repo.get_contents("country.txt")
    #contents4=repo.get_contents("dailydistrict.txt")
    contents5=repo.get_contents("dailystate.txt")
    contents6=repo.get_contents("continent.txt")
    contents7=repo.get_contents("countryyesterday.txt")
    contents8=repo.get_contents("dailyalldata.txt")
    contents9=repo.get_contents("dailyalldatayesterday.txt")
    contents10=repo.get_contents("countryyesterday2.txt")
#     str=str+" test"
    now1=datetime.datetime.now()
 
    dcnt2=2
    dcnt1=1
#     if(now1.hour<=6):
#         dcnt2=dcnt2+1
#         dcnt1=dcnt1+1
    yestdt2=datetime.date.today()-datetime.timedelta(days=dcnt2)
    yestdt=datetime.date.today()-datetime.timedelta(days=dcnt1)
    #print("DATE")
    #print(datetime.datetime.now())
    url = "https://api.covid19india.org/v2/state_district_wise.json"
    url1= "https://api.covid19india.org/zones.json"
    url2= "https://api.covid19india.org/data.json"
    url3= "https://corona.lmao.ninja/v2/countries"
    #url4= "https://api.covid19india.org/districts_daily.json"
    url5= "https://api.covid19india.org/states_daily.json"
    url6= "https://corona.lmao.ninja/v2/continents"
    url7= "https://disease.sh/v2/countries?yesterday=true"
    url8= "https://api.covid19india.org/v4/data-"+str(yestdt)+".json"
    url9= "https://api.covid19india.org/v4/data-"+str(yestdt2)+".json"
    url10= "https://disease.sh/v2/countries?twoDaysAgo=true"
    ck=0
    err=0
    try:
        respo = requests.request("GET", url, timeout=5)
        respo1 = requests.request("GET", url1, timeout=5)
        respo2 = requests.request("GET", url2, timeout=5)
        respo3 = requests.request("GET", url3, timeout=5)
        #respo4 = requests.request("GET", url4, timeout=5)
        respo5 = requests.request("GET", url5, timeout=5)
        respo6 = requests.request("GET", url6, timeout=5)
        respo7 = requests.request("GET", url7, timeout=5)
        respo8 = requests.request("GET", url8, timeout=5)
        if(respo8==''):
            #print('INCORRECT')
            respo8 = requests.request("GET", 'https://api.covid19india.org/v4/data.json', timeout=5)
        respo9 = requests.request("GET", url9, timeout=5)
        respo10 = requests.request("GET", url10, timeout=5)
#         print("FREEEEEEEEEEEEEE")
#         print(respo.status_code)
    except:
        err=1
    finally:
        if(err==0):
            respo=respo.json()
            respo1=respo1.json()
            respo2=respo2.json()
            respo3=respo3.json()
            #respo4=respo4.json()
            respo5=respo5.json()
            respo6=respo6.json()
            respo7=respo7.json()
            respo8=respo8.json()
            respo9=respo9.json()
            respo10=respo10.json()
            respo2=str(respo2)
            respo=str(respo)
            respo3=str(respo3)
            respo1=str(respo1)
            #respo4=str(respo4)
            respo5=str(respo5)
            respo6=str(respo6)
            respo7=str(respo7)
            respo8=str(respo8)
            respo9=str(respo9)
            respo10=str(respo10)
            
            respo2=respo2.replace('\"','\'')
            respo2=respo2.replace('{\'','{\"')
            respo2=respo2.replace('\'}','\"}')
            respo2=respo2.replace('\':','\":')
            respo2=respo2.replace(': \'',': \"')
            respo2=respo2.replace(', \'',', \"')
            respo2=respo2.replace('\',','\",')
            respo2=respo2.replace('Reason given : \"','Reason given : \'')
            respo2=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo2)
            
            respo1=respo1.replace('\"','\'')
            respo1=respo1.replace('{\'','{\"')
            respo1=respo1.replace('\'}','\"}')
            respo1=respo1.replace('\':','\":')
            respo1=respo1.replace(': \'',': \"')
            respo1=respo1.replace(', \'',', \"')
            respo1=respo1.replace('\',','\",')
            respo1=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo1)
            
            respo3=respo3.replace('\"','\'')
            respo3=respo3.replace('{\'','{\"')
            respo3=respo3.replace('\'}','\"}')
            respo3=respo3.replace('\':','\":')
            respo3=respo3.replace(': \'',': \"')
            respo3=respo3.replace(', \'',', \"')
            respo3=respo3.replace('\',','\",')
            #respo3=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo3)
            respo3=respo3.replace('None','\"0\"')
            
            respo=respo.replace('\"','\'')
            respo=respo.replace('{\'','{\"')
            respo=respo.replace('\'}','\"}')
            respo=respo.replace('\':','\":')
            respo=respo.replace(': \'',': \"')
            respo=respo.replace(', \'',', \"')
            respo=respo.replace('\',','\",')
            #respo=respo.replace('None','\"0\"')
            respo=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo)
            
#             respo4=respo4.replace('\"','\'')
#             respo4=respo4.replace('{\'','{\"')
#             respo4=respo4.replace('\'}','\"}')
#             respo4=respo4.replace('\':','\":')
#             respo4=respo4.replace(': \'',': \"')
#             respo4=respo4.replace(', \'',', \"')
#             respo4=respo4.replace('\',','\",')
#             respo4=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo4)
            
            respo5=respo5.replace('\"','\'')
            respo5=respo5.replace('{\'','{\"')
            respo5=respo5.replace('\'}','\"}')
            respo5=respo5.replace('\':','\":')
            respo5=respo5.replace(': \'',': \"')
            respo5=respo5.replace(', \'',', \"')
            respo5=respo5.replace('\',','\",')
            respo5=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo5)
            
            respo6=respo6.replace('\"','\'')
            respo6=respo6.replace('{\'','{\"')
            respo6=respo6.replace('\'}','\"}')
            respo6=respo6.replace('\':','\":')
            respo6=respo6.replace(': \'',': \"')
            respo6=respo6.replace(', \'',', \"')
            respo6=respo6.replace('\',','\",')
            respo6=respo6.replace('\']','\"]')
            respo6=respo6.replace('[\'','[\"')
            #respo6=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo6)
            respo6=respo6.replace('None','\"0\"')
            
            respo7=respo7.replace('\"','\'')
            respo7=respo7.replace('{\'','{\"')
            respo7=respo7.replace('\'}','\"}')
            respo7=respo7.replace('\':','\":')
            respo7=respo7.replace(': \'',': \"')
            respo7=respo7.replace(', \'',', \"')
            respo7=respo7.replace('\',','\",')
            #respo7=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo7)
            respo7=respo7.replace('None','\"0\"')
            
            respo8=respo8.replace('\"','\'')
            respo8=respo8.replace('{\'','{\"')
            respo8=respo8.replace('\'}','\"}')
            respo8=respo8.replace('\':','\":')
            respo8=respo8.replace(': \'',': \"')
            respo8=respo8.replace(', \'',', \"')
            respo8=respo8.replace('\',','\",')
            respo8=respo8.replace('\']','\"]')
            respo8=respo8.replace('[\'','[\"')
            respo8=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo8)
            respo8=respo8.replace('Reason given : \"','Reason given : \'')
            
            respo9=respo9.replace('\"','\'')
            respo9=respo9.replace('{\'','{\"')
            respo9=respo9.replace('\'}','\"}')
            respo9=respo9.replace('\':','\":')
            respo9=respo9.replace(': \'',': \"')
            respo9=respo9.replace(', \'',', \"')
            respo9=respo9.replace('\',','\",')
            respo9=respo9.replace('\']','\"]')
            respo9=respo9.replace('[\'','[\"')
            respo9=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo9)
            respo9=respo9.replace('Reason given : \"','Reason given : \'')
            
            respo10=respo10.replace('\"','\'')
            respo10=respo10.replace('{\'','{\"')
            respo10=respo10.replace('\'}','\"}')
            respo10=respo10.replace('\':','\":')
            respo10=respo10.replace(': \'',': \"')
            respo10=respo10.replace(', \'',', \"')
            respo10=respo10.replace('\',','\",')
            #respo10=re.sub(r'^\s*(N|n)\s*(O|o)\s*(N|n)\s*(E|e)\s*$','\"0\"',respo10)
            respo10=respo10.replace('None','\"0\"')
            
            try:
                repo.update_file(contents.path,"Updated",respo,contents.sha)
                repo.update_file(contents1.path,"Updated",respo1,contents1.sha)
                repo.update_file(contents2.path,"Updated",respo2,contents2.sha)
                repo.update_file(contents3.path,"Updated",respo3,contents3.sha)
                #repo.update_file(contents4.path,"Updated",respo4,contents4.sha)
                repo.update_file(contents5.path,"Updated",respo5,contents5.sha)
                repo.update_file(contents6.path,"Updated",respo6,contents6.sha)
                repo.update_file(contents7.path,"Updated",respo7,contents7.sha)
                repo.update_file(contents8.path,"Updated",respo8,contents8.sha)
                repo.update_file(contents9.path,"Updated",respo9,contents9.sha)
                repo.update_file(contents10.path,"Updated",respo10,contents10.sha)
            except:
                ck=1
#     file1 = open("test.txt", "w")  # append mode 
#     file1.write("Today") 
#     file1.close()
            finally:
                print('abcd1234')


# Will run with a 10 second interval synced to the top of the minute
#Cron().schedule(Tab(name='run_my_job').every(seconds=10).run(my_job)).go()

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    #app.run(debug=False, port=port, host='0.0.0.0')
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', seconds=3600)
    scheduler.start()

    while True:
        time.sleep(5)
