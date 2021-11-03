from enum import Enum


class InstanceTypeEnum(Enum):
    SP = 'Single Player'
    CLIENT = 'Multiplayer Client'
    SERVER = 'Multiplayer Server'
    DEDICATED = 'Multiplayer Server (Dedicated)'
