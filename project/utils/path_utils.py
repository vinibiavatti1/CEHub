import sys
import os
from project.enums.game_zip_enum import GameZipEnum


class PathUtils:

    @classmethod
    def get_instance_path(cls, instance_name: str) -> str:
        return os.path.join(cls.get_current_dir(), 'instances', instance_name)

    @classmethod
    def get_game_zip_path(cls, game_zip: GameZipEnum) -> str:
        return os.path.join(cls.get_current_dir(), 'game', game_zip.value)

    @classmethod
    def get_data_path(cls) -> str:
        return os.path.join(cls.get_current_dir(), 'data')

    @classmethod
    def get_data_file_path(cls) -> str:
        return os.path.join(cls.get_data_path(), 'data.dat')

    @classmethod
    def get_current_dir(cls) -> str:
        if getattr(sys, 'frozen', False):
            return os.getcwd()
        elif __file__:
            return os.path.dirname(sys.argv[0])
