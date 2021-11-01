class ConnectionModel:
    def __init__(self, name: str, address: str) -> None:
        self._name = name
        self._address = address

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address
