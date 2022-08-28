class MapModel:
    """
    Object to represent a map
    """
    def __init__(self, name: str, val: int) -> None:
        self.__name = name
        self.__val = val

    @property
    def name(self) -> str:
        return self.__name

    @property
    def val(self) -> int:
        return self.__val

    def __str__(self) -> str:
        return f'LEVEL {self.val}: {self.name}'
