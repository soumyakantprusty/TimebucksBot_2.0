import datetime


class tasktimers:
    def __init__(self, basefilepath):
        super(tasktimers, self).__init__()
    def settimers(self,taskid):
        current_time = datetime.datetime.now().time()
        start=False
        if taskid in range(5):
            start_time = datetime.time(0, 0, 0)
            end_time = datetime.time(23, 0, 0)
            start_time2 = datetime.time(0, 0, 0)
            end_time2 = datetime.time(23, 0, 0)
            if start_time <= current_time <= end_time or start_time2 <= current_time <end_time2:
                start=True
            else:
                start= False
        elif taskid==5:
            start_time = datetime.time(5, 0, 0)
            end_time = datetime.time(9, 0, 0)
            if start_time <= current_time <= end_time:
                start= True
            else:
                start= False
            print(start)
        return start



