from Interface import *

if __name__ == "__main__":
    # a+(ab+b(cb+a)*c)+a(b)*c
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
