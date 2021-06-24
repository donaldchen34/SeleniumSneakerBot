from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.recyclegridlayout import RecycleGridLayout
import webbrowser

#Root Box Layout for screens - Contains a toolbar
class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(ToolBar())

#Toolbar with buttons
class ToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolBar, self).__init__(**kwargs)

        height = .15
        self.size_hint = (1,height)
        self.orientation = 'horizontal'

        tasks = Button(text='Tasks')
        tasks.bind(on_press = self.tasksButton)
        self.add_widget(tasks)

        accounts = Button(text="Accounts")
        accounts.bind(on_press = self.accountsButton)
        self.add_widget(accounts)

        proxy = Button(text="Proxies")
        proxy.bind(on_press = self.proxyButton)
        self.add_widget(proxy)

        captcha = Button(text="Captchas")
        captcha.bind(on_press = self.captchaButton)
        self.add_widget(captcha)

        log = Button(text="Log")
        log .bind(on_press = self.logButton)
        self.add_widget(log)

    def tasksButton(self,instance):
        instance.parent.parent.parent.parent.current = "tasks"

    def accountsButton(self, instance):
        instance.parent.parent.parent.parent.current = "accounts"

    def proxyButton(self, instance):
        instance.parent.parent.parent.parent.current = "proxy"

    def captchaButton(self, instance):
        instance.parent.parent.parent.parent.current = "captcha"

    def logButton(self, instance):
        instance.parent.parent.parent.parent.current = "log"

#https://stackoverflow.com/questions/48287204/recycleview-module-in-kivy
class DataScreen(RecycleView):
    def __init__(self,**kwargs):
        super(DataScreen,self).__init__(**kwargs)

class DataCol(RecycleGridLayout):
    def __init__(self,**kwargs):
        super(DataCol,self).__init__(**kwargs)
        self.default_size_hint = 1,1
        self.size_hint_y = None
        self.size_hint_x = 1
        #Not sure how to setup maximum height/ a set height for Grid layout
        #self.height = int(Window.height/5)
        self.row_default_height = 75
        self.height = 1500


#Use to create the popups to ask for information
def createGridSquare(data,label):
    """
    :param data: List,Set or Dict of data
    :param label: Label for the data (String)
    :return: Returns a BoxLayout with a label on top and a dropdown on the bottom and the dropdown
    """
    square = BoxLayout()
    square.orientation = 'vertical'

    dropdown_label = Label(text=label)
    #dropdown = createDropDown(data, label)



    dropdown = TaskDropDown(data,label)

    dropdown_btn = Button(text=label, size_hint=(None, None))
    dropdown_btn.bind(on_release=dropdown.open)
    dropdown.bind(on_select=lambda instance, x: setattr(dropdown_btn, 'text', x))

    square.add_widget(dropdown_label)
    square.add_widget(dropdown_btn)

    return square,dropdown,dropdown_btn

#Create a form with a label on top of it
def createForm(label):
    """
    :param label: name that represents the form (String)
    :return: returns Form with a label on top of it and the text_input
    """
    form = BoxLayout()
    form.orientation = 'vertical'

    form_label = Label(text=label)
    text_input = TextInput(multiline=False)

    form.add_widget(form_label)
    form.add_widget(text_input)

    return form, text_input

#Create a dropdown with the info from data
class TaskDropDown(DropDown):
    def __init__(self,data,label):
        super(TaskDropDown, self).__init__()
        for x in data:
            btn = Button(text=x, size_hint_y=None)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.add_widget(btn)

#Create a form with a label on top of it
def createForm(label):
    """
    :param label: name that represents the form (String)
    :return: returns Form with a label on top of it and the text_input
    """
    form = BoxLayout()
    form.orientation = 'vertical'

    form_label = Label(text=label)
    text_input = TextInput(multiline=False)

    form.add_widget(form_label)
    form.add_widget(text_input)

    return form, text_input

#Creates a popup with a title and label
class Alert(Popup):
    def __init__(self,msg,title,**kwargs):
        """
        :param msg: message of the popup
        :param title: title of popup
        """
        super(Alert, self).__init__(**kwargs)
        self.title = title
        self.size_hint = .35,.35

        root = BoxLayout()
        root.orientation = 'vertical'

        label = Label(text = msg)

        confirm_button = Button(text="Okay")
        confirm_button.bind(on_press= self.dismiss)

        root.add_widget(label)
        root.add_widget(confirm_button)

        self.content = root
