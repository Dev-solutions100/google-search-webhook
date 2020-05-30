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
#     str=str+" test"
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
            respo=respo.json()
            repo.update_file(contents.path,"Updated",respo,contents.sha)
#     file1 = open("test.txt", "w")  # append mode 
#     file1.write("Today") 
#     file1.close()

        print('abcd1234')


# Will run with a 10 second interval synced to the top of the minute
#Cron().schedule(Tab(name='run_my_job').every(seconds=10).run(my_job)).go()

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    #app.run(debug=False, port=port, host='0.0.0.0')
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', seconds=30)
    scheduler.start()

    while True:
        time.sleep(5)
