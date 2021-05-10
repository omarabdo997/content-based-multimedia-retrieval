import sys
from PySide2.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow("ui_file.ui")
    main_window.show()
    app.exec_()
    sys.exit(0)