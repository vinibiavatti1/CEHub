from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QWidget
)
from project.enums.game_map_enum import GameMapEnum
from project.enums.game_team_enum import GameTeamEnum
from project.enums.game_type_enum import GameTypeEnum
from project.models.instance_model import InstanceModel
from project.models.instance_properties_model import InstancePropertiesModel
from project.services.setup_service import SetupService
from project.enums.instance_version_enum import InstanceVersionEnum
from project.enums.instance_type_enum import InstanceTypeEnum
from project.enums.instance_patch_enum import InstancePatchEnum
from project.services.data_service import DataService


class InstanceFormFrame(QFrame):
    """
    Instance form add/edit frame
    """

    DEFAULT_HOST_PORT = 24711

    def __init__(self, main_window, instance: InstanceModel = None) -> None:
        """
        Construct a new InstanceFormFrame
        """
        super().__init__(main_window, objectName='form')
        self.main_window = main_window
        self.instance = instance
        self._build()
        self._register_handlers()
        self._handle_instance_type_field_change(
            InstanceTypeEnum.SP.value
        )
        if self.instance is not None:
            self._fill_form()

    def _build(self):
        """
        Build frame
        """
        container = QVBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        self.setLayout(container)

        # Tabs
        self.tabs = QTabWidget()
        self.instance_tab = QWidget()
        self.client_tab = QWidget()
        self.server_tab = QWidget()
        self.tabs.addTab(self.instance_tab, 'Instance Properties')
        self.tabs.addTab(self.client_tab, 'Client Properties')
        self.tabs.addTab(self.server_tab, 'Server Properties')

        # Layouts
        self.instance_tab_layout = QVBoxLayout()
        self.client_tab_layout = QVBoxLayout()
        self.server_tab_layout = QVBoxLayout()
        self.instance_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.client_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.server_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.instance_tab.setLayout(self.instance_tab_layout)
        self.client_tab.setLayout(self.client_tab_layout)
        self.server_tab.setLayout(self.server_tab_layout)
        container.addWidget(self.tabs)

        # Build forms
        self._build_instance_form()
        self._build_server_form()
        self._build_client_form()

    def _build_instance_form(self) -> None:
        """
        Build the instance form (tab 1)
        """

        # Instance Name
        self.instance_tab_layout.addWidget(QLabel('Instance Name', self))
        self.instance_name_field = QLineEdit(self)
        self.instance_name_field.setPlaceholderText(
            'Enter the instance identifier'
        )
        self.instance_tab_layout.addWidget(self.instance_name_field)

        # Instance Type
        self.instance_tab_layout.addWidget(QLabel('Instance Type', self))
        self.instance_type_field = QComboBox(self)
        for option in InstanceTypeEnum:
            self.instance_type_field.addItem(option.value, option)
        self.instance_tab_layout.addWidget(self.instance_type_field)

        # Instance Version
        self.instance_tab_layout.addWidget(QLabel('Instance Version', self))
        self.instance_version_field = QComboBox(self)
        for option in InstanceVersionEnum:
            self.instance_version_field.addItem(option.value, option)
        self.instance_tab_layout.addWidget(self.instance_version_field)

        # Install Patch
        self.instance_tab_layout.addWidget(QLabel('Instance Patch', self))
        self.instance_patch_field = QComboBox(self)
        for option in InstancePatchEnum:
            self.instance_patch_field.addItem(option.value, option)
        self.instance_tab_layout.addWidget(self.instance_patch_field)

    def _build_client_form(self) -> None:
        """
        Build the client form (tab 2)
        """

        # Team
        self.client_tab_layout.addWidget(QLabel('Team', self))
        self.instance_team_field = QComboBox(self)
        for item in GameTeamEnum:
            self.instance_team_field.addItem(item.value, item)
        self.client_tab_layout.addWidget(self.instance_team_field)

        # Nickname
        self.client_tab_layout.addWidget(QLabel('Nickname', self))
        self.instance_nickname_field = QComboBox(self)
        self.instance_nickname_field.addItem('Use CEHub Profile', None)
        self.instance_nickname_field.addItem('Custom...', 'custom')
        self.client_tab_layout.addWidget(self.instance_nickname_field)

        # Custom Nickname
        self.instance_custom_nickname_field = QLineEdit(self)
        self.instance_custom_nickname_field.setPlaceholderText(
            'Enter the custom nickname'
        )
        self.instance_custom_nickname_field.setDisabled(True)
        self.client_tab_layout.addWidget(self.instance_custom_nickname_field)

        # Focus
        self.instance_name_field.setFocus()

    def _build_server_form(self) -> None:
        """
        Build the server form (tab 3)
        """
        # Host
        self.server_tab_layout.addWidget(QLabel('Host Port', self))
        self.instance_host_field = QComboBox(self)
        self.instance_host_field.addItem(
            'Default port (24711)', InstanceFormFrame.DEFAULT_HOST_PORT
        )
        self.instance_host_field.addItem('Custom...', 'custom')
        self.server_tab_layout.addWidget(self.instance_host_field)

        self.instance_custom_host_field = QSpinBox(self)
        self.instance_custom_host_field.setMinimum(1)
        self.instance_custom_host_field.setMaximum(65535)
        self.instance_custom_host_field.setValue(
            InstanceFormFrame.DEFAULT_HOST_PORT
        )
        self.instance_custom_host_field.setDisabled(True)
        self.server_tab_layout.addWidget(self.instance_custom_host_field)

        # Max Players
        self.server_tab_layout.addWidget(QLabel('Max Players (2-30)', self))
        self.instance_max_players_field = QSpinBox(self)
        self.instance_max_players_field.setMinimum(2)
        self.instance_max_players_field.setMaximum(30)
        self.instance_max_players_field.setValue(16)
        self.server_tab_layout.addWidget(self.instance_max_players_field)

        # Host Name
        self.server_tab_layout.addWidget(QLabel('Host Name', self))
        self.instance_host_name_field = QLineEdit(self)
        self.instance_host_name_field.setPlaceholderText(
            'Enter the name of the host'
        )
        self.server_tab_layout.addWidget(self.instance_host_name_field)

        # Map
        self.server_tab_layout.addWidget(QLabel('Map', self))
        self.instance_map_field = QComboBox(self)
        for option in GameMapEnum:
            self.instance_map_field.addItem(option.value, option)
        self.instance_map_field.addItem('Custom...', 'custom')
        self.server_tab_layout.addWidget(self.instance_map_field)

        # Custom Map
        self.instance_custom_map_field = QLineEdit(self)
        self.instance_custom_map_field.setPlaceholderText(
            'Enter the custom map name'
        )
        self.instance_custom_map_field.setDisabled(True)
        self.server_tab_layout.addWidget(self.instance_custom_map_field)

        # Game Type
        self.server_tab_layout.addWidget(QLabel('Game Type', self))
        self.instance_game_type_field = QComboBox(self)
        for option in GameTypeEnum:
            self.instance_game_type_field.addItem(option.value, option)
        self.server_tab_layout.addWidget(self.instance_game_type_field)

    def _fill_form(self) -> None:
        """
        Fill form with instance data
        """
        props = self.instance.properties

        # Instance Tab
        self.instance_name_field.setText(
            self.instance.name
        )
        self.instance_name_field.setDisabled(True)
        self.instance_type_field.setCurrentText(
            self.instance.type
        )
        self.instance_type_field.setDisabled(True)
        self.instance_version_field.setCurrentText(
            self.instance.version
        )
        self.instance_version_field.setDisabled(True)
        self.instance_patch_field.setCurrentText(
            self.instance.patch
        )
        self.instance_patch_field.setDisabled(True)

        # Client tab
        self.instance_team_field.setCurrentText(
            props.team
        )
        self.instance_nickname_field.setCurrentIndex(0)
        if props.custom_nickname:
            self.instance_nickname_field.setCurrentIndex(1)
            self.instance_custom_nickname_field.setText(
                props.nickname
            )

        # Server tab
        self.instance_host_field.setCurrentIndex(0)
        if props.custom_port:
            self.instance_host_field.setCurrentIndex(1)
            self.instance_custom_host_field.setValue(
                props.port
            )
        self.instance_max_players_field.setValue(
            props.max_players
        )
        self.instance_host_name_field.setText(
            props.hostname
        )
        if props.custom_map:
            self.instance_map_field.setCurrentIndex(7)
            self.instance_custom_map_field.setText(
                props.map
            )
        else:
            self.instance_map_field.setCurrentText(
                props.map
            )
        self.instance_game_type_field.setCurrentText(
            props.game_type
        )

    ###########################################################################
    # Handlers
    ###########################################################################

    def _register_handlers(self) -> None:
        """
        Register input handlers
        """
        self.instance_type_field.currentTextChanged.connect(
            self._handle_instance_type_field_change
        )
        self.instance_version_field.currentTextChanged.connect(
            self.handle_instance_version_field_change
        )
        self.instance_nickname_field.currentTextChanged.connect(
            self.handle_instance_nickname_field_change
        )
        self.instance_map_field.currentTextChanged.connect(
            self.handle_instance_map_field_change
        )
        self.instance_host_field.currentTextChanged.connect(
            self.handle_instance_host_field_change
        )

    def handle_instance_host_field_change(self, value) -> None:
        """
        Handle instance host field change event
        """
        self.instance_custom_host_field.setDisabled(True)
        self.instance_custom_host_field.setValue(
            InstanceFormFrame.DEFAULT_HOST_PORT
        )
        if value == 'Custom...':
            self.instance_custom_host_field.setDisabled(False)
            self.instance_custom_host_field.setFocus()

    def handle_instance_map_field_change(self, value) -> None:
        """
        Handle instance map field change event
        """
        self.instance_custom_map_field.setDisabled(True)
        self.instance_custom_map_field.setText('')
        if value == 'Custom...':
            self.instance_custom_map_field.setDisabled(False)
            self.instance_custom_map_field.setFocus()

    def handle_instance_nickname_field_change(self, value) -> None:
        """
        Handle instance nickname field change event
        """
        self.instance_custom_nickname_field.setDisabled(True)
        self.instance_custom_nickname_field.setText('')
        if value == 'Custom...':
            self.instance_custom_nickname_field.setDisabled(False)
            self.instance_custom_nickname_field.setFocus()

    def handle_instance_version_field_change(self, value) -> None:
        """
        Handle instance version field change event
        """
        self.instance_patch_field.setDisabled(False)
        if value == InstanceVersionEnum.MP_DEMO_DAFOOSA.value:
            self.instance_patch_field.setCurrentIndex(3)
            self.instance_patch_field.setDisabled(True)
        elif value == InstanceVersionEnum.MP_DEMO_MYG.value:
            self.instance_patch_field.setCurrentIndex(3)
            self.instance_patch_field.setDisabled(True)
        elif value == InstanceVersionEnum.MP_DEMO_OFFICIAL.value:
            self.instance_patch_field.setCurrentIndex(0)
            self.instance_patch_field.setDisabled(True)

    def _handle_instance_type_field_change(self, value) -> None:
        """
        Handle instance type field change event
        """
        self.server_tab.setDisabled(False)
        self.client_tab.setDisabled(False)
        self.instance_version_field.setDisabled(False)
        self.instance_patch_field.setCurrentIndex(0)
        for i in range(self.instance_patch_field.count()):
            self.instance_patch_field.model().item(i).setEnabled(True)

        if value == InstanceTypeEnum.SP.value:
            self.server_tab.setDisabled(True)
            self.client_tab.setDisabled(True)
            self.instance_version_field.setCurrentIndex(0)
            self.instance_version_field.setDisabled(True)
            self.instance_patch_field.setDisabled(True)
            self.instance_patch_field.setCurrentIndex(0)
        else:
            self.instance_version_field.setCurrentIndex(3)
            self.instance_patch_field.setCurrentIndex(3)
            if value == InstanceTypeEnum.CLIENT.value:
                self.server_tab.setDisabled(True)
            elif value == InstanceTypeEnum.DEDICATED.value:
                self.client_tab.setDisabled(True)

    ###########################################################################
    # Validations
    ###########################################################################

    def validate_forms(self, edit: bool = False) -> bool:
        try:
            if not edit:
                self._validate_instance_form()
            instance_type = self.instance_type_field.currentText()
            if instance_type == InstanceTypeEnum.CLIENT.value:
                self._validate_client_form()
            elif instance_type == InstanceTypeEnum.SERVER.value:
                self._validate_client_form()
                self._validate_server_form()
            elif instance_type == InstanceTypeEnum.DEDICATED.value:
                self._validate_server_form()
            return True
        except ValueError as err:
            message = QMessageBox()
            message.warning(self, '', str(err))
            return False

    def _validate_instance_form(self) -> None:
        """
        Validate instance form
        """
        instance_name = self.instance_name_field.text()
        if len(instance_name.strip()) == 0:
            self.instance_name_field.setFocus()
            self.tabs.setCurrentIndex(0)
            raise ValueError('The instance name is required')
        for instance in DataService.get_data().instances:
            if instance.name == instance_name:
                self.instance_name_field.setFocus()
                self.tabs.setCurrentIndex(0)
                raise ValueError(
                    f'The name "{instance_name}" is already being used to \
                    other instance.'
                )

    def _validate_client_form(self) -> None:
        if self.instance_nickname_field.currentIndex() == 'Custom...':
            custom_nickname = self.instance_custom_nickname_field.text()
            if not custom_nickname:
                self.tabs.setCurrentIndex(1)
                self.instance_custom_nickname_field.setFocus()
                raise ValueError('The custom nickname must be set')
            elif len(custom_nickname) > 10:
                self.tabs.setCurrentIndex(1)
                self.instance_custom_nickname_field.setFocus()
                raise ValueError(
                    'The custom nickname has a limit of 10 characters'
                )

    def _validate_server_form(self) -> None:
        hostname = self.instance_host_name_field.text()
        if not hostname:
            self.tabs.setCurrentIndex(2)
            self.instance_host_name_field.setFocus()
            raise ValueError('The hostname is required')
        if self.instance_map_field.currentText() == 'Custom...':
            if not self.instance_custom_map_field.text():
                self.tabs.setCurrentIndex(2)
                self.instance_custom_map_field.setFocus()
                raise ValueError('The custom map must be set')

    ###########################################################################
    # Actions
    ###########################################################################

    def setup(self) -> None:
        """
        Call the SetupService to install the instance
        """
        if self.validate_forms():
            confirm = QMessageBox()
            answer = confirm.question(
                self,
                'Confirmation',
                'The instance will be installed. Proceed?'
            )
            if answer == QMessageBox.Yes:
                instance = self.create_instance_model()
                try:
                    SetupService.install_instance(instance)
                    feedback = QMessageBox()
                    feedback.information(
                        self,
                        'Information',
                        f'Instance "{instance.name}" installed successfully'
                    )
                    data = DataService.get_data()
                    data.instances.append(instance)
                    DataService.save_data(data)
                    self.parent().regirect_to_instance_list()
                except Exception as err:
                    message = QMessageBox()
                    message.critical(self, 'Error', str(err))

    def save(self):
        """
        Save the instance data
        """
        if self.validate_forms(True):
            confirm = QMessageBox()
            answer = confirm.question(
                self,
                'Confirmation',
                'Save changes?'
            )
            if answer == QMessageBox.Yes:
                instance = self.create_instance_model()
                data = DataService.get_data()
                for instance_ in data.instances:
                    if instance_.name == instance.name:
                        data.instances.remove(instance_)
                        data.instances.append(instance)
                        break
                DataService.save_data(data)
                self.main_window.regirect_to_instance_list()

    ###########################################################################
    # Form models
    ###########################################################################

    def create_instance_model(self) -> InstanceModel:
        """
        Create the instance model by the forms
        """
        instance_properties = InstancePropertiesModel()

        # Common data
        instance_properties.game_type = \
            self.instance_game_type_field.currentText()
        instance_properties.hostname = \
            self.instance_host_name_field.text()
        instance_properties.max_players = \
            self.instance_max_players_field.value()
        instance_properties.team = \
            self.instance_team_field.currentText()

        # Custom data
        if self.instance_host_field.currentText() == 'Custom...':
            instance_properties.custom_port = True
            instance_properties.port = \
                self.instance_custom_host_field.value()
        else:
            instance_properties.port = None
        if self.instance_map_field.currentText() == 'Custom...':
            instance_properties.custom_map = True
            instance_properties.map = \
                self.instance_custom_map_field.text()
        else:
            instance_properties.map = \
                self.instance_map_field.currentText()
        if self.instance_nickname_field.currentText() == 'Custom...':
            instance_properties.custom_nickname = True
            instance_properties.nickname = \
                self.instance_custom_nickname_field.text()
        else:
            instance_properties.nickname = None

        # General data
        instance = InstanceModel(
            self.instance_name_field.text(),
            self.instance_version_field.currentText(),
            self.instance_type_field.currentText(),
            self.instance_patch_field.currentText(),
            instance_properties
        )
        return instance
