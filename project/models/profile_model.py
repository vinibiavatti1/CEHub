class ProfileModel:

    def __init__(self) -> None:
        self._nickname = 'CE Player'

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, name) -> str:
        self._nickname = name
