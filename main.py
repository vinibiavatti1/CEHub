import sys
from PyQt5.QtWidgets import QApplication
from project.main_window import MainWindow
from project.services.data_service import DataService


# Main
def main():
    DataService.load_data()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


# Init
if __name__ == '__main__':
    main()
