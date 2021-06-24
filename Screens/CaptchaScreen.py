from kivy.uix.screenmanager import Screen
from Screens.ScreenHelper import RootWidget,DataCol,DataScreen
import time
from selenium import webdriver
from FilePaths import FIREFOX_WEB_DRIVER_PATH

#Todo
#Created global variable "captcha_screen" to load captchas into the screen
#Need to find a better way to this

class CaptchaScreen(Screen):
    def __init__(self,**kwargs):
        super(CaptchaScreen,self).__init__(**kwargs)
        root = RootWidget()

        self.DEFAULT_ROWS_ = 20 #Make this more global -> It is also used in Accounts Screen
        self.data_table = DataScreen()
        self.col_ = 1
        self.captchas = 0

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Button'

        self.setupDataTable()
        #self.data_table.data = self.getData()

        root.add_widget(self.data_table)

        self.add_widget(root)

    #Creates the data for DataScreen.data
    def setupDataTable(self):

        data = [{"text":"Captchas"}]
        data.extend([{"text":""} for i in range(self.DEFAULT_ROWS_ - len(data))])

        self.data_table.data = data


    #Update/Adds new task
    def addCaptcha(self,link,store, product_num, size, account, proxy, driver):

        print("ADDD")
        self.captchas += 1
        self.data_table.data[self.captchas] = {'text': "Click Me!",
                                               'on_press': lambda: self.CaptchaHandler(link,store, product_num, size, account, proxy, driver)                                     }


        self.data_table.refresh_from_data()

    ### COOKIES ###
    # https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver
    # https://www.bureauserv.com.au/blog/captcha-cookies-data-security/
    # https://stackoverflow.com/questions/58872451/how-can-i-bypass-the-google-captcha-with-selenium-and-python
    # https://stackoverflow.com/questions/55501524/how-does-recaptcha-3-know-im-using-selenium-chromedriver/55502835#55502835

    #Change time.sleep
    def CaptchaHandler(self,link, store, product_num, size, account, proxy, driver):

        #Open Site
        driver.get(link)

        #Wait for captcha to be done
        while (not self.errorCheck(driver)):
            time.sleep(2)


        #driver.close()

        #Add task back to queue
        self.parent.get_screen('tasks').TaskHandler.addTask(store=store,product_num = product_num, size=size,
                                                    account=account, proxy=proxy, time = "00:00", driver = driver, priority = 1)



    def errorCheck(self, driver):
        try:
            driver.find_element_by_xpath('/html/body/h1')
            return True
        except:
            return False

    #Deletes task
    def deleteTask(self,row):
        #Done animation -> then remove
        pass


captcha_screen = CaptchaScreen(name = 'captcha')