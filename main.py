from screens.start_screen import StartScreen, QApplication

# Start app
if __name__ == '__main__':
    import sys
    app = QApplication (sys.argv)
    ui = StartScreen()
    app.exec_()
