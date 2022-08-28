import os
import shutil


class ZipUtils:
    """
    Zip utilities.
    """

    @classmethod
    def make_zip_archive(cls, path_source: str, path_dest: str):
        """
        Create a file
        path_source: directory to compress (Ex: /dir)
        path_dest: directory to create zip (Ex: /dir/folder.zip)
        """
        base = os.path.basename(path_dest)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(path_source)
        archive_to = os.path.basename(path_source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), path_dest)
