import nltk
from selenium.webdriver.common.by import By

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
class AnswerIdentifier:
    def __init__(self, bot_driver, bodycontent):
        self.bodycontent = bodycontent
        self.answer_register = []
        self.bot_driver = bot_driver
    def IdentifyCPXanswers(self):
        answertag=self.bot_driver.find_elements(By.CLASS_NAME,"custom-checkbox")
        for answer in answertag:
            value=answer.find_element(By.TAG_NAME,'label').text
            self.answer_register.append(value)
        return self.answer_register
    def Identifysampliciuosanswers(self):
        answer=self.bodycontent.find_element(By.CLASS_NAME,"answer").text
        #print(answer)
        self.answer_register.append(answer)


        return self.answer_register
