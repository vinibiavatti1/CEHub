from project.enums.instance_type_enum import InstanceTypeEnum
from project.models.instance_model import InstanceModel
from project.utils.path_utils import PathUtils
import os


class CommandLineService:
    """
    Service to execute and generate command line arguments for instance
    execution
    """

    CE_EXE_NAME: str = 'ce.exe'

    ###########################################################################
    # Public methods
    ###########################################################################

    @classmethod
    def generate_arguments(cls, instance: InstanceModel,
                           profile_nickname: str, connect: str = None) -> str:
        """
        Generate command line arguments to ce.exe execution. The available
        arguments are:

        Connection Arguments:
            +connect 132.42.12.1:24711

        Server Arguments:
            +host [PORT_VALUE]
            +maxplayers 2-30
            +hostname "internal war"
            +map "no mans land"
            +game "deathmatch" [values: deathmatch,ctf or teamplay]
            +dedicated"

        Client Arguments:
            +name "joe black"
            +team "red" [values: red,blue or auto]
        """
        arguments = [CommandLineService.CE_EXE_NAME]
        if instance.type == InstanceTypeEnum.CLIENT.value:
            arguments.append(cls._generate_client_arguments(
                instance, profile_nickname, connect
            ))
        elif instance.type == InstanceTypeEnum.SERVER.value:
            arguments.append(cls._generate_server_arguments(
                instance
            ))
            arguments.append(cls._generate_client_arguments(
                instance, profile_nickname
            ))
        elif instance.type == InstanceTypeEnum.DEDICATED.value:
            arguments.append(cls._generate_server_arguments(
                instance
            ))
        return ' '.join(arguments)

    ###########################################################################
    # Private methods
    ###########################################################################

    @classmethod
    def _generate_client_arguments(cls, instance: InstanceModel,
                                   profile_nickname: str,
                                   connect: str = None) -> str:
        """
        Generate command line argument for a client type instance
        """
        arguments = []
        if connect is not None:
            arguments.append(f'+connect {connect}')
        arguments.append(f'+team "{instance.properties.team}"')
        if instance.properties.custom_nickname:
            arguments.append(f'+name "{instance.properties.nickname}"')
        else:
            arguments.append(f'+name "{profile_nickname}"')
        return ' '.join(arguments)


    @classmethod
    def _generate_server_arguments(cls, instance: InstanceModel) -> str:
        """
        Generate command line argument for a server type instance
        """
        arguments = []
        if instance.properties.custom_port:
            arguments.append(f'+host {instance.properties.port}')
        else:
            arguments.append('+host')
        arguments.append(f'+maxplayers {instance.properties.max_players}')
        arguments.append(f'+hostname "{instance.properties.hostname}"')
        arguments.append(f'+map "{instance.properties.map}"')
        arguments.append(f'+game "{instance.properties.game_type}"')
        if instance.type == InstanceTypeEnum.DEDICATED.value:
            arguments.append('+dedicated')
        return ' '.join(arguments)
