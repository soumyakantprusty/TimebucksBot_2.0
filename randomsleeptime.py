import random


class RandomSleepTime:
    def __init__(self,startnumber,endnumber):
        super(RandomSleepTime, self).__init__()
        self.startnumber=startnumber
        self.endnumber=endnumber
    def getsleeptime(self):
        sleeptime=random.randint(int(self.startnumber), int(self.endnumber))
        return sleeptime