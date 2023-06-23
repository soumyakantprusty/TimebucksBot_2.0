import nltk
from selenium.webdriver.common.by import By

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

class SurveyquestionIdentifier:
    def __init__(self,bot_driver, bodycontent):
        self.question_words = ["what", "why", "when", "where",
             "name", "is", "how", "do", "does",
             "which", "are", "could", "would",
             "should", "has", "have", "whom", "whose", "don't", "provide","state","country/language","district","select","PIN"]
        self.bodycontent=bodycontent
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<")
        print(self.bodycontent)
        self.sentenceregister=[]
        self.questionidentifier_register=[]
        self.bot_driver=bot_driver

    def identifyquestion(self):
        #newbodycontent = self.bodycontent.text.split("\n")
        newbodycontent = self.bodycontent.text
        print(newbodycontent)

        for sentence in newbodycontent:
            question = sentence.lower()
            question = word_tokenize(question)

            if any(x in question for x in self.question_words):

                print(sentence.lower())
                self.sentenceregister.append(sentence)
                self.questionidentifier_register.append('y')
        print(self.sentenceregister)
        return self.sentenceregister
    def IdentifyCPXquestion(self):
        question=self.bodycontent.find_element(By.ID,"question_title").text
        print(question)
        self.sentenceregister.append(question)
        return self.sentenceregister
    def Identifysampliciuosquestion(self):
        question=self.bodycontent.find_element(By.CLASS_NAME,"question").text
        print(question)
        self.sentenceregister.append(question)
        return self.sentenceregister

