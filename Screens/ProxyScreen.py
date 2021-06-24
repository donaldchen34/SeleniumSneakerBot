from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import ReadData
from Screens.ScreenHelper import Alert,createForm,createGridSquare,RootWidget,DataCol,DataScreen

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

        proxy_data = ReadData.getProxyData()
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

        data = ReadData.getProxyData()
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

        account_data = ReadData.getProxyData()
        if proxy_name in account_data:
            ReadData.deleteProxy(proxy_name)
            self.setupDataTable()

        else:
            wrong_account = Alert("Proxy Name does not exist","Proxy Name does not exist")
            wrong_account.open()
