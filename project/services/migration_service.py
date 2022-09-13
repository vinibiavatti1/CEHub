from project.models.data_model import DataModel


class MigrationService:
    """
    Data migration service
    """

    @classmethod
    def migrate_data(self, data: DataModel) -> DataModel:
        """
        Update old data file by the current version
        """
        if data.version < 1:
            pass
        if data.version < 2:
            data._version = 2
            data._cd_drive = 'E:'
        if data.version < 3:
            data._version = 3
            data._ce_exec_file_name = 'ce.exe'
        if data.version < 4:
            data._version = 4
            for i in data.instances:
                i.properties._fov = 200
                i.properties._mousesens = 9
                i.properties._viewdist = 0
                i.properties._latency = 600
        return data
