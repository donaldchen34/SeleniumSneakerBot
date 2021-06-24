from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from files.sites import sites #Use either Sites.py or sites.json -> ReadData. getsitesdata()?
import ReadData
from Screens.ScreenHelper import Alert,createForm,createGridSquare,RootWidget,DataCol,DataScreen
from TaskHandler import TaskHandler

#Todo
#Change file.sites to sites.json and get it from ReadData
#Add taskpopup: Better UI
#   -> Choose Size -> Use input instead?
#   -> Choose Store -> Handle a huge amount a stores better -> Issue for later
#Sometimes dropdown does not load still
#Fix dimensions and picture of buttons

class TasksScreen(Screen):

    def __init__(self,**kwargs):
        super(TasksScreen,self).__init__(**kwargs)
        root = RootWidget()


        self.TaskHandler = TaskHandler()
        self.TaskHandler.start()

        self.DEFAULT_SIZE_ = 105 #Make this more global -> It is also used in Accounts Screen
        self.data_table = DataScreen()
        self.col_ = 7

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Label'

        self.setupDataTable()

        root.add_widget(self.data_table)
        root.add_widget(self.createButtons())

        self.add_widget(root)

    #Converts files/task.json into a list of text for table data
    def getData(self):

        task_data = ReadData.getTasksData()
        data = []
        for task in task_data:
            for field in task_data[task]:
                data.append(field)

        return data

    #Creates the data for DataScreen.data
    def setupDataTable(self):

        #Header - For reference
        FIELDS = ['Store','Product','Size','Account','Proxy','Time','Priority']

        data = []
        for field in FIELDS: #Header
            data.append({"text": field})

        data.extend(self.getData())

        if len(data) < self.DEFAULT_SIZE_:
            data.extend([{"text":""} for i in range(self.DEFAULT_SIZE_-len(data))])

        self.data_table.data = data

    #Creates the boxlayout with a plus and minus button
    def createButtons(self):
        """
        :return: returns  a boxlayout with the plus and minus button
        """
        #Butons
        buttons = BoxLayout()
        buttons.size_hint = 1,.15

        #Filler
        filler = BoxLayout()

        #Add Button
        add_button = Button(background_normal='files/Pictures/plussign.png')
        add_button.border = (30,30,30,30)
        add_button.size_hint_x = .25

        add_button.bind(on_press=self.addTaskPopup)

        #Minus Button
        minus_button = Button(background_normal='files/Pictures/minussign.png')
        minus_button.border = (30,30,30,30)
        minus_button.size_hint_x = .25

        minus_button.bind(on_press= self.deleteTaskPopup)


        buttons.add_widget(add_button)
        buttons.add_widget(filler)
        buttons.add_widget(minus_button)

        return buttons

    #Creates the popup to enter information for the new task
    def addTaskPopup(self,instance):
        """
        :param instance: represents the add task button(not used)
        :return: Either returning the task or just populates the data table and returns nothing or return true/false
        Todo
        Buttons stop working sometimes
        Fix General UI -> Make prettier and more dynamic
        Add data into empty grid is janky
        """


        task_popup = Popup()
        task_popup.size_hint = 0.5,0.5
        task_popup.title = "Add Task"

        task_root = BoxLayout()
        task_root.orientation = 'vertical'

        #Contents of task_popup
        task_info = GridLayout()
        task_info.cols = 2

        #Stores
        stores,stores_dropdown,stores_dropdown_text = createGridSquare(sites,'Store')
        task_info.add_widget(stores)

        #Product
        product,product_text = createForm("Product Num")
        task_info.add_widget(product)

        #Size
        SUPPORTEDSIZES= ['XS','S','M','L','XL','XXL',
                         '6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5',
                         '10.0','10.5','11.0','11.5','12.0']

        sizes,sizes_dropdown,sizes_dropdown_text = createGridSquare(SUPPORTEDSIZES,'Size')
        task_info.add_widget(sizes)

        #Account
        accounts,accounts_dropdown,accounts_dropdown_text = createGridSquare(ReadData.getAccountsData(),'Accounts')
        task_info.add_widget(accounts)

        #Proxy
        proxies,proxies_dropdown,proxies_dropdown_text = createGridSquare(ReadData.getProxyData(),'Proxies')
        task_info.add_widget(proxies)

        #Time
        time,time_text = createForm("Time, Enter 00:00 - 23:59")
        task_info.add_widget(time)

        #Confirm Button
        confirm = Button(text='Confirm')
        confirm.bind(on_press = lambda x:
                self.addTask(x,stores_dropdown_text.text,product_text.text,sizes_dropdown_text.text,
                                   accounts_dropdown_text.text,proxies_dropdown_text.text,time_text.text))
        confirm.bind(on_press = task_popup.dismiss)
        confirm.size_hint_y = .15


        task_root.add_widget(task_info)
        task_root.add_widget(confirm)

        task_popup.content = task_root
        task_popup.open()

    #Update/Adds new task
    def addTask(self,instance,store,product,size,account,proxy,time):

        data = [store,product,size,account,proxy,time,'Standby']
        pos =  (len(ReadData.getTasksData()) + 1) * self.col_

        if pos < self.DEFAULT_SIZE_:
            for x in data:
                self.data_table.data[pos]['text'] = x
                pos += 1

        else:
            for x in data:
                self.data_table.data.append({'text':x})

        self.TaskHandler.addTask(store=data[0],product=data[1],size=data[2],account=data[3],
                                 proxy=data[4],time=data[5])

        #Convert data to correct data structure to be saved
        new_data = []
        for x in data:
            new_data.append({"text":x})

        ReadData.addTasksData(new_data)
        self.data_table.refresh_from_data()

    #Creates the popup to ask what task to delete
    def deleteTaskPopup(self,instance):
        delete_popup = Popup()
        delete_popup.size_hint = 0.35,0.35
        delete_popup.title = "Delete Task"

        delete_root = BoxLayout()
        delete_root.orientation = 'vertical'

        delete_text = Label(text="What task number to delete")
        delete_input = TextInput()
        delete_input.multiline = False

        delete_button = Button(text = "Confirm")
        delete_button.bind(on_press = lambda x: self.deleteTask(delete_input.text))
        delete_button.bind(on_press = delete_popup.dismiss)


        delete_root.add_widget(delete_text)
        delete_root.add_widget(delete_input)
        delete_root.add_widget(delete_button)

        delete_popup.content = delete_root
        delete_popup.open()

    #Deletes task
    def deleteTask(self,row):
        if row.isnumeric():
            row = int(row)

            size = len(ReadData.getTasksData())
            if size >= row and row != 0:
                for i in range(self.col_):
                    self.data_table.data.pop((row) * self.col_)
                    self.data_table.data.append({'text':''})

                self.TaskHandler.deleteTask()

                new_data = {}
                data = []
                for x,field in enumerate(self.data_table.data[self.col_:]):
                    if x > (size -  1) * self.col_:
                        break
                    data.append(field)
                    if x % 7 == 6:
                        new_data[len(new_data)] = data
                        data = []

                ReadData.setTasksData(new_data)

            else:
                wrong_input = Alert("You have {} tasks".format(size),"Unknown Task")
                wrong_input.open()
        else:
            wrong_input = Alert("Enter the task number","Not a valid Number")
            wrong_input.open()
