import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from crontabs import Cron, Tab
import time

def my_job():
    file1 = open("test.txt", "a")  # append mode 
    file1.write("Today \n") 
    file1.close()


# Will run with a 10 second interval synced to the top of the minute
#Cron().schedule(Tab(name='run_my_job').every(seconds=10).run(my_job)).go()

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    #app.run(debug=False, port=port, host='0.0.0.0')
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', seconds=10)
    scheduler.start()
    
    while True:
            time.sleep(5)
