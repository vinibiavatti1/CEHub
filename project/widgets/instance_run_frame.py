from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextBlock
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QTabBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget
)
from project.models.connection_model import ConnectionModel
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.utils.path_utils import PathUtils


class InstanceRunFrame(QFrame):
    def __init__(self, main_window, instance: InstanceModel) -> None:
        super().__init__(main_window, objectName='frame')
        self.main_window = main_window
        self.instance = instance
        self.create_layout()
        self.refresh_addresses()
        self.register_handlers()

    def create_layout(self) -> None:
        self.grid = QVBoxLayout()
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        # Instance name
        self.grid.addWidget(QLabel('Instance Name', self))
        self.instance_name_field = QLineEdit()
        self.instance_name_field.setReadOnly(True)
        self.instance_name_field.setText(self.instance.name)
        self.grid.addWidget(self.instance_name_field)

        # Instance path
        self.grid.addWidget(QLabel('Instance Path', self))
        self.instance_path_field = QLineEdit()
        self.instance_path_field.setReadOnly(True)
        self.instance_path_field.setText(
            PathUtils.get_instance_path(self.instance.name)
        )
        self.grid.addWidget(self.instance_path_field)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_run = QWidget()
        self.tab_connect = QWidget()
        self.tabs.addTab(self.tab_run, QIcon(':run-icon'), 'Run')
        self.tabs.addTab(self.tab_connect, QIcon(':connect-icon'), 'Connect')
        self.grid.addWidget(self.tabs)

        # Tab Run
        self.grid_tab_run = QVBoxLayout()
        self.grid_tab_run.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tab_run.setLayout(self.grid_tab_run)

        # Arguments Run
        self.grid_tab_run.addWidget(QLabel('Command Line', self))
        self.command_line_field = QLineEdit(self)
        self.command_line_field.setText('ce.exe +host')
        self.grid_tab_run.addWidget(self.command_line_field)

        # Actions
        self.run_button = QPushButton('Run!', self)
        self.run_button.setIcon(QIcon(':run-icon'))
        self.run_button.setFixedWidth(150)
        self.grid_tab_run.addWidget(self.run_button)

        # Tab Connect
        self.grid_tab_connect = QVBoxLayout()
        self.grid_tab_connect.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tab_connect.setLayout(self.grid_tab_connect)

        # Connect
        self.grid_tab_connect.addWidget(QLabel('Address (IP or Host)'))
        self.addresses_field = QComboBox()
        self.grid_tab_connect.addWidget(self.addresses_field)
        self.address_field = QLineEdit()
        self.address_field.setPlaceholderText(
            'Type or select the address to connect'
        )
        self.grid_tab_connect.addWidget(self.address_field)

        self.btn_frame = QFrame()
        self.btn_frame_grid = QHBoxLayout()
        self.btn_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.btn_frame_grid.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btn_frame.setLayout(self.btn_frame_grid)
        self.grid_tab_connect.addWidget(self.btn_frame)

        self.save_address_button = QPushButton('Save Connection')
        self.save_address_button.setIcon(QIcon(':address-add-icon'))
        self.save_address_button.setFixedWidth(150)
        self.btn_frame_grid.addWidget(self.save_address_button)

        self.delete_address_button = QPushButton('Delete Connection')
        self.delete_address_button.setIcon(QIcon(':address-delete-icon'))
        self.delete_address_button.setFixedWidth(150)
        self.btn_frame_grid.addWidget(self.delete_address_button)

        # Arguments Connect
        self.grid_tab_connect.addWidget(QLabel('Command Line', self))
        self.command_line_connect_field = QLineEdit(self)
        self.command_line_connect_field.setText('ce.exe +host')
        self.grid_tab_connect.addWidget(self.command_line_connect_field)

        self.connect_button = QPushButton('Connect!')
        self.connect_button.setIcon(QIcon(':connect-icon'))
        self.connect_button.setFixedWidth(150)
        self.grid_tab_connect.addWidget(self.connect_button)

    def refresh_addresses(self) -> None:
        self.addresses_field.clear()
        self.addresses_field.addItem('--- Select the address or type one ---')
        for connection in DataService.get_data().connections:
            self.addresses_field.addItem(
                f'{connection.name} ({connection.address})'
            )

    ###########################################################################
    # Handlers
    ###########################################################################

    def register_handlers(self) -> None:
        self.save_address_button.clicked.connect(
            self.handle_save_address
        )
        self.delete_address_button.clicked.connect(
            self.handle_delete_address
        )
        self.addresses_field.currentTextChanged.connect(
            self.handle_addresses_change
        )

    def handle_addresses_change(self) -> None:
        if self.addresses_field.currentIndex() == 0:
            self.address_field.setText('')
            return
        connection = DataService.get_data().connections[
            self.addresses_field.currentIndex() - 1
        ]
        self.address_field.setText(connection.address)

    def handle_delete_address(self) -> None:
        if (self.addresses_field.count() == 0 or
                self.addresses_field.currentIndex() == 0):
            message = QMessageBox()
            message.information(
                self, 'Information', 'Please, select some connection to delete'
            )
            return
        message = QMessageBox()
        answer = message.question(
            self,
            'Confirmation',
            'Do you really want to delete the selected connection?'
        )
        if answer == QMessageBox.Yes:
            con_index = self.addresses_field.currentIndex()
            data = DataService.get_data()
            data.connections.pop(con_index - 1)
            DataService.save_data(data)
            self.refresh_addresses()

    def handle_save_address(self) -> None:
        address = self.address_field.text()
        if not address:
            message = QMessageBox()
            message.warning(
                self, 'Warning', 'You have to inform an address to save'
            )
            return
        input_box = QInputDialog()
        connection_name, ok = input_box.getText(
            self,
            'Connection name',
            'Type some identifier for the address to save'
        )
        if not ok:
            return
        if len(connection_name.strip()) == 0:
            message = QMessageBox()
            message.critical(
                self, 'Error', 'Invalid identifier'
            )
            return
        data = DataService.get_data()
        for c in data.connections:
            if c.name == connection_name:
                message = QMessageBox()
                message.critical(
                    self,
                    'Error',
                    f'The name "{connection_name}" is already being used'
                )
                return
        data.connections.append(ConnectionModel(
            connection_name,
            address
        ))
        DataService.save_data(data)
        self.refresh_addresses()
