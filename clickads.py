import csv
import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException,UnexpectedAlertPresentException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import random
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from clearunwantedtabs import clearunwantedtabs
from randomsleeptime import RandomSleepTime

class clickads:
    def __init__(self,url,basepath,bot_port,startnum,endnum):
        super(clickads, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.random_sleeptime = random.randint(5, 8)
        self.webdriver_obj = botwebdriver(bot_port, basepath)
        self.obj_randomsleeptime=RandomSleepTime(startnum,endnum)
        self.sleeptime=self.obj_randomsleeptime.getsleeptime()
        print("sleep time>>>:"+str(self.sleeptime))
        logging.basicConfig(filename=self.basefilepath+"//bot"+str(datetime.datetime.now().date())+".log", level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        #obj_clearunwantedtabs.close()
    def startAdclickbot(self):
        self.bot_driver = self.webdriver_obj.startwebdriver()
        obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.bot_driver.get(self.url)

    def check_presenceofAds(self):
        time.sleep(self.sleeptime)
        try:
            numberofclicksavailable = self.bot_driver.find_element(By.XPATH,'/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div[1]/span/span').text

            print("No of Ads available:{adsavailable}".format(adsavailable=numberofclicksavailable))
            return int(numberofclicksavailable)
            self.logger.info("Successfully Checked presence of Ads")
        except:
            self.logger.error("Unable to get presence of Ads Information")
            return 0

    def startAdclicking(self,noofads):
        for ads in range(noofads):
            try:
                try:
                    advmsg = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                         (By.XPATH, '//*[@id="viewAdsTOffers1"]/tbody/tr/td[2]/p[1]'))).text
                    print(advmsg)
                    self.logger.info("Ad Message:{advmsg}".format(advmsg=advmsg))
                except:
                     print("Ad Message not found.")
                clickprice = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                             (By.XPATH, '//*[@id="viewAdsTOffers1"]/tbody/tr/td[3]'))).text

                print("click price:" + clickprice)
                self.logger.info("Ad Click Price:{clickprice}".format(clickprice=clickprice))
                self.logger.info("Successfully Checked presence of Ads")
                clickwait_msg = WebDriverWait(self.bot_driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="viewAdsTOffers1"]/tbody/tr/td[2]/span/span')))
                clickwaittime_msg_splits = clickwait_msg.text.split()
                viewclick = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="viewAdsTOffers1"]/tbody/tr/td[4]/div/a[1]/span/input')))
                viewclick.click()
                try:
                    WebDriverWait(self.bot_driver, 5).until(
                        EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                    alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                    alert.accept()
                except:
                    adactivetime = 0
                    for items in clickwaittime_msg_splits:
                        if (items.isnumeric()):
                            adactivetime = items

                    print("Bot will sleep for:{sleeptime} secs".format(sleeptime=adactivetime))
                    self.logger.info("Bot will sleep for:{sleeptime} secs".format(sleeptime=adactivetime))
                    time.sleep(self.sleeptime)
                    print(self.bot_driver.window_handles)
                    try:
                        parent = self.bot_driver.window_handles[0]
                        child = self.bot_driver.window_handles[1]
                        self.bot_driver.switch_to.window(child)
                        time.sleep(int(adactivetime)+10)
                    except:
                        print("Issue while switching to child window")
                    timernotend=True
                    self.bot_driver.switch_to.window(parent)
                    while timernotend:
                        try:
                            timerleft = self.bot_driver.find_element(By.XPATH,
                                                    '//*[@id="viewAdsTOffers1"]/tbody/tr/td[4]/div/h2').text
                            print("Amount of time still left:{time} sec(s)".format(time=timerleft))
                            self.logger.error("Amount of time still left:{time} sec(s)".format(time=timerleft))
                            time.sleep(self.sleeptime)
                            self.bot_driver.switch_to.window(child)
                            time.sleep(int(timerleft)+5)
                            self.bot_driver.switch_to.window(parent)
                        except (ValueError,NoSuchElementException,UnexpectedAlertPresentException):
                            print(self.bot_driver.window_handles)
                            self.bot_driver.switch_to.window(child)
                            try:
                                WebDriverWait(self.bot_driver, 5).until(
                                    EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                                alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                                alert.accept()
                            except:
                                print("No Alert Found")
                            self.bot_driver.close()
                            self.bot_driver.switch_to.window(parent)
                            break
                    try:
                        WebDriverWait(self.bot_driver, 5).until(
                            EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                        alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                        alert.accept()
                        print("Ad Expired.")
                    except (TimeoutException,NoSuchWindowException):
                        print("Ad clicked successfully")
                        with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([datetime.datetime.now().date(), '0', 'ClickAds', 'Success', '0.001'])
            except TimeoutException:
                print("Unable to fetch click price or ad message")
                self.logger.error("Unable to fetch click price or ad message")










