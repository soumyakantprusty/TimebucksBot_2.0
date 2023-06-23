
import csv
import datetime
import logging
import re
import time

import pandas as pd
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from clearunwantedtabs import clearunwantedtabs
from bs4 import BeautifulSoup

from botwebdriver import botwebdriver
from bottaskdetails import BotTaskDetails
from randomsleeptime import RandomSleepTime
class dailyyoutubetask:
    def __init__(self, url, basepath, bot_port,curentuser):
        super(dailyyoutubetask, self).__init__()
        self.url = url
        self.basefilepath = basepath
        self.bot_port = bot_port
        self.bot_driver=""
        self.curentuser=curentuser
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        self.taskregistry_obj = BotTaskDetails(basepath, curentuser)
        self.obj_randomsleeptime = RandomSleepTime(startnum, endnum)
        self.sleeptime = self.obj_randomsleeptime.getsleeptime()
        try:
            logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        except Exception as e:
            print(repr(e))
        self.logger = logging.getLogger(__name__)
    def startdailytaskbot(self):
        issuccessful=True
        self.bot_driver = self.webdriver_obj.startwebdriver()
        obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.bot_driver.get(self.url)
        self.logger.info("Successfully started daily Youtube task")
        return True
    def check_presenceoftask(self):
        time.sleep(self.sleeptime)
        taskclosed=True
        print("Checking if any unfinish task is present")
        self.logger.info("Checking if any unfinish task is present")
        try:
            self.bot_driver.find_element(By.XPATH, '//input[@class="btnCancelBuyTasksCampaign"]').click()
            WebDriverWait(self.bot_driver, 20).until(EC.alert_is_present())
            alert = self.bot_driver.switch_to.alert
            alert.accept()
            self.logger.info("Unfinished Task is closed successfully")
        except Exception as e:
            print(str(e))
            print("No Unfinished Task found")
            self.logger.info("No Unfinished Task found")
            taskclosed=True
        return taskclosed
    def setfilterforbtnclicktask(self):
        retry_count=0
        isjobdone = True
        time.sleep(self.sleeptime)
        print("starting of setting filters")
        self.logger.info("starting of setting filters")
        time.sleep(self.sleeptime)
        try:
            actionlist = (WebDriverWait(self.bot_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/button'))))

            actionlist.click()
            select_allbtn = (WebDriverWait(self.bot_driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/div/button[1]'))))
            select_allbtn.click()
            time.sleep(self.sleeptime)
            selectbuttonclicktaskbtn = (WebDriverWait(self.bot_driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/div/button[13]'))))
            selectbuttonclicktaskbtn.click()
            time.sleep(self.sleeptime)
            submitbtn = (WebDriverWait(self.bot_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[4]/div[2]/div/div/div[7]/span/span'))))
            submitbtn.click()
            time.sleep(self.sleeptime)

        except Exception as e:
            isjobdone=False
            print(repr(e))
        return isjobdone
