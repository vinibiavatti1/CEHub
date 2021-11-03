from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)
from project.app_info import AppInfo


class AboutFrame(QFrame):
    def __init__(self, main_window) -> None:
        super().__init__(main_window, objectName='frame')
        self.create_layout()

    def create_layout(self) -> None:
        self.grid = QVBoxLayout()
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        self.grid.addWidget(QLabel('Application', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText(AppInfo.TITLE + ' ' + AppInfo.VERSION)
        self.grid.addWidget(app_field)

        self.grid.addWidget(QLabel('Author', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('ViniB')
        self.grid.addWidget(app_field)

        self.grid.addWidget(QLabel('CE Multiplayer Website', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://www.codenameeaglemultiplayer.com/')
        self.grid.addWidget(app_field)

        self.grid.addWidget(QLabel('Discord Community', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://discord.gg/VGW9AaQJne')
        self.grid.addWidget(app_field)

        self.grid.addWidget(QLabel('Reddit Community', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://www.reddit.com/r/CodenameEagle/')
        self.grid.addWidget(app_field)

        thanks = 'Thanks to the Codename Eagle community for the motivation \
and opportunity to bring CE to us again!'
        self.grid.addWidget(QLabel(thanks, self))
