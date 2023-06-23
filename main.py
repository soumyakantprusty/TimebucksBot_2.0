import csv
import json
import logging
from datetime import datetime, timedelta
import os
import random
import traceback
import pandas as pd
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, \
    StaleElementReferenceException, WebDriverException
#from msedge.selenium_tools import Edge, EdgeOptions
import time
import sys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from clickads import clickads
from dailytask import dailymandatorytask
from pushclick import pushclick
from slideshow import slideshow

from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from defaultsurvey import defaultsurvey
from hydeouttv import hydeouttv
from tasktimers import tasktimers
from botincomedetails import botincomedetails
from dailyyoutubetask import dailyyoutubetask
from survey import Surveys
from sampliciousprofiler import SampliciousProfiler
from surveybot import SurveyBot
from loottv import LootTv
from randomsleeptime import RandomSleepTime

class TimeBucksBots:
    def __init__(self,bot_port):
        super(TimeBucksBots, self).__init__()
        self.username = "soumyakantprusty@gmail.com "
        self.password = "@Ork5612skp"
        self.bot_port=bot_port
        self.starttaskid=starttaskid
        self.endtaskid=endtaskid
        self.curentuser= os.getlogin()
        self.profilearguments="user-data-dir=C:\\Users\\"+self.curentuser+"\\AppData\Local\\Microsoft\\Edge\\User Data\\Default\\"
        self.webdriverpath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\edgedriver_win32\\msedgedriver.exe"
        self.basefilepath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots"
        self.credentialfilepath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\timebuckscredentials.csv"
        self.tasklistfilepath = "C:\\Users\\" + self.curentuser + "\\Documents\\TimeBucksBots\\tasklist.csv"
        self.dailyclickpngpath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\Dailyclick.png"
        self.dailyupvotepngpath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\Dailyupvote.png"
        self.dailyquizpngpath="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\Dailyquiz.png"
        self.dailytasktitle = ['WEBSITE ENGAGE AND AD 1-CLICK NEW', 'Daily Click', "Upvote this comment Daily ",
                               "Receive Email and Open Link - Daily  ", "Complete a Quiz - DAILY"]

        self.taskurls=[
            "https://timebucks.com/publishers/index.php?pg=earn&tab=view_content_ads",
            "https://timebucks.com//publishers/index.php?pg=earn&tab=tasks_tasks",
            "https://timebucks.com/redirects/PushClicks.php",
            "https://timebucks.com/publishers/index.php?pg=earn&tab=view_content_timecave_slideshows",
            "https://timebucks.com/publishers/index.php?pg=earn&tab=all_surveys",
            "https://timebucks.com//publishers/index.php?pg=earn&tab=offerwall_hideout",
            "https://timebucks.com/publishers/index.php?pg=earning",
            "https://timebucks.com//publishers/index.php?pg=earn&tab=offerwall_lootably"

        ]
        self.current_time=datetime.now()
        self.webdriver_obj=botwebdriver(self.bot_port,self.basefilepath)
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        print(self.profilearguments)
        print(self.webdriverpath)
        print(self.credentialfilepath)
        print(self.dailyclickpngpath)
        print(self.dailyupvotepngpath)
        print(self.dailyquizpngpath)
        isworkregsiterexist = os.path.isfile(self.basefilepath+"\\botregister.csv")

        # If the file doesn't exist, create a new one and write the header row
        if not isworkregsiterexist:
            with open(self.basefilepath+"\\botregister.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['datetime', 'taskid', 'taskname','status','price'])
        print("Initiating selenenium webdriver Options")
        #self.options = EdgeOptions()
        #self.prefs = {"credentials_enable_service": False,
                      #"profile.password_manager_enabled": False}
        # subprocess.call([r'C:\Users\sam\Documents\TimeBucksBots\chromestartup.bat'])
    def __loginpage(self,bot_driver):

               try:
                   username = WebDriverWait(bot_driver, 10).until(
                             EC.visibility_of_element_located((By.XPATH, '//*[@id="username_box"]')))
                   time.sleep(5)
                   #username.send_keys(self.username)
                   #time.sleep(5)
                   password = WebDriverWait(bot_driver, 10).until(
                           EC.visibility_of_element_located((By.XPATH, '//*[@id="password_box"]')))
                   #password.send_keys(self.password)
                   time.sleep(10)
                   WebDriverWait(bot_driver, 20).until(
                           EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                   WebDriverWait(bot_driver, 20).until(
                           EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                   time.sleep(60)
                   bot_driver.switch_to.parent_frame()
                   WebDriverWait(bot_driver, 10).until(
                           EC.element_to_be_clickable(
                               (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[1]/form/input[5]'))).click()
               except TimeoutException:
                   try:
                       WebDriverWait(bot_driver, 20).until(
                               EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrmCookieBanner")))
                       time.sleep(8)
                       WebDriverWait(bot_driver, 20).until(EC.element_to_be_clickable(
                               (By.XPATH, '//*[@id="grouped-pageload-Banner"]/div/div/div/div[3]/button[2]'))).click()
                       time.sleep(5)
                       bot_driver.switch_to.parent_frame()
                   except TimeoutException:
                       print("ClickToPay Bot:No Cookie Banner")


    def startwebdriver(self):
        bot_driver=self.webdriver_obj.startwebdriver()
        bot_driver.get("https://timebucks.com/publishers/index.php?pg=dashboard")
        bot_driver.maximize_window()
        self.__loginpage(bot_driver)
        time.sleep(5)
        bot_driver.quit()
        self.webdriver_obj.quitwebdriver()
        return self.credentialfilepath,self.curentuser,self.username,self.password,self.taskurls,self.logger,self.current_time,self.dailytasktitle,self.basefilepath,self.tasklistfilepath,self.dailyquizpngpath,self.dailyupvotepngpath,self.dailyclickpngpath
if __name__ == '__main__':
    print("Bot program started")
    print("Reading excepted inputs for the Bot parameters")
    noofparameters = len(sys.argv)
    if noofparameters<10:
        print("Required parameters not found.Check and relaunch the program")
    else:
        bot_port=sys.argv[1]
        starttaskid=sys.argv[2]
        endtaskid = sys.argv[3]
        startnum = sys.argv[4]
        endnum = sys.argv[5]
        pushclicklimit=sys.argv[6]
        slideshowlimit=sys.argv[7]
        hideoutdefaultacct=sys.argv[8]
        hideouttvwatchtime= sys.argv[9]
        loottvwatchtime = sys.argv[10]
        #webdriverswitch=sys.argv[5]
        #bot_profile=sys.argv[1]
        webdriverclass = TimeBucksBots(bot_port)
        credentials,curentuser,username,password,taskurlslist,logger,current_time,dailytasktitle,basefilepath,tasklistfilepath,dailyquizpngpath,dailyupvotepngpath,\
            dailyclickpngpath = webdriverclass.startwebdriver()
        obj_clickads=clickads(taskurlslist[0],basefilepath,bot_port,startnum,endnum)
        obj_dailytask=dailymandatorytask(taskurlslist[1],basefilepath,dailytasktitle,dailyquizpngpath,dailyupvotepngpath,dailyclickpngpath,bot_port,startnum,endnum)
        obj_pushclick=pushclick(taskurlslist[2],basefilepath,bot_port,startnum,endnum,pushclicklimit)
        obj_slideshow=slideshow(taskurlslist[3],basefilepath,bot_port,startnum,endnum,slideshowlimit)
        obj_defaultsurvey=defaultsurvey(taskurlslist[4],basefilepath,bot_port)
        obj_hydeouttv=hydeouttv(taskurlslist[5],basefilepath,bot_port,credentials,hideoutdefaultacct,hideouttvwatchtime)
        obj_loottv=LootTv(taskurlslist[7],basefilepath,bot_port,credentials,loottvwatchtime,startnum,endnum)
        obj_tasktimers=tasktimers(basefilepath)
        obj_botincomedetails=botincomedetails(taskurlslist[6],basefilepath,bot_port,curentuser)
        obj_dailyyoutubetask=dailyyoutubetask(taskurlslist[1],basefilepath,bot_port,curentuser,startnum,endnum)

        while True:
            cntr=1
            start_range = int(starttaskid)  # Specify the start of the range
            end_range = int(endtaskid) # Specify the end of the range
            # Create a randomly organized list of numbers within the range
            random_list = random.sample(range(start_range, end_range + 1), end_range - start_range + 1)
            print("################")
            print(random_list)
            print("################")
            for random_int in random_list:
                #random_int=6
                instantdatetime=datetime.now()
                pushclicktime=datetime.now() - timedelta(hours=2)
                if random_int==0 and obj_tasktimers.settimers(0):
                    print("Ad Clicks-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Ad Clicks-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_clickads.startAdclickbot()
                    noofclicks=obj_clickads.check_presenceofAds()
                    if noofclicks>0:
                        obj_clickads.startAdclicking(noofclicks)
                    incomedetails=obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath+"\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)
                elif random_int==1 and obj_tasktimers.settimers(1):
                    print("Daily24hrtask-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Daily24hrtask-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_dailytask.startdailytaskbot()
                    availabletask=obj_dailytask.check_presenceoftask()
                    print(availabletask)
                    if len(availabletask)>0:
                        obj_dailytask.executedailytask(availabletask)
                    else:
                        print("No Task Available")
                        logger.info("No Task Available")
                    incomedetails = obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)
                elif random_int==2 and obj_tasktimers.settimers(2):
                    print("PushClick-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("PushClick-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_pushclick.startpushclickbot()
                    availablepushclick=obj_pushclick.check_presenceofpushclick()
                    if availablepushclick:
                        pushclicktime=obj_pushclick.executepushclickbot()
                    incomedetails = obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)
                elif random_int==3 and obj_tasktimers.settimers(3):
                    print("SlideShow Task-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("SlideShow Task-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_slideshow.startslideshowtaskbot()
                    slideavaibletowatch=obj_slideshow.check_presenceofslide()
                    print(slideavaibletowatch)
                    if slideavaibletowatch:
                        current_time=obj_slideshow.startslideshowtask()
                    incomedetails = obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)
                elif random_int == 4 and obj_tasktimers.settimers(4):
                    print("Default Survey-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Default Survey-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_defaultsurvey.startdefaultsurveytaskbot()
                    defaulttaskavailable = obj_defaultsurvey.check_presenceofdefaultsurvey()
                    if defaulttaskavailable:
                        obj_defaultsurvey.startdefaultsurveytask()
                    incomedetails = obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)

                elif random_int==5 and obj_tasktimers.settimers(1):
                    print("Hydeout TV-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Hydeout TV-Bot JobId:{jobid}".format(jobid=random_int))
                    obj_hydeouttv.starthydeouttv(username,password)
                    incomedetails = obj_botincomedetails.getbotincometaskdetails()

                    with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        json.dump(incomedetails, json_file)
                elif random_int==6:
                    print("Youtubevideo watch-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Youtubevideo watch-Bot JobId:{jobid}".format(jobid=random_int))
                    iswebdriverstarted=obj_dailyyoutubetask.startdailytaskbot()
                    if iswebdriverstarted:
                        istaskclosedproperly=obj_dailyyoutubetask.check_presenceoftask()
                        if istaskclosedproperly:
                            isfilterset=obj_dailyyoutubetask.setfilterfoytubetask()
                            if isfilterset:
                                obj_dailyyoutubetask.perfromYtubewatchtask()
                elif random_int==7:
                    obj_survey = Surveys(taskurlslist[4], basefilepath, bot_port)
                    print("############################")
                    print("Survey-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Survey--Bot JobId:{jobid}".format(jobid=random_int))
                    print('#################################')
                    isstarted=obj_survey.startsurveybot()
                    if isstarted:
                        ispresent,url,bot_driver=obj_survey.check_presenceofsurvey()
                        print(ispresent,url)
                        if ispresent and url.startswith("https://www.samplicio.us/"):
                            obj_surveybot=SurveyBot(url,basefilepath,bot_driver)
                            obj_surveybot.startappearingsurvey("sampli")
                        elif ispresent and  url.startswith("https://offers.cpx-research.com/"):
                            obj_surveybot=SurveyBot(url,basefilepath,bot_driver)
                            obj_surveybot.startappearingsurvey("cpx")
                        elif ispresent and not url.startswith("https://offers.cpx-research.com/") and not  url.startswith("https://www.samplicio.us/"):
                            obj_surveybot = SurveyBot(url, basefilepath, bot_driver)
                            obj_surveybot.actualsurveybot()
                        else:
                            print("No active survey available")
                elif random_int==8 and obj_tasktimers.settimers(1):
                    print("LOOT TV-Bot JobId:{jobid}".format(jobid=random_int))
                    logger.info("Loot TV-Bot JobId:{jobid}".format(jobid=random_int))
                    isLootTVavailable=obj_loottv.checkLoottv()
                    #time.sleep(20)
                    if isLootTVavailable:
                        print("LootTV Available Starting to switchit on")
                        logger.info("LootTV Available Starting to switchit on")
                        obj_loottv.switchLoottvOn()
                    else:
                        print("Unable to start loottv")
                    print("LootTV task completed")
                    #incomedetails = obj_botincomedetails.getbotincometaskdetails()
                   #with open(basefilepath + "\\incomedetails.json", 'w') as json_file:
                        #json.dump(incomedetails, json_file)
            print("################################")
            print("End of {batch} batch Job".format(batch=cntr))
            print("################################")
            cntr = cntr+1
