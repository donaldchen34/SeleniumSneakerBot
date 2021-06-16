from Task import Task
import ReadData
import threading
import datetime
import time
import sys
from Errors import CheckOutError,CaptchaError,ImageError,XPathError
from TaskThread import TaskThread

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

        tasks = self.getTasks()
        print(tasks)

        #Is this multithreading or multiprocessing
        #Not sure what the correct procedure is for threading and sleeping
        # Main issue: handling large amount of tasks:
        #  -> Most tasks will be of the same thing
        #     -> If different, will probably be around same time
        #
        # Method:
        # -> Run each task on separate thread and then sleep or run depending on time_left
        #    -> May take too much memory for tasks that are just sleeping
        #    -> Still does not handle large amount of tasks
        #    ->
        # or
        # -> Make a queue for when tasks should be run and run tasks in ascending order
        #    -> Still does not handle large amount of tasks
        #    -> May take too much time
        # or
        # Do a combination of both
        # Make a queue for when certain tasks should run and create irrigation method for tasks
        # -> Tasks that run at 12: split up and run ahd Tasks thatn ru at 12:30 will sleep til 12:30


        #Current Method: Run each task on a seperate thread and sleep or run depending on time_left
        threads = []
        for task in tasks:
            try:
                task_time = datetime.time(int(task[5][:2]),int(task[5][3:]),0)

                current_time = datetime.datetime.now()
                current_time = current_time.strftime("%H:%M:%S")
                current_time = datetime.time(int(current_time[0:2]),int(current_time[3:5]),int(current_time[7:]))

                date = datetime.date(1, 1, 1)
                task_time = datetime.datetime.combine(date, task_time)
                current_time = datetime.datetime.combine(date, current_time)
                time_left = task_time - current_time

                print(task_time)
                print(current_time)
                print(time_left)

                #Timer to wait for task to run
                #Is a bit delayed or ahead
                #Stop a minute ahead and add a while check?

                time_left = time_left.total_seconds()

                if time_left > 0:
                    print('waiting for {} seconds'.format(time_left))
                    time.sleep(time_left)
                    print('done sleeping')

                #https://www.geeksforgeeks.org/handling-a-threads-exception-in-the-caller-thread-in-python/
                #https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
                #Create a threading.thread class to overwrite task.start() and task.join()

                #threading.Thread(target=self.runTask, args=(task,)).start()
                #self.runTask(task)
                t = TaskThread(store=task[0],product_num=task[1],size= task[2],account=task[3],proxy=task[4]
                               ,time=task[5],status=task[6],runTaskFunc=self.runTask)
                #threads.join(t,) make a list of info for joining
                threads.append(t)
                t.start()
            except:
                print("WAT")

            for thread in threads:
                thread.join()
            """    
            except (CheckOutError,CaptchaError,ImageError,XPathError) as e: #Known Error
                print("My error :)")
                print(e.message)

                ReadData.addLog([task[0],task[1],task[2],task[3],task[4],
                                 task[5],"Error",e.message])
            except Exception as e: #Unknown Error
                #Todo
                #sys.exc_info()[0] has empty line -> Need to remove for log or keep? because easier to find
                #Remove prints()

                print("Unexpected error:", sys.exc_info()[0])
                print(str(e))
                ReadData.addLog([task[0],task[1],task[2],task[3],task[4],
                                 task[5],"Error",sys.exc_info()[0]])
            else: #Bought
                ReadData.addLog([task[0],task[1],task[2],task[3],task[4],
                                 task[5],"Successful","Bought"])
            """

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