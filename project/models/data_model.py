from project.models.connection_model import ConnectionModel
from project.models.instance_model import InstanceModel
from project.models.profile_model import ProfileModel


class DataModel:
    def __init__(self) -> None:
        self._profile: ProfileModel = ProfileModel()
        self._instances: list[InstanceModel] = []
        self._connections: list[ConnectionModel] = []

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

    ###########################################################################
    # Methods
    ###########################################################################

    def add_instance(self, instance: InstanceModel) -> None:
        self._instances.append(instance)

    def get_instance(self, instance_name: str) -> InstanceModel:
        instances = list(
            filter(lambda e: e.name == instance_name, self._instances)
        )
        if len(instances) > 0:
            return instances[0]
        else:
            return None

    def delete_instance(self, instance_name: str) -> InstanceModel:
        for i in range(len(self._instances)):
            if self._instances[i].name == instance_name:
                return self._instances.pop(i)

    def add_connection(self, connection: ConnectionModel) -> None:
        self._connections.append(connection)

    def get_connection(self, connection_name: str) -> ConnectionModel:
        connections = list(
            filter(lambda e: e.name == connection_name, self._connections)
        )
        if len(connections) > 0:
            return connections[0]
        else:
            return None

    def delete_connection(self, connection_name: str) -> ConnectionModel:
        for i in range(len(self._connections)):
            if self._connections[i].name == connection_name:
                return self._connections.pop(i)
