from selenium.webdriver.common.by import By
import operator
import requests
import time
from bs4 import BeautifulSoup
class webpagestructureidentifier:
    def __init__(self,bot_driver,questionlist,webpagedictlist,submitbuttonsdict):
        self.questionlist = questionlist
        self.webpagedictlist = webpagedictlist
        self.submitbuttonsdict = submitbuttonsdict
        self.bot_driver=bot_driver
        self.questionlistlocationdict=[]
        self.webpageelementlistlocationdict=[]
        self.questionlocationdict = {}


    def __webpagestructure_definer(self, questionlistlocationdict, webpageelementlistlocationdict):
        print(questionlistlocationdict)
        webpagestructuredefiner = []
        questionordering=sorted(questionlistlocationdict,key=lambda question:question['location_y'])
        print("##### Ordered List of Question ##############")
        print(questionordering)
        questionpairing = []
        for index in range(0, len(questionordering)):
            if index < len(questionordering) - 1:
                questionpairing.append((index, index + 1))
            elif index == len(questionordering) - 1:
                questionpairing.append((index, index))
        if len(questionpairing)==0:
            questionoption = {}

            questionoption["question"]={'question': 'N/A', 'location_x': -1, 'location_y': -1}
            optionsgrp = []
            for webpageelements in webpageelementlistlocationdict:
                optionsgrp.append(webpageelements)
                questionoption['optiongrp'] = optionsgrp
            webpagestructuredefiner.append(questionoption)
        else:
            for questionpair in questionpairing:
                questionoption={}
                questionoption["question"]=questionordering[questionpair[0]]
                optionsgrp = []
                for webpageelements in webpageelementlistlocationdict:

                    #print(webpageelements)
                    if((questionpair[0]<questionpair[1]) and questionordering[questionpair[0]]['location_y']<=webpageelements['location_y']<=questionordering[questionpair[1]]['location_y']):
                        optionsgrp.append(webpageelements)
                    elif ((questionpair[0]==questionpair[1]) and (questionordering[questionpair[0]]['location_y']<=webpageelements['location_y'])  ):
                        optionsgrp.append(webpageelements)

                    questionoption['optiongrp']=optionsgrp
                webpagestructuredefiner.append(questionoption)
        print(webpagestructuredefiner)
        return webpagestructuredefiner






    def getwebpageinfo(self):
        print("$$$$$$$$$$$$$$$$$$$$$$")
        content=self.bot_driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        print(self.questionlist)
        for question in self.questionlist:
            local_questionlocationdict = {}
            print("Checking presence of question in soup")
            matched_tags1 = soup.find_all(lambda tag: (len(tag.find_all())==0 and question in tag.text))
            matched_tags2 = soup.find_all(lambda tag: (len(tag.find_all())==1 and question in tag.text))
            print(len(matched_tags1),len(matched_tags2))
            matched_tags=[]
            if len(matched_tags1)==0:
                matched_tags=matched_tags2
            else:
                matched_tags=matched_tags1
            print(matched_tags)
            for tags in matched_tags:
                print(tags.name)
                questionxpath="//"+tags.name+"[contains(string(),"+'"{}"'.format(question)+")]"
                print(questionxpath)
                local_questionlocationdict["question"] = question
                local_questionlocationdict["location_x"] = self.bot_driver.find_element(by=By.XPATH,value=questionxpath).location['x']
                local_questionlocationdict["location_y"] = self.bot_driver.find_element(by=By.XPATH, value=questionxpath).location['y']
            if len(local_questionlocationdict)!=0:
                self.questionlistlocationdict.append(local_questionlocationdict)
        print(self.questionlistlocationdict)

        for element in self.webpagedictlist:
            #print('############# Element location #########################')
            #print(element)
            webpageelement=self.bot_driver.find_element(by=By.XPATH, value=element['elementxpath'])
            location=webpageelement.location
            print(location)
            element["location_x"]=location['x']
            element["location_y"] = location['y']
            self.webpageelementlistlocationdict.append(element)
        webpagestructuredefiner=self.__webpagestructure_definer(self.questionlistlocationdict, self.webpageelementlistlocationdict)
        return webpagestructuredefiner



