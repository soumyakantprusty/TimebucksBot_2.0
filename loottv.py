import logging
import time
import random
import concurrent.futures
import datetime
import traceback

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from randomsleeptime import RandomSleepTime
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from statusfileupdater import statusfileupdater
from clearunwantedtabs import clearunwantedtabs

class LootTv:
    def __init__(self,url,basepath,bot_port,credentials,watchtime,startnum,endnum):
        super(LootTv, self).__init__()
        self.bot_port=bot_port
        print(url)
        self.credentials=credentials
        self.parenthandle = ""
        self.url = url
        self.obj_randomsleeptime = RandomSleepTime(startnum, endnum)
        self.sleeptime = self.obj_randomsleeptime.getsleeptime()
        self.basefilepath = basepath
        self.watchtime=watchtime
        self.statusfileupdater=statusfileupdater("Watch Video-LOOTTV",self.basefilepath)
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.credentials_df = pd.read_csv(self.credentials)
        #executor = concurrent.futures.ThreadPoolExecutor()
        #self.file_update_future = executor.submit(self.statusfileupdater.run)
    def checkLoottv(self):
        self.logger.info("Checking LooTV Availability")
        isLootTVavailable=False
        try:
            print("Checking LooTV Availability")
            self.bot_driver = self.webdriver_obj.startwebdriver()
            clearunwantedtabs(self.bot_driver, self.basefilepath)
            time.sleep(self.sleeptime)
            self.parent_handle = self.bot_driver.window_handles[0]
            print("Parent webdriver handle is:{handle}".format(handle=self.parenthandle))
            self.bot_driver = self.webdriver_obj.startwebdriver()
            self.bot_driver.get(self.url)
            time.sleep(self.sleeptime)
            isLootTVavailable = True
        except Exception as e:
            print(traceback.print_exc())
        return isLootTVavailable
    def switchLoottvOn(self):
        self.statusfileupdater = statusfileupdater("Watch Video-LOOTTV", self.basefilepath)
        WebDriverWait(self.bot_driver, 8).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='iframeInstallApp401']")))
        time.sleep(self.sleeptime)
        self.bot_driver.find_element(By.XPATH,'//*[@id="root"]/div/div[1]/div[2]/a[6]/button').click()
        time.sleep(self.sleeptime)
        self.bot_driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div[1]/a').click()
        time.sleep(self.sleeptime)
        parent = self.bot_driver.window_handles[0]
        child = self.bot_driver.window_handles[1]
        self.bot_driver.switch_to.window(child)
        current_datetime = datetime.datetime.now()
        print("Activity Start time:")
        print(current_datetime)
        executor = concurrent.futures.ThreadPoolExecutor()
        file_update_future = executor.submit(self.statusfileupdater.run)
        time.sleep(int(self.watchtime))
        self.statusfileupdater.stop()
        file_update_future.result()
        current_datetime = datetime.datetime.now()
        print("Activity End time:")
        print(current_datetime)
        self.bot_driver.close()
        time.sleep(5)
        self.bot_driver.switch_to.window(parent)






