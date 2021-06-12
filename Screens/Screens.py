from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from files.sites import sites #Use either Sites.py or sites.json
from ReadData import getAccountsData, getProxyData, getTasksData #Change to just ReadData
import ReadData
from Screens.ScreenHelper import Alert,createForm,createGridSquare,RootWidget,DataCol,DataScreen
from TaskHandler import TaskHandler

#Split into different files?

class TasksScreen(Screen):

    def __init__(self,**kwargs):
        super(TasksScreen,self).__init__(**kwargs)
        root = RootWidget()

        self.TaskHandler = TaskHandler()

        self.DEFAULT_SIZE_ = 105 #Make this more global -> It is also used in Accounts Screen
        self.data_table = DataScreen()
        self.col_ = 7

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Label'

        self.setupDataTable()
        #self.data_table.data = self.getData()

        root.add_widget(self.data_table)
        root.add_widget(self.createButtons())

        self.add_widget(root)

    #Converts files/task.json into a list of text for table data
    def getData(self):

        task_data = getTasksData()
        data = []
        for task in task_data:
            for field in task_data[task]:
                data.append(field)

        return data

    #Creates the data for DataScreen.data
    def setupDataTable(self):

        #Header - For reference
        FIELDS = ['Store','Product','Size','Account','Proxy','Time','Status']

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
        #Fix dimensions and picture
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
        accounts,accounts_dropdown,accounts_dropdown_text = createGridSquare(getAccountsData(),'Accounts')
        task_info.add_widget(accounts)

        #Proxy
        proxies,proxies_dropdown,proxies_dropdown_text = createGridSquare(getProxyData(),'Proxies')
        task_info.add_widget(proxies)

        #Time
        time,time_text = createForm("Time")
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
        pos =  (len(getTasksData()) + 1) * self.col_

        if pos < self.DEFAULT_SIZE_:
            for x in data:
                self.data_table.data[pos]['text'] = x
                pos += 1

        else:
            for x in data:
                self.data_table.data.append({'text':x})

        self.TaskHandler.addTask()

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

            size = len(getTasksData())
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


