from enum import Enum


class GameTypeEnum(Enum):
    """
    CE multiplayer game type enum
    """
    CTF = 'ctf'
    DEATHMATCH = 'deathmatch'
    TEAMPLAY = 'teamplay'
