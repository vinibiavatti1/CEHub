from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMessageBox,
    QPushButton,
    QStatusBar,
)
from project import qrc_resources
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.utils.path_utils import PathUtils
import os


class InstanceButton(QPushButton):

    def __init__(self, main_window, instance: InstanceModel) -> None:
        super().__init__(main_window, objectName='instance-button')
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.action)
        self.instance = instance
        self.main_window = main_window
        self.instance_path = PathUtils.get_instance_path(instance.name)
        if os.path.exists(self.instance_path):
            self.setIcon(QIcon(':ce-icon'))
            self.set_text()
            self.error = False
        else:
            self.setIcon(QIcon(':warn-icon'))
            self.set_text(True)
            self.error = True

    def set_text(self, error: bool = False) -> None:
        texts = [self.instance.name, self.instance.version,
                 self.instance.patch, self.instance.type]
        if error:
            texts.append('ERROR: The instance path was not found.')
        self.setText('\n'.join(texts))

    def action(self, value) -> None:
        if self.error:
            message = QMessageBox()
            answer = message.question(
                self,
                'Instance Path Not Found',
                f'The instance path "{self.instance_path}" was not found. ' +
                'Do you want to delete this instance?'
            )
            if answer == QMessageBox.Yes:
                data = DataService.get_data()
                for instance in data.instances:
                    if instance.name == self.instance.name:
                        data.instances.remove(instance)
                        break
                DataService.save_data(data)
                self.main_window.central_widget.refresh()
            return
        self.main_window.set_current_instance(self.instance)
        self.setStyleSheet('border: 2px solid rgb(200, 200, 200);')

    def deselect(self) -> None:
        self.setStyleSheet('border: 1px solid rgba(0, 0, 0, .1);')
