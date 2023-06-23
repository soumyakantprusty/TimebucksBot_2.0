import logging
import time
from datetime import datetime, date, timedelta

from selenium.webdriver.common.by import By

#from botwebdriver import botwebdriver
from botwendriver_chrome import botwebdriver


class botincomedetails:
    def __init__(self,url,basepath,bot_port,currentuser):
        super(botincomedetails, self).__init__()
        self.url=url
        self.basefilepath=basepath
        self.bot_port=bot_port
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)

        self.incomedetails={"user":currentuser,"total_task_done":0,"total_task_approved":0,"total_earnings":0,"total_bonus":0,"total_referal_earning":0,"net_earning":0}
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def getbotincometaskdetails(self):
        try:
            print("##################")
            print("Checking income details...")
            print("##################")
            self.logger.info("Checking income details...")
            self.bot_driver = self.webdriver_obj.startwebdriver()
            self.bot_driver.get(self.url)
            time.sleep(10)
            earningdetailtable=self.bot_driver.find_element(By.ID,"earningsTable")
            tablebody = earningdetailtable.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            cols=tablerows[1].find_elements(By.TAG_NAME, "td")

            totalamountearned=cols[1].text
            totaltaskapproved=cols[2].text
            totaltaskdone=cols[3].text
            self.incomedetails['total_task_done']=totaltaskdone
            self.incomedetails['total_task_approved'] = totaltaskapproved
            self.incomedetails['total_earnings'] = totalamountearned
            time.sleep(3)
            self.bot_driver.get("https://timebucks.com/publishers/index.php?pg=my_bonuses")
            time.sleep(5)
            bonustable = self.bot_driver.find_element(By.ID, "bounsTable")
            tablebody = bonustable.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            total_bonus = []
            for row in tablerows:

                cols=row.find_elements(By.TAG_NAME, "td")
                if (datetime.strptime(cols[2].text, '%Y-%m-%d %H:%M:%S')).date()==(date.today()-timedelta(days=1)):
                    total_bonus.append(float(cols[1].text.replace('$',"")))
            time.sleep(5)

            self.incomedetails['total_bonus']=sum(total_bonus)
            totalreferal_earnings=self.bot_driver.find_element(By.XPATH,'/html/body/div[9]/div[2]/div/div[1]/div[2]/div/div[2]/a/span').text
            self.incomedetails['total_referal_earning']=totalreferal_earnings
            return self.incomedetails
        except:
            print("Encountered Error")
            self.logger.info("Encountered Error")












    