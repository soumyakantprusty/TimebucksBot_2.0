import time

import nltk
from selenium.webdriver.common.by import By
import spacy
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

class SurveyquestionIdentifier:
    def __init__(self,bot_driver, bodycontent):
        self.question_words = ["Who","What","When","Where","Why","How","Which","Whose","Whom",
                               "Is", "Are", "Am", "Was", "Were", "Do", "Does", "Did", "Can"
            , "Could", "Should", "Would", "Will", "Shall", "May", "Might"
            , "Must", "Can", "Could", "Should", "Would", "Will", "Shall", "May"
            , "Might", "Must","state","country/language","district","select","PIN","I'm a"]
        # Load the pre-trained BERT model and tokenizer

        self.bodycontent=bodycontent
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<")
        print(self.bodycontent)
        self.questionregister=[]
        self.questionidentifier_register=[]
        self.bot_driver=bot_driver




    def identifyquestion(self,bodycontent):
        #print(bodycontent.text)
        print("###############Body Content#######################")
        newbodycontent = bodycontent.text.split("\n")
        print(newbodycontent)

        for sentence in newbodycontent:
            question = sentence.lower()
            question = word_tokenize(question)
            if any(x.lower() in question for x in self.question_words):
                #print(sentence.lower())
                self.questionregister.append(sentence)
                self.questionidentifier_register.append('y')
        print(self.questionregister)
        return self.questionregister



    def IdentifyCPXquestion(self):
        try:
            question=self.bodycontent.find_element(By.ID,"question_title").text
            print(question)
            self.questionregister.append(question)
        except:
            print("No question in page")
        return self.questionregister
    def Identifysampliciuosquestion(self):
        try:
            question=self.bodycontent.find_element(By.CLASS_NAME,"question").text
            print(question)
            self.questionregister.append(question)
        except:
            print("You are disqualified from survey.")
            try:
                self.bodycontent.find_element(By.XPATH,'//*[@id="ctl00_Content_btnReturnToSupplier"]').click()
            except:
                pass
        return self.questionregister

