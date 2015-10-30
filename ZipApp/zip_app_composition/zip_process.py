import zipfile
import shutil
import sys
import os


class ZipProcess:

    def __init__(self, zipname, zipscale):
        self.zipname = zipname
        self.zipscale = zipscale
        zipscale.processor = self
        self.temp_directory = 'processing-{}'.format(zipname)

    def _file_path(self, filename):
        return os.path.join(self.temp_directory, filename)

    def process_zip(self):
        self.unzip_files()
        self.zipscale.process_files()
        self.zip_files()

    def unzip_files(self):
        file = zipfile.ZipFile(self.zipname)
        if os.path.exists(self.temp_directory):
            shutil.rmtree(self.temp_directory)
        os.mkdir(self.temp_directory)
        try:
            file.extractall(self.temp_directory)
        finally:
            file.close()

    def zip_files(self):
        file = zipfile.ZipFile(self.zipname, 'w')
        for filename in os.listdir(self.temp_directory):
            file.write(self._file_path(filename), filename)
        shutil.rmtree(self.temp_directory)
