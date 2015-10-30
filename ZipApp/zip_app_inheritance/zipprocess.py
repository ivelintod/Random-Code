import os
import sys
import shutil
import zipfile

class ZipProcessor:

    def __init__(self, zipname):
        self.zipname = zipname
        self.temp_directory = "unzipped-{}".format(zipname[:-4])

    def _full_filename(self, filename):
        return os.path.join(self.temp_directory, filename)

    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def unzip_files(self):
        if os.path.isdir(self.temp_directory):
            shutil.rmtree(self.temp_directory)
        os.mkdir(self.temp_directory)
        zip = zipfile.ZipFile(self.zipname)
        try:
            zip.extractall(self.temp_directory)
        finally:
            zip.close()

    def zip_files(self):
        file = zipfile.ZipFile(self.zipname, 'w')
        for filename in os.listdir(self.temp_directory):
            file.write(self._full_filename(filename), filename)
        shutil.rmtree(self.temp_directory)


class ZipReplace(ZipProcessor):

    def __init__(self, name, search_str, replace_str):
        super().__init__(name)
        self.search_str = search_str
        self.replace_str = replace_str

    def process_files(self):
        for filename in os.listdir(self.temp_directory):
            with open(self._full_filename(filename), 'r') as f:
                contents = f.read()
            contents = contents.replace(self.search_str, self.replace_str)
            with open(self._full_filename(filename), 'w') as f:
                f.write(contents)


if __name__ == '__main__':
    ZipReplace(*sys.argv[1:4]).process_zip()


