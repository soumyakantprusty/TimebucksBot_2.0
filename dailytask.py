import csv
import datetime
import os
import traceback
from urllib.parse import urlparse
import concurrent.futures
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import random
from  botwebdriver import botwebdriver
from clearunwantedtabs import clearunwantedtabs
from statusfileupdater import statusfileupdater
from randomsleeptime import RandomSleepTime
from anticaptcha import AntiCaptcha
class dailymandatorytask:
    def __init__(self,url,basepath,dailytasktitle,dailyquizpngpath,hr12websitevisit,dailyupvotepngpath,dailyclickpngpath,bot_port,startnum,endnum):
        super(dailymandatorytask, self).__init__()
        self.url = url
        self.basefilepath = basepath
        self.dailytasktitle=dailytasktitle
        self.dailyquizpngpath=dailyquizpngpath
        self.dailyupvotepngpath=dailyupvotepngpath
        self.dailyclickpngpath=dailyclickpngpath
        self.hr12websitevisit=hr12websitevisit
        self.random_sleeptime = random.randint(int(startnum), int(endnum))
        self.statusfileupdater = statusfileupdater("Daily Task-quiz", self.basefilepath)
        self.webdriver_obj = botwebdriver(bot_port, basepath)
        try:
            logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        except Exception as e:
            print(repr(e))
        self.logger = logging.getLogger(__name__)

    def startdailytaskbot(self):
        issuccessful=True
        self.bot_driver = self.webdriver_obj.startwebdriver()
        obj_clearunwantedtabs = clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.bot_driver.get(self.url)
        self.logger.info("Successfully started daily Bot task")

    def check_presenceoftask(self):
        time.sleep(self.random_sleeptime)
        print("Checking if any unfinish task is present")
        self.logger.info("Checking if any unfinish task is present")
        try:
            self.bot_driver.find_element(By.XPATH, '//input[@class="btnCancelBuyTasksCampaign"]').click()
            WebDriverWait(self.bot_driver, 20).until(EC.alert_is_present())
            alert = self.bot_driver.switch_to.alert
            alert.accept()
            self.logger.info("Unfinished Task is closed successfully")
        except:
            print("No Unfinished Task found")
            self.logger.info("No Unfinished Task found")
        time.sleep(self.random_sleeptime)
        taskfrequencylist = (WebDriverWait(self.bot_driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/button'))))
        taskfrequencylist.click()
        time.sleep(self.random_sleeptime)
        try:
            selectalltask = (WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located(
                    (
                    By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[1]'))))
            selectalltask.click()
            time.sleep(self.random_sleeptime)
        except:
            self.bot_driver.find_element(By.XPATH,
                                    '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[4]/div[2]/div/p[2]/span/a').click()
            time.sleep(self.random_sleeptime)
            selectalltask = (WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[1]'))))
            selectalltask.click()
            time.sleep(self.random_sleeptime)
        try:
            every24hour = (WebDriverWait(self.bot_driver, 10).until(
                    EC.visibility_of_element_located(
                             (By.XPATH,
                                  '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[8]'))))

            self.bot_driver.execute_script("arguments[0].scrollIntoView();", every24hour)
            every24hour.click()
        except TimeoutException as e:
            self.bot_driver.refresh()
            every24hour = (WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[8]'))))


            every24hour.click()
        try:
            every12hour = (WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                        '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[7]'))))

            self.bot_driver.execute_script("arguments[0].scrollIntoView();", every12hour)
            every12hour.click()
        except TimeoutException as e:
            self.bot_driver.refresh()
            every12hour = (WebDriverWait(self.bot_driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                        '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[3]/div/span/div/div/button[7]'))))

            every12hour.click()



        time.sleep(self.random_sleeptime)
        taskfrequencylist.click()
        time.sleep(self.random_sleeptime)
        submitbtn = (WebDriverWait(self.bot_driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[4]/div[2]/div/div/div[7]/span/span'))))
        submitbtn.click()
        time.sleep(self.random_sleeptime)
        table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
        tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
        tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
        availabletask=[]
        for row in tablerows:
            col = row.find_elements(By.TAG_NAME, "td")
            for title in self.dailytasktitle:
                if title in col[0].text:
                    availabletask.append(title)
        return availabletask
    def __solveCaptcha(self):
        print("Calling AntiCaptcha API.")
        obj_captchasolver = AntiCaptcha(self.bot_driver,1,self.basefilepath)
        obj_captchasolver.callanticaptcha()

    def __dailyclick(self):
        try:
            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            for row in tablerows:
                col = row.find_elements(By.TAG_NAME, "td")
                if "Daily Click" in col[0].text:
                    print("Found my Daily Click task")
                    self.logger.info("Found my Daily Click task")
                    col[1].find_element(By.TAG_NAME, "a").click()
                    time.sleep(self.random_sleeptime)
                    try:
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                        print("Captcha Code found")
                        self.logger.info("Captcha Code found")
                        self.bot_driver.switch_to.parent_frame()
                        self.__solveCaptcha()
                        time.sleep(self.random_sleeptime)
                    except Exception as e:
                        print(repr(e))
                        self.bot_driver.switch_to.parent_frame()
                        self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]')
                        time.sleep(self.random_sleeptime)
                    url = self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                    atag = url.find_element(By.TAG_NAME, 'a')
                # linktext1=atag.text
                    linktext2 = atag.get_attribute("href")
                # print(linktext1)
                    print(linktext2)
                    self.bot_driver.find_element(By.LINK_TEXT, linktext2).click()
                    parent = self.bot_driver.window_handles[0]
                # obtain browser tab window
                    child = self.bot_driver.window_handles[1]
                    self.bot_driver.switch_to.window(child)
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.XPATH,
                                            '/html/body/div[2]/div[2]/div/section/div/div[3]/div/center[1]/center/div[1]/div/div/div/div[2]/div/div/div[1]/a[2]').click()


                    time.sleep(self.random_sleeptime)
                    child2 = self.bot_driver.window_handles[2]
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(self.bot_driver.window_handles[1])
                    self.bot_driver.save_screenshot(self.dailyclickpngpath)
                    self.logger.info("Screen shot taken")
                    print("Screenshot taken")
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(parent)
                    self.bot_driver.find_element(By.XPATH, '//*[@id="buyTasksForm"]/div[2]/span/input[2]').click()
                    time.sleep(self.random_sleeptime)
                    pyautogui.write(self.dailyclickpngpath)  # enter file with path
                    time.sleep(self.random_sleeptime)
                    pyautogui.press('enter')
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitForApproval"]').click()
                    time.sleep(self.random_sleeptime)
                    with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.datetime.now(), '1', 'dailytask', 'Success', '0.001'])
                    break
        except Exception as e:
            print("Encountered error as below ")
            print(repr(e))
            self.logger.info("Encountered error as below ::"+repr(e))



    def __dailyYtubecomment(self):
        try:
            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            for row in tablerows:
                col = row.find_elements(By.TAG_NAME, "td")
                if "Upvote this comment Daily " in col[0].text:
                    self.logger.info("Found my Daily Youtube comment upvote task")
                    print("Found my Daily Youtube comment upvote task")
                    col[1].find_element(By.TAG_NAME, "a").click()
                    time.sleep(self.random_sleeptime)
                    try:
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                        print("Captcha Code found")
                        self.logger.info("Captcha Code found")
                        self.bot_driver.switch_to.parent_frame()
                        self.__solveCaptcha()
                        time.sleep(4)
                    except Exception as e:
                        print(repr(e))
                        self.bot_driver.switch_to.parent_frame()
                        self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]').click()
                        time.sleep(self.random_sleeptime)
                    url = self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                    atag = url.find_element(By.TAG_NAME, 'a')
                # linktext1=atag.text
                    linktext2 = atag.get_attribute("href")
                # print(linktext1)
                    print(linktext2)
                    self.bot_driver.find_element(By.LINK_TEXT, linktext2).click()
                    time.sleep(self.random_sleeptime)
                    parent = self.bot_driver.window_handles[0]
                # obtain browser tab window
                    child = self.bot_driver.window_handles[1]
                    self.bot_driver.switch_to.window(child)
                    current_url = self.bot_driver.current_url
                    print(current_url)
                    while "www.youtube.com" not in self.bot_driver.current_url:
                        self.bot_driver.refresh()
                        time.sleep(self.random_sleeptime)
                        current_url = self.bot_driver.current_url
                        print(current_url)
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.execute_script("window.scrollTo(0, 500)")
                    time.sleep(self.random_sleeptime)
                # element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-comment-thread-renderer')))

                # scroll to the element using ActionChains
                # actions = ActionChains(bot_driver)
                # actions.move_to_element(element).perform()
                ##""
                    try:
                        usercommentslist = self.bot_driver.find_elements(By.TAG_NAME, 'ytd-comment-thread-renderer')
                        butttonbar = usercommentslist[0].find_element(By.TAG_NAME,
                                                                    'ytd-comment-action-buttons-renderer')

                    except:
                        self.bot_driver.execute_script("window.scrollTo(0, 100)")
                        time.sleep(self.sleeptime)
                        usercommentslist = self.bot_driver.find_elements(By.TAG_NAME, 'ytd-comment-thread-renderer')
                        butttonbar = usercommentslist[0].find_element(By.TAG_NAME,
                                                                  'ytd-comment-action-buttons-renderer')
                    butttonbar.find_element(By.ID, 'like-button').click()
                ## // *[ @ id = "like-button"]
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.save_screenshot(self.dailyupvotepngpath)
                    print("Screenshot taken")
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(parent)
                    self.bot_driver.find_element(By.XPATH, '//*[@id="buyTasksForm"]/div[2]/span/input[2]').click()
                    time.sleep(self.random_sleeptime)
                    pyautogui.write(
                    self.dailyupvotepngpath)  # enter file with path
                    time.sleep(self.random_sleeptime)
                    pyautogui.press('enter')
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitForApproval"]').click()
                    time.sleep(self.random_sleeptime)
                    with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.datetime.now(), '1', 'dailytask', 'Success', '0.001'])
                    break
        except Exception as e:
            print("Encountered error as below ")
            print(repr(e))
            self.logger.info("Encountered error as below ::" + repr(e))



    def __dailyEmail(self):
        try:
            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            for row in tablerows:
                col = row.find_elements(By.TAG_NAME, "td")
                if "Receive Email and Open Link - Daily"   in col[0].text:
                    print("Found my Daily Email task")
                    self.logger.info("Found my Daily Email task")
                    col[1].find_element(By.TAG_NAME, "a").click()
                    time.sleep(self.random_sleeptime)
                    try:
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                        print("Captcha Code found")
                        self.logger.info("Captcha Code found")
                        self.bot_driver.switch_to.parent_frame()
                        self.__solveCaptcha()
                        time.sleep(4)

                    except Exception as e:
                        print(repr(e))
                        self.bot_driver.switch_to.parent_frame()
                        self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]').click()
                        time.sleep(self.random_sleeptime)
                    url = self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                    atag = url.find_element(By.TAG_NAME, 'a')
                # linktext1=atag.text
                    linktext2 = atag.get_attribute("href")
                # print(linktext1)
                    print(linktext2)
                    self.bot_driver.find_element(By.LINK_TEXT, linktext2).click()
                    time.sleep(self.random_sleeptime)
                    parent = self.bot_driver.window_handles[0]
                # obtain browser tab window
                    child = self.bot_driver.window_handles[1]
                    self.bot_driver.switch_to.window(child)
                    try:
                        self.bot_driver.get('https://timebucks.com/task_email_code.php')
                    except WebDriverException as e:
                        print("Webdriver exception occurred.")

                    time.sleep(self.random_sleeptime)
                    code = self.bot_driver.find_element(By.XPATH, '/html/body/strong').text
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(parent)

                    time.sleep(self.random_sleeptime)
                    textarea = self.bot_driver.find_element(By.XPATH,
                                                   '//textarea[@id="Username"]')
                    textarea.click()
                    time.sleep(self.random_sleeptime)
                    textarea.send_keys(code)
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitForApproval"]').click()
                    time.sleep(self.random_sleeptime)
                    with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.datetime.now(), '1', 'dailytask', 'Success', '0.001'])
                    break
        except Exception as e:
            print("Encountered error as below ")
            print(repr(e))
            self.logger.info("Encountered error as below ::" + repr(e))
    def __checkAdvertisement(self,bot_driver):
        adfound=False
        try:
            adframe=WebDriverWait(bot_driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='aswift_2']")))
            display_value = adframe.value_of_css_property('display')
            print(display_value)
            if display_value !='none':
                adfound=True
        except:
            print("No Ad Found")
        return adfound


    def __randomclick(self,driver):
        screen_width = driver.execute_script("return window.innerWidth")
        screen_height = driver.execute_script("return window.innerHeight")

        # Generate random coordinates at the edge of the screen
        #edge = random.choice(['top', 'bottom', 'left', 'right'])
        edge='top'
        if edge == 'top':
            x = 1
            y = 0
        elif edge == 'bottom':
            x = random.randint(0, screen_width)
            x = screen_width-10
            y = screen_height-10
        elif edge == 'left':
            x = 0
            y = random.randint(0, screen_height)
        else:  # edge == 'right'
            x = screen_width
            y = random.randint(0, screen_height)

        # Perform the random click
        print("X coordinate{x} and Y Coordinate{y}".format(x=x,y=y))
        driver.execute_script(f"window.scrollTo({x}, {y});")
        driver.find_element_by_tag_name('body').click()
        time.sleep(5)

    def __dailyQuiz(self):
        try:
            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            isswift2Adpresent = False
            isswift3Adpresent = False
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            randomsleeptime=random.randint(5,10)
        # Create a ThreadPoolExecutor
            executor = concurrent.futures.ThreadPoolExecutor()
            file_update_future = executor.submit(self.statusfileupdater.run)
            try:
                for row in tablerows:
                    col = row.find_elements(By.TAG_NAME, "td")
                    if "Complete a Quiz - DAILY" in col[0].text:
                        print("Found my Daily Quiz task")
                        self.logger.info("Found my Daily Quiz task")
                #executor = concurrent.futures.ThreadPoolExecutor()
                #file_update_future = executor.submit(self.statusfileupdater.run)
                        col[1].find_element(By.TAG_NAME, "a").click()
                        time.sleep(self.random_sleeptime)
                        try:
                            WebDriverWait(self.bot_driver, 20).until(
                                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                            WebDriverWait(self.bot_driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
                            print("Captcha Code found")
                            self.logger.info("Captcha Code found")
                            self.bot_driver.switch_to.parent_frame()
                            self.__solveCaptcha()
                            time.sleep(4)


                        except Exception as e:
                            print(repr(e))
                            self.logger.info("No Captcha Code found")
                            self.bot_driver.switch_to.parent_frame()
                            self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]').click()
                            time.sleep(self.random_sleeptime)
                        url = self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                        atag = url.find_element(By.TAG_NAME, 'a')
                    # linktext1=atag.text
                        linktext2 = atag.get_attribute("href")
                        print(linktext2)
                        self.bot_driver.execute_script("window.open('about:blank', '_blank');")
                        self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                        self.bot_driver.get(linktext2)
                        time.sleep(self.random_sleeptime)
                        try:
                            self.bot_driver.find_element(By.XPATH,
                                                        '/html/body/main/div/section/div/div[1]/div/div[1]/div/a[2]').click()
                            time.sleep(randomsleeptime)
                            self.bot_driver.find_element(By.XPATH,
                                                        '/html/body/main/div/section/div/div[1]/div/div[2]/div/a[2]').click()
                            time.sleep(randomsleeptime)
                            self.bot_driver.find_element(By.XPATH, '//*[@id="letsstart"]').click()
                            time.sleep(randomsleeptime)
                        except:
                            print("Intial question not shown")
                        time.sleep(self.random_sleeptime)
                        adfound=self.__checkAdvertisement(self.bot_driver)
                        if adfound:
                            self.__randomclick(self.bot_driver)
                            self.bot_driver.switch_to.parent_frame()
                        try:
                            self.bot_driver.find_element(By.XPATH,'//*[@id="playcontest"]').click()
                        except:
                            print("Play contest button not found")
                        time.sleep(self.random_sleeptime)
                        adfound = self.__checkAdvertisement(self.bot_driver)
                        if adfound:
                            self.__randomclick(self.bot_driver)
                        self.bot_driver.switch_to.parent_frame()
                        time.sleep(5)
                        repeaters = self.bot_driver.find_elements(By.CLASS_NAME, 'repeater')
                        #repeaters=quiz.find_elements(By.CLASS_NAME,'repeater')
                        print("No of available quizes:{quiznum}".format(quiznum=len(repeaters)))
                        for cntr in range(len(repeaters)):
                            randomrepeater = random.randint(3, len(repeaters) - 1)
                            btntext = repeaters[randomrepeater].find_element(By.CLASS_NAME, 'playbtn').find_element(By.TAG_NAME,
                                                                                                                'a').text
                            print("buttontext{text}".format(text=btntext))
                            if btntext == "PLAY NOW":
                                repeaters[randomrepeater].find_element(By.CLASS_NAME, 'playbtn').find_element(By.TAG_NAME,'a').click()
                                time.sleep(5)
                                try:
                                    self.bot_driver.find_element(By.XPATH, '//*[@id="playcontest"]').click()
                                except Exception as e:
                                    print(repr(e))
                            time.sleep(5)
                            break
                        time.sleep(self.sleeptime)

                        adfound = self.__checkAdvertisement(self.bot_driver)
                        if adfound:
                            self.__randomclick(self.bot_driver)
                        self.bot_driver.switch_to.parent_frame()
                        for cntr in range(0, 25):
                            adfound = self.__checkAdvertisement(self.bot_driver)
                            if adfound:
                                self.__randomclick(self.bot_driver)
                            self.bot_driver.switch_to.parent_frame()
                            try:
                                if self.bot_driver.find_element(By.XPATH,'/html/body/main/section/div/div/div/div[2]/div[2]/h2').text=="Time's up, well played!":
                                    break
                            except:
                                print("Quiz is in progress.")
                            randomans = random.randint(1, 3)
                            try:
                                xpath = '/html/body/main/section/div/div/div/div[3]/div[2]/a[' + str(randomans) + ']'
                                self.bot_driver.find_element(By.XPATH, xpath).click()
                            except Exception as e:
                                print(traceback.print_stack())
                            time.sleep(self.random_sleeptime)
                        adfound = self.__checkAdvertisement(self.bot_driver)
                        if adfound:
                            self.__randomclick(self.bot_driver)
                        self.bot_driver.switch_to.parent_frame()
                        self.bot_driver.save_screenshot(self.dailyquizpngpath)
                        print("Screenshot taken")
                        self.logger.info("Screenshot taken")
                        self.bot_driver.close()
                        self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                        self.bot_driver.find_element(By.XPATH, '//*[@id="buyTasksForm"]/div[2]/span/input[2]').click()
                        time.sleep(self.random_sleeptime)
                        pyautogui.write(self.dailyquizpngpath)  # enter file with path
                        time.sleep(self.random_sleeptime)
                        pyautogui.press('enter')
                        time.sleep(self.random_sleeptime)
                        self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitForApproval"]').click()
                        time.sleep(25)
                        print("Successfully completed daily quiz task.")
                        self.logger.info("Successfully completed daily quiz task.")
                        self.statusfileupdater.stop()
                        file_update_future.result()
                        with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([datetime.datetime.now(), '1', 'dailytask', 'Success', '0.001'])
                        break

            except:
                print("Encountered Error while completing daily quiz task.1")
                self.logger.info("Encountered Error while completing daily quiz task.1")
                self.statusfileupdater.stop()
                file_update_future.result()
                self.bot_driver.close()
                self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
        except:
            print("Encountered Error while completing daily quiz task.2")
            self.logger.info("Encountered Error while completing daily quiz task.2")
            self.bot_driver.close()
            self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
    def __12hrwebsitevisit(self):
        try:
            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            for row in tablerows:
                col = row.find_elements(By.TAG_NAME, "td")
                if "Website visit" in col[0].text:
                    print("Found Once in 12 Hr Website visit")
                    self.logger.info("Found Once in 12 Hr Website visit")
                    col[1].find_element(By.TAG_NAME, "a").click()
                    time.sleep(self.random_sleeptime)
                    try:
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                        WebDriverWait(self.bot_driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                        time.sleep(60)
                        self.bot_driver.switch_to.parent_frame()
                    except Exception as e:
                        print(repr(e))
                        self.bot_driver.switch_to.parent_frame()
                        self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]').click()
                        time.sleep(self.random_sleeptime)
                    url = self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                    atag = url.find_element(By.TAG_NAME, 'a')
                # linktext1=atag.text
                    linktext2 = atag.get_attribute("href")
                # print(linktext1)
                    print(linktext2)
                    self.bot_driver.find_element(By.LINK_TEXT, linktext2).click()
                    time.sleep(10)
                    parent = self.bot_driver.window_handles[0]
                # obtain browser tab window
                    child = self.bot_driver.window_handles[1]
                    self.bot_driver.switch_to.window(child)
                    time.sleep(self.random_sleeptime)
                    #self.bot_driver.find_element(By.XPATH,
                                            #'//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[1]/div/a').click()
                    self.bot_driver.get("https://greatoceanrd.org.au/")


                    time.sleep(200)
                    self.bot_driver.save_screenshot(self.hr12websitevisit)
                    self.logger.info("Screen shot taken")
                    print("Screenshot taken")
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(parent)
                    self.bot_driver.find_element(By.XPATH, '//*[@id="buyTasksForm"]/div[2]/span/input[2]').click()
                    time.sleep(self.random_sleeptime)
                    pyautogui.write(self.hr12websitevisit)  # enter file with path
                    time.sleep(self.random_sleeptime)
                    pyautogui.press('enter')
                    time.sleep(self.random_sleeptime)
                    self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitForApproval"]').click()
                    time.sleep(20)
                    with open(self.basefilepath + "\\botregister.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.datetime.now(), '1', 'dailytask', 'Success', '0.001'])
                    break
        except Exception as e:
            print("Encountered error as below ")
            print(repr(e))
            self.logger.info("Encountered error as below ::"+repr(e))









    def executedailytask(self,availabletask):
        print(availabletask)
        for task in availabletask:
                if task =="Daily Click":
                    self.__dailyclick()
                elif task =="Complete a Quiz - DAILY":
                    self.__dailyQuiz()
                elif task =="Receive Email and Open Link - Daily  ":
                    self.__dailyEmail()
                elif task =="Upvote this comment Daily ":
                    self.__dailyYtubecomment()
                #elif task =="Website visit":
                    #self.__12hrwebsitevisit()
                availabletask=self.check_presenceoftask()
        self.bot_driver.quit()
        self.webdriver_obj.quitwebdriver()







