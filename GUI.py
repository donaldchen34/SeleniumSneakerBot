from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Screens.CaptchaScreen import CaptchaScreen, captcha_screen
from Screens.ProxyScreen import ProxyScreen
from Screens.AccountsScreen import AccountsScreen
from Screens.TasksScreen import TasksScreen
from Screens.LogScreen import LogScreen

###Structure
#Database/ File Storage:
# ReadData.py
# FilePaths.py
# CreateDataFiles.py
#
#FrontEnd:
# GUI - Load up the screens
# Screens/* - Folder for all the screens
#   -> TaskScreen contains TaskHandler()
#
#Backend:
# TaskHandler() - is Thread dispatcher for all tasks(TaskThread)
#   -> TaskThread() The separate thread that runs Task()
#       -> Task - calls the separate sites
# CaptchaSolver() - Auto Captcha Handler *** IN THE WORKS(not really) ***
#


#TODO
#Finish TaskHandler -> Add and Delete Tasks()
#Captcha Handling????
#Change the len(getXData()) to a variable in the Screen classes
#Speed up Tensorflow loading -> Delete the resnet50
#Delete Tempfiles -> Located in Appdata/Local/Temp/scoped_*

#### NOW #####
#Learn about cookies
#How are cookies used for captchas
#How to manipulate cookies and bot detection
#Make interaction with site more humanlike
#------------- Maybe do after?
#Log into Gmail for one-click? -> Make a Gmail Trainer?

### Issues ###
# Doing a captcha sucessfully does not save the cookies and will require you to do the captcha again
# -> Not sure if this is due to unsucessful cookie saving or Bot Detection or Ip Ban


## Goal:
# 1. Create a full SneakerBot Model that can run a single task successfully
# 2. Incorporate Better AntiBot Behavior/ Bypass and Include Use of Proxies
# 3. Test and Optimize SneakerBot Model to be more efficient (Speed and Memory wise)
# 4. Add More Site Support
# 5. AutoCaptcha?
# 6. Fully Automate -> Get drop info from Discord Bots and Twitter Bots and create tasks automatically
#                            and Deploy for complete Automation. Deployment is not necessary. Program can be left on
#                            This can also include automating the Gmail Trainer.
# 7. FLUFF STUFF (Pretty GUI, More Features?)

#Steps:
# 1. Captcha Handling
# 2. Cookies
# 3. Basic Bot Detection Bypass
# 4. Delete Captcha from captcha_screen.data when completed
#  *** ALWAYS ***
# 5. Code Cleanup and Documentation (Includes the README and requirements.txt)

class GUI(App):
    def __init__(self):
        super().__init__()

    def build(self):

        self.sm = ScreenManager()
        self.createScreens()


        return self.sm

    def createScreens(self):

        task_screen = TasksScreen(name='tasks')
        accounts_screen = AccountsScreen(name='accounts')
        proxy_screen = ProxyScreen(name='proxy')
        #captcha_screen = CaptchaScreen(name='captcha') #Global variable is used in CaptchaScreen.py
        log_screen = LogScreen(name='log')

        self.sm.add_widget(task_screen)
        self.sm.add_widget(accounts_screen)
        self.sm.add_widget(proxy_screen)
        self.sm.add_widget(captcha_screen)
        self.sm.add_widget(log_screen)


if __name__ == "__main__":

    GUI().run()