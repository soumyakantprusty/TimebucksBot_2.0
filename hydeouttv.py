import datetime
import logging
import time
import random
import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from statusfileupdater import statusfileupdater

class hydeouttv:
    def __init__(self,url,basepath,bot_port,credentials):
        super(hydeouttv, self).__init__()
        self.bot_port=bot_port
        print(url)
        self.url = url
        self.basefilepath = basepath
        self.statusfileupdater=statusfileupdater("Watch Video-HYDEOUTTV",self.basefilepath)
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)



    def starthydeouttv(self,username,password):


        randomsleeptime=random.randint(5,10)
        self.bot_driver = self.webdriver_obj.startwebdriver()
        self.bot_driver.get(self.url)
        self.logger.info("Successfully started hydeout tv task")
        time.sleep(randomsleeptime)
        # Create a ThreadPoolExecutor
        executor = concurrent.futures.ThreadPoolExecutor()
        file_update_future = executor.submit(self.statusfileupdater.run)
        try:
            self.bot_driver.find_element_by_xpath('//*[@id="aw_loadmore"]').click()
        except:
            print("Button not found")
        time.sleep(randomsleeptime)
        try:
            iframe = self.bot_driver.find_element(By.XPATH,"//iframe[@id='iframeInstallApp400']")
            self.bot_driver.switch_to.frame(iframe)
            wait = WebDriverWait(self.bot_driver, 10)
            offer_holders = self.bot_driver.find_element(By.XPATH, '/html/body/div[5]')
            aw_offers= offer_holders.find_element(By.XPATH, './div[2]')
            offers=aw_offers.find_elements(By.CLASS_NAME,"offer")
            randomoffer=random.randint(0,len(offers))

            try:
                print(len(offers))
                random_list = random.sample(range(0, len(offers)), 1)
                print(random_list)
            except Exception as e:
                print(repr(e))
            hrefvalue=offers[random_list[0]].find_element(By.XPATH,'./div[1]/div[1]/div[2]/div[2]/a').get_attribute("href")
            print(hrefvalue)
            self.bot_driver.execute_script("window.open('about:blank', '_blank');")
            # self.bot_driver.find_element(By.XPATH,'/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[5]/div[3]/div[4]/p[2]/a').click()
            time.sleep(5)
            self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
            self.bot_driver.get(hrefvalue)
            time.sleep(10)
            try:
                self.bot_driver.find_element(By.XPATH,'//*[@id="signIn"]/a[2]').click()
                time.sleep(10)
                self.bot_driver.find_element(By.XPATH, '//*[@id="g-signin2"]/div/div/div').click()
                time.sleep(10)
            except:
                print("Already signed in.")
            time.sleep(5)
            elapsedtime=self.bot_driver.find_element(By.XPATH,'//*[@id="Brid_92783923"]/div/div[14]/div[10]/div').text
            print(elapsedtime)
            if elapsedtime=="00:00":
                print("Video Not playing")
                try:
                    self.bot_driver.find_element(By.XPATH,'/html/body/div[7]/div[1]/div[1]/div[5]/div[2]/div/div[14]/div[4]/span/svg/path').click()
                except:
                    print("Play button not found")
            current_datetime = datetime.datetime.now()
            print("Activity Start time:")
            print(current_datetime)
            time.sleep(900)
            self.statusfileupdater.stop()
            file_update_future.result()
            self.bot_driver.close()
            self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
        except:
            self.statusfileupdater.stop()
            file_update_future.result()
            print("offer block not available")
            self.logger.info("offer block not available")



