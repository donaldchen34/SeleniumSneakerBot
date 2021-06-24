from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import ReadData
from Screens.ScreenHelper import Alert,createForm, RootWidget,DataCol,DataScreen

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

        account_data = ReadData.getAccountsData()
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

        pos =  (len(ReadData.getAccountsData()) + 1) * self.col_
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

        account_data = ReadData.getAccountsData()
        if account_name in account_data:
            ReadData.deleteAccount(account_name)
            self.setupDataTable()

        else:
            wrong_account = Alert("Account does not exist","Account does not exist")
            wrong_account.open()