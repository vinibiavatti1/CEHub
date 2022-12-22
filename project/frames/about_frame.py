from PyQt5.QtCore import Qt
from project.app_info import AppInfo
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class AboutFrame(QFrame):
    """
    About frame
    """

    def __init__(self, main_window) -> None:
        """
        Construct a new AboutFrame
        """
        super().__init__(main_window, objectName='frame')
        self._build()

    def _build(self) -> None:
        """
        Build AboutFrame
        """
        self._container = QVBoxLayout()
        self._container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._container)

        # App info
        self._container.addWidget(QLabel('Application', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText(AppInfo.TITLE + ' ' + AppInfo.VERSION)
        self._container.addWidget(app_field)

        # Author info
        self._container.addWidget(QLabel('Author', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('ViniB')
        self._container.addWidget(app_field)

        # Website info
        self._container.addWidget(QLabel('CE Multiplayer Website', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://cenation.co.uk/')
        self._container.addWidget(app_field)

        # Discord info
        self._container.addWidget(QLabel('Discord Community', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://discord.gg/VGW9AaQJne')
        self._container.addWidget(app_field)

        # Reddit info
        self._container.addWidget(QLabel('Reddit Community', self))
        app_field = QLineEdit()
        app_field.setReadOnly(True)
        app_field.setText('https://www.reddit.com/r/CodenameEagle/')
        self._container.addWidget(app_field)

        # Thanks message
        thanks = 'Thanks to the Codename Eagle community for the ' + \
                 'motivation and opportunity to bring CE to us again!'
        self._container.addWidget(QLabel(thanks, self))
