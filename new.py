import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from crontabs import Cron, Tab
import time
import github


def my_job():
#     file1 = open("test.txt", "a")  # append mode 
#     file1.write("Today \n") 
#     file1.close()

#     with open("./test.txt", "w") as file1:  # append mode 
#         file1.write("Today") 
#     file1.close()
    
    g=github.Github("Dev-solutions100","kk202050")
    repo=g.get_user().get_repo("google-search-webhook")
    contents=repo.get_contents("test.txt")
    contents1=repo.get_contents("zone.txt")
    contents2=repo.get_contents("state.txt")
    contents3=repo.get_contents("country.txt")
#     str=str+" test"
    url = "https://api.covid19india.org/v2/state_district_wise.json"
    url1= "https://api.covid19india.org/zones.json"
    url2= "https://api.covid19india.org/data.json"
    url3= "https://corona.lmao.ninja/v2/countries"
    ck=0
    err=0
    try:
        respo = requests.request("GET", url, timeout=5)
        respo1 = requests.request("GET", url1, timeout=5)
        respo2 = requests.request("GET", url2, timeout=5)
        respo3 = requests.request("GET", url3, timeout=5)
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
            respo2=str(respo2)
            respo=str(respo)
            respo3=str(respo3)
            respo1=str(respo1)
            
            respo2=respo2.replace('\"','\'')
            respo2=respo2.replace('{\'','{\"')
            respo2=respo2.replace('\'}','\"}')
            respo2=respo2.replace('\':','\":')
            respo2=respo2.replace(': \'',': \"')
            respo2=respo2.replace(', \'',', \"')
            respo2=respo2.replace('\',','\",')
            
            respo1=respo1.replace('\"','\'')
            respo1=respo1.replace('{\'','{\"')
            respo1=respo1.replace('\'}','\"}')
            respo1=respo1.replace('\':','\":')
            respo1=respo1.replace(': \'',': \"')
            respo1=respo1.replace(', \'',', \"')
            respo1=respo1.replace('\',','\",')
            
            respo3=respo3.replace('\"','\'')
            respo3=respo3.replace('{\'','{\"')
            respo3=respo3.replace('\'}','\"}')
            respo3=respo3.replace('\':','\":')
            respo3=respo3.replace(': \'',': \"')
            respo3=respo3.replace(', \'',', \"')
            respo3=respo3.replace('\',','\",')
            
            respo=respo.replace('\"','\'')
            respo=respo.replace('{\'','{\"')
            respo=respo.replace('\'}','\"}')
            respo=respo.replace('\':','\":')
            respo=respo.replace(': \'',': \"')
            respo=respo.replace(', \'',', \"')
            respo=respo.replace('\',','\",')
            
            try:
                repo.update_file(contents.path,"Updated",respo,contents.sha)
                repo.update_file(contents1.path,"Updated",respo1,contents1.sha)
                repo.update_file(contents2.path,"Updated",respo2,contents2.sha)
                repo.update_file(contents3.path,"Updated",respo3,contents3.sha)
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
    scheduler.add_job(my_job, 'interval', seconds=60)
    scheduler.start()

    while True:
        time.sleep(5)
