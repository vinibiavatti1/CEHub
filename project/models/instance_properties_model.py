class InstancePropertiesModel:
    def __init__(self) -> None:
        # Client
        self._team: str = None
        self._nickname: str = None
        self._custom_nickname: bool = False

        # Server
        self._hostname: str = None
        self._port: int = None
        self._custom_port: bool = False
        self._max_players: int = None
        self._game_type: str = None
        self._map: str = None
        self._custom_map: bool = False

        # Connection
        self._last_connection_index: int = None

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def team(self) -> str:
        return self._team

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def port(self) -> int:
        return self._port

    @property
    def max_players(self) -> int:
        return self._max_players

    @property
    def game_type(self) -> str:
        return self._game_type

    @property
    def map(self) -> str:
        return self._map

    @property
    def custom_nickname(self) -> bool:
        return self._custom_nickname

    @property
    def custom_port(self) -> bool:
        return self._custom_port

    @property
    def custom_map(self) -> bool:
        return self._custom_map

    @property
    def last_connection_index(self) -> int:
        return self._last_connection_index

    @team.setter
    def team(self, _team: str) -> None:
        self._team = _team

    @nickname.setter
    def nickname(self, _nickname: str) -> None:
        self._nickname = _nickname

    @hostname.setter
    def hostname(self, _hostname: str) -> None:
        self._hostname = _hostname

    @port.setter
    def port(self, _port: int) -> None:
        self._port = _port

    @max_players.setter
    def max_players(self, _max_players: int) -> None:
        self._max_players = _max_players

    @game_type.setter
    def game_type(self, _game_type: str) -> None:
        self._game_type = _game_type

    @map.setter
    def map(self, _map: str) -> None:
        self._map = _map

    @custom_nickname.setter
    def custom_nickname(self, _custom: bool) -> None:
        self._custom_nickname = _custom

    @custom_port.setter
    def custom_port(self, _custom: bool) -> None:
        self._custom_port = _custom

    @custom_map.setter
    def custom_map(self, _custom: bool) -> None:
        self._custom_map = _custom

    @last_connection_index.setter
    def last_connection_index(self, _index: int) -> None:
        self._last_connection_index = _index