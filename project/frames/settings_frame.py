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

        # CD-ROM drive
        self._container.addWidget(QLabel(
            'CD-ROM Drive: (Default: E:) (Requires Elevated Permission)'
        ))
        self._drive_field = QComboBox(self)
        for drive in SettingsFrame.DRIVES:
            self._drive_field.addItem(drive + ':')
        self._drive_field.setCurrentText(data.cd_drive)
        self._container.addWidget(self._drive_field)

    def save(self) -> None:
        """
        Save changes.
        """
        data = DataService.get_data()
        data.profile.nickname = self._profile_name_field.text()
        data.ce_exec_file_name = self._executable_command_field.currentText()
        DataService.save_data(data)

        drive = self._drive_field.currentText()
        if drive == data.cd_drive:
            return

        answer = DialogService.question(
            self,
            'The Codename Eagle registry drive key will be added/updated in ' +
            'Windows Registry Editor. This action usually needs elevated ' +
            'permission. Proceed?'
        )
        if not answer:
            return

        # CD-ROM drive
        try:
            WinRegService.update_drive_key(drive)
            data.cd_drive = drive
            DataService.save_data(data)
        except Exception as err:
            DialogService.error(
                self, f'Could not update CD-Drive in registry: {err}'
            )