class AccountsScreen(Screen):
    def __init__(self,**kwargs):
        super(AccountsScreen,self).__init__(**kwargs)
        root = RootWidget()

        self.DEFAULT_SIZE_ = 105
        self.data_table = DataScreen()
        self.col_ = 5

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Label'

        self.setupDataTable()

        root.add_widget(self.data_table)
        root.add_widget(self.createButtons())

        self.add_widget(root)

    #Saves new account to files/accounts.json
    def saveData(self,account_name,first_name,last_name,email,phone,
                   street,apt_num,zip_code,city,state,card_number,mm,yy,csc):

        data = {}
        data["first_name"] = first_name
        data["last_name"] = last_name
        data["email"] = email
        data["phone"] = phone
        data["address"] = {
            "street":street,
            "apt" : apt_num,
            "zip_code" : zip_code,
            "city" : city,
            "state": state
        }
        data["payment"] = {
            "card_number" : card_number,
            "mm" : mm,
            "yy" : yy,
            "csc" : csc
        }

        ReadData.addAccount(account_name,data)

    #Gets text info for data_screen.data- Retrieves account_name,first,last,email,card_num[-4:]
    def getData(self):

        account_data = getAccountsData()
        data = []
        for account in account_data:
            data.append({"text": account})
            data.append({"text": account_data[account]["first_name"]})
            data.append({"text": account_data[account]["last_name"]})
            data.append({"text": account_data[account]["email"]})
            data.append({"text": account_data[account]["payment"]["card_number"][-4:]})

        return data

    #Creates the data for DataScreen.data
    def setupDataTable(self):

        #Header - For reference
        FIELDS = ['Account Name','First','Last','Email','Card_Number']

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
        #Fix dimensions and picture
        add_button = Button(background_normal='files/Pictures/plussign.png')
        add_button.border = (30,30,30,30)
        add_button.size_hint_x = .25

        add_button.bind(on_press=self.addAccountPopup)

        #Minus Button
        minus_button = Button(background_normal='files/Pictures/minussign.png')
        minus_button.border = (30,30,30,30)
        minus_button.size_hint_x = .25

        minus_button.bind(on_press= self.deleteAccountPopup)


        buttons.add_widget(add_button)
        buttons.add_widget(filler)
        buttons.add_widget(minus_button)

        return buttons

    #Creates the popup to enter information for the new Account
    def addAccountPopup(self,instance):
        """
        :param instance: represents the add task button(not used)
        :return: Either returning the task or just populates the data table and returns nothing or return true/false
        """

        account_popup = Popup()
        account_popup.size_hint = 0.5,0.75
        account_popup.title = "Add Account"

        account_root = BoxLayout()
        account_root.orientation = 'vertical'

        #Contents of account_popup
        account_info = GridLayout()
        account_info.cols = 3

        account,account_text = createForm("Account Name")
        account_info.add_widget(account)

        first_name, first_name_text = createForm("First Name")
        account_info.add_widget(first_name)

        last_name, last_name_text = createForm("Last Name")
        account_info.add_widget(last_name)

        email, email_text = createForm("Email")
        account_info.add_widget(email)

        phone, phone_text = createForm("Phone Number")
        account_info.add_widget(phone)

        #Address
        street, street_text = createForm("Street")
        account_info.add_widget(street)

        apt, apt_text = createForm("Apartment Number")
        account_info.add_widget(apt)

        zip_code, zip_code_text = createForm("ZipCode")
        account_info.add_widget(zip_code)

        city, city_text = createForm("City")
        account_info.add_widget(city)

        state, state_text = createForm("State")
        account_info.add_widget(state)

        #Payment
        card_number, card_number_text = createForm("Card Number")
        account_info.add_widget(card_number)

        month, month_text = createForm("Expiry Month")
        account_info.add_widget(month)

        year, year_text = createForm("Expiry Year")
        account_info.add_widget(year)

        csc, csc_text = createForm("CSC")
        account_info.add_widget(csc)


        #Confirm Button
        confirm = Button(text='Confirm')
        confirm.bind(on_press = lambda x:
                self.addAccount(x,account_text.text,first_name_text.text,last_name_text.text,
                                   email_text.text,phone_text.text,street_text.text,apt_text.text,
                                zip_code_text.text,city_text.text,state_text.text,card_number_text.text,
                                month_text.text,year_text.text,csc_text.text))
        confirm.bind(on_press = account_popup.dismiss)
        confirm.size_hint_y = .15


        account_root.add_widget(account_info)
        account_root.add_widget(confirm)

        account_popup.content = account_root
        account_popup.open()

    #Update data_screen.data and calls saveData() to save account to accounts.json
    #Fix parameters :(
    def addAccount(self,instance,account_name,first_name,last_name,email,phone,
                   street,apt_num,zip_code,city,state,card_number,mm,yy,csc):

        data = [account_name,first_name,last_name,email,card_number[-4:]]

        pos =  (len(getAccountsData()) + 1) * self.col_
        if pos < self.DEFAULT_SIZE_:
            for x in data:
                self.data_table.data[pos]['text'] = x
                pos += 1
        else:
            for x in data:
                self.data_table.data.append({'text':x})

        self.saveData(account_name,first_name,last_name,email,phone,
                   street,apt_num,zip_code,city,state,card_number,mm,yy,csc)

        self.data_table.refresh_from_data()

    #Creates the popup to ask what task to delete
    def deleteAccountPopup(self,instance):
        delete_popup = Popup()
        delete_popup.size_hint = 0.35,0.35
        delete_popup.title = "Delete Task"

        delete_root = BoxLayout()
        delete_root.orientation = 'vertical'

        delete_text = Label(text="Which Account to delete (Case Sensitive)")
        delete_input = TextInput()
        delete_input.multiline = False

        delete_button = Button(text = "Confirm")
        delete_button.bind(on_press = lambda x: self.deleteAccount(delete_input.text))
        delete_button.bind(on_press = delete_popup.dismiss)


        delete_root.add_widget(delete_text)
        delete_root.add_widget(delete_input)
        delete_root.add_widget(delete_button)

        delete_popup.content = delete_root
        delete_popup.open()

    #Deletes account
    def deleteAccount(self,account_name):

        account_data = getAccountsData()
        if account_name in account_data:
            ReadData.deleteAccount(account_name)
            self.setupDataTable()

        else:
            wrong_account = Alert("Account does not exist","Account does not exist")
            wrong_account.open()


