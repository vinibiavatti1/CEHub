from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from project.enums.instance_type_enum import InstanceTypeEnum
from project.models.connection_model import ConnectionModel
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.utils.path_utils import PathUtils
from project.services.command_line_service import CommandLineService
from project.services.process_service import ProcessService
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget
)
import os


class InstanceRunFrame(QFrame):
    def __init__(self, main_window, instance: InstanceModel,
                 connect_tab: bool) -> None:
        super().__init__(main_window, objectName='frame')
        self.main_window = main_window
        self.instance = instance
        self.create_layout(connect_tab)
        self.refresh_addresses()
        self.register_handlers()
        self.refresh_run_arguments()
        if instance.type == InstanceTypeEnum.CLIENT.value:
            self.refresh_connect_arguments()

    def create_layout(self, connect_tab: bool) -> None:
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
        if self.instance.type != InstanceTypeEnum.CLIENT.value:
            self.tab_connect.setDisabled(True)

        # Select tab
        if connect_tab:
            self.tabs.setCurrentIndex(1)

        # Tab Run
        self.grid_tab_run = QVBoxLayout()
        self.grid_tab_run.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tab_run.setLayout(self.grid_tab_run)

        # Arguments Run
        self.grid_tab_run.addWidget(QLabel('Command Line', self))
        self.command_line_field = QLineEdit(self)
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
        if self.instance.properties.last_connection_index is not None:
            index = self.instance.properties.last_connection_index
            if index < self.addresses_field.count():
                self.addresses_field.setCurrentIndex(
                    self.instance.properties.last_connection_index
                )
                self.handle_addresses_change()

    def refresh_run_arguments(self) -> None:
        instance_type = self.instance.type
        if instance_type == InstanceTypeEnum.CLIENT.value or \
                instance_type == InstanceTypeEnum.SP.value:
            self.command_line_field.setText(
                CommandLineService.CE_EXE_NAME
            )
            return
        profile = DataService.get_data().profile.nickname
        arguments = CommandLineService.generate_arguments(
            self.instance, profile
        )
        self.command_line_field.setText(arguments)

    def refresh_connect_arguments(self) -> None:
        profile = DataService.get_data().profile.nickname
        arguments = CommandLineService.generate_arguments(
            self.instance, profile, self.address_field.text()
        )
        self.command_line_connect_field.setText(arguments)

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
        self.connect_button.clicked.connect(
            self.handle_connect
        )
        self.run_button.clicked.connect(
            self.handle_run
        )
        self.address_field.textChanged.connect(
            self.handle_address_change
        )

    def handle_run(self) -> None:
        try:
            ProcessService.execute(
                PathUtils.get_instance_path(self.instance.name),
                self.command_line_field.text()
            )
        except Exception as err:
            message = QMessageBox()
            message.critical(self, 'Error', str(err))
        self.main_window.refresh_statusbar_message()

    def handle_connect(self) -> None:
        data = DataService.get_data()
        for instance in data.instances:
            if instance.name == self.instance.name:
                instance.properties.last_connection_index = \
                    self.addresses_field.currentIndex()
                break
        DataService.save_data(data)
        try:
            ProcessService.execute(
                PathUtils.get_instance_path(self.instance.name),
                self.command_line_connect_field.text()
            )
        except Exception as err:
            message = QMessageBox()
            message.critical(self, 'Error', str(err))
        self.main_window.refresh_statusbar_message()

    def handle_address_change(self) -> None:
        self.refresh_connect_arguments()

    def handle_addresses_change(self) -> None:
        if self.addresses_field.currentIndex() == 0:
            self.address_field.setText('')
            return
        data = DataService.get_data()
        connection = data.connections[
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
