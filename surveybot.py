import csv
import datetime
import logging
import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from AutomatedXpathGenerator import Xpath_Util
from QuestionIdentifier import SurveyquestionIdentifier
from answeroptionsIdentifier import AnswerIdentifier
from AutomatedXpathGenerator import Xpath_Util
class SurveyBot:
    def __init__(self, url, basepath, bot_driver):
        super(SurveyBot, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_driver=bot_driver
        self.bodycontent = self.bot_driver.find_element(by=By.TAG_NAME, value='body')
        logging.basicConfig(filename=self.basefilepath + "//bot" + str(datetime.datetime.now().date()) + ".log",
                            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)


    def startappearingsurvey(self,surveyroute):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(self.bodycontent.text)
        obj_questionidentifier = SurveyquestionIdentifier(self.bot_driver,self.bodycontent)
        obj_answeridentifier=AnswerIdentifier(self.bot_driver,self.bodycontent)
        while surveyroute=="cpx" or surveyroute=="sampli":
            if surveyroute=="cpx":
                questions = obj_questionidentifier.IdentifyCPXquestion()
                answer=obj_answeridentifier.IdentifyCPXanswers()
                print(questions[0])
                print(answer)
                obj_xpathparserobject = Xpath_Util(self.bot_driver)
                result_flag, webpagedictlist, submitbuttonxpath = obj_xpathparserobject.parseUrl(self.url)
                print(result_flag)
                print(webpagedictlist)
                print(submitbuttonxpath)
                choosen_answer = " "
                isquestionRegistered = False
                df_profilequestionlist = pd.read_csv(self.basefilepath + "\\surveyprofilequestion.csv")
                for index, row in df_profilequestionlist.iterrows():
                    if str(row['profile_question']).strip() == questions[0].strip():
                        print("Choosen answer is:"+str(row['Answer']).strip())
                        choosen_answer = str(row['Answer']).strip()
                        isquestionRegistered = True
                        break
                if choosen_answer != "" and isquestionRegistered:
                    for element in webpagedictlist:
                        if element['attr_type'] == 'text' and len(webpagedictlist)==1:
                            self.bot_driver.find_element(By.XPATH,element['elementxpath']).send_keys(choosen_answer)
                            break
                        elif not element['attr_type'] == 'text' and len(webpagedictlist)>1:
                            for element in webpagedictlist:
                                if element['siblingofelementvalue'].strip() == choosen_answer:
                                    print (">>>>>>>>>>>>answer found<<<<<<<<<<<<")
                                    print(element['siblingofelementvalue'])
                                    answeroption=self.bot_driver.find_element(By.XPATH, element['elementxpath'])
                                    self.bot_driver.execute_script("arguments[0].scrollIntoView();", answeroption)
                                    time.sleep(5)
                                    self.bot_driver.find_element(By.XPATH, element['elementxpath'] + "/..").click()
                                    time.sleep(5)
                                    break

                elif choosen_answer == "" and isquestionRegistered:
                    if  webpagedictlist[0]['attr_type'] == 'text':
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[0]['elementxpath']).send_keys("I cant / dont want to answer this question.")
                    elif not webpagedictlist[0]['attr_type'] == 'text':
                        randomanswer = random.randint(0, len(webpagedictlist) - 1)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                elif choosen_answer.strip() == "" and not isquestionRegistered:
                    with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a',encoding='utf-8',newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([questions[0], answer, "NA"])
                    if webpagedictlist[0]['attr_type'] == 'text':
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[0]['elementxpath']).send_keys("NA")
                    elif not webpagedictlist[0]['attr_type'] == 'text':
                        randomanswer = random.randint(0, len(webpagedictlist) - 1)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()





                elif choosen_answer == "" and isquestionRegistered:
                    randomanswer = random.randint(0, len(webpagedictlist) - 1)
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                elif choosen_answer.strip() == "" and not isquestionRegistered:
                    with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a',encoding='utf-8',newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([questions[0], answer, "NA"])
                        randomanswer = random.randint(0, len(webpagedictlist) - 1)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                self.bot_driver.find_element(By.XPATH, '//*[@id="submitquestion1"]').click()
                time.sleep(10)
                if self.bot_driver.current_url.startswith("https://offers.cpx-research.com/"):
                    surveyroute='cpx'
                else:
                    surveyroute="NA"
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            elif surveyroute=="sampli":
                questions = obj_questionidentifier.Identifysampliciuosquestion()
                answer = obj_answeridentifier.Identifysampliciuosanswers()
                obj_xpathparserobject=Xpath_Util(self.bot_driver)
                result_flag, webpagedictlist, submitbuttonxpath = obj_xpathparserobject.parseUrl(self.url)
                print(result_flag)
                print(webpagedictlist)
                print(submitbuttonxpath)
                choosen_answer=" "
                submitbuttonindex = 0
                for element in reversed(webpagedictlist):
                    if element['elementtype'] == 'input' and element['attr_type'] == 'submit':
                        submitbuttonindex = webpagedictlist.indexof(element)
                        break
                print("submitbuttonindex:"+submitbuttonindex)
                isquestionRegistered=False
                df_profilequestionlist = pd.read_csv(self.basefilepath + "\\surveyprofilequestion.csv")
                for index, row in df_profilequestionlist.iterrows():
                    if str(row['profile_question']).strip()==questions[0].strip():
                        choosen_answer=str(row['Answer']).strip()
                        isquestionRegistered=True
                        print("Answer in register:"+choosen_answer)
                        break
                if  choosen_answer!=" " and isquestionRegistered:
                    for element in webpagedictlist:
                        if element['siblingofelementvalue'].strip()==choosen_answer:
                            print("Answer found")
                            self.bot_driver.find_element(By.XPATH,element['elementxpath']).click()
                            time.sleep(5)
                            self.bot_driver.find_element(By.XPATH,webpagedictlist[submitbuttonindex]['elementxpath']).click()
                            break
                elif choosen_answer=="" and isquestionRegistered:
                    randomanswer=random.randint(0,len(webpagedictlist)-1)
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                    time.sleep(5)
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[submitbuttonindex]['elementxpath']).click()
                elif choosen_answer.strip()=="" and not isquestionRegistered:
                    with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a', encoding='utf-8',
                              newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([questions[0], answer, "NA"])
                    randomanswer = random.randint(0, len(webpagedictlist) - 1)
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                    time.sleep(5)
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[submitbuttonindex]['elementxpath']).click()
                time.sleep(10)
                if self.bot_driver.current_url.startswith("https://www.samplicio.us/"):
                    surveyroute = 'sampli'
                else:
                    surveyroute = "NA"






            time.sleep(50)


