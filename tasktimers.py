import datetime


class tasktimers:
    def __init__(self, basefilepath):
        super(tasktimers, self).__init__()
        print("Task timer Intialized")
    def settimers(self,taskid):
        print("Task Timer for Task")
        current_time = datetime.datetime.now().time()
        start=False
        if taskid in [1,3,4,5,7]:
            start_time = datetime.time(10, 0, 0)
            end_time = datetime.time(21, 59, 0)
            start_time2 = datetime.time(22, 0, 0)
            end_time2 = datetime.time(23,59,0)
            start_time3 = datetime.time(0, 0, 0)
            end_time3 = datetime.time(9, 30, 0)
            if start_time2 <= current_time <= end_time2 or start_time3 <= current_time <= end_time3:
                start=True
            else:
                start= False
        elif taskid in [6,2,0]:
            start_time = datetime.time(9, 35, 0)
            end_time = datetime.time(22, 0, 0)
            print(start_time,current_time,end_time)
            if start_time <= current_time <= end_time:
                start= True
            else:
                start= False
            print("Is task running"+str(start))
        return start



