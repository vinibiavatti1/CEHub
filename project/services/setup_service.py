from project.enums.game_zip_enum import GameZipEnum as ZipEnum
from project.enums.instance_patch_enum import InstancePatchEnum
from project.enums.instance_version_enum import InstanceVersionEnum
from project.models.instance_model import InstanceModel
from project.utils.path_utils import PathUtils
import zipfile
import os


class SetupService:

    ###########################################################################
    # Public methods
    ###########################################################################

    @classmethod
    def install_instance(cls, instance: InstanceModel) -> None:
        """
        Install an instance by its version to /instances folder
        """
        print(f'Installing {instance.name} instance...')
        cls.create_instance_folder(instance.name)
        if instance.version == InstanceVersionEnum.FULL.value:
            cls._install_full_version(instance)
        elif instance.version == InstanceVersionEnum.MP_DEMO_OFFICIAL.value:
            cls._install_mp_demo_official(instance)
        elif instance.version == InstanceVersionEnum.MP_DEMO_DAFOOSA.value:
            cls._install_mp_demo_dafoosa(instance)
        elif instance.version == InstanceVersionEnum.MP_DEMO_MYG.value:
            cls._install_mp_demo_myg(instance)
        cls._unzip_game_file(ZipEnum.ZIP_DGVOODOO, instance.name)

    ###########################################################################
    # Private methods
    ###########################################################################

    @classmethod
    def create_instance_folder(cls, instance_name: str) -> None:
        """
        Create instance directory
        """
        instance_path = PathUtils.get_instance_path(instance_name)
        os.mkdir(instance_path)

    @classmethod
    def _install_full_version(cls, instance: InstanceModel) -> None:
        """
        Install the full version
        """
        name = instance.name
        cls._unzip_game_file(ZipEnum.ZIP_FULL_VERSION, name)
        if instance.patch == InstancePatchEnum.PATCH_141.value:
            cls._unzip_game_file(ZipEnum.ZIP_PATCH_141, name)
        elif instance.patch == InstancePatchEnum.PATCH_142.value:
            cls._unzip_game_file(ZipEnum.ZIP_PATCH_141, name)
            cls._unzip_game_file(ZipEnum.ZIP_PATCH_142, name)
        elif instance.patch == InstancePatchEnum.PATCH_143.value:
            cls._unzip_game_file(ZipEnum.ZIP_PATCH_143, name)

    @classmethod
    def _install_mp_demo_official(cls, instance: InstanceModel) -> None:
        """
        Install the multiplayer demo official version
        """
        cls._unzip_game_file(ZipEnum.ZIP_MP_DEMO_OFFICIAL, instance.name)

    @classmethod
    def _install_mp_demo_dafoosa(cls, instance: InstanceModel) -> None:
        """
        Install the multiplayer demo (dafoosa's version)
        """
        cls._unzip_game_file(ZipEnum.ZIP_DAFOOSA, instance.name)

    @classmethod
    def _install_mp_demo_myg(cls, instance: InstanceModel) -> None:
        """
        Install the multiplayer demo (Myg's version)
        """
        cls._unzip_game_file(ZipEnum.ZIP_MYG, instance.name)

    ###########################################################################
    # Utils
    ###########################################################################

    @classmethod
    def _unzip_game_file(cls, game_zip: ZipEnum,
                         instance_name: str, folder: str = None) -> None:
        """
        Unzip the game_zip file to the instance directory
        """
        zip_path = PathUtils.get_game_zip_path(game_zip)
        instance_path = PathUtils.get_instance_path(instance_name)
        if folder:
            instance_path = os.path.join(instance_path, folder)
        print(f'Unzipping {zip_path} to {instance_path}')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(instance_path)
