from PyQt5.QtCore import Qt
from project.app_info import AppInfo
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
)

from project.services.data_service import DataService
from project.services.dialog_service import DialogService
from project.services.winreg_service import WinRegService


class SettingsFrame(QFrame):
    """
    Settings frame
    """

    DRIVES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, main_window) -> None:
        """
        Construct a new SettingsFrame
        """
        super().__init__(main_window, objectName='frame')
        self._build()

    def _build(self) -> None:
        """
        Build SettingsFrame
        """
        data = DataService.get_data()

        self._container = QVBoxLayout()
        self._container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._container)

        # Profile name
        self._container.addWidget(QLabel(
            'Profile Name: (max 10 chars)'
        ))
        self._profile_name_field = QLineEdit(self)
        self._profile_name_field.setMaxLength(10)
        self._profile_name_field.setPlaceholderText(
            'Enter the name of the player'
        )
        self._profile_name_field.setText(data.profile.nickname)
        self._container.addWidget(self._profile_name_field)

        # CE Executable command
        self._container.addWidget(QLabel(
            'Execution Command: (Default: ce.exe)'
        ))
        self._executable_command_field = QComboBox(self)
        self._executable_command_field.setEditable(True)
        self._executable_command_field.addItem('ce.exe')
        self._executable_command_field.addItem('game.exe')
        self._executable_command_field.addItem('wine ce.exe')
        self._executable_command_field.addItem('wine game.exe')
        self._executable_command_field.setCurrentText(data.ce_exec_file_name)
        self._container.addWidget(self._executable_command_field)

    def save(self) -> None:
        """
        Save changes.
        """
        data = DataService.get_data()
        data.profile.nickname = self._profile_name_field.text()
        data.ce_exec_file_name = self._executable_command_field.currentText()
        DataService.save_data(data)
