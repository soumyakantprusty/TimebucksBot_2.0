import csv
import datetime
import random

from selenium.webdriver.common.by import By
import logging
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from clearunwantedtabs import clearunwantedtabs
from randomsleeptime import RandomSleepTime
from anticaptcha import AntiCaptcha
from humansim import HumanActionSimulator
class pushclick:
    def __init__(self, url, basepath,bot_port,startnum, endnum,pushclicklimit):
        super(pushclick, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_port=bot_port
        self.pushclicklimit=pushclicklimit
        self.webdriver_obj=botwebdriver(bot_port,basepath)
        self.random_sleeptime = random.randint(int(startnum), int(endnum))
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.obj_HumanActionSimulator = HumanActionSimulator()

    def startpushclickbot(self):
        self.bot_driver=self.webdriver_obj.startwebdriver()
        obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.bot_driver.get(self.url)
    def __dashboardcheck(self):
        dailyquotacomplete=False
        if self.pushclicklimit=="yes":
            self.bot_driver.get("https://timebucks.com/publishers/index.php?pg=dashboard")
            time.sleep(self.random_sleeptime)
            pushclickquota_1=self.bot_driver.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/p[2]/span/img').get_attribute("src")
            pushclickquota_2 = self.bot_driver.find_element(By.XPATH,
                                                       '//*[@id="main"]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/p[2]/span/img').get_attribute(
                "src")
            print(pushclickquota_1)
            print(pushclickquota_2)
            if pushclickquota_1=="https://timebucks.com/publishers/images/tick-green.png" and pushclickquota_2=="https://timebucks.com/publishers/images/tick-green.png":
                dailyquotacomplete=True
            self.bot_driver.get(self.url)
        else:
            dailyquotacomplete = False
        return dailyquotacomplete



    def check_presenceofpushclick(self):
        time.sleep(self.random_sleeptime)
        self.logger.info("Checking if pushclick availble or not.")
        isnewpushclickavailable=True
        if not self.__dashboardcheck():
            try:
                bodymsg = self.bot_driver.find_element(By.TAG_NAME, value="body")
                sleeptime = int(bodymsg.text.split(" ")[10])
                print("The next push to click will come at {sleeptime}".format(sleeptime=sleeptime, ))
                self.logger.info("The next push to click will come at {sleeptime} mins".format(sleeptime=sleeptime, ))
                self.webdriver_obj.quitwebdriver()
                isnewpushclickavailable = False
            except:
                print("New Pushclick Job is available")
                self.logger.info("New Pushclick Job is available")
                isnewpushclickavailable=True
                time.sleep(self.random_sleeptime)
        else:
            print("Pushclick Job daily quota fullfilled.")
            self.logger.info(" Pushclick Job daily quota fullfilled.")
            isnewpushclickavailable=False
        return isnewpushclickavailable
    def executepushclickbot(self):

        try:
            WebDriverWait(self.bot_driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))

            WebDriverWait(self.bot_driver, 8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
            print("Captcha Code found")
            self.logger.info("Captcha Code found")
            self.bot_driver.switch_to.parent_frame()
            obj_anticaptcha = AntiCaptcha(self.bot_driver, 2, self.basefilepath)
            obj_anticaptcha.callanticaptcha()
        except:
            print("Successfully clicked")
            self.logger.info("Successfully clicked")
            self.bot_driver.quit()
            self.webdriver_obj.quitwebdriver()
            with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.datetime.now(), '2', 'pushclick', 'Success', '0.001'])

        return datetime.datetime.now()

