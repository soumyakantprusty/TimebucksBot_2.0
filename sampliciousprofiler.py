import datetime
import logging
import random
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from AutomatedXpathGenerator import Xpath_Util

class SampliciousProfiler:
    def __init__(self, url, basepath, bot_driver):
        super(SampliciousProfiler, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_driver=bot_driver
        self.soup = BeautifulSoup(self.bot_driver.page_source, 'html.parser')
        logging.basicConfig(filename=self.basefilepath + "//bot" + str(datetime.datetime.now().date()) + ".log",
                            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    def appearProfileMCQ(self):
        print('Reached to the survey')
        try:
            question = self.soup.find('div', class_='question').text
            print(question.strip())
            answerset=[]
            answer_options = self.soup.find_all('label')
            for option in answer_options:
                answer_text = option.text.strip()  # Extract the answer text
                answerset.append(answer_text)
            xpathparserobject = Xpath_Util(self.bot_driver)
            while 1>0:
                result_flag, webpagedictlist, submitbuttonxpath=xpathparserobject.parseUrl(self.bot_driver.current_url)
                print(">>>>>>>>>>>>>>"+len(webpagedictlist)+"<<<<<<<<<<<<<<")
                randomanswer=random.randint(0,len(webpagedictlist))
                self.bot_driver.find_element(By.XPATH,webpagedictlist[randomanswer]['elementxpath']).click()
                time.sleep(5)
                self.bot_driver.find_element(By.XPATH,webpagedictlist[-1]['elementxpath']).click()
                time.sleep(5)
                if  not self.bot_driver.current_url.startswith("Samplicious"):
                    break
        except:
            print("Disqualified from survey.")
            print(traceback.print_stack())




