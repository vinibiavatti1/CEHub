import copy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from project.models.instance_model import InstanceModel
from project.models.map_model import MapModel
from project.services.map_manager_service import MapManagerService
from project.services.path_service import PathService
from project.services.dialog_service import DialogService
from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QFileDialog,
)


class MapManagerFrame(QFrame):
    """
    Map manager frame
    """

    def __init__(self, main_window, instance: InstanceModel) -> None:
        """
        Construct a new MapManagerFrame
        """
        super().__init__(main_window, objectName='frame')
        self.main_window = main_window
        self.instance = instance
        self.selected_map = None
        self.maps = []
        self._build()
        self._register_handlers()
        self.load_maps_from_levels_nfo_file()
        self.refresh_map_list()

    def _build(self) -> None:
        """
        Build frame
        """
        self.grid = QVBoxLayout()
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.grid)

        # Instance Name
        self.grid.addWidget(QLabel('Instance Name', self))
        self.instance_name_field = QLineEdit()
        self.instance_name_field.setReadOnly(True)
        self.instance_name_field.setText(self.instance.name)
        self.grid.addWidget(self.instance_name_field)

        # Instance path
        self.grid.addWidget(QLabel('Instance Path', self))
        self.instance_path_field = QLineEdit()
        self.instance_path_field.setReadOnly(True)
        self.instance_path_field.setText(
            PathService.get_instance_path(self.instance.name)
        )
        self.grid.addWidget(self.instance_path_field)

        # Map actions label
        self.grid.addWidget(QLabel('Map Actions', self))

        # Actions Frame
        self.horizontal_frame = QFrame()
        self.horizontal_grid = QHBoxLayout()
        self.horizontal_grid.setContentsMargins(0, 0, 0, 0)
        self.horizontal_grid.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.horizontal_frame.setLayout(self.horizontal_grid)
        self.grid.addWidget(self.horizontal_frame)

        # Upload Action
        self.btn_upload_map = QPushButton('Upload Map Folder (zip)', self)
        self.btn_upload_map.setIcon(QIcon(':map-upload-icon'))
        self.horizontal_grid.addWidget(self.btn_upload_map)

        # Export Action
        self.btn_export_map = QPushButton('Export Map Folder (zip)', self)
        self.btn_export_map.setIcon(QIcon(':map-export-icon'))
        self.horizontal_grid.addWidget(self.btn_export_map)
        self.btn_export_map.setDisabled(True)

        # Add Action
        self.btn_add_map = QPushButton('Register Map Record', self)
        self.btn_add_map.setIcon(QIcon(':map-add-icon'))
        self.horizontal_grid.addWidget(self.btn_add_map)

        # Delete Action
        self.btn_delete_map = QPushButton('Delete Map Record', self)
        self.btn_delete_map.setIcon(QIcon(':map-delete-icon'))
        self.horizontal_grid.addWidget(self.btn_delete_map)
        self.btn_delete_map.setDisabled(True)

        # Map list label
        self.grid.addWidget(QLabel('Map List (LEVELS.NFO)', self))

        # Map list
        self.map_list = QListWidget(self)
        self.grid.addWidget(self.map_list)

    ###########################################################################
    # Loaders
    ###########################################################################

    def load_maps_from_levels_nfo_file(self) -> None:
        """
        Load maps from levels.nfo
        """
        try:
            self.maps = MapManagerService.list_maps_from_instance(
                self.instance
            )
        except Exception as err:
            print(err)
            DialogService.error(
                self,
                'An error ocurred while getting the maps of the ' +
                f'instance: {err}. Please, check if the file LEVELS.nfo ' +
                'is not corrupted.'
            )
            self._disable_actions()

    ###########################################################################
    # Refreshes
    ###########################################################################

    def refresh_map_list(self) -> None:
        """
        Refresh the map list
        """
        self.map_list.clear()
        for map in self.maps:
            self.map_list.addItem(str(map))
        self.selected_map = None
        self.btn_delete_map.setDisabled(True)
        self.btn_export_map.setDisabled(True)

    ###########################################################################
    # Handlers
    ###########################################################################

    def _register_handlers(self) -> None:
        """
        Register frame handlers
        """
        self.map_list.currentTextChanged.connect(
            self._handle_map_selection
        )
        self.btn_add_map.clicked.connect(
            self._handle_add_map
        )
        self.btn_upload_map.clicked.connect(
            self._handle_map_upload
        )
        self.btn_export_map.clicked.connect(
            self.handle_map_export
        )
        self.btn_delete_map.clicked.connect(
            self._handle_map_delete
        )

    def _handle_map_selection(self, item: str) -> None:
        """
        Handle map selection event
        """
        if len(item) == 0:
            self.btn_delete_map.setDisabled(True)
            self.btn_export_map.setDisabled(True)
            return
        self.btn_export_map.setDisabled(False)
        self.selected_map = self._convert_map_list_str_to_map_model(item)
        self.btn_delete_map.setDisabled(
            MapManagerService.is_native_map(self.selected_map)
        )

    def _handle_map_upload(self) -> None:
        """
        Handle map upload click
        """
        file, _ = QFileDialog.getOpenFileName(
            self,
            'Select the level zip folder to upload to the instance folder',
            filter='*.zip'
        )
        if len(file) == 0:
            return
        if not MapManagerService.is_map_zip_file_valid(file):
            DialogService.error(
                self,
                f'The selected file is invalid. Check if the file was ' +
                'exported from CEHub. It must contain the ' +
                'level folder in the root, and this folder has to follow ' +
                'the format "LEVEL<number>".'
            )
            return
        try:
            path = MapManagerService.upload_map_zip_file(
                self.instance, file
            )
            DialogService.info(
                self,
                f'Map uploaded successfully to directory: {path}'
            )
        except Exception as err:
            print(err)
            DialogService.error(
                self,
                f'An error ocurred while trying to upload the map: {err}'
            )

    def _handle_add_map(self) -> None:
        """
        Handle add map
        """
        map_name, ok = self._ask_map_name()
        if not ok:
            return
        map_value, ok = self._ask_map_value()
        if not ok:
            return
        map = MapModel(map_name, map_value)
        if not MapManagerService.map_folder_exists(self.instance, map.val):
            DialogService.error(
                self,
                f'The map folder "LEVEL{map.val}" does not exist in the ' +
                'instance folder. Please, do the upload of the map folder ' +
                'before to register it.'
            )
            return
        maps = copy.deepcopy(self.maps)
        maps.append(map)
        try:
            MapManagerService.update_levels_nfo_file(
                self.instance, maps
            )
            self.maps = maps
            self.refresh_map_list()
            DialogService.info(
                self,
                f'The map "{map_name}" with value "{map_value}" was added ' +
                'successfully to LEVELS.NFO file.'
            )
        except Exception as err:
            print(err)
            DialogService.error(
                self,
                f'Could not update the LEVELS.NFO file. Please, check if ' +
                'the file is available and can be writable. Also check ' +
                'the permissions, or try to open the CEHub as Administrator.'
            )

    def handle_map_export(self) -> None:
        """
        Handle map export button click event
        """
        if self.selected_map is None:
            return
        dest = QFileDialog.getExistingDirectory(
            self,
            'Select the directory to export the map.'
        )
        if dest is None or len(dest) == 0:
            return
        try:
            dest = MapManagerService.export_map_as_zip_file(
                self.instance, self.selected_map, dest
            )
            DialogService.info(
                self,
                f'Map exported successfully to path: {dest}.'
            )
        except Exception as err:
            print(err)
            DialogService.error(
                self,
                f'An error ocurred to export the map: {err}'
            )

    def _handle_map_delete(self) -> None:
        """
        Handle map delete button click event
        """
        if self.selected_map is None:
            return
        name = self.selected_map.name
        val = self.selected_map.val
        ok = DialogService.question(
            self,
            f'The map "{name}" with the value "{val}" will be removed ' +
            'from the LEVELS.NFO file. The folder of the map WILL NOT be ' +
            'deleted. Proceed?'
        )
        if not ok:
            return
        maps = copy.deepcopy(self.maps)
        for index, map in enumerate(maps):
            if map.val == val:
                maps.pop(index)
                break
        try:
            MapManagerService.update_levels_nfo_file(self.instance, maps)
            DialogService.info(
                self,
                f'Map removed successfully!'
            )
            self.maps = maps
            self.refresh_map_list()
        except Exception as err:
            print(err)
            DialogService.error(
                self,
                f'Could not remove the map from the file. Please, check if ' +
                'the file is available, or try to execute CEHub as ' +
                'Administrator.'
            )

    ###########################################################################
    # Prompts
    ###########################################################################

    def _ask_map_name(self) -> tuple[str, bool]:
        """
        Open dialog input to ask for a map name
        """
        while True:
            map_name, ok = DialogService.input(
                self, 'Enter the name of the map:'
            )
            if not ok:
                return map_name, ok
            map_name = map_name.strip()
            if len(map_name.strip()) == 0:
                DialogService.error(self, 'The map name is invalid.')
                continue
            return map_name, ok

    def _ask_map_value(self, validate_exist_in_list: bool = True
                       ) -> tuple[str, bool]:
        """
        Open dialog input to ask for a map value
        """
        while True:
            map_value, ok = DialogService.input_int(
                self, 'Enter the number (value) of the map: (128 ~ 999)'
            )
            if not ok:
                return map_value, ok
            found = False
            for map_record in self.maps:
                if map_record.val == map_value:
                    found = True
            if found and validate_exist_in_list:
                DialogService.error(
                    self,
                    f'The map number "{map_value}" already exists in the '
                    'map list.'
                )
                continue
            return map_value, ok

    ###########################################################################
    # Utils
    ###########################################################################

    def _disable_actions(self) -> None:
        """
        Disable map actions
        """
        self.btn_add_map.setDisabled(True)
        self.btn_delete_map.setDisabled(True)
        self.btn_export_map.setDisabled(True)

    def _convert_map_list_str_to_map_model(self, item: str) -> MapModel:
        """
        Convert the item from list to map model
        """
        split = item.split(':')
        map_val = split[0].replace('LEVEL', '').strip()
        map_name = split[1].strip()
        return MapModel(map_name, int(map_val))
