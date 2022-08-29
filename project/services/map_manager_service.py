import zipfile
from project.models.instance_model import InstanceModel
from project.models.map_model import MapModel
from project.services.path_service import PathService
import re
import os

from project.utils.zip_utils import ZipUtils


class MapManagerService:
    """
    Service with logic for map manager

    Levels.nfo example:
    Name:No mans land Val:128
    Name:Breakpoint Val:129
    Name:The palace Val:130
    Name:Carrier war Val:131
    Name:The airbase Val:132
    Name:Fortress Val:133
    Name:Fever valley Val:134
    """
    NATIVE_MAPS: list[int] = [128, 129, 130, 131, 132, 133, 134]
    MAP_RECORDS_FILE: str = 'LEVELS.nfo'
    MAP_RECORD_NAME_KEY: str = 'Name:'
    MAP_RECORD_VALUE_KEY: str = 'Val:'
    LEVEL_FOLDER_NAME: str = 'LEVEL'

    @classmethod
    def list_maps_from_instance(cls, instance: InstanceModel
                                ) -> list[MapModel]:
        """
        List the maps from an instance checking the levels.nfo file
        """
        levels_nfo = cls.get_levels_nfo_path(instance)
        with open(levels_nfo, 'r') as file:
            maps_str = file.readlines()
        return cls.map_levels_nfo_to_map_models(maps_str)

    @classmethod
    def map_levels_nfo_to_map_models(cls, levels_nfo_content: list[str]
                                     ) -> list[MapModel]:
        """
        Convert str levels.nfo file format to map model list
        """
        map_list: list[MapModel] = []
        for line in levels_nfo_content:
            stripped_line = line.strip()
            if len(stripped_line) == 0:
                continue
            if cls.MAP_RECORD_VALUE_KEY not in stripped_line:
                continue
            map_record_str = stripped_line.split(cls.MAP_RECORD_VALUE_KEY)
            if len(map_record_str) != 2:
                continue
            map_name = map_record_str[0].replace(
                cls.MAP_RECORD_NAME_KEY, ''
            ).strip()
            map_val = map_record_str[1].strip()
            try:
                map_val = int(map_val)
            except ValueError as err:
                print(err)
                continue
            map_list.append(MapModel(map_name, map_val))
        return map_list

    @classmethod
    def is_native_map(cls, map: MapModel) -> bool:
        """
        Return True if the map is native
        """
        return map.val in cls.NATIVE_MAPS

    @classmethod
    def get_levels_nfo_path(cls, instance: InstanceModel) -> str:
        """
        Get the path to access levels.nfo
        """
        instance_path = PathService.get_instance_path(instance.name)
        return instance_path + f'/{cls.MAP_RECORDS_FILE}'

    @classmethod
    def map_folder_exists(cls, instance: InstanceModel, map_value: int
                          ) -> bool:
        """
        Return True if the map folder exists
        """
        instance_path = PathService.get_instance_path(instance.name)
        path = instance_path + f'/{cls.LEVEL_FOLDER_NAME}{map_value}'
        return os.path.exists(path)

    @classmethod
    def update_levels_nfo_file(cls, instance: InstanceModel,
                               maps: list[MapModel]) -> None:
        """
        Update the levels.nfo file by a list of MapModel
        """
        if len(maps) == 0:
            return
        path = cls.get_levels_nfo_path(instance)
        content = cls.generate_levels_nfo_content(maps)
        print(content)
        with open(path, 'w') as file:
            file.write(content)

    @classmethod
    def generate_levels_nfo_content(cls, maps: list[MapModel]) -> str:
        """
        Generate LEVELS.nfo file format content
        """
        content = ''
        for map in maps:
            content += f'{cls.MAP_RECORD_NAME_KEY}{map.name} '
            content += f'{cls.MAP_RECORD_VALUE_KEY}{map.val}'
            content += '\n'
        return content

    @classmethod
    def create_level_folder(cls, instance: InstanceModel, map_value: int
                            ) -> str:
        """
        Create a new level folder in the instance directory
        """
        if cls.map_folder_exists(instance, map_value):
            raise ValueError(
                f'The map folder with the map value {map_value} already ' +
                'exists.'
            )
        path = PathService.get_instance_path(instance.name)
        path += f'/{cls.LEVEL_FOLDER_NAME}{map_value}'
        os.mkdir(path)
        return path

    @classmethod
    def upload_map_zip_file(cls, instance: InstanceModel, zip_path: str
                            ) -> str:
        """
        Upload the zip map folder to instance
        """
        path = PathService.get_instance_path(instance.name)
        with zipfile.ZipFile(zip_path, 'r') as zip:
            zip.extractall(path)
        return path

    @classmethod
    def export_map_as_zip_file(cls, instance: InstanceModel, map: MapModel,
                               dest: str) -> str:
        """
        Export a map folder to zip file
        """
        if not cls.map_folder_exists(instance, map.val):
            raise ValueError(
                f'The map folder with the map value {map.val} does not ' +
                'exist.'
            )
        instance_path = PathService.get_instance_path(instance.name)
        path = instance_path + f'/{cls.LEVEL_FOLDER_NAME}{map.val}'
        dest = f'{dest}/{cls.LEVEL_FOLDER_NAME}{map.val}_{map.name}.zip'
        ZipUtils.make_zip_archive(
            path,
            dest
        )
        return dest

    @classmethod
    def is_map_zip_file_valid(cls, path: str) -> bool:
        """
        Check if the map zip file is valid to upload
        """
        file = zipfile.ZipFile(path)
        files = file.namelist()
        if len(files) == 0:
            return False
        if not re.match(r'level[0-9]{3}', files[0].lower()):
            return False
        return True
