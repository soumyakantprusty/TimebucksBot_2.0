import logging
import time
import random

#from botwebdriver import botwebdriver
from botwendriver_chrome import botwebdriver

class clearunwantedtabs:
    def __init__(self,bot_webdriver,basefilepath):
        super(clearunwantedtabs, self).__init__()
        self.bot_driver=bot_webdriver
        self.basefilepath=basefilepath
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        print(self.bot_driver.window_handles)
        self.parent_handle = self.bot_driver.window_handles[0]
        if len(self.bot_driver.window_handles)>1:
            for index,value in enumerate(self.bot_driver.window_handles):
                if value !=self.parent_handle:
                    self.bot_driver.switch_to.window(value)
                    self.bot_driver.close()
                    self.bot_driver.switch_to.window(self.parent_handle)
        else:
            print("No Child tab found")


    def close(self):
        # Cleanup tasks
        self.close()
