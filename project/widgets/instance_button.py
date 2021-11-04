from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from project import qrc_resources
from project.enums.main_window_states_enum import MainWindowStatesEnum
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.services.dialog_service import DialogService
from project.utils.path_utils import PathUtils
from PyQt5.QtWidgets import QPushButton
import os


class InstanceButton(QPushButton):
    """
    Instance push button
    """

    def __init__(self, main_window, list_frame,
                 instance: InstanceModel) -> None:
        """
        Construct a new InstanceButton
        """
        super().__init__(main_window, objectName='instance-button')
        self.instance = instance
        self.list_frame = list_frame
        self.main_window = main_window
        self.instance_path = PathUtils.get_instance_path(instance.name)
        self._build()

    ###########################################################################
    # Build widget
    ###########################################################################

    def _build(self) -> None:
        """
        Build widget
        """
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.action)
        texts = [self.instance.name, self.instance.version,
                 self.instance.patch, self.instance.type]
        if os.path.exists(self.instance_path):
            self.setIcon(QIcon(':ce-icon'))
            self.error = False
        else:
            self.setIcon(QIcon(':warn-icon'))
            texts.append('ERROR: The instance path was not found.')
            self.error = True
        self.setText('\n'.join(texts))

    ###########################################################################
    # Styles
    ###########################################################################

    def set_selected_style(self) -> None:
        """
        Set the stylesheet for selected button
        """
        self.setStyleSheet('border: 2px solid rgb(200, 200, 200);')

    def set_deselected_style(self) -> None:
        """
        Set the stylesheet for de-selected button
        """
        self.setStyleSheet('border: 1px solid rgba(0, 0, 0, .1);')

    ###########################################################################
    # Handler
    ###########################################################################

    def action(self, _) -> None:
        """
        Button click event handler
        """
        if self.error:
            self._error_action()
        else:
            self._select_instance_action()

    ###########################################################################
    # Actions
    ###########################################################################

    def _error_action(self) -> None:
        """
        Process click action when the instance has an error
        """
        answer = DialogService.question(
            self,
            f'The instance path "{self.instance_path}" was not found. ' +
            f'Do you want to delete this instance?'
        )
        if answer:
            self._delete_instance_from_data_file()
            self.list_frame.refresh()

    def _select_instance_action(self) -> None:
        """
        Process click action when the instance is ok
        """
        self.main_window.set_current_instance(self.instance)
        self.main_window.set_actions_state(
            MainWindowStatesEnum.INSTANCE_SELECTED
        )
        self.set_selected_style()

    ###########################################################################
    # Private Methods
    ###########################################################################

    def _delete_instance_from_data_file(self) -> None:
        """
        Delete instance when there is an error
        """
        data = DataService.get_data()
        for instance in data.instances:
            if instance.name == self.instance.name:
                data.instances.remove(instance)
                break
        DataService.save_data(data)
