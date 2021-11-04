import sys
import os
from project.enums.game_zip_enum import GameZipEnum


class PathUtils:
    """
    Path utilities
    """

    @classmethod
    def get_instance_path(cls, instance_name: str) -> str:
        """
        Get instance path by the instance name
        """
        return os.path.join(cls.get_current_dir(), 'instances', instance_name)

    @classmethod
    def get_game_zip_path(cls, game_zip: GameZipEnum) -> str:
        """
        Get game zip path by game zip enum
        """
        return os.path.join(cls.get_current_dir(), 'game', game_zip.value)

    @classmethod
    def get_data_file_path(cls) -> str:
        """
        Get data file path
        """
        return os.path.join(cls.get_current_dir(), 'data', 'data.dat')

    @classmethod
    def get_current_dir(cls) -> str:
        """
        Get current dir depending the way the app is running: .exe or .py
        """
        if getattr(sys, 'frozen', False):
            return os.getcwd()
        elif __file__:
            return os.path.dirname(sys.argv[0])
