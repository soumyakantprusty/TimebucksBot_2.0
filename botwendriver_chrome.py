import logging
import os
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver



class botwebdriver:
    def __init__(self, bot_port,basepath):
        super(botwebdriver, self).__init__()
        self.bot_port = bot_port
        self.basefilepath=basepath
        self.curentuser = os.getlogin()
        self.profilearguments = "user-data-dir=C:\\Users\\" + self.curentuser + "\\AppData\Local\\Microsoft\\Edge\\User Data\\Default\\"
        self.webdriverpath = "C:\\Users\\" + self.curentuser + "\\Documents\\TimeBucksBots\\chromedriver_win32\\chromedriver.exe"
        self.timebucksurl="https://timebucks.com/publishers/index.php?pg=dashboard"
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        print("Closing all old webdriver instances")
        os.system("taskkill /F /IM chromedriver.exe")
        print("Initiating selenenium webdriver Options")
        self.options = Options()
        self.prefs = {"credentials_enable_service": False,
                      "profile.password_manager_enabled": False}

    def startwebdriver(self):
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--port=12345')
        self.options.add_argument("--start-maximized")
        self.options.add_argument(self.profilearguments)
        self.options.use_chromium = True
        self.debuggerAddress = "127.0.0.1:" + self.bot_port
        print(self.debuggerAddress)
        self.options.add_experimental_option("debuggerAddress", self.debuggerAddress)
        self.driver_timesbuck = webdriver.Chrome(executable_path=self.webdriverpath, options=self.options)
            # self.driver_timesbuck = webdriver.Edge(executable_path="C:\\Users\\sam\\Documents\\TimeBucksBots\\edgedriver_win32\\msedgedriver.exe",options=self.options)
        print("Successfully Initiated selenenium webdriver Options")
        time.sleep(1)
        print("Successfully started selenenium webdriver")
        return self.driver_timesbuck

    def quitwebdriver(self):
        self.driver_timesbuck.quit()
