class InstancePropertiesModel:
    def __init__(self) -> None:
        # Client
        self._team: str = None
        self._nickname: str = None

        # Server
        self._hostname: str = None
        self._port: int = None
        self._max_players: int = None
        self._game_type: str = None
        self._map: str = None

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
