import winreg


class WinRegService:
    """
    Windows registry service
    """

    CE_SRCDISK_LOCATION = \
        'SOFTWARE\\WOW6432Node\\Take2\\Codename Eagle\\SrcDisk'

    @classmethod
    def update_drive_key(cls, drive: str) -> None:
        """
        Update Codename Eagle Drive key
        """
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, cls.CE_SRCDISK_LOCATION)
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            cls.CE_SRCDISK_LOCATION,
            0,
            winreg.KEY_WRITE
        )
        winreg.SetValueEx(key, 'Drive', 0, winreg.REG_SZ, drive)
        winreg.CloseKey(key)
