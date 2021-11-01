from enum import Enum


class InstanceTypeEnum(Enum):
    SP = 'Single Player'
    CLIENT = 'Multiplayer Client'
    SERVER = 'Multiplayer Client/Server'
    DEDICATED = 'Multiplayer Server (Dedicated)'
