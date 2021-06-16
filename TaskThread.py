import threading
from Errors import CheckOutError,CaptchaError,ImageError,XPathError
import sys
import ReadData

#Break down data parameter
#Currently data is [store, product_num, size, accout, proxy, time, status]
class TaskThread(threading.Thread):
    def __init__(self,store,product_num,size,account,proxy,time, status, runTaskFunc):
        super(TaskThread, self).__init__()
        self.store = store
        self.product_num = product_num
        self.size = size
        self.account = account
        self.proxy = proxy
        self.time = time
        self.status = status
        self.func = runTaskFunc
        print(self.func)
        print('test')

    def run(self):
        self.exc = None
        try:
            self.func([self.store,self.product_num,self.size,self.account,self.proxy,self.time,self.status])
        except (CheckOutError, CaptchaError, ImageError, XPathError) as e:  # Known Error
            print("My error :)")
            print(e.message)
            self.exc = e
            ReadData.addLog([self.store, self.product_num, self.size, self.account, self.proxy, self.time, "Error", e.message])

        except Exception as e:  # Unknown Error
            # Todo
            # sys.exc_info()[0] has empty line -> Need to remove for log or keep? because easier to find
            # Remove prints()

            self.exc = e
            print("Unexpected error:", sys.exc_info()[0])
            print(str(e))
            ReadData.addLog([self.store, self.product_num, self.size, self.account, self.proxy, self.time,  "Error", sys.exc_info()[0]])

    def join(self):
        threading.Thread.join(self)
        if self.exc:
            raise self.exc
