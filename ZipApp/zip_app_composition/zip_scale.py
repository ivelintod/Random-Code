import os
import sys
from pygame import image
from pygame.transform import scale
from zip_process import ZipProcess


class ScaleZip:

    def process_files(self):
        for filename in os.listdir(self.processor.temp_directory):
            img = image.load(self.processor._file_path(filename))
            scaled_img = scale(img, (800, 600))
            image.save(scaled_img, self.processor._file_path(filename))

if __name__ == '__main__':
    zipscale = ScaleZip()
    proc = ZipProcess("Gerrard.zip", zipscale)
    proc.process_zip()
