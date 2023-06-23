
import csv
import datetime
import logging
import re
import time

import pandas as pd
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from clearunwantedtabs import clearunwantedtabs
from bs4 import BeautifulSoup

from botwebdriver import botwebdriver
from bottaskdetails import BotTaskDetails
from randomsleeptime import RandomSleepTime
class dailyyoutubetask:
    def __init__(self, url, basepath, bot_port,curentuser,startnum, endnum):
        super(dailyyoutubetask, self).__init__()
        self.url = url
        self.basefilepath = basepath
        self.bot_port = bot_port
        self.bot_driver=""
        self.curentuser=curentuser
        self.max_retries=1
        self.skiptask_df=pd.read_csv(basepath+"\\youtubeskiptask.csv")
        self.dailyyoutubetaskpng="C:\\Users\\"+self.curentuser+"\\Documents\\TimeBucksBots\\DailyYtube.png"
        self.webdriver_obj = botwebdriver(self.bot_port, basepath)
        self.taskregistry_obj=BotTaskDetails(basepath,curentuser)
        self.obj_randomsleeptime = RandomSleepTime(startnum, endnum)
        self.sleeptime = self.obj_randomsleeptime.getsleeptime()
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
        self.logger.info("Successfully started daily Youtube task")
        return True
    def check_presenceoftask(self):
        time.sleep(self.sleeptime)
        taskclosed=True
        print("Checking if any unfinish task is present")
        self.logger.info("Checking if any unfinish task is present")
        try:
            self.bot_driver.find_element(By.XPATH, '//input[@class="btnCancelBuyTasksCampaign"]').click()
            WebDriverWait(self.bot_driver, 20).until(EC.alert_is_present())
            alert = self.bot_driver.switch_to.alert
            alert.accept()
            self.logger.info("Unfinished Task is closed successfully")
        except Exception as e:
            print(str(e))
            print("No Unfinished Task found")
            self.logger.info("No Unfinished Task found")
            taskclosed=True
        return taskclosed

    def setfilterfoytubetask(self):
        retry_count=0
        isjobdone = True
        time.sleep(self.sleeptime)
        print("starting of setting filters")
        self.logger.info("starting of setting filters")
        time.sleep(self.sleeptime)
        try:
            actionlist = (WebDriverWait(self.bot_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/button'))))

            actionlist.click()
            select_allbtn = (WebDriverWait(self.bot_driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/div/button[1]'))))
            select_allbtn.click()
            time.sleep(self.sleeptime)
            selectytubevideowatchbtn = (WebDriverWait(self.bot_driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '//*[@id="tasks_content_375"]/div[4]/div[2]/div/div/div[1]/div/span/div/div/button[17]'))))
            selectytubevideowatchbtn.click()
            time.sleep(self.sleeptime)
            sortbybtn=(WebDriverWait(self.bot_driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,'//*[@id="buyTasksSortBy"]'))))
            sortbybtn.click()
            time.sleep(self.sleeptime)
            newestfirstoption=(WebDriverWait(self.bot_driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,'//*[@id="buyTasksSortBy"]/option[4]'))))
            newestfirstoption.click()
            time.sleep(self.sleeptime)
            submitbtn = (WebDriverWait(self.bot_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[4]/div[2]/div/div/div[7]/span/span'))))
            submitbtn.click()
            time.sleep(self.sleeptime)

        except Exception as e:
            isjobdone=False
            print(repr(e))
        return isjobdone
    def __stringcategorization(self,instructions):
        instructions = instructions.strip()
        file_path = self.basefilepath+"\\taskinstructions.txt"  # Provide the desired file path

        # Open the file in write mode
        with open(file_path, "a") as file:
            data = instructions
            file.write(data)
        with open(file_path, "a") as file:
            file.write("###############################################################################")
        patternlist = [
            r"1\. Go to\s+(.*?)\s+and click(?:\son\s)?(?:the\s)?video titled\s+(.*?)\s+with this thumbnail\s+(.*?)\s+from(?:\sthe\s)?(.*?)you will need to scroll down a bit\s+2\. Watch at-least\s+(.*?)\s+minutes of(?:\sthe\s)?video\.?\s+3\. Optional Like the video",
            r"1\. Go to\s+(.*?)\s+and click on the video titled\s+(.*?)\s+with this thumbnail\s+(.*?)\s+from(?:\sthe\s)?(.*?)you will need to scroll down a bit\s+2\. Watch at-least\s+(.*?)\s+minutes of the video\.?\s+3\. Optional Like the video",
            r"1\. Go to\s+(.*?)\s+and click on the video titled\s+(.*?)\s+with this\s+(.*?)\s+from(?:\sthe\s)?(.*?)you will need to scroll down a bit\s+2\. Watch(?:\sthe\s)?entire\s+(.*?)\s+minutes (?:\sof\s)?(?:\sthe\s)? video\.?\s",
            r"1\. Go to\s+(.*?)\s+and click(?:\son\s)?(?:the\s)?video titled\s+(.*?)\s+with this thumbnail\s+(.*?)\s+from(?:\sthe\s)?(.*?)you will need to scroll down a bit\s+2\. Watch at-least\s+(.*?)\s+minutes of(?:\sthe\s)?video\.?\s+3\. Optional Like the video",
            r"1\. watch our youtube video for\s+(.*?)\s+minute\s+(.*?)",
            r"1\. Click this link\s+(.*?)\s+2\. Watch the video\s+(.*?)\s+min\."
        ]
        instructiontype=-1
        for pattern in patternlist:
            matches = re.search(pattern,instructions, re.DOTALL | re.IGNORECASE)
            if matches:
                instructiontype=patternlist.index(pattern)
                break
        return instructiontype




    def __extractinformation(self,instruction,ytubetasktype):
        print("Starting extraction of infromation from Instructions")
        if ytubetasktype==1 or ytubetasktype==0:
            videotitle_pattern = r"video titled(.*?)with this thumbnail"
            ytubevideolist_pattern = r"Go to(.*?)and click"
            videowatchduration_pattern = r"Watch at-least(.*?)of the video"
            videowatchduration_pattern2 = r"Watch the entire(.*?)of the video"
            # Extract the desired strings using regular expressions
            matches = re.findall(videotitle_pattern, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches = [match.strip() for match in matches]
            # Print the extracted strings
            print("Extracted Video title")
            video_title = ""
            for match in matches:
                print(match)
                if "???" in match:
                    # Replace "???" placeholders with spaces in the second string
                    string2_replaced = match.replace("???", " ")
                    video_title = string2_replaced
                else:
                    string2_replaced = match
                    video_title = string2_replaced


            matches2 = re.findall(ytubevideolist_pattern, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches2 = [match.strip() for match in matches2]
            # Print the extracted strings
            print("Extracted url")
            ytubevideolist_url = ""
            for match in matches2:
                print(match)
                ytubevideolist_url = match
            matches3 = re.findall(videowatchduration_pattern, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches3 = [match.strip() for match in matches3]
            # Print the extracted strings
            print("Extracted video duration")
            videowatchduration = ""
            for match in matches3:
                print(match)
                videowatchduration = match

            if videowatchduration=="":
                matches3 = re.findall(videowatchduration_pattern2, instruction, re.DOTALL)
                # Remove leading and trailing whitespace from each match
                matches3 = [match.strip() for match in matches3]
                # Print the extracted strings
                print("Extracted video duration")
                for match in matches3:
                    print(match)
                    videowatchduration = match
        elif ytubetasktype==-1:
            print("No match found")
            video_title=""
            ytubevideolist_url=""
            videowatchduration=""
        elif ytubetasktype==2:
            videotitle_pattern = r"video titled(.*?)with this thumbnail"
            ytubevideolist_pattern = r"Go to(.*?)and click"
            #videowatchduration_pattern = r"Watch at-least(.*?)of the video"
            videowatchduration_pattern2 = r"Watch the entire(.*?)of the video"
            # Extract the desired strings using regular expressions
            matches = re.findall(videotitle_pattern, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches = [match.strip() for match in matches]
            # Print the extracted strings
            print("Extracted Video title")
            video_title = ""
            for match in matches:
                print(match)
                if "???" in match:
                    # Replace "???" placeholders with spaces in the second string
                    string2_replaced = match.replace("???", " ")
                    video_title = string2_replaced
                else:
                    string2_replaced = match
                    video_title = string2_replaced

            matches2 = re.findall(ytubevideolist_pattern, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches2 = [match.strip() for match in matches2]
            # Print the extracted strings
            print("Extracted url")
            ytubevideolist_url = ""
            for match in matches2:
                print(match)
                ytubevideolist_url = match
            matches3 = re.findall(videowatchduration_pattern2, instruction, re.DOTALL)
            # Remove leading and trailing whitespace from each match
            matches3 = [match.strip() for match in matches3]
            # Print the extracted strings
            print("Extracted video duration")
            videowatchduration = ""
            for match in matches3:
                print(match)
                videowatchduration = match

        return video_title,ytubevideolist_url,videowatchduration

    def remove_emoji(self,text):
        # Regular expression pattern to match emoji characters
        pattern = r"[^\w\s]|(\?{3,})"

        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002600-\U000027BF"  # miscellaneous symbols
                                   u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                                   u"\U0001F1F2-\U0001F1F4"  # country flags
                                   u"\U0001F1E6-\U0001F1FF"  # flags (other)
                                   "]+", flags=re.UNICODE)
        cleaned_text = re.sub(pattern, "", emoji_pattern.sub(r'', text))
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)
        return cleaned_text



    def perfromYtubewatchtask(self):
        try:

            table_id = self.bot_driver.find_element(By.ID, 'tblBuyReferrals')
            tablebody = table_id.find_element(By.TAG_NAME, "tbody")  # get all of the rows in the table
            tablerows = tablebody.find_elements(By.TAG_NAME, "tr")
            print("No of youtube task:{count}".format(count=len(tablerows)))
            videocomp = False
            skiplist=[]
            for row in tablerows:
                print("Starting a new task.")
                print("#################################")
                time.sleep(self.sleeptime)
                col = row.find_elements(By.TAG_NAME, "td")
                col[1].find_element(By.TAG_NAME, "a").click()
                time.sleep(self.sleeptime)
                campaignid=self.bot_driver.find_element(By.XPATH,'//*[@id="tasks_content_375"]/div[5]/div[2]/div[1]/div[1]/div[1]/p/span').text
                print("Campaign Id:{id}".format(id=campaignid))
                Advertiserid = self.bot_driver.find_element(By.XPATH,
                                                      '//*[@id="tasks_content_375"]/div[5]/div[2]/div[1]/div[1]/div[2]/p/span').text
                print("Advertiser Id:{id}".format(id=Advertiserid))
                print("#################################")
                try:
                    instructions=self.bot_driver.find_element(By.XPATH, '//p[@class="instructions"]')
                #print(instructions.get_attribute('innerHTML'))
                    soup = BeautifulSoup(instructions.get_attribute('innerHTML'), 'html.parser')
                    text_content = soup.get_text()
                    if text_content.strip()=="":
                        text_content="Task expired"
                    time.sleep(self.sleeptime)
                #print(text_content)
                except Exception as e:
                    print(repr(e))
                if (campaignid=="" and Advertiserid=="")  :
                    print("Task Expired")
                    wait = WebDriverWait(self.bot_driver, 5)
                    a_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tasks_content_375"]/div[5]/div[1]/p[2]/span')))
                    a_element.click()

                else:
                    print("###########################################################")
                    print("Start extracting required youtube video information from instructions")
                    time.sleep(self.sleeptime)
                    concatenated_list = self.skiptask_df['campaignid'].astype(str) +"-"+self.skiptask_df[' advertiserid'].astype(str)
                    list_result = concatenated_list.tolist()
                    if (campaignid+"-"+Advertiserid) in list_result:
                        video_title=""
                        url=""
                        duration=""
                    else:
                        category=self.__stringcategorization(text_content)
                        print(">>>>>>>>>>>>>>>"+str(category)+"<<<<<<<<<<<<<<")
                        video_title,url,duration=self.__extractinformation(text_content,category)


                    if video_title != "" and url != "" and duration != "":
                        print("Negotiating Captcha code if present")
                        try:
                            WebDriverWait(self.bot_driver, 5).until(
                                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
                            try:
                                WebDriverWait(self.bot_driver, 5).until(
                                    EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                                alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                                alert.accept()
                                with open(self.basefilepath + "\\youtubeskiptask.csv", 'a', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow(
                                        [datetime.datetime.now().date(), campaignid, Advertiserid])
                                print("Campaign limit reached")
                            except:
                                WebDriverWait(self.bot_driver, 8).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                                self.logger.info("Captcha Code found")
                                time.sleep(60)
                            self.bot_driver.switch_to.parent_frame()

                        except Exception as e:
                            print(repr(e))
                            self.logger.info("No Captcha Code found")
                            self.bot_driver.switch_to.parent_frame()
                            self.bot_driver.find_element(By.XPATH, '//input[@class="btnSubmitCaptcha"]').click()
                            try:
                                WebDriverWait(self.bot_driver, 5).until(
                                    EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                                alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                                alert.accept()

                                print("Campaign limit reached")
                                with open(self.basefilepath + "\\youtubeskiptask.csv", 'a', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow(
                                        [datetime.datetime.now().date(), campaignid, Advertiserid])
                                self.bot_driver.find_element(By.XPATH,
                                                            '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[5]/div[2]/p[1]/a').click()

                            except:
                                print("Campaign limit not reached")
                                time.sleep(self.sleeptime)
                                self.bot_driver.execute_script("window.open('about:blank', '_blank');")
                                self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                                self.bot_driver.get(url)
                                time.sleep(self.sleeptime)
                                content = self.bot_driver.find_element(By.ID, 'contents')
                                videolist = self.bot_driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
                                print(len(videolist))
                                videotitlefound=False

                                for counter in range(len(videolist)):
                                    time.sleep(self.sleeptime)

                                    videotitle=videolist[counter].find_element(By.XPATH, './/*[@id="video-title"]/yt-formatted-string').text
                                    print("########################")
                                    print(self.remove_emoji(video_title))
                                    print(self.remove_emoji(videotitle))
                                    print("########################")

                                    if self.remove_emoji(videotitle).strip()==self.remove_emoji(video_title).strip():
                                        videotitlefound=True
                                        videolist[counter].find_element(By.XPATH, './/*[@id="video-title"]').click()
                                        print(
                                            "sleep time:{sleeptime}".format(sleeptime=(int(duration.split()[0]) * 60) + 7))
                                        time.sleep((int(duration.split()[0]) * 60) + 3)
                                        body = self.bot_driver.find_element_by_css_selector("body")
                                        body.send_keys(Keys.SPACE)
                                        self.bot_driver.save_screenshot(self.dailyyoutubetaskpng)
                                        print("Screenshot taken")
                                        self.logger.info("Screenshot taken")
                                        self.bot_driver.close()
                                        self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                                        self.bot_driver.find_element(By.XPATH,
                                                                    '//*[@id="buyTasksForm"]/div[2]/span/input[2]').click()
                                        time.sleep(self.sleeptime)
                                        pyautogui.write(self.dailyyoutubetaskpng)  # enter file with path
                                        time.sleep(self.sleeptime)
                                        pyautogui.press('enter')
                                        time.sleep(self.sleeptime)
                                        self.bot_driver.find_element(By.XPATH,
                                                                    '//input[@class="btnSubmitForApproval"]').click()
                                        time.sleep(self.sleeptime)
                                        videocomp = True
                                        self.taskregistry_obj.addcompletedtask(1,0.001)
                                        break
                                    elif counter >20:
                                        videotitlefound=False
                                        break
                                if not videotitlefound:
                                    print("Video Title not found!Now closing the windows")
                                    skiplist.append(campaignid + "-" + Advertiserid)
                                    with open(self.basefilepath + "\\youtubeskiptask.csv", 'a', newline='') as csvfile:
                                        writer = csv.writer(csvfile)
                                        writer.writerow(
                                            [datetime.datetime.now().date(), campaignid, Advertiserid])
                                    self.bot_driver.close()
                                    self.bot_driver.switch_to.window(self.bot_driver.window_handles[-1])
                                    self.bot_driver.find_element(By.XPATH,'/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[5]/div[3]/div[7]/form/span[2]/input').click()
                                    time.sleep(self.sleeptime)
                                    try:
                                        WebDriverWait(self.bot_driver, 5).until(
                                            EC.alert_is_present())  # this will wait 5 seconds for alert to appear
                                        alert = self.bot_driver.switch_to.alert  # or self.driver.switch_to_alert() depends on your selenium version
                                        alert.accept()
                                    except:
                                        pass

                    else:
                        print("This Task will be skipped for now as required information is not extracted.")
                        try:
                            self.bot_driver.find_element(By.XPATH,'/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[5]/div[2]/p[1]/a').click()
                        except:
                            pass
                if videocomp:
                    break

        except Exception as e:
            print(repr(e))



