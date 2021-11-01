class InstanceModel:
    def __init__(self, name: str, version: str, type: str, patch: str,
                 properties: str) -> None:
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
    def properties(self) -> str:
        return self._properties
