from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QComboBox, QTextEdit, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QCalendarWidget
from functions.company_database import read_company_db
from functions.bid_database import get_price
from models.bid_db import Bid_Items, engine
from models.company_db import Company_Data
from models.to_word import export_to_word
from sqlalchemy.orm import sessionmaker
from datetime import date
from PyQt5 import uic

# Class for screen with information about bid
class BidScreen (QMainWindow):
    def __init__(self):
        super (BidScreen, self).__init__()

        # loading UI screen
        uic.loadUi("infobid.ui", self)

        # List of units 
        self.unit_list = ['m', 'h', 'kg', 'kom']

        # loading all QWidgets from UI file
        self.company_cmb = self.findChild (QComboBox, 'company_comboBox')
        self.name_txt = self.findChild (QTextEdit, 'name_edit')
        self.quantity_txt = self.findChild (QLineEdit, 'quantity_edit')
        self.unit_cmb = self.findChild (QComboBox, 'unit_comboBox')
        self.price_txt = self.findChild (QLineEdit, 'price_edit')
        self.bid_table = self.findChild (QTableWidget, 'bid_table')
        self.price = self.findChild (QLabel, 'price_value')
        self.tax = self.findChild (QLabel, 'tax_value')
        self.total = self.findChild (QLabel, 'total_value')
        self.bid_num = self.findChild (QLineEdit, 'bid_num_edit')
        # Variable for counting rows in table
        self.row = 0

        # Statement for importing all units into combobox
        for i in range (4):
            self.unit_cmb.addItem ('')
            self.unit_cmb.setItemText (i, self.unit_list [i])

        # Finding and connecting all buttons to its methods
        self.add_rec_btn = self.findChild (QPushButton, 'add_record_button')
        self.add_rec_btn.clicked.connect (lambda: self.add_bid(self.read_name(), self.read_quantity(), self.read_price(), self.read_unit()))
        self.next_btn = self.findChild (QPushButton, 'next_button')
        self.next_btn.clicked.connect (self.message_box)
        self.close_btn = self.findChild (QPushButton, "back_button")
        self.close_btn.clicked.connect (self.show_main)

    # showing bid screen
    def load_bid_screen (self):
        self.show()
        self.combo_items(read_company_db())

    # closing bid screen
    def close_screen (self):
        self.close()

    # showing main screen
    def show_main (self):
        self.hide()
        from screens.start_screen import StartScreen
        screen = StartScreen()
        screen.show_main_window()

    # Method for importing all company names from database
    def combo_items (self, names):
        index = 0
        for item in names:
            self.company_cmb.addItem ('')
            self.company_cmb.setItemText (index, item [0])
            index += 1

    # Reading methods from all QLineEdits 
    def read_name (self):
        return str (self.name_txt.toPlainText())
    
    def read_quantity (self):
        return float (self.quantity_txt.text())
    
    def read_price (self):
        return float (self.price_txt.text())
    
    def read_unit (self):
        return str (self.unit_cmb.currentText())
    
    def read_bid_num (self):
        return self.bid_num.text()

    # Todays date  
    def today_date (self):
        self.today = date.today()
        return self.today.strftime('%d/%m/%Y')

    # Clear all inputs from QLineEdits   
    def clear_bid_data (self):
        self.name_txt.clear()
        self.quantity_txt.clear()
        self.price_txt.clear()

    # Method for adding bid info to bid database
    def add_bid (self, name, quantity, price, unit):
        Session = sessionmaker (bind=engine)
        session = Session()
        data = Bid_Items (name = name, quantity = quantity, price = price, unit = unit)
        session.add (data)
        session.commit()
        self.fill_table()
        self.clear_bid_data()

    # Writing bid info into table 
    def fill_table (self):
        self.bid_table.setItem (self.row, 0, QTableWidgetItem (self.read_name()))
        self.bid_table.setItem (self.row, 1, QTableWidgetItem (str (self.read_quantity())))
        self.bid_table.setItem (self.row, 2, QTableWidgetItem (self.read_unit()))
        self.bid_table.setItem (self.row, 3, QTableWidgetItem (str(self.read_price())))
        self.row += 1
        self.labels_value()

    # Getting values from table
    def read_table_name (self):
        num = self.bid_table.rowCount()
        name = []
        for i in range(num):
            if self.bid_table.item(i, 0) and self.bid_table.item(i, 0).text():
                name.append (self.bid_table.item(i, 0).text())
        return name
    
    def read_table_quantity (self):
        num = self.bid_table.rowCount()
        quantity = []
        for i in range(num):
            if self.bid_table.item(i, 1) and self.bid_table.item(i, 1).text():
                quantity.append (self.bid_table.item(i, 1).text())
        return quantity
    
    def read_table_unit (self):
        num = self.bid_table.rowCount()
        unit = []
        for i in range(num):
            if self.bid_table.item(i, 2) and self.bid_table.item(i, 2).text():
                unit.append (self.bid_table.item(i, 2).text())
        return unit
    
    def read_table_price (self):
        num = self.bid_table.rowCount()
        price = []
        for i in range(num):
            if self.bid_table.item(i, 3) and self.bid_table.item(i, 3).text():
                price.append (self.bid_table.item(i, 3).text())
        return price

    # Get price values from labels   
    def read_label_value (self):
        data = []
        data.append(self.price.text())
        data.append (self.tax.text())
        data.append (self.total.text())
        return data

    # Calculate total value including tax from prices
    def labels_value (self):
        prices = get_price()
        price = round (sum (prices), 2)
        tax = price * 0.25
        tax = round (tax, 2)
        total = price + tax
        total = round (total, 2)
        self.price.setText(str (f'{price} €'))
        self.tax.setText(f'{tax} €')
        self.total.setText(f'{total} €')

    # Matching if selected company in combobox is in database, and getting info from db about that company
    def check_company (self, names):
        for data in names:
            if self.company_cmb.currentText() == data [0]:
                company = Company_Data (data [0], data[2], data[1])
                cm_data = company.data_to_dict()
        return cm_data

    # Message if you want proceed
    def message_box (self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Jeste li sigurni da želite nastaviti?")
        msgBox.setWindowTitle("Info")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.write_company()

    # Unified method for write everything into word function
    def write_company (self):
        company_data = self.check_company (read_company_db())
        names = self.read_table_name()
        quantity = self.read_table_quantity()
        prices = self.read_table_price()
        units = self.read_table_unit()
        total = self.read_label_value()
        bid_num = self.read_bid_num()
        calendar = self.today_date()
        export_to_word(company_data, names, quantity, units, prices, total, bid_num, calendar)
        self.show_main()

    