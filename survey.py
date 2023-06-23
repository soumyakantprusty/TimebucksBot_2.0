import concurrent.futures
import logging
import time
import random
import datetime
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from clearunwantedtabs import clearunwantedtabs
from statusfileupdater import statusfileupdater
from humansim import HumanActionSimulator
from anticaptcha import AntiCaptcha
class Surveys:
    def __init__(self,url,basepath,bot_port):
        super(Surveys, self).__init__()
        self.url=url
        self.basepath=basepath
        self.bot_port=bot_port
        self.random_sleeptime = random.randint(8, 10)

        self.webdriver_obj = botwebdriver(bot_port, basepath)
        logging.basicConfig(filename=self.basepath + "//bot" + str(datetime.datetime.now().date()) + ".log",
                            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    def startsurveybot(self):
        isstarted=True
        try:
            self.bot_driver = self.webdriver_obj.startwebdriver()
            obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basepath)
            self.bot_driver.get(self.url)
            self.logger.info("Successfully started survey Bot")
        except:
            isstarted=False
        return isstarted
    def __checkvalidcpxsurvey(self):
        issurveypresent=False
        try:
            self.bot_driver.find_element(By.ID,"closemessage")
        except:
            issurveypresent = True
        return issurveypresent


    def __check_Termination_msg(self):
        issurveyterminated=False
        try:
            msg=self.bot_driver.find_element_by_xpath('/html/body/h3').text
            print("#############")
            print(msg)
            print("#############")
            if msg in "Unfortunately you didn't quality for a survey, try one of the other routers instead." or msg in "You have reached your limit for checking Samplicious surveys for today." \
                                                                                                                       " You can try again tomorrow when the day flips over. You can try other providers in the meantime":
                issurveyterminated = True
                print("Disqualified from survey.")
                self.logger.info("Disqualified from survey.")
        except:
            try:
                msg=self.bot_driver.find_element_by_xpath('//*[@id="question-container"]').text
                if msg.strip().startswith("Unfortunately"):
                    issurveyterminated = True
                    print("Disqualified from survey.")
                    self.logger.info("Disqualified from survey.")
            except:
                print(">>>>Survey not terminated<<<")
                self.logger.info("Survey not terminated")
        return issurveyterminated
    def __BitLabsrouter(self):
       pass

    def check_presenceofsurvey(self):
        obj_HumanActionSimulator=HumanActionSimulator()
        surveyproviderlist=["Samplicious Best Converting Survey Router","Samplicious $0.70 Survey Router","Samplicious $0.35 Survey Router","CPX Research","Samplicious 5 minute Survey Router","Samplicious 15 minute Survey Router","Samplicious 30 minute Survey Router"]
        #surveyproviderlist = ["CPX Research","Dynata Survey Router"]
        time.sleep(self.random_sleeptime)
        print("Starting to check for availability for survey")
        self.logger.info("Starting to check for availability for survey")
        ispresent=False
        url=""
        try:
            content = WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="top_main_menu_57"]')))
            content.click()
            time.sleep(self.random_sleeptime)
            surveytableparent = WebDriverWait(self.bot_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "offers-table")))
            surveytableprow = surveytableparent.find_element(By.ID, "allSurveysTable")
            surveyrows = surveytableprow.find_elements(By.TAG_NAME, "tr")
            for rows1 in surveyrows:
                innerrows = rows1.find_elements(By.TAG_NAME, "td")
                for rows2 in innerrows:
                    if (rows2.text in surveyproviderlist ) and rows2.text.strip().startswith("Samplicious"):
                        print(rows2.text+":Survey found")
                        self.logger.info(rows2.text+":Survey found")
                        rows1.find_element(By.TAG_NAME, "a").click()

                        try:
                            parent = self.bot_driver.window_handles[0]
                            child = self.bot_driver.window_handles[1]
                            self.bot_driver.switch_to.window(child)
                            #obj_anticaptcha = AntiCaptcha(self.bot_driver)
                            #obj_anticaptcha.callanticaptcha()

                            WebDriverWait(self.bot_driver, 20).until(
                                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                            captchacheckbox=WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                            action = ActionChains(self.bot_driver);
                            obj_HumanActionSimulator.human_like_mouse_move(action, captchacheckbox)

                            WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                            time.sleep(60)
                            isterminated=self.__check_Termination_msg()
                            if isterminated:
                                ispresent = False
                                print("Survey Terminated")
                                self.bot_driver.close()
                                self.bot_driver.switch_to.window(parent)

                            else:
                                print("Survey not Terminated")
                                ispresent = True
                                url=self.bot_driver.current_url
                                print(url)
                                break
                        except:
                            traceback.print_exc()
                            self.bot_driver.close()
                            self.bot_driver.switch_to.window(parent)
                            print("Survey Limit reached")
                            ispresent = False
                            break


                    elif (rows2.text in surveyproviderlist ) and rows2.text.strip().startswith("CPX Research"):
                        print(rows2.text + ":Survey found")
                        self.logger.info(rows2.text + ":Survey found")
                        rows1.find_element(By.TAG_NAME, "a").click()
                        time.sleep(self.random_sleeptime)
                        parent = self.bot_driver.window_handles[0]
                        child = self.bot_driver.window_handles[1]
                        self.bot_driver.switch_to.window(child)
                        try:
                            WebDriverWait(self.bot_driver, 20).until(
                                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                            captchacheckbox = WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                            action = ActionChains(self.bot_driver);
                            obj_HumanActionSimulator.human_like_mouse_move(action, captchacheckbox)

                            WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                            time.sleep(60)
                            ispresent=self.__checkvalidcpxsurvey()
                            url=self.bot_driver.current_url
                            break
                        except:
                            print(traceback.print_exc())
                    elif (rows2.text in surveyproviderlist) and rows2.text.strip().startswith("BitLabs"):
                        print(rows2.text + ":Survey found")
                        self.logger.info(rows2.text + ":Survey found")
                        rows1.find_element(By.TAG_NAME, "a").click()
                        time.sleep(self.random_sleeptime)
                        iframe= self.bot_driver.find_element(By.CLASS_NAME, 'surveyIframeDiv')
                        bitlabgrid=iframe.find_element(By.XPATH,'//*[@id="offerwall"]/div[3]')
                        surveys = bitlabgrid.find_element(By.TAG_NAME, 'div')
                        print("No of Div available is:" + str(len(surveys)))
                    elif (rows2.text in surveyproviderlist) and rows2.text.strip().startswith("Dynata Survey Router"):
                        print(rows2.text + ":Survey found")
                        self.logger.info(rows2.text + ":Survey found")
                        rows1.find_element(By.TAG_NAME, "a").click()
                        time.sleep(self.random_sleeptime)
                        parent = self.bot_driver.window_handles[0]
                        child = self.bot_driver.window_handles[1]
                        self.bot_driver.switch_to.window(child)
                        url = self.bot_driver.current_url
                        ispresent=True
                        try:
                            WebDriverWait(self.bot_driver, 20).until(
                                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                            captchacheckbox = WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                            action = ActionChains(self.bot_driver);
                            obj_HumanActionSimulator.human_like_mouse_move(action, captchacheckbox)

                            WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                            time.sleep(60)
                            ispresent=self.__checkvalidcpxsurvey()
                            url=self.bot_driver.current_url
                            break
                        except:
                            print(traceback.print_exc())

                    else:
                        print("Match not found")


                if ispresent:
                    break

        except Exception as e:
            traceback.print_exc()
            print("Survey router Not found:"+repr(e))
            self.logger.info("Survey router Not found:"+repr(e))
            self.webdriver_obj.quitwebdriver()
        return ispresent,url,self.bot_driver







