from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QToolBar,
)
from project.enums.instance_type_enum import InstanceTypeEnum
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.services.process_service import ProcessService
from project.services.setup_service import SetupService
from project.widgets.about_frame import AboutFrame
from project.widgets.instance_button import InstanceButton
from project.utils.path_utils import PathUtils
from project import qrc_resources
from project.stylesheet import stylesheet
from project.widgets.instance_list_frame import InstanceListFrame
from project.widgets.instance_form_frame import InstanceFormFrame
from project.widgets.instance_run_frame import InstanceRunFrame
from project.app_info import AppInfo
import psutil
import os


class MainWindow(QMainWindow):

    STATE_NORMAL = 0
    STATE_ADD = 1
    STATE_EDIT = 2
    STATE_INSTANCE_SELECTED = 3
    STATE_RUN = 4
    STATE_ABOUT = 5

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.current_instance: InstanceModel = None
        self.setWindowIcon(QIcon(':ce-icon'))
        self.resize(800, 600)
        self.register_actions()
        self.create_toolbar()
        self.create_menu()
        self.create_statusbar()
        self.create_central_widget()
        self.set_stylesheets()
        self.register_handlers()
        self.refresh_statusbar_message()
        self.update_window_title()
        self.set_state(MainWindow.STATE_NORMAL)

    ###########################################################################
    # GUI Build
    ###########################################################################

    def update_window_title(self) -> None:
        nickname = DataService.get_data().profile.nickname
        self.setWindowTitle(
            f'{AppInfo.TITLE} {AppInfo.VERSION} ({nickname})'
        )

    def set_stylesheets(self) -> None:
        self.central_widget.setStyleSheet(stylesheet)

    def register_actions(self) -> None:
        self.add_action = \
            QAction(QIcon(':add-icon'), 'Add Instance', self)
        self.edit_action = \
            QAction(QIcon(':edit-icon'), 'Edit Instance', self)
        self.delete_action = \
            QAction(QIcon(':delete-icon'), 'Delete Instance', self)
        self.open_folder_action = \
            QAction(QIcon(':open-folder-icon'), 'Open Folder', self)
        self.open_dg_action = \
            QAction(QIcon(':open-dg-icon'), 'Open Dg&oodoo', self)
        self.run_action = \
            QAction(QIcon(':run-icon'), 'Run Instance', self)
        self.connect_action = \
            QAction(QIcon(':connect-icon'), 'Connect', self)
        self.refresh_action = \
            QAction(QIcon(':refresh-icon'), 'Refresh', self)
        self.save_action = \
            QAction(QIcon(':save-icon'), 'Save', self)
        self.cancel_action = \
            QAction(QIcon(':cancel-icon'), 'Cancel', self)
        self.setup_action = \
            QAction(QIcon(':setup-icon'), 'Setup', self)
        self.change_nickname_action = \
            QAction(QIcon(':profile-icon'), 'Change Nickname', self)
        self.kill_process_action = \
            QAction(QIcon(':stop-icon'), 'Kill CE and Lobby Process', self)
        self.about_action = \
            QAction(QIcon(':about-icon'), 'About CEHub', self)

    def create_toolbar(self) -> None:
        toolbar = QToolBar('toolbar', self)

        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.edit_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.run_action)
        toolbar.addAction(self.connect_action)
        toolbar.addSeparator()
        toolbar.addAction(self.open_folder_action)
        toolbar.addAction(self.open_dg_action)
        toolbar.addSeparator()
        toolbar.addAction(self.kill_process_action)
        toolbar.addAction(self.refresh_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.setup_action)
        toolbar.addAction(self.cancel_action)
        toolbar = self.addToolBar(toolbar)

    def create_menu(self) -> None:
        menubar = QMenuBar(self)

        instance_menu = QMenu('Instance', self)
        instance_menu.addAction(self.add_action)
        instance_menu.addAction(self.edit_action)
        instance_menu.addAction(self.delete_action)
        instance_menu.addSeparator()
        instance_menu.addAction(self.run_action)
        instance_menu.addAction(self.connect_action)

        open_menu = QMenu('Open', self)
        open_menu.addAction(self.open_folder_action)
        open_menu.addAction(self.open_dg_action)

        actions_menu = QMenu('Actions', self)
        actions_menu.addAction(self.save_action)
        actions_menu.addAction(self.setup_action)
        actions_menu.addAction(self.cancel_action)
        actions_menu.addSeparator()
        actions_menu.addAction(self.kill_process_action)
        actions_menu.addAction(self.refresh_action)

        profile_menu = QMenu('Profile', self)
        profile_menu.addAction(self.change_nickname_action)

        about_menu = QMenu('About', self)
        about_menu.addAction(self.about_action)

        menubar.addMenu(instance_menu)
        menubar.addMenu(open_menu)
        menubar.addMenu(actions_menu)
        menubar.addMenu(profile_menu)
        menubar.addMenu(about_menu)
        self.setMenuBar(menubar)

    def create_statusbar(self) -> None:
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar_label = QLabel()
        self.statusbar.addPermanentWidget(self.statusbar_label, 100)

    def create_central_widget(self) -> None:
        self.central_widget = InstanceListFrame(self)
        self.setCentralWidget(self.central_widget)

    def refresh_statusbar_message(self) -> None:
        nickname = DataService.get_data().profile.nickname
        ce_process = 'STOPPED'
        lobby_process = 'STOPPED'
        for p in psutil.process_iter():
            if p.name().lower() == 'ce.exe':
                ce_process = 'RUNNING'
            if p.name().lower() == 'lobby.exe':
                lobby_process = 'RUNNING'
        self.statusbar_label.setText(
            f'Profile: {nickname} / CE process: {ce_process} / \
Lobby process: {lobby_process}'
        )

    ###########################################################################
    # State
    ###########################################################################

    def set_state(self, state) -> None:
        self.state = state
        self.add_action.setDisabled(True)
        self.edit_action.setDisabled(True)
        self.delete_action.setDisabled(True)
        self.open_folder_action.setDisabled(True)
        self.open_dg_action.setDisabled(True)
        self.run_action.setDisabled(True)
        self.connect_action.setDisabled(True)
        self.refresh_action.setDisabled(True)
        self.save_action.setDisabled(True)
        self.cancel_action.setDisabled(True)
        self.setup_action.setDisabled(True)
        if state == MainWindow.STATE_NORMAL:
            self.add_action.setDisabled(False)
            self.refresh_action.setDisabled(False)
            self.set_stylesheets()
        elif state == MainWindow.STATE_ADD:
            self.cancel_action.setDisabled(False)
            self.setup_action.setDisabled(False)
        elif state == MainWindow.STATE_EDIT:
            self.cancel_action.setDisabled(False)
            self.save_action.setDisabled(False)
        elif state == MainWindow.STATE_INSTANCE_SELECTED:
            self.add_action.setDisabled(False)
            self.edit_action.setDisabled(False)
            self.delete_action.setDisabled(False)
            self.open_folder_action.setDisabled(False)
            self.open_dg_action.setDisabled(False)
            self.run_action.setDisabled(False)
            if self.current_instance.type == InstanceTypeEnum.CLIENT.value:
                self.connect_action.setDisabled(False)
            self.refresh_action.setDisabled(False)
            self.cancel_action.setDisabled(False)
        elif state == MainWindow.STATE_RUN:
            self.cancel_action.setDisabled(False)
        elif state == MainWindow.STATE_ABOUT:
            self.cancel_action.setDisabled(False)

    ###########################################################################
    # Redirects
    ###########################################################################

    def go_instance_list(self) -> None:
        self.central_widget = InstanceListFrame(self)
        self.setCentralWidget(self.central_widget)
        self.set_state(MainWindow.STATE_NORMAL)

    ###########################################################################
    # Action Handlers
    ###########################################################################

    def register_handlers(self) -> None:
        self.add_action.triggered.connect(
            self.handle_add_action
        )
        self.edit_action.triggered.connect(
            self.handle_edit_action
        )
        self.delete_action.triggered.connect(
            self.handle_delete_action
        )
        self.cancel_action.triggered.connect(
            self.handle_cancel_action
        )
        self.save_action.triggered.connect(
            self.handle_save_action
        )
        self.setup_action.triggered.connect(
            self.handle_setup_action
        )
        self.change_nickname_action.triggered.connect(
            self.handle_change_nickname
        )
        self.kill_process_action.triggered.connect(
            self.handle_kill_ce_action
        )
        self.refresh_action.triggered.connect(
            self.handle_refresh_action
        )
        self.open_folder_action.triggered.connect(
            self.handle_open_folder_action
        )
        self.open_dg_action.triggered.connect(
            self.handle_open_dg_action
        )
        self.run_action.triggered.connect(
            lambda: self.handle_run_action(False)
        )
        self.connect_action.triggered.connect(
            lambda: self.handle_run_action(True)
        )
        self.about_action.triggered.connect(
            self.handle_about_action
        )

    def handle_about_action(self) -> None:
        self.central_widget = AboutFrame(
            self
        )
        self.setCentralWidget(self.central_widget)
        self.set_state(MainWindow.STATE_ABOUT)

    def handle_run_action(self, connect_tab: bool) -> None:
        self.central_widget = InstanceRunFrame(
            self, self.current_instance, connect_tab
        )
        self.setCentralWidget(self.central_widget)
        self.set_state(MainWindow.STATE_RUN)

    def handle_open_folder_action(self) -> None:
        if self.current_instance is not None:
            instance_path = \
                PathUtils.get_instance_path(self.current_instance.name)
            if os.path.exists(instance_path):
                os.startfile(instance_path)
            else:
                message = QMessageBox()
                message.critical(
                    self, 'Error', 'The instance folder was not found'
                )

    def handle_open_dg_action(self) -> None:
        if self.current_instance is not None:
            instance_path = \
                PathUtils.get_instance_path(self.current_instance.name)
            os.startfile(os.path.join(instance_path, 'dgVoodooCpl.exe'))

    def handle_refresh_action(self) -> None:
        self.refresh_statusbar_message()
        self.set_current_instance(None)
        if isinstance(self.central_widget, InstanceListFrame):
            self.central_widget.refresh()

    def handle_kill_ce_action(self) -> None:
        confirm = QMessageBox()
        answer = confirm.question(
            self,
            'Confirmation',
            'Do you realy want to kill the ce.exe and lobby.exe process?'
        )
        if answer == QMessageBox.Yes:
            ProcessService.kill_ce_and_lobby_process()
            self.refresh_statusbar_message()

    def handle_add_action(self) -> None:
        self.central_widget = InstanceFormFrame(self)
        self.setCentralWidget(self.central_widget)
        self.set_state(MainWindow.STATE_ADD)

    def handle_edit_action(self) -> None:
        self.central_widget = InstanceFormFrame(self, self.current_instance)
        self.setCentralWidget(self.central_widget)
        self.set_state(MainWindow.STATE_EDIT)

    def handle_save_action(self) -> None:
        self.central_widget.save()

    def handle_setup_action(self) -> None:
        self.central_widget.setup()

    def handle_cancel_action(self) -> None:
        if self.state == MainWindow.STATE_INSTANCE_SELECTED:
            for btn in self.central_widget.buttons:
                btn.deselect()
            self.set_state(MainWindow.STATE_NORMAL)
        elif self.state == MainWindow.STATE_RUN:
            self.go_instance_list()
        elif self.state == MainWindow.STATE_ABOUT:
            self.go_instance_list()
        else:
            confirm = QMessageBox()
            if confirm.question(
                self, 'Confirmation', 'Do you really want to cancel?'
            ) == QMessageBox.Yes:
                self.go_instance_list()

    def handle_delete_action(self) -> None:
        if self.current_instance is None:
            return
        question = QMessageBox()
        answer = question.question(
            self,
            'Confirmation',
            f'Do you really want to delete the "{self.current_instance.name}" \
instance?'
        )
        if answer == QMessageBox.Yes:
            try:
                SetupService.delete_instance(self.current_instance)
                self.central_widget.refresh()
                self.set_state(MainWindow.STATE_NORMAL)
            except Exception as err:
                print(err)
                message = QMessageBox()
                message.critical(self, 'Error', str(err))

    def handle_change_nickname(self) -> None:
        data = DataService.get_data()
        current_nickname = data.profile.nickname
        text, ok = QInputDialog.getText(
            self,
            'Change Nickname',
            'CE Player Nickname:',
            text=current_nickname
        )
        if ok:
            if not text:
                message = QMessageBox()
                message.warning(
                    self,
                    'Error',
                    'The nickname is invalid'
                )
                return
            if len(text) > 10:
                message = QMessageBox()
                message.warning(
                    self,
                    'Error',
                    'The custom nickname has a limit of 10 characters'
                )
                return
            data.profile.nickname = text
            DataService.save_data(data)
            self.refresh_statusbar_message()
            self.update_window_title()

    ###########################################################################
    # Behaviors
    ###########################################################################

    def set_current_instance(self, instance: InstanceModel) -> None:
        for widget in self.central_widget.buttons:
            widget.deselect()
        self.current_instance = instance
        if instance is not None:
            self.set_state(MainWindow.STATE_INSTANCE_SELECTED)
        else:
            self.set_state(MainWindow.STATE_NORMAL)
