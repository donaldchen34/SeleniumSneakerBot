import threading
from Errors import CheckOutError,LoadCaptchaError,ImageError,XPathError, CaptchaError
import sys
import ReadData
import time
import Task
from Screens.CaptchaScreen import captcha_screen

# Todo
# Remove prints after testing is finished
# Remove join()?
# Add locks to CaptchaList, ThreadsRunning

class TaskThread(threading.Thread):
    def __init__(self,store,product_num,size,account,proxy,time, runTaskFunc, CaptchaList, updateThreadsRunning, driver = None):
        super(TaskThread, self).__init__()

        self.store = store
        self.product_num = product_num
        self.size = size
        self.account = account
        self.proxy = proxy
        self.sleep_time = time
        self.func = runTaskFunc
        self.CaptchaList = CaptchaList
        self.updateThreadsRunning = updateThreadsRunning
        self.driver = driver

        self.setDaemon(True) #Don't know if this matters
        self.attempts = 2 #Amount of times to try

    def run(self):
        self.exc = None
        time.sleep(self.sleep_time)
        for i in range(self.attempts):
            try:
                self.func(store=self.store, product_num=self.product_num, size=self.size,
                          account=self.account, proxy=self.proxy, driver = self.driver )
            except CaptchaError as e:
                print("Waiting for Captcha")
                print(e.link)
                #Ideally it would pause the threadand then run again
                #Currently adds to CaptchaScreen.data to be done
                #Will open a new driver to open captcha link
                #and then closes that driver adds back to queue
                # to be reran again with the new driver
                captcha_screen.addCaptcha(link=e.link,store=self.store,product_num = self.product_num,
                                          size=self.size, account=self.account, proxy=self.proxy, driver = e.driver)
                self.CaptchaList.append((len(self.CaptchaList))) #Add things needed to runTask func
                self.updateThreadsRunning(-1)

                break

            #Remove Errors
            #Check CaptchaList

            except (CheckOutError, LoadCaptchaError, ImageError, XPathError) as e:  # Known Error
                print("My error :)")
                self.exc = e
                ReadData.addLog([self.store, self.product_num, self.size, self.account, self.proxy, "Error", e.message])

            except Exception as e:  # Unknown Error

                self.exc = e
                print("Unexpected error:", sys.exc_info()[0])
                print("Unexpected error:", sys.exc_info())

                ReadData.addLog([self.store, self.product_num, self.size, self.account, self.proxy, "Error", sys.exc_info()[0]])
            else: #Worked
                ReadData.addLog([self.store, self.product_num, self.size, self.account, self.proxy, "Successful", "Bought"])
                break

    #Don't think i'mma use this
    #Join pauses the program
    # -> Need to separate TaskHandler into separate thread if i want to use
    # -> Also not sure how to add new tasks with TaskHandler on hold
    def join(self):
        threading.Thread.join(self)
        if self.exc:
            raise self.exc

    """
    def runTask(self,store,product_num,size,account,proxy):
        #print(store,product_num,size,account,proxy)
        Task(site=store, product_num=product_num, size=size, account=account, proxy=proxy)
    """
