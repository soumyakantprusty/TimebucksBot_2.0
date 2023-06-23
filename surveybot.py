import csv
import datetime
import logging
import random
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from AutomatedXpathGenerator import Xpath_Util
from QuestionIdentifier import SurveyquestionIdentifier
from answeroptionsIdentifier import AnswerIdentifier
from AutomatedXpathGenerator import Xpath_Util
from WebpagestructureIdentifier import webpagestructureidentifier
class SurveyBot:
    def __init__(self, url, basepath, bot_driver):
        super(SurveyBot, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_driver=bot_driver
        #self.bodycontent = self.bot_driver.find_element(by=By.TAG_NAME, value='body')
        logging.basicConfig(filename=self.basefilepath + "//bot" + str(datetime.datetime.now().date()) + ".log",
                            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    def __cpxsurvey(self,obj_questionidentifier,obj_answeridentifier,surveyroute_in):
        breaktheloop=False
        surveyroute_out=surveyroute_in
        try:
            msg = self.bot_driver.find_element(By.XPATH, '/html/body/div[2]/div/div/p[1]').text
            if msg == 'Unfortunately we couldnt find a survey for your profile.':
                print("Survey is Ended")
                breaktheloop=True
        except:
            print("Survey is Active")
        questions = obj_questionidentifier.IdentifyCPXquestion()
        answer = obj_answeridentifier.IdentifyCPXanswers()
        if len(questions)==0:
            try:
                self.bot_driver.find_element(By.XPATH,'//*[@id="go_to_survey"]').click()
            except:
                breaktheloop = True

            '''obj_xpathparserobject = Xpath_Util(self.bot_driver)
            result_flag, webpagedictlist, submitbuttonxpath = obj_xpathparserobject.parseUrl(self.url)
            print(webpagedictlist)
            print(submitbuttonxpath)'''
        else:
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
                    print("Choosen answer is:" + str(row['Answer']).strip())
                    choosen_answer = str(row['Answer']).strip()
                    isquestionRegistered = True
                    break
            if (choosen_answer != "" and choosen_answer != 'nan') and isquestionRegistered and len(webpagedictlist) > 0:
                print("Cat 1")
                for element in webpagedictlist:
                    if element['attr_type'] == 'text' and len(webpagedictlist) == 1:
                        self.bot_driver.find_element(By.XPATH, element['elementxpath']).send_keys(choosen_answer)
                        break
                    elif not element['attr_type'] == 'text' and len(webpagedictlist) > 1:
                        for element in webpagedictlist:
                            if element['siblingofelementvalue'].strip() == choosen_answer:
                                print(">>>>>>>>>>>>answer found<<<<<<<<<<<<")
                                print(element['siblingofelementvalue'])
                                answeroption = self.bot_driver.find_element(By.XPATH, element['elementxpath'])
                                self.bot_driver.execute_script("arguments[0].scrollIntoView();", answeroption)
                                time.sleep(5)
                                self.bot_driver.find_element(By.XPATH, element['elementxpath'] + "/..").click()
                                time.sleep(5)
                                self.bot_driver.find_element(By.XPATH, '//*[@id="submitquestion1"]').click()
                                break

            elif (choosen_answer == "" or choosen_answer == 'nan') and isquestionRegistered and len(
                    webpagedictlist) > 0:
                print("Cat 2")
                if webpagedictlist[0]['attr_type'] == 'text' and len(webpagedictlist) == 1:
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[0]['elementxpath']).send_keys(
                        "I cant / dont want to answer this question.")
                elif not webpagedictlist[0]['attr_type'] == 'text' and len(webpagedictlist) > 1:
                    randomanswer = random.randint(0, len(webpagedictlist) - 1)
                    print(webpagedictlist[randomanswer]['elementxpath'])
                    self.bot_driver.find_element(By.XPATH,
                                                 webpagedictlist[randomanswer]['elementxpath'] + "/..").click()
                    time.sleep(10)
                    with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a', encoding='utf-8',
                              newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(
                            [questions[0], answer, webpagedictlist[randomanswer]['siblingofelementvalue']])
                    time.sleep(5)
                    self.bot_driver.find_element(By.XPATH, '//*[@id="submitquestion1"]').click()
            elif (choosen_answer.strip() == "" or choosen_answer == 'nan') and not isquestionRegistered and len(
                    webpagedictlist) > 0:
                print("Cat 3")
                if webpagedictlist[0]['attr_type'] == 'text' and len(webpagedictlist) == 1:
                    self.bot_driver.find_element(By.XPATH, webpagedictlist[0]['elementxpath']).send_keys("NA")
                elif not webpagedictlist[0]['attr_type'] == 'text' and len(webpagedictlist) > 1:
                    randomanswer = random.randint(0, len(webpagedictlist) - 1)

                    # self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                    self.bot_driver.find_element(By.XPATH,
                                                 webpagedictlist[randomanswer]['elementxpath'] + "/..").click()
                    time.sleep(10)
                    with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a', encoding='utf-8',
                              newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([questions[0], answer, webpagedictlist[randomanswer]['siblingofelementvalue']])
                    self.bot_driver.find_element(By.XPATH, '//*[@id="submitquestion1"]').click()
            elif len(webpagedictlist) == 0:
                self.bot_driver.find_element(by=By.XPATH, value=submitbuttonxpath['submitbtnxpath']).click()
            time.sleep(15)
            if self.bot_driver.current_url.startswith("https://offers.cpx-research.com/"):
                surveyroute_out = 'cpx'
            elif self.bot_driver.current_url.startswith("https://timebucks.com/"):
                surveyroute_out = "NA"
            else:
                print("Passed Prescreening.Actual Survey started.")
                self.actualsurveybot()

        return breaktheloop,surveyroute_out


    def startappearingsurvey(self,surveyroute):

        while surveyroute=="cpx" or surveyroute=="sampli":
            self.bodycontent = self.bot_driver.find_element(by=By.TAG_NAME, value='body')
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(self.bodycontent.text)
            obj_questionidentifier = SurveyquestionIdentifier(self.bot_driver, self.bodycontent)
            obj_answeridentifier = AnswerIdentifier(self.bot_driver, self.bodycontent)
            if surveyroute=="cpx":
                breakout,surveyroute=self.__cpxsurvey(obj_questionidentifier,obj_answeridentifier,surveyroute)
                if breakout:
                    break
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            elif surveyroute=="sampli":
                questions = obj_questionidentifier.Identifysampliciuosquestion()
                if len(questions)!=0:
                    answer = obj_answeridentifier.Identifysampliciuosanswers()
                    obj_xpathparserobject=Xpath_Util(self.bot_driver)
                    result_flag, webpagedictlist, submitbuttonxpath,multiplebtn = obj_xpathparserobject.parseUrl(self.url)
                    print(result_flag)
                    print(webpagedictlist)
                    print(submitbuttonxpath)
                    print(multiplebtn)
                    choosen_answer=" "
                    submitbuttonindex = 0
                    for element in reversed(webpagedictlist):
                        if element['elementtype'] == 'input' and element['attr_type'] == 'submit':
                            submitbuttonindex = webpagedictlist.index(element)
                            break
                    print("submitbuttonindex:"+str(submitbuttonindex))
                    isquestionRegistered=False
                    df_profilequestionlist = pd.read_csv(self.basefilepath + "\\surveyprofilequestion.csv",encoding="cp1252")
                    for index, row in df_profilequestionlist.iterrows():
                        if str(row['profile_question']).strip()==questions[0].strip():
                            choosen_answer=str(row['Answer']).strip()
                            isquestionRegistered=True
                            print("Answer in register:"+choosen_answer)
                            break
                    if  (choosen_answer != "" and choosen_answer !='nan') and isquestionRegistered:
                        for element in webpagedictlist:
                            if element['siblingofelementvalue'].strip()==choosen_answer:
                                print("Answer found")
                                self.bot_driver.find_element(By.XPATH,element['elementxpath']).click()
                                time.sleep(5)
                                self.bot_driver.find_element(By.XPATH,webpagedictlist[submitbuttonindex]['elementxpath']).click()
                                break
                    elif (choosen_answer == "" or choosen_answer =='nan') and isquestionRegistered:
                        randomanswer=random.randint(0,len(webpagedictlist)-2)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                        time.sleep(5)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[submitbuttonindex]['elementxpath']).click()
                    elif (choosen_answer.strip() == "" or choosen_answer =='nan') and not isquestionRegistered:
                        with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a', encoding='utf-8',
                                newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([questions[0], answer, ""])
                        randomanswer = random.randint(0, len(webpagedictlist) - 2)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[randomanswer]['elementxpath']).click()
                        time.sleep(5)
                        self.bot_driver.find_element(By.XPATH, webpagedictlist[submitbuttonindex]['elementxpath']).click()
                    time.sleep(10)
                    if self.bot_driver.current_url.startswith("https://www.samplicio.us/"):
                        surveyroute = 'sampli'
                    elif  self.bot_driver.current_url.startswith("https://timebucks.com/"):
                        surveyroute = "NA"
                    else:
                        print("Passed Prescreening.Actual Survey started.")
                        self.actualsurveybot()

                else:
                    print("Disqaulified from Survey.")
            time.sleep(25)
    def __checkifquestionisnew(self,questiontext):
        isquestionRegistered=False
        choosen_answer=""
        df_profilequestionlist = pd.read_csv(self.basefilepath + "\\surveyprofilequestion.csv",encoding="cp1252")
        for index, row in df_profilequestionlist.iterrows():
            if str(row['profile_question']).strip() == questiontext.strip():
                choosen_answer = str(row['Answer']).strip()
                isquestionRegistered = True
                print("Answer in register:" + choosen_answer)
                break
        return isquestionRegistered,choosen_answer
    def __addnewquestion(self,question,options):
        with open(self.basefilepath + "\\surveyprofilequestion.csv", 'a', encoding='utf-8',
                  newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([question, options," "])
    def actualsurveybot(self):
        obj_xpathparserobject = Xpath_Util(self.bot_driver)
        self.bodycontent=" "
        questionslist = []
        tableelementrelationlist = []
        counter=1
        while True:
            print("####PAGE No:############## {counter}".format(counter=counter))
            url = self.bot_driver.current_url
            bodycontent = self.bot_driver.find_element(by=By.TAG_NAME, value='body')
            obj_questionidentifier = SurveyquestionIdentifier(self.bot_driver, bodycontent)
            sentenceregister = obj_questionidentifier.identifyquestion(bodycontent)
            if 1==0:
                print("Not a valid survey")
                parent = self.bot_driver.window_handles[0]
                child = self.bot_driver.window_handles[1]
                self.bot_driver.close()
                self.bot_driver.switch_to.window(parent)

                break
            else:

                result_flag, webpagedictlist, submitbuttonxpath,multiplebtn = obj_xpathparserobject.parseUrl(url)
                print("###Webpage dictionary#########")
                print(webpagedictlist)
                print("###Submit button List#########")
                print(submitbuttonxpath)
                print("###Button List#########")
                print(multiplebtn)
                for question in sentenceregister:
                    questionslist.append(question)
                print("########### List of Questions in page ###########")
                print(questionslist)
                time.sleep(20)
                obj_webpagestructureidentifier=webpagestructureidentifier(self.bot_driver,questionslist,webpagedictlist,submitbuttonxpath)
                webpagestructuredefiner = obj_webpagestructureidentifier.getwebpageinfo()
                print("########### Webpage structure definer ###########")
                print(webpagestructuredefiner)
                try:
                    filtered_webpagestructuredefiner = [structure for structure in webpagestructuredefiner if
                                                    len(structure['optiongrp']) > 0]
                except:
                    print("No MCQ strucuture found")

                time.sleep(20)
                if len(webpagedictlist)>0:
                    for question in filtered_webpagestructuredefiner:
                        questiontext = question['question']['question']
                        print("#########The Question##############")
                        print(questiontext)
                        isquestionregistered,answer = self.__checkifquestionisnew(questiontext)
                        textfield_list = [option for option in question['optiongrp'] if
                                          option['elementtype'] == 'input' and (
                                                      option['attr_type'] == 'text' or option['attr_type'] == 'number' or option['attr']=='placeholder')]
                        optionfield_list = [option for option in question['optiongrp'] if
                                            option['elementtype'] == 'input' and option['attr_type'] != 'submit' and
                                            option['attr_type'] != 'text' and option['attr_type'] != 'number']
                        buttonfield_list = [option for option in question['optiongrp'] if
                                            (option['elementtype'] == 'input' and option['attr_type'] == 'submit') or (
                                                        option['elementtype'] == 'button')]
                        selectfield_list = [option for option in question['optiongrp'] if
                                            option['elementtype'] == 'select']
                        print("######## TEXTFIELD LIST ##############")
                        print(len(textfield_list))
                        print("######## OPTIONFIELD LIST ##############")
                        print(len(optionfield_list))
                        print("######## SELECT FIELD LIST ##############")
                        print(len(selectfield_list))
                        print("######## BUTTON FIELD LIST ##############")
                        print(len(buttonfield_list))
                        if not isquestionregistered:
                            self.__addnewquestion(questiontext,optionfield_list)
                        if len(textfield_list) > 0 and len(optionfield_list) == 0:
                            textfield = self.bot_driver.find_element(by=By.XPATH,
                                                                value=textfield_list[0]['elementxpath'])
                            textfield.click()
                            if isquestionregistered:
                                textfield.send_keys(answer)
                            else:
                                textfield.send_keys("NA")
                        elif len(textfield_list)== 0 and len(optionfield_list) == 0 and len(selectfield_list) >0:
                            for select in selectfield_list:
                                optionvalue=[]
                                for childelement in select['childelements']:
                                    print("######################Checking values of option#####################")
                                    optionvalue.append(childelement.text.strip().lower())
                                if  answer.strip().lower() in optionvalue and isquestionregistered:
                                    try:
                                        select['childelements'][optionvalue.index(answer.strip().lower())].click()
                                    except:
                                        print("Unable to select the drop downvalue")
                                else:
                                    randomvalue=random.randint(0,len(select['childelements'])-1)
                                    select['childelements'][randomvalue].click()

                        elif len(textfield_list)== 0 and len(optionfield_list) > 0 and len(selectfield_list)==0:
                            for option in optionfield_list:
                                print("###########Checking Value of Each option##################")
                                print(option["siblingofelementvalue"].lower(), answer.lower())
                                if option["siblingofelementvalue"].lower() == answer.lower() and isquestionregistered:
                                    try:
                                        self.bot_driver.find_element(by=By.XPATH,
                                                                value=option['elementxpath']).click()
                                    except:
                                        print('Element not interactable.Trying to check Clickablity of element')
                                        try:
                                            WebDriverWait(self.bot_driver, 20).until(
                                                EC.element_to_be_clickable(
                                                    (By.XPATH,
                                                     option['elementxpath']))).click()
                                        except:
                                            print('Element still not interactable.Tyring to interact with its parent.')
                                            try:
                                                option['parentelementinfo'].click()
                                            except Exception as e:
                                                print("Trying to interact with sibling")
                                                try:
                                                    option['siblingofelement'].click()
                                                except:
                                                    print(
                                                        "unable to interact with options.I will wait for  your input for 45 sec.")
                                                time.sleep(45)
                                    time.sleep(5)
                                else:
                                    randomclicknumber = random.randint(0, len(optionfield_list) - 1)
                                    optionfield_list[randomclicknumber]
                                    try:
                                        self.bot_driver.find_element(by=By.XPATH, value=optionfield_list[randomclicknumber][
                                            'elementxpath']).click()
                                    except:
                                        try:
                                            optionfield_list[randomclicknumber]['siblingofelement'].click()
                                        except:
                                            print("Unable to click on the option")
                                            break
                                    time.sleep(5)
                        try:
                            self.bot_driver.find_element(by=By.XPATH, value=submitbuttonxpath['submitbtnxpath']).click()
                        except:
                            print(
                                "Either Button is not available or not able to click.Checking in webelementdict for submit button")
                            try:
                                self.bot_driver.find_element(by=By.XPATH, value=buttonfield_list[0]['elementxpath']).click()
                            except:
                                print("unable to find a button to continue.I will wait for  your input for 1 min.")
                                time.sleep(60)


                elif len(webpagedictlist) == 0:
                    try:
                        if webpagedictlist[0]['elementtype']=='textarea':
                            self.bot_driver.find_element(by=By.XPATH, value=webpagedictlist[0]['elementxpath']).send_keys("None")
                            time.sleep(10)
                            self.bot_driver.find_element(by=By.XPATH, value=submitbuttonxpath['submitbtnxpath']).click()
                        time.sleep(15)
                    except:
                        print("Unable to participate in the Survey")
                    try:
                        self.bot_driver.find_element(by=By.XPATH,value='//*[@id="btn"]/a').click()
                    except:
                        print("Unable to participate in the Survey")
                        break


            time.sleep(15)








