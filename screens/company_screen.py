from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from models.company_db import Company_Items, engine
from sqlalchemy.orm import sessionmaker
from PyQt5 import uic

# Class for company screen
class CompanyScreen (QMainWindow):
    def __init__ (self):
        super (CompanyScreen, self).__init__()

        # Load Company UI
        uic.loadUi("company.ui", self)

        # finding QWidgets in UI file
        self.name = self.findChild (QLineEdit, 'name_edit')
        self.address = self.findChild (QLineEdit, 'address_edit')
        self.oib = self.findChild (QLineEdit, 'oib_edit')

        # Connecting buttons to methods
        self.add_btn = self.findChild(QPushButton, 'add_button')
        self.add_btn.clicked.connect (self.add_company)
        self.back_btn = self.findChild (QPushButton, 'back_button')
        self.back_btn.clicked.connect (self.show_main)

    # Method to show company screen
    def load_company_screen(self):
        self.show()

    # Method to show start screen
    def show_main (self):
        self.hide()
        from screens.start_screen import StartScreen
        ui = StartScreen()
        ui.show_main_window()

    # Methods to get string from QLineEdit 
    def read_name (self) -> str:
        name = str (self.name.text())
        return name
    
    def read_address (self) -> str:
        address = str (self.address.text())
        return address
    
    def read_oib (self) -> str:
        oib = str (self.oib.text())
        return oib

    # Method to clear all inputs from QLineEdit
    def clear_text (self):
        self.name.clear()
        self.address.clear()
        self.oib.clear()
    
    # Method for sending all company info to Company database
    def company_to_db (self, name, address, oib):
        Session = sessionmaker (bind=engine)
        session = Session()
        data = Company_Items (name = name, oib = oib, address = address)
        session.add (data)
        session.commit()
        self.message_box_info()
        self.clear_text()

    # Message if everything went good
    def message_box_info (self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Tvrtka je uspješno dodana!")
        msgBox.setWindowTitle("Info")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    # Warning if lenght of OIB isn't 11 
    def oib_lenght_error (self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("OIB mora sadržavati točno 11 brojeva!")
        msgBox.setWindowTitle("Greška")
        msgBox.exec()

    # Warning if input text isn't just digits
    def oib_text_error (self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("OIB mora sadržavati samo brojeve!")
        msgBox.setWindowTitle("Greška")
        msgBox.exec()
   
    # Unified method for adding company to db if everything is ok
    def add_company (self):
        if len (self.oib.text ()) != 11:
            self.oib_lenght_error()
        elif self.oib.text().isdigit() == False:
            self.oib_text_error()
        else:
            self.company_to_db (self.read_name(), self.read_address(), self.read_oib())

        