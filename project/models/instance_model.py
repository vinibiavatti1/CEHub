from project.models.instance_properties_model import InstancePropertiesModel


class InstanceModel:
    """
    Instance model
    """

    def __init__(self, name: str, version: str, type: str, patch: str,
                 properties: InstancePropertiesModel) -> None:
        """
        Construct a new instance model
        """
        self._name = name
        self._version = version
        self._type = type
        self._patch = patch
        self._properties = properties

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def type(self) -> str:
        return self._type

    @property
    def patch(self) -> str:
        return self._patch

    @property
    def properties(self) -> InstancePropertiesModel:
        return self._properties
