import logging
import time
import random
import concurrent.futures
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver
from statusfileupdater import statusfileupdater

class LootTv:
    def __init__(self,url,basepath,bot_port,credentials):
        super(LootTv, self).__init__()
        self.bot_port=bot_port
        print(url)
        self.credentials=credentials
        self.url = url
        self.basefilepath = basepath
        self.statusfileupdater=statusfileupdater("Watch Video-LOOTTV",self.basefilepath)
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.credentials_df = pd.read_csv(self.credentials)

    def starloottv(self):
        loottvstarted=True
        credentials_df=pd.read_csv(self.credentials)
        print(credentials_df)
        self.bot_driver = self.webdriver_obj.startwebdriver()
        self.bot_driver.get(self.url)
        time.sleep(5)
        WebDriverWait(self.bot_driver, 8).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='iframeInstallApp401']")))
        try:
            self.bot_driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/a[6]/button').click()
        except Exception as e:
            print("Unable to click on videos button")
            self.logger.info(repr(e))
            loottvstarted = True
        return loottvstarted
    def startwatchingloottv(self):
        executor = concurrent.futures.ThreadPoolExecutor()
        file_update_future = executor.submit(self.statusfileupdater.run)
        time.sleep(10)
        xpathlist=['//*[@id="root"]/div/div[2]/div/div[1]','//*[@id="root"]/div/div[2]/div/div[2]',
                   '//*[@id="root"]/div/div[2]/div/div[3]','//*[@id="root"]/div/div[2]/div/div[4]',
                   '//*[@id="root"]/div/div[2]/div/div[5]']
        randomxpath=random.randint(0,4)
        loottvlink=self.bot_driver.find_element(By.XPATH,xpathlist[randomxpath])
        print(loottvlink.get_attribute("class"))
        loottvlinks=loottvlink.find_elements_by_xpath('.//*')
        print(loottvlinks[1].get_attribute("href"))
        loottvlinks[1].click()
        parent = self.bot_driver.window_handles[0]
        child = self.bot_driver.window_handles[1]
        self.bot_driver.switch_to.window(child)
        time.sleep(10)
        try:
            self.bot_driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div/div[2]/a[1]/button').click()
            time.sleep(10)
            username=self.credentials_df.loc[self.credentials_df['appname']=='loottv','username'].values
            password = self.credentials_df.loc[self.credentials_df['appname'] == 'loottv','password'].values
            print(username+password)
            self.bot_driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div[2]/div[1]/input').clear()
            time.sleep(5)
            self.bot_driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div/div[2]/div[2]/div/div/div[2]/div[1]/input').send_keys(username)

            self.bot_driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div[2]/div[2]/input').clear().send_keys(password)
            time.sleep(5)
            self.bot_driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/div[2]/div/div/div[3]/button').click()
        except:
            print("No login required.")
            current_datetime = datetime.datetime.now()
            print("Activity Start time:")
            print(current_datetime)
            time.sleep(900)
            print(datetime.datetime.now())
            self.bot_driver.close()
            self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
            self.statusfileupdater.stop()
            print("Task Complete.")



