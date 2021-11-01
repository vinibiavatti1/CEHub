import sys
import os

from project.enums.game_zip_enum import GameZipEnum


APP_DIR = sys.path[0]


class PathUtils:
    INSTANCE_PATH = os.path.join(APP_DIR, 'instances')
    GAME_ZIPS_PATH = os.path.join(APP_DIR, 'game_zips')
    DATA_PATH = os.path.join(APP_DIR, 'data')
    DAT_FILE: str = os.path.join(DATA_PATH, 'data.dat')

    @classmethod
    def get_instance_path(cls, instance_name) -> str:
        return os.path.join(cls.INSTANCE_PATH, instance_name)

    @classmethod
    def get_game_zip_path(cls, game_zip: GameZipEnum) -> str:
        return os.path.join(cls.GAME_ZIPS_PATH, game_zip.value)
