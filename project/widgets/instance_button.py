from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QPushButton,
    QStatusBar,
)
from project import qrc_resources
from project.models.instance_model import InstanceModel


class InstanceButton(QPushButton):

    def __init__(self, main_window, instance: InstanceModel) -> None:
        super().__init__(main_window, objectName='instance-button')
        self.setIcon(QIcon(':ce-icon'))
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.action)
        self.instance = instance
        self.main_window = main_window
        self.set_text()

    def set_text(self) -> None:
        self.setText('\n'.join(
            (self.instance.name,
                self.instance.version,
                self.instance.patch,
                self.instance.type)
        ))

    def action(self, value) -> None:
        self.main_window.set_current_instance(self.instance)
        self.setStyleSheet('border: 2px solid rgb(200, 200, 200);')

    def deselect(self) -> None:
        self.setStyleSheet('border: 1px solid rgba(0, 0, 0, .1);')
