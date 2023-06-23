import csv
import datetime
import logging

import pandas as pd


class BotTaskDetails:
    def __init__(self, basepath, currentuser):
        super(BotTaskDetails, self).__init__()
        self.basefilepath=basepath
        self.currentuser=currentuser
        self.tasksummary_df=pd.read_csv(basepath+"\\tasksummary.csv")
        try:
            logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        except Exception as e:
            print(repr(e))
        self.logger = logging.getLogger(__name__)
    def addcompletedtask(self,taskid,price):
        with open(self.basefilepath+"\\tasksummary.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if taskid==0:
                writer.writerow([datetime.datetime.now().date(), 1,0,0,0,0,0,price])
            elif taskid==1:
                writer.writerow([datetime.datetime.now().date(), 0,1, 0, 0, 0,0, price])
            elif taskid == 2:
                writer.writerow([datetime.datetime.now().date(), 0, 0, 1, 0, 0,0,price])
            elif taskid==3:
                writer.writerow([datetime.datetime.now().date(), 0,0,0,1,0,0, price])
            elif taskid==4:
                writer.writerow([datetime.datetime.now().date(), 0,0, 0, 0, 1,0, price])
            elif taskid == 5:
                writer.writerow([datetime.datetime.now().date(), 0, 0, 0, 0, 0, 1, price])
            elif taskid == 6:
                writer.writerow([datetime.datetime.now().date(), 0, 1, 0, 0, 0, 0, price])


