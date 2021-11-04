from project.models.data_model import DataModel
from project.utils.path_utils import PathUtils
import pickle
import sys
import os


class DataService:
    """
    Application data service
    """

    data: DataModel = None

    @classmethod
    def load_data(cls, retry=True) -> None:
        """
        Load the data from the .dat file
        """
        try:
            with open(PathUtils.get_data_file_path(), 'rb') as f:
                cls.data = pickle.load(f)
        except Exception as err:
            print(err)
            if retry:
                print('(Retry) The data file will be recreated...')
                cls.reset_data_file()
                cls.load_data(False)
            else:
                print('Could not open the data file')
                sys.exit(1)

    @classmethod
    def reset_data_file(cls) -> None:
        """
        Re-create data file
        """
        if not os.path.exists(PathUtils.get_data_path()):
            os.mkdir(PathUtils.get_data_path())
        initial_data = DataModel()
        with open(PathUtils.get_data_file_path(), 'wb') as f:
            pickle.dump(initial_data, f)

    @classmethod
    def get_data(cls):
        """
        Return in-memory data
        """
        return cls.data

    @classmethod
    def save_data(cls, data):
        """
        Update in-memory data and persist it to .dat file
        """
        cls.data = data
        with open(PathUtils.get_data_file_path(), 'wb') as f:
            pickle.dump(data, f)