class ProxyScreen(Screen):
    def __init__(self,**kwargs):
        super(ProxyScreen,self).__init__(**kwargs)
        root = RootWidget()

        self.DEFAULT_ROWS_ = 30
        self.data_table = DataScreen()
        self.col_ = 2

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Label'

        self.setupDataTable()

        root.add_widget(self.data_table)
        root.add_widget(self.createButtons())

        self.add_widget(root)

    #Gets text info for data_screen.data- Retrieves account_name,first,last,email,card_num[-4:]
    def getData(self):

        proxy_data = getProxyData()
        data = []
        for proxy in proxy_data:
            data.append({"text": proxy})
            data.append({"text": proxy_data[proxy]["IP"]})

        return data

    #Creates the data for DataScreen.data
    def setupDataTable(self):

        #Header - For reference
        FIELDS = ['Proxy Name','IP']

        data = []
        for field in FIELDS: #Header
            data.append({"text": field})

        data.extend(self.getData())

        if len(data) / self.col_ < self.DEFAULT_ROWS_:
            data.extend([{"text":""} for i in range(self.DEFAULT_ROWS_ * self.col_ - len(data))])

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
        #Fix dimensions and picture
        add_button = Button(background_normal='files/Pictures/plussign.png')
        add_button.border = (30,30,30,30)
        add_button.size_hint_x = .25

        add_button.bind(on_press=self.addProxyPopup)

        #Minus Button
        minus_button = Button(background_normal='files/Pictures/minussign.png')
        minus_button.border = (30,30,30,30)
        minus_button.size_hint_x = .25

        minus_button.bind(on_press= self.deleteProxyPopup)


        buttons.add_widget(add_button)
        buttons.add_widget(filler)
        buttons.add_widget(minus_button)

        return buttons

    #Creates the popup to enter information for the new Account
    def addProxyPopup(self,instance):
        """
        :param instance: represents the add task button(not used)
        """

        proxy_popup = Popup()
        proxy_popup.size_hint = 0.5,0.5
        proxy_popup.title = "Add Proxy"

        proxy_root = BoxLayout()
        proxy_root.orientation = 'vertical'

        #Contents of account_popup
        proxy_name,proxy_name_text = createForm("Proxy name")
        proxy_ip,proxy_ip_text = createForm("IP Address")


        #Confirm Button
        confirm = Button(text='Confirm')
        confirm.bind(on_press = lambda x:
                self.addProxy(x,proxy_name_text.text,proxy_ip_text.text))
        confirm.bind(on_press = proxy_popup.dismiss)
        confirm.size_hint_y =.5


        proxy_root.add_widget(proxy_name)
        proxy_root.add_widget(proxy_ip)
        proxy_root.add_widget(confirm)

        proxy_popup.content = proxy_root
        proxy_popup.open()

    #Update data_screen.data and calls saveData() to save account to proxy.json
    def addProxy(self,instance,name,ip):

        data = getProxyData()
        if name in data:
            wrong_input = Alert("Name is already used","Name is already used")
            wrong_input.open()
        else:
            pos = len(data) + 1
            if pos < self.DEFAULT_ROWS_:
                pos = pos * 2
                for x in [name,ip]:
                    self.data_table.data[pos]['text'] = x
                    pos += 1
            else:
                for x in [name,ip]:
                    self.data_table.data.append({'text':x})

            ReadData.addProxy(name,ip)

            self.data_table.refresh_from_data()

    #Creates the popup to ask what task to delete
    def deleteProxyPopup(self,instance):
        delete_popup = Popup()
        delete_popup.size_hint = 0.35,0.35
        delete_popup.title = "Delete Proxy"

        delete_root = BoxLayout()
        delete_root.orientation = 'vertical'

        delete_text = Label(text="Which Proxy to delete (Case Sensitive)")
        delete_input = TextInput()
        delete_input.multiline = False

        delete_button = Button(text = "Confirm")
        delete_button.bind(on_press = lambda x: self.deleteProxy(delete_input.text))
        delete_button.bind(on_press = delete_popup.dismiss)


        delete_root.add_widget(delete_text)
        delete_root.add_widget(delete_input)
        delete_root.add_widget(delete_button)

        delete_popup.content = delete_root
        delete_popup.open()

    #Deletes Proxy
    def deleteProxy(self,proxy_name):

        account_data = getProxyData()
        if proxy_name in account_data:
            ReadData.deleteProxy(proxy_name)
            self.setupDataTable()

        else:
            wrong_account = Alert("Proxy Name does not exist","Proxy Name does not exist")
            wrong_account.open()


class LogScreen(Screen):
    def __init__(self, **kwargs):
        super(LogScreen, self).__init__(**kwargs)
        root = RootWidget()

        self.DEFAULT_ROWS_ = 20
        self.data_table = DataScreen()
        fields, data = ReadData.getLogData(self.DEFAULT_ROWS_)
        self.col_ = len(fields)

        setup = DataCol()
        setup.cols = self.col_

        self.data_table.add_widget(setup)
        self.data_table.viewclass = 'Label'

        self.setupDataTable(fields,data)

        root.add_widget(self.data_table)

        self.add_widget(root)

    #Creates the data for DataScreen.data
    def setupDataTable(self, fields, log_data):

        #Header - For reference
        #FIELDS = ['Store', 'Product', 'Size', 'Account', 'Proxy', 'Status', 'Comment']

        table_data = []
        for field in fields:
            table_data.append({"text":field})

        for data in log_data:
            for field in data:
                table_data.append({"text":field})

        if len(table_data) < self.DEFAULT_ROWS_ * self.col_:
            table_data.extend([{"text":""} for i in range((self.DEFAULT_ROWS_ * self.col_) - len(table_data))])

        self.data_table.data = table_data

