class ProfileModel:
    """
    Profile model
    """

    def __init__(self) -> None:
        """
        Construct a new profile model
        """
        self._nickname = 'CE Player'

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, name) -> str:
        self._nickname = name
