from PyQt5.QtGui import QIcon
from project.enums.instance_type_enum import InstanceTypeEnum
from project.models.instance_model import InstanceModel
from project.services.data_service import DataService
from project.services.process_service import ProcessService
from project.services.setup_service import SetupService
from project.frames.about_frame import AboutFrame
from project.services.path_service import PathService
from project import qrc_resources
from project.services.winreg_service import WinRegService
from project.stylesheet import stylesheet
from project.frames.instance_list_frame import InstanceListFrame
from project.frames.instance_form_frame import InstanceFormFrame
from project.frames.instance_run_frame import InstanceRunFrame
from project.app_info import AppInfo
from project.enums.main_window_states_enum import MainWindowStatesEnum
from project.services.dialog_service import DialogService
from project.services.validation_service import ValidationService
from PyQt5.QtWidgets import (
    QAction,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QStatusBar,
    QToolBar,
    QWidget,
)
import os


class MainWindow(QMainWindow):
    """
    Application main window
    """

    DRIVES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, parent=None) -> None:
        """
        Construct a new MainWindow
        """
        super().__init__(parent)
        self.current_instance: InstanceModel = None
        self.current_state: MainWindowStatesEnum = None
        self.setWindowIcon(QIcon(':ce-icon'))
        self.resize(800, 600)
        self.register_actions()
        self.build_toolbar()
        self.build_menu()
        self.build_statusbar()
        self.register_handlers()
        self.refresh_window_title()
        self.set_actions_state(MainWindowStatesEnum.NORMAL)
        self.set_central_widget(InstanceListFrame(self))
        self.register_stylesheets()

    ###########################################################################
    # GUI Build
    ###########################################################################

    def build_toolbar(self) -> None:
        """
        Build toolbar
        """
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
        toolbar.addAction(self.kill_processes_action)
        toolbar.addAction(self.refresh_action)
        toolbar.addSeparator()
        toolbar.addAction(self.setup_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.cancel_action)
        toolbar = self.addToolBar(toolbar)

    def build_menu(self) -> None:
        """
        Build top menu
        """
        self.menu_bar = QMenuBar(self)
        self.build_instance_menu()
        self.build_open_menu()
        self.build_actions_menu()
        self.build_config_menu()
        self.build_about_menu()
        self.setMenuBar(self.menu_bar)

    def build_instance_menu(self) -> None:
        """
        Build the instance menu
        """
        instance_menu = QMenu('Instance', self)
        instance_menu.addAction(self.add_action)
        instance_menu.addAction(self.edit_action)
        instance_menu.addAction(self.delete_action)
        instance_menu.addSeparator()
        instance_menu.addAction(self.run_action)
        instance_menu.addAction(self.connect_action)
        self.menu_bar.addMenu(instance_menu)

    def build_open_menu(self) -> None:
        """
        Build the open menu
        """
        open_menu = QMenu('Open', self)
        open_menu.addAction(self.open_folder_action)
        open_menu.addAction(self.open_dg_action)
        self.menu_bar.addMenu(open_menu)

    def build_actions_menu(self) -> None:
        """
        Build the actions menu
        """
        actions_menu = QMenu('Actions', self)
        actions_menu.addAction(self.save_action)
        actions_menu.addAction(self.setup_action)
        actions_menu.addAction(self.cancel_action)
        actions_menu.addSeparator()
        actions_menu.addAction(self.kill_processes_action)
        actions_menu.addAction(self.refresh_action)
        self.menu_bar.addMenu(actions_menu)

    def build_config_menu(self) -> None:
        """
        Build the configuration menu
        """
        config_menu = QMenu('Configuration', self)
        config_menu.addAction(self.set_nickname_action)
        config_menu.addAction(self.set_drive_action)
        self.menu_bar.addMenu(config_menu)

    def build_about_menu(self) -> None:
        """
        Build the about menu
        """
        about_menu = QMenu('About', self)
        about_menu.addAction(self.about_action)
        self.menu_bar.addMenu(about_menu)

    def build_statusbar(self) -> None:
        """
        Build bottom status bar
        """
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar_label = QLabel()
        self.statusbar.addPermanentWidget(self.statusbar_label, 100)
        self.refresh_statusbar()

    ###########################################################################
    # Registrations
    ###########################################################################

    def register_stylesheets(self) -> None:
        """
        Register styles
        """
        self.central_widget.setStyleSheet(stylesheet)

    def register_actions(self) -> None:
        """
        Register actions
        """
        self.add_action = \
            QAction(QIcon(':add-icon'), 'Add Instance', self)
        self.edit_action = \
            QAction(QIcon(':edit-icon'), 'Edit Instance', self)
        self.delete_action = \
            QAction(QIcon(':delete-icon'), 'Delete Instance', self)
        self.open_folder_action = \
            QAction(QIcon(':open-folder-icon'), 'Open Folder', self)
        self.open_dg_action = \
            QAction(QIcon(':open-dg-icon'), 'Open DgVoodoo', self)
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
        self.kill_processes_action = \
            QAction(QIcon(':stop-icon'), 'Kill CE and Lobby Process', self)
        self.about_action = \
            QAction(QIcon(':about-icon'), 'About CEHub', self)
        self.set_nickname_action = \
            QAction(QIcon(':profile-icon'), 'Set Profile Nickname', self)
        self.set_drive_action = \
            QAction(QIcon(':drive-icon'), 'Set CD-ROM/ISO Drive', self)

    def register_handlers(self) -> None:
        """
        Register action handlers
        """
        self.add_action.triggered.connect(
            lambda: self.handle_add_action()
        )
        self.edit_action.triggered.connect(
            lambda: self.handle_edit_action()
        )
        self.delete_action.triggered.connect(
            lambda: self.handle_delete_action()
        )
        self.cancel_action.triggered.connect(
            lambda: self.handle_cancel_action()
        )
        self.save_action.triggered.connect(
            lambda: self.handle_save_action()
        )
        self.setup_action.triggered.connect(
            lambda: self.handle_setup_action()
        )
        self.kill_processes_action.triggered.connect(
            lambda: self.handle_kill_ce_processes_action()
        )
        self.refresh_action.triggered.connect(
            lambda: self.handle_refresh_action()
        )
        self.open_folder_action.triggered.connect(
            lambda: self.handle_open_folder_action()
        )
        self.open_dg_action.triggered.connect(
            lambda: self.handle_open_dg_action()
        )
        self.about_action.triggered.connect(
            lambda: self.handle_about_action()
        )
        self.run_action.triggered.connect(
            lambda: self.handle_run_action(False)
        )
        self.connect_action.triggered.connect(
            lambda: self.handle_run_action(True)
        )
        self.set_nickname_action.triggered.connect(
            lambda: self.handle_set_nickname_action()
        )
        self.set_drive_action.triggered.connect(
            lambda: self.handle_set_drive_action()
        )

    ###########################################################################
    # State
    ###########################################################################

    def set_actions_state(self, state: MainWindowStatesEnum) -> None:
        """
        Set current actions state of the window's toolbar and menu
        """
        self.current_state = state
        self.disable_actions()
        if state == MainWindowStatesEnum.NORMAL:
            self.enable_actions_to_normal_state()
        elif state == MainWindowStatesEnum.ADD:
            self.enable_actions_to_adding_state()
        elif state == MainWindowStatesEnum.EDIT:
            self.enable_actions_to_editing_state()
        elif state == MainWindowStatesEnum.INSTANCE_SELECTED:
            self.enable_actions_to_instance_selection_state()
        elif state == MainWindowStatesEnum.RUN:
            self.enable_actions_to_instance_running_state()
        elif state == MainWindowStatesEnum.ABOUT:
            self.enable_actions_to_about_state()

    def disable_actions(self) -> None:
        """
        Disable all actions
        """
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
        self.kill_processes_action.setDisabled(True)

    def enable_actions_to_normal_state(self) -> None:
        """
        Enable the actions for NORMAL state
        """
        self.add_action.setDisabled(False)
        self.refresh_action.setDisabled(False)
        self.kill_processes_action.setDisabled(False)

    def enable_actions_to_adding_state(self) -> None:
        """
        Enable the actions for ADD state
        """
        self.cancel_action.setDisabled(False)
        self.setup_action.setDisabled(False)

    def enable_actions_to_editing_state(self) -> None:
        """
        Enable the actions for EDIT state
        """
        self.cancel_action.setDisabled(False)
        self.save_action.setDisabled(False)

    def enable_actions_to_instance_selection_state(self) -> None:
        """
        Enable the actions for INSTANCE_SELECTED state
        """
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
        self.kill_processes_action.setDisabled(False)

    def enable_actions_to_instance_running_state(self) -> None:
        """
        Enable the actions for RUN state
        """
        self.cancel_action.setDisabled(False)
        self.kill_processes_action.setDisabled(False)

    def enable_actions_to_about_state(self) -> None:
        """
        Enable the actions for ABOUT state
        """
        self.cancel_action.setDisabled(False)

    ###########################################################################
    # Redirects
    ###########################################################################

    def redirect_to_instance_list(self) -> None:
        """
        Redirect to instance list page
        """
        self.set_central_widget(InstanceListFrame(self))
        self.set_actions_state(MainWindowStatesEnum.NORMAL)
        self.register_stylesheets()

    ###########################################################################
    # Handlers
    ###########################################################################

    def handle_about_action(self) -> None:
        """
        Handle click event to about action
        """
        self.set_central_widget(AboutFrame(self))
        self.set_actions_state(MainWindowStatesEnum.ABOUT)

    def handle_run_action(self, connect_tab: bool) -> None:
        """
        Handle click event to run action
        """
        self.set_central_widget(InstanceRunFrame(
            self, self.current_instance, connect_tab
        ))
        self.set_actions_state(MainWindowStatesEnum.RUN)

    def handle_open_folder_action(self) -> None:
        """
        Handle click event to open folder action
        """
        if self.current_instance is not None:
            instance_path = \
                PathService.get_instance_path(self.current_instance.name)
            if os.path.exists(instance_path):
                os.startfile(instance_path)
            else:
                DialogService.error(
                    self,
                    'The instance folder was not found'
                )

    def handle_open_dg_action(self) -> None:
        """
        Handle click event to open DgVoodoo action
        """
        if self.current_instance is not None:
            instance_path = \
                PathService.get_instance_path(self.current_instance.name)
            os.startfile(os.path.join(instance_path, 'dgVoodooCpl.exe'))

    def handle_refresh_action(self) -> None:
        """
        Handle click event to refresh action
        """
        self.refresh_statusbar()
        self.current_instance = None
        self.set_actions_state(MainWindowStatesEnum.NORMAL)
        self.set_current_instance(None)
        if isinstance(self.central_widget, InstanceListFrame):
            self.central_widget.refresh()

    def handle_kill_ce_processes_action(self) -> None:
        """
        Handle click event to kill processes action
        """
        answer = DialogService.question(
            self,
            'Do you realy want to kill the ce.exe and lobby.exe process?'
        )
        if answer:
            ProcessService.kill_ce_processes()
            self.refresh_statusbar()

    def handle_add_action(self) -> None:
        """
        Handle click event to add instance action
        """
        self.set_central_widget(InstanceFormFrame(self))
        self.set_actions_state(MainWindowStatesEnum.ADD)

    def handle_edit_action(self) -> None:
        """
        Handle click event to edit instance action
        """
        self.set_central_widget(InstanceFormFrame(self, self.current_instance))
        self.set_actions_state(MainWindowStatesEnum.EDIT)

    def handle_save_action(self) -> None:
        """
        Handle click event to save instance action
        """
        self.central_widget.save()
        self.refresh_statusbar()
        self.refresh_window_title()
        DialogService.info(self, 'Saved successfully')

    def handle_setup_action(self) -> None:
        """
        Handle click event to setup instance action
        """
        self.central_widget.setup()
        self.refresh_statusbar()
        self.refresh_window_title()

    def handle_cancel_action(self) -> None:
        """
        Handle click event to cancel action
        """
        if self.current_state == MainWindowStatesEnum.INSTANCE_SELECTED:
            if isinstance(self.central_widget, InstanceListFrame):
                self.central_widget.deselect_instances()
            self.set_actions_state(MainWindowStatesEnum.NORMAL)
        elif self.current_state == MainWindowStatesEnum.RUN:
            self.redirect_to_instance_list()
        elif self.current_state == MainWindowStatesEnum.ABOUT:
            self.redirect_to_instance_list()
        else:
            answer = DialogService.question(
                self,
                'Do you really want to cancel?'
            )
            if answer:
                self.redirect_to_instance_list()

    def handle_delete_action(self) -> None:
        """
        Handle click event to delete action
        """
        if self.current_instance is None:
            return
        answer = DialogService.question(
            self,
            f'Do you really want to delete the ' +
            f'"{self.current_instance.name}" instance?'
        )
        if answer:
            try:
                SetupService.delete_instance(self.current_instance)
                self.central_widget.refresh()
                self.set_actions_state(MainWindowStatesEnum.NORMAL)
            except Exception as err:
                print(err)
                DialogService.error(self, str(err))

    def handle_set_nickname_action(self) -> None:
        """
        Handle click event to set nickname action
        """
        data = DataService.get_data()
        nickname, ok = DialogService.input(
            self,
            'Set profile nickname:',
            data.profile.nickname
        )
        if ok:
            try:
                ValidationService.validate_nickname(nickname)
                data.profile.nickname = nickname
                DataService.save_data(data)
                DialogService.info(self, 'Nickname updated successfully')
                self.refresh_statusbar()
                self.refresh_window_title()
            except ValueError as err:
                DialogService.error(self, str(err))

    def handle_set_drive_action(self) -> None:
        """
        Handle click event to set CD-ROM drive action
        """
        data = DataService.get_data()
        answer = DialogService.question(
            self,
            'The Codename Eagle registry drive key will be added/updated in ' +
            'Windows Registry Editor. This action usually needs elevated ' +
            'permission. Proceed?'
        )
        if not answer:
            return
        drive, ok = DialogService.combobox(
            self,
            'Select the CD-ROM/ISO drive:',
            [d + ':' for d in MainWindow.DRIVES],
            data.cd_drive
        )
        if ok:
            try:
                WinRegService.update_drive_key(drive)
                data.cd_drive = drive
                DataService.save_data(data)
                DialogService.info(self, 'Registry updated successfully')
            except Exception as err:
                DialogService.error(self, str(err))

    ###########################################################################
    # Refreshes
    ###########################################################################

    def refresh_window_title(self) -> None:
        """
        Update window top bar title with application TITLE and VERSION
        """
        nickname = DataService.get_data().profile.nickname
        self.setWindowTitle(
            f'{AppInfo.TITLE} {AppInfo.VERSION} ({nickname})'
        )

    def refresh_statusbar(self) -> None:
        """
        Refresh the status bar message with process status and profile
        """
        nickname = DataService.get_data().profile.nickname
        ce_process_status = ProcessService.get_ce_process_status().value
        lobby_process_status = ProcessService.get_lobby_process_status().value
        self.statusbar_label.setText(
            f'Profile: {nickname} / ce.exe: {ce_process_status} / ' +
            f'lobby.exe: {lobby_process_status}'
        )

    ###########################################################################
    # Sets
    ###########################################################################

    def set_current_instance(self, instance: InstanceModel) -> None:
        """
        Set the selected instance of MainWindow
        """
        self.current_instance = instance

    def set_central_widget(self, central_widget: QWidget) -> None:
        """
        Set the central widget
        """
        self.central_widget = central_widget
        self.setCentralWidget(central_widget)
