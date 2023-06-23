import datetime
import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from clearunwantedtabs import clearunwantedtabs


class defaultsurvey:
    def __init__(self, url, basepath, bot_port):
        super(defaultsurvey, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_port=bot_port
        self.random_sleeptime = random.randint(5, 8)
        self.webdriver_obj = botwebdriver(bot_port, basepath)
        logging.basicConfig(filename=self.basefilepath + "//bot" + str(datetime.datetime.now().date()) + ".log",
                            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)


    def startdefaultsurveytaskbot(self):
        self.bot_driver = self.webdriver_obj.startwebdriver()
        obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.bot_driver.get(self.url)

        self.logger.info("Successfully started default task")

    def check_presenceofdefaultsurvey(self):
        time.sleep(10)
        content = WebDriverWait(self.bot_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="top_main_menu_57"]')))
        content.click()
        time.sleep(5)
        surveytableparent = WebDriverWait(self.bot_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "offers-table")))
        surveytableprow = surveytableparent.find_element(By.ID, "allSurveysTable")
        surveyrows = surveytableprow.find_elements(By.TAG_NAME, "tr")
        randomsurveyrouter = random.randint(1, 1)
        print("random Survwey router {routernum}".format(routernum=randomsurveyrouter))
        issurveyavailable=False
        for rows1 in surveyrows:
            innerrows = rows1.find_elements(By.TAG_NAME, "td")
            for rows2 in innerrows:
                # print(rows2.text)
                if (randomsurveyrouter == 1 and rows2.text == "Daily Poll"):
                    issurveyavailable= True
                    self.logger.info("Default Survey found")
                    break
        return issurveyavailable
    def startdefaultsurveytask(self):
        content = WebDriverWait(self.bot_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="top_main_menu_57"]')))
        content.click()
        time.sleep(5)
        surveytableparent = WebDriverWait(self.bot_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "offers-table")))
        surveytableprow = surveytableparent.find_element(By.ID, "allSurveysTable")
        surveyrows = surveytableprow.find_elements(By.TAG_NAME, "tr")
        randomsurveyrouter = random.randint(1, 1)
        print("random Survwey router {routernum}".format(routernum=randomsurveyrouter))
        for rows1 in surveyrows:
            innerrows = rows1.find_elements(By.TAG_NAME, "td")
            for rows2 in innerrows:
                # print(rows2.text)
                if (randomsurveyrouter == 1 and rows2.text == "Daily Poll"):
                    print("##########################")
                    print(rows2.text)
                    print("##########################")
                    rows1.find_element(By.TAG_NAME, "a").click()
                    time.sleep(10)
                    self.bot_driver.find_element(By.XPATH, '//*[@id="daily_poll_alls_available"]/p[2]/a').click()
                    time.sleep(15)
                    optionlist = self.bot_driver.find_elements(By.CLASS_NAME, "compare-col")
                    randomchoiceselect = random.randint(0, len(optionlist) - 1)
                    optionlist[randomchoiceselect].find_element(By.TAG_NAME, 'a').click()
                    break



