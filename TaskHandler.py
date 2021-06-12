from Task import Task
import ReadData
import threading
import time
import sys
from Errors import CheckOutError,CaptchaError,ImageError,XPathError

#TODO
#Change tasks into threads
#Make it so webdriver does not popup??
# --> Figure out how to handle captchas
#Thread everything
# -> Thread the GUI with the TaskHandler -> ASYNCH
#Add timer for tasks to run at X time
#INCORPORATE LOGS
# -> Log the try/catch 
#Finish AddLog and add somewhere
#Incorporate Proxies???



class TaskHandler:
    def __init__(self):

        threads = self.getTasks()
        print(threads)

        for thread in threads:
            try:
                self.runTask(thread)
            except (CheckOutError,CaptchaError,ImageError,XPathError) as e: #Known Error
                print("My error :)")
                print(e.message)

                ReadData.addLog([thread[0],thread[1],thread[2],thread[3],thread[4],
                                 thread[5],"Error",e.message])
            except Exception as e: #Unknown Error
                print("Unexpected error:", sys.exc_info()[0])
                print(str(e))
                ReadData.addLog([thread[0],thread[1],thread[2],thread[3],thread[4],
                                 thread[5],"Error",sys.exc_info()[0]])
            else: #Bought
                ReadData.addLog([thread[0],thread[1],thread[2],thread[3],thread[4],
                                 thread[5],"Successful","Bought"])

    def getTasks(self):
        tasks = ReadData.getTasksData()

        #For reference:
        #Header/ Fields -  ['Store','Product','Size','Account','Proxy','Time','Status']

        thread = []
        for task in tasks:
            data = []
            for field in tasks[task]:
                data.append(field['text'])

            thread.append(data)

        return thread

    def addTask(self):
        print("Add")

    def deleteTask(self):
        print("Delete")

    def createThread(self):
        pass

    def runTask(self,data):

        store = data[0]
        product_num = data[1]
        size = data[2]
        account = data[3]
        proxy = data[4]
        time = data[5]
        status = data[6]


        Task(store,product_num,size,account,proxy)