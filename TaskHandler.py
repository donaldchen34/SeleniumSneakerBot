from Task import Task
import ReadData
import threading
import datetime
import time
import sys
from Errors import CheckOutError,LoadCaptchaError,ImageError,XPathError, CaptchaError
from TaskThread import TaskThread
import heapq

#TODO
#Make it so webdriver does not popup??
# --> Figure out how to handle captchas
#Incorporate Proxies???
#How to handle large amount of tasks


class TaskHandler(threading.Thread):
    def __init__(self):
        super(TaskHandler, self).__init__()

        self.setDaemon(True)

        self.ThreadManagerQueue = [] #Stores as (Time_left,Priority, Thread_Num, TaskThread)
        self.CaptchaList = [] # Stores as (Thread_Num, Captcha_Link)

        self.MAXTHREADS = 3 #Max amount of threads running at once
        self.ThreadsRunning = 0 #Threads Currently Running
        self.ThreadsAdded = 0 #Total Threads Added to the Thread Manager Queue
        self.loadTasks()

    def run(self):

        while True: #Make this a background processs
            #print("CaptchaList: ", self.CaptchaList)
            #Could make both of them thread classes if more efficient? Not sure tho
            self.ThreadManqagerQueueHandler()
            self.CaptchaListHandler()
            time.sleep(1) #IDK IF NEEDED; IF DO CHANGE TO BE MORE ADAPTIVE

    def join(self):
        pass

    # While loop
    #Run thread
    # When thread reaches captcha
    # -> Post captcha in captcha screens and add to captcalist
    # -> -> Separate loop checking captcha list,
    # -> -> When captcha is done, thread is re-added to threadmanagerqueue with prio 1
    # Thread is ran next in the queue


    def CaptchaListHandler(self):


        pass

    def ThreadManqagerQueueHandler(self):
        # Self.ThreadManagerQueue stores as (Time_left,Priority, Thread_Num, TaskThread)

        while len(self.ThreadManagerQueue) != 0 and self.ThreadsRunning < self.MAXTHREADS:

            thread = heapq.heappop(self.ThreadManagerQueue)
            self.ThreadsRunning += 1
            thread[3].start()


    #Sets up the ThreadManager Queue from the task.json
    def loadTasks(self):

        tasks = self.getTasks()

        print("Amount of tasks:", len(tasks))
        for x,task in enumerate(tasks):

                time_left = self.getSleepTime(int(task[5][:2]),int(task[5][3:]),0)
                t = TaskThread(store=task[0],product_num=task[1],size= task[2],account=task[3],proxy=task[4]
                               ,time=time_left,runTaskFunc=self.runTask,CaptchaList= self.CaptchaList,
                               updateThreadsRunning = self.updateThreadsRunning)

                # Stores as (Time_left,Priority, Thread_Num, TaskThread)
                heapq.heappush(self.ThreadManagerQueue,(time_left,int(task[6]),x,t))

        self.ThreadsAdded = len(self.ThreadManagerQueue)
        print("Size of Queue:", self.ThreadsAdded)
        print("Queue: ", self.ThreadManagerQueue)

    def updateThreadsRunning(self,num):
        self.ThreadsRunning += num

    #Returns the time before a task should be ran
    def getSleepTime(self,tasK_hour,task_minute,task_second):
        """
        :param task_time: String hour:minutes as xx:xx
        :return: time to sleep in seconds
        """
        # Is a bit delayed or ahead
        # Stop a minute ahead and add a while check?
        # Change current_time to not convert to string first

        task_time = datetime.time(tasK_hour, task_minute, task_second)

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S") #Prob dont need to switch to strings, theres prob a method for getting time
        current_time = datetime.time(int(current_time[0:2]), int(current_time[3:5]), int(current_time[7:]))

        date = datetime.date(1, 1, 1)
        task_time = datetime.datetime.combine(date, task_time)
        current_time = datetime.datetime.combine(date, current_time)
        time_left = task_time - current_time

        time_left = time_left.total_seconds() if time_left.total_seconds() > 0 else 0

        return time_left

    #Returns list of tasks
    def getTasks(self):
        tasks = ReadData.getTasksData()

        #For reference:
        #Header/ Fields -  ['Store','Product','Size','Account','Proxy','Time','Priority']

        thread = []
        for task in tasks:
            data = []
            for field in tasks[task]:
                data.append(field['text'])

            thread.append(data)

        return thread

    #Need a better format for time - time is error-bound(prone for errors)
    # Also did not test addTask()
    def addTask(self,store,product_num,size,account,proxy,time,priority,driver= None):

        print("Add")
        print(time)
        time_left = self.getSleepTime(int(time[:2]),int(time[3:]),0) #time is "xx:xx"
        t = TaskThread(store=store,product_num=product_num,size= size,account=account,proxy=proxy
                               ,time=time_left,runTaskFunc=self.runTask,CaptchaList= self.CaptchaList,
                               updateThreadsRunning = self.updateThreadsRunning,driver=driver)

        heapq.heappush(self.ThreadManagerQueue,(time_left,priority,self.ThreadsAdded,t))
        self.ThreadsAdded += 1




    def deleteTask(self):
        print("Delete")

    def runTask(self,store,product_num,size,account,proxy, driver = None):
        #print(store,product_num,size,account,proxy)
        Task(site=store, product_num=product_num, size=size, account=account, proxy=proxy,driver = driver)