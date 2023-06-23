import logging
import threading
import time
class statusfileupdater:
    def __init__(self, taskname, basepath):
        super(statusfileupdater, self).__init__()
        self.portal=taskname
        self.basefilepath=basepath
        self.stop_event = threading.Event()
        self.is_running = True
        logging.basicConfig(filename=self.basefilepath + "//bot.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def run(self):
        while self.is_running:
            # Perform the file update here
            self.logger.info("Bot is still looking at:{videoportal}".format(videoportal=self.portal))
            time.sleep(60)  # Sleep for 3 minutes (180 seconds)

    def stop(self):
        self.is_running = False
