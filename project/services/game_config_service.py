from project.models.instance_model import InstanceModel
from project.services.path_service import PathService
import os


class GameConfigService:
    """
    Game configuration service
    """

    DEFAULT_FOV: int = 200
    DEFAULT_MOUSE_SENS: int = 9
    DEFAULT_LATENCY: int = 0
    DEFAULT_VIEWDIST: int = 3000
    FILE_NAME: str = 'default.cfg'

    @classmethod
    def save_game_configuration(cls, instance: InstanceModel) -> None:
        """
        Save game configuration to default.cfg file in instance
        """
        instance_path = PathService.get_instance_path(instance.name)
        default_cfg_path = f'{instance_path}/{cls.FILE_NAME}'
        game_configuration = cls.generate_default_cfg_content(instance)
        with open(default_cfg_path, 'w+') as file:
            file.write(game_configuration)

    @classmethod
    def generate_default_cfg_content(cls, instance: InstanceModel) -> str:
        """
        Generate default cfg configuration content
        """
        content: list[str] = []
        content.append(f'fov {instance.properties.fov}')
        content.append(f'mousesens {instance.properties.mousesens}')
        content.append(f'latency {instance.properties.latency}')
        content.append(f'viewdist {instance.properties.viewdist}')
        return '\n'.join(content)
