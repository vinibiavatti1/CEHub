from enum import Enum


class InstanceTypeEnum(Enum):
    """
    Instance type enum
    """
    SP = 'Single Player'
    CLIENT = 'Multiplayer Client'
    SERVER = 'Multiplayer Server'
    DEDICATED = 'Multiplayer Server (Dedicated)'
