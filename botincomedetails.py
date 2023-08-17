import logging
import re
import time
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pytz
from botwebdriver import botwebdriver
#from botwendriver_chrome import botwebdriver


class botincomedetails:
    def __init__(self,url,basepath,bot_port,currentuser):
        super(botincomedetails, self).__init__()
        print("Intializing bot income fetcher")
        self.url=url
        self.basefilepath=basepath
        self.bot_port=bot_port
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        self.ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        self.gmt8_timezone = pytz.timezone("America/New_York")
        self.incomedetails=[]
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def getbotincometaskdetails(self):
        self.bot_driver = self.webdriver_obj.startwebdriver()
        try:
            print("###################")
            print("Checking income details...")
            print("##################")
            self.logger.info("Checking income details...")
            self.bot_driver.get(self.url)
            time.sleep(5)
           # Process or store the extracted data as needed
            pagination=self.bot_driver.find_element(By.XPATH,'//*[@id="pagination"]/div')
            noofpages=pagination.find_elements(By.TAG_NAME,'a')
            pageurls=[ page.get_attribute("href") for page in noofpages ]
            #print(pageurls)
            for page in range(0,len(noofpages)):
                lastrowfound=False
                self.bot_driver.execute_script("window.open('');")
                self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                # self.bot_driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
                time.sleep(2)
                self.bot_driver.get(pageurls[page])
                time.sleep(2)
                earningdetailtable = self.bot_driver.find_element(By.ID, "widget_table")
                tablebody = earningdetailtable.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
                tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
                for row in tablerows:
                    income=[]
                    cols = row.find_elements(By.TAG_NAME, "td")
                    taskname=cols[0].text
                    taskcost=cols[2].text
                    taskdate=cols[3].text
                    print(taskname+":"+taskcost+":"+taskdate)


                    pattern = r"\d{1,2}(?:st|nd|rd|th)\s+\w+\s+\d{2}"
                    match = re.search(pattern, taskdate)
                    if match:
                        date_part = match.group()
                        print("Date part:", date_part)
                        # Convert the date part to a datetime object
                        date_obj = datetime.strptime(date_part, "%dth %b %y")
                        # Calculate the current date
                        current_gmtdate = datetime.now(self.ist_timezone).astimezone(self.gmt8_timezone).date()
                        print(date_obj,current_gmtdate)
                        if date_obj.date()==current_gmtdate:
                            lastrowfound = False
                            income.append(taskname)
                            income.append(taskcost)
                            income.append(taskdate)
                            self.incomedetails.append(income)
                        else:
                            lastrowfound = True
                            print("last row found")
                            break



                    else:
                        print("Date part not found in the string.")
                self.bot_driver.close()
                self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                if lastrowfound:
                    break
            print("#####################Getting Bonus Income##########################")
            self.bot_driver.get("https://timebucks.com/publishers/index.php?pg=my_bonuses")
            time.sleep(3)
            earningdetailtable = self.bot_driver.find_element(By.ID, "bounsTable")
            tablebody = earningdetailtable.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            for row in tablerows:
                income = []
                cols = row.find_elements(By.TAG_NAME, "td")
                taskname = cols[0].text
                taskcost = cols[1].text
                taskdate = cols[2].text
                print(taskname + ":" + taskcost + ":" + taskdate)
                date_obj = datetime.strptime(taskdate, "%Y-%m-%d %H:%M:%S").date()
                    # Calculate the current date
                current_gmtdate = datetime.now(self.ist_timezone).astimezone(self.gmt8_timezone).date()
                print(date_obj, current_gmtdate)
                if date_obj==current_gmtdate:
                    income.append(taskname)
                    income.append(taskcost)
                    income.append(taskdate)
                    self.incomedetails.append(income)
                else:
                    lastrowfound = False
                    print("last row not found")
                    break
            else:
                print("Date part not found in the string.")
            #print(self.incomedetails)
            return self.incomedetails,current_gmtdate
        except Exception as e:
            print(repr(e))
            self.logger.info(repr(e))












    