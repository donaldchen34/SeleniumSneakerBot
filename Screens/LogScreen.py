from kivy.uix.screenmanager import Screen
import ReadData
from Screens.ScreenHelper import RootWidget,DataCol,DataScreen

#Todo
#Remove Error from log fields -> Only need to show status(if bought/missed/error)

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

