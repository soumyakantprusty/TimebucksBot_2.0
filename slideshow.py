import csv
import datetime
import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from clearunwantedtabs import clearunwantedtabs
from statusfileupdater import statusfileupdater
from randomsleeptime import RandomSleepTime
from anticaptcha import AntiCaptcha
from humansim import HumanActionSimulator

class slideshow:
    def __init__(self,url,basepath,bot_port,startnum, endnum,slideshowlimit):
        super(slideshow, self).__init__()
        self.bot_port=bot_port
        self.url = url
        self.slideshowlimit=slideshowlimit
        self.basefilepath = basepath
        self.parenthandle=""
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        self.statusfileupdater = statusfileupdater("Slide watch:", self.basefilepath)
        self.obj_randomsleeptime = RandomSleepTime(startnum, endnum)
        self.sleeptime = self.obj_randomsleeptime.getsleeptime()
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    def startslideshowtaskbot(self):
        self.bot_driver = self.webdriver_obj.startwebdriver()
        clearunwantedtabs(self.bot_driver, self.basefilepath)
        self.parent_handle = self.bot_driver.window_handles[0]
        print("Parent webdriver handle is:{handle}".format(handle=self.parenthandle))
        self.bot_driver.get(self.url)
        self.logger.info("Successfully started slideshow task")
    def check_presenceofslide(self):
        time.sleep(self.sleeptime)
        isslideavailable=True
        try:
            noofslideavailable = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH,
                 '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[3]/div[2]/div[2]/span/span'))).text

            # noofslideavailable=noofslideavailable1.find_element(By.TAG_NAME,'span').text

            if noofslideavailable == '':
                noofslideavailable = 0
        except:
            noofslideavailable = 0
        print("Number of slide left to watch:{slideleft}".format(slideleft=noofslideavailable))
        self.logger.info("Number of slide left to watch:{slideleft}".format(slideleft=noofslideavailable))
        try:
            timeremainingfornextslide = self.bot_driver.find_element(By.XPATH,
                                                                '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[5]/div[2]/div[1]/span/span').text
            print("Time remaining for next slide:{timeleft}".format(timeleft=timeremainingfornextslide))
            self.logger.info("Time remaining for next slide:{timeleft}".format(timeleft=timeremainingfornextslide))
        except:
            timeremainingfornextslide = 'Not Found'
        isviewbuttonavailable=True
        if int(noofslideavailable) == 0 or (int(noofslideavailable) == 17 and self.slideshowlimit=="yes"):
            print("No slide left to watch")
            self.logger.info("No slide left to watch")
            isslideavailable=False
        else:
            try:
               viewbutton = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                      (By.XPATH, '//*[@id="viewTimecaveTOffers"]/tbody/tr/td[5]/div/a/span/input')))
               isviewbuttonavailable = True
            except:
                print("View button No Available")
                self.logger.info("View button No Available for starting valid slide")
                isviewbuttonavailable=False
        while int(noofslideavailable)>0 and not isviewbuttonavailable:
            self.bot_driver.refresh()
            time.sleep(self.sleeptime)
            try:
               viewbutton = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                      (By.XPATH, '//*[@id="viewTimecaveTOffers"]/tbody/tr/td[5]/div/a/span/input')))
               isviewbuttonavailable = True
               isslideavailable = True
               break
            except:
                print("View button No Available")
                self.logger.info("View button No Available for starting valid slide")
                isviewbuttonavailable=False

        return isslideavailable

    def startslideshowtask(self):
        obj_anticaptcha = AntiCaptcha(self.bot_driver,3,self.basefilepath)
    
        try:
            viewbutton = WebDriverWait(self.bot_driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="viewTimecaveTOffers"]/tbody/tr/td[5]/div/a/span/input')))
            viewbutton.click()
            time.sleep(self.sleeptime+5)
            parent = self.bot_driver.window_handles[0]
            child = self.bot_driver.window_handles[1]
            self.bot_driver.switch_to.window(child)
            obj_anticaptcha.callanticaptcha()
            try:
                WebDriverWait(self.bot_driver, 8).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                WebDriverWait(self.bot_driver, 8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                time.sleep(30)
            except:
                currenturl = self.bot_driver.current_url
                if currenturl !="https://timebucks.com/redirects/timecave_redirect.php" and currenturl !="https://thetimecave.com/":
                    slideurl = []
                    for pagenum in range(2, 9):
                        newurl = currenturl.replace("/?", "/page/" + str(pagenum) + "/?")
                        slideurl.append(newurl)
                    print("Starting Slide Watch")
                    self.logger.info("Starting Slide Watch")
                    for url in slideurl:
                        print(url)
                        self.logger.info(url)
                        try:
                            self.bot_driver.get(url)
                        except Exception as e:
                            self.logger.info("Unable to connect to url.")
                            print("Unable to connect to url.")

                            break
                        time.sleep(self.sleeptime+5)
                    current_time=datetime.datetime.now()
                    self.bot_driver.get("https://timebucks.com/publishers/index.php?pg=earn&tab=view_content_timecave_slideshows")
                    for index, value in enumerate(self.bot_driver.window_handles):
                        if value != self.parent_handle:
                            self.bot_driver.switch_to.window(value)
                            self.bot_driver.close()
                            self.bot_driver.switch_to.window(self.parent_handle)
                    self.webdriver_obj.quitwebdriver()
                    with open(self.basefilepath+"\\botregister.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([datetime.datetime.now(), '3', 'Slideshow','Success','0.001'])
                else:
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(parent)
                    print("Correct URL not fetched.Skipping this task")
                    self.bot_driver.quit()
                    self.webdriver_obj.quitwebdriver()

        except:
            print("View Button not found")

        return datetime.datetime.now()

