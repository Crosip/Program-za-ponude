from screens.bid_screen import BidScreen, QMainWindow, QApplication, QLabel, QPushButton, QWidget, uic
from screens.company_screen import CompanyScreen
from functions.bid_database import delete_db

# Create class for Start Screen window

class StartScreen (QMainWindow):
    def __init__(self):
        super (StartScreen, self).__init__()

        # Load start screen
        uic.loadUi("start.ui", self)
        self.show_main_window()

        # Import all QWidgets from UI file
        self.new_bid_btn = self.findChild (QPushButton, 'new_bid_button')
        self.exit_btn = self.findChild (QPushButton, 'exit_button')
        self.add_company_btn = self.findChild (QPushButton, 'add_company_button')

        # Connect buttons to methods
        self.new_bid_btn.clicked.connect(self.open_bid_window)
        self.exit_btn.clicked.connect (self.exit)
        self.add_company_btn.clicked.connect (self.open_company_window)
    
    # Method to open window with information about bid
    def open_bid_window (self):
        self.app = QMainWindow()
        self.ui = BidScreen ()
        self.ui.load_bid_screen()

    # Method to open window for entering new company
    def open_company_window (self):
        self.app = QMainWindow()
        self.ui = CompanyScreen ()
        self.ui.load_company_screen()

    # Method to show this screen
    def show_main_window (self):
        self.show()

    # Method to hide this screen
    def hide_main_window (self):
        self.hide()

    # Method to exit app
    def exit (self):
        self.close()
        delete_db()