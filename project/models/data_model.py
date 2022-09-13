from project.models.connection_model import ConnectionModel
from project.models.instance_model import InstanceModel
from project.models.profile_model import ProfileModel


class DataModel:
    """
    Application Data model
    """

    def __init__(self) -> None:
        """
        Construct a new data model
        """
        self._version: int = 5
        self._profile: ProfileModel = ProfileModel()
        self._instances: list[InstanceModel] = []
        self._connections: list[ConnectionModel] = []
        self._cd_drive: str = 'E:'
        self._ce_exec_file_name: str = 'ce.exe'
        self._register_default_connections()

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def instances(self) -> list[InstanceModel]:
        return self._instances

    @property
    def profile(self) -> ProfileModel:
        return self._profile

    @property
    def connections(self) -> list[ConnectionModel]:
        return self._connections

    @property
    def cd_drive(self) -> str:
        return self._cd_drive

    @property
    def version(self) -> int:
        return self._version

    @property
    def ce_exec_file_name(self) -> str:
        return self._ce_exec_file_name

    @version.setter
    def version(self, new_version: int) -> None:
        self._version = new_version

    @cd_drive.setter
    def cd_drive(self, drive: str) -> None:
        self._cd_drive = drive

    @ce_exec_file_name.setter
    def ce_exec_file_name(self, file_name: str) -> None:
        self._ce_exec_file_name = file_name

    ###########################################################################
    # Public methods
    ###########################################################################

    def add_instance(self, instance: InstanceModel) -> None:
        """
        Add a new instance to instance list
        """
        self._instances.append(instance)

    def get_instance(self, instance_name: str) -> InstanceModel:
        """
        Get the instance buy the name
        """
        instances = list(
            filter(lambda e: e.name == instance_name, self._instances)
        )
        if len(instances) > 0:
            return instances[0]
        else:
            return None

    def delete_instance(self, instance_name: str) -> InstanceModel:
        """
        Delete instance by the name
        """
        for i in range(len(self._instances)):
            if self._instances[i].name == instance_name:
                return self._instances.pop(i)

    def add_connection(self, connection: ConnectionModel) -> None:
        """
        Add a new connection to the list
        """
        self._connections.append(connection)

    def get_connection(self, connection_name: str) -> ConnectionModel:
        """
        Get connection by the name
        """
        connections = list(
            filter(lambda e: e.name == connection_name, self._connections)
        )
        if len(connections) > 0:
            return connections[0]
        else:
            return None

    def delete_connection(self, connection_name: str) -> ConnectionModel:
        """
        Delete connection by the name
        """
        for i in range(len(self._connections)):
            if self._connections[i].name == connection_name:
                return self._connections.pop(i)

    ###########################################################################
    # Private methods
    ###########################################################################

    def _register_default_connections(self) -> None:
        """
        Register default connections to connection list
        """
        self._connections.append(
            ConnectionModel(
                'codenameeaglemultiplayer.com',
                '89.38.98.12:24711'
            )
        )
