from zipprocess import ZipProcessor
from pygame import image
from pygame.transform import scale
import sys
import os


class ScaleZip(ZipProcessor):

    def process_files(self):
        for filename in os.listdir(self.temp_directory):
            im = image.load(self._full_filename(filename))
            scaled = scale(im, (640, 480))
            image.save(scaled, self._full_filename(filename))

if __name__ == '__main__':
    ScaleZip(sys.argv[1]).process_zip()
