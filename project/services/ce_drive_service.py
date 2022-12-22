import os


class CEDriveService:
    """
    CE Unity Drive service
    """

    DRIVE_VALIDATE_FILES: tuple[str] = ('CODENAME.ICO', 'CESPY.ICO')

    @classmethod
    def validate_ce_drive_exists(cls, drive: str) -> bool:
        """
        Validate if the CD or ISO drive is set by checking CD files. Only one
        valid file is required to validate the CD data.
        """
        for file in CEDriveService.DRIVE_VALIDATE_FILES:
            path = f'{drive}\\{file}'
            if os.path.exists(path):
                return True
        return False
