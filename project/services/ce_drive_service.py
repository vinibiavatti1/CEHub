import os


class CEDriveService:
    """
    CE Unity Drive service
    """

    DRIVE_VALIDATE_FILE: str = 'CODENAME.ICO'

    @classmethod
    def validate_ce_drive_exists(cls, drive: str) -> bool:
        """
        Validate if the CD or ISO drive is set
        """
        path = f'{drive}\\{cls.DRIVE_VALIDATE_FILE}'
        return os.path.exists(path)
