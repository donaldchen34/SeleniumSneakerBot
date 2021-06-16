from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Screens.Screens import TasksScreen,AccountsScreen,ProxyScreen,LogScreen

###Structure
#Database/ File Storage:
# ReadData.py
# FilePaths.py
# CreateDataFiles.py
#
#FrontEnd:
# GUI
# -> TaskScreen contains TaskHandler()
#   -> TaskHandler() -> is Thread dispatcher for all tasks
#Backend:
# Task -> call the Separate Sites/ Tasks


#TODO
#Finish TaskHandler
#Update Log with Finished Tasks
#Figure out how to run tasks at certain times
#Thread Tasks with each loop
#Different Errors for Log
#Captcha Handling????
#Change the len(getXData()) to a variable in the Screen classes
#Speed up Tensorflow loading

#Steps:
# 1. Log w/ Try & Catch
# 2. Timer
# 3. Thread
# 4. Proxies
# 5. Other Sites


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
        log_screen = LogScreen(name='log')

        self.sm.add_widget(task_screen)
        self.sm.add_widget(accounts_screen)
        self.sm.add_widget(proxy_screen)
        self.sm.add_widget(log_screen)


if __name__ == "__main__":

    GUI().run()