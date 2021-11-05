class ValidationService:
    """
    Validation service
    """

    @classmethod
    def validate_nickname(cls, nickname: str) -> None:
        """
        Validate the nickname by the CE rules
        """
        nickname = nickname.strip()
        if len(nickname) == 0:
            raise ValueError(
                'The nickname is invalid'
            )
        if len(nickname) > 10:
            raise ValueError(
                'The nickname has a limit of 10 characters'
            )
