import os
import laspy
from plyfile import PlyData

from pcsrt.cli import FileType

class Reader:
    def __init__(self, input_file):
        self.input_file = input_file
        self.input_file_type = input_file.file_type

    def to_point_reader(self):
        if self.input_file_type == FileType.LAS:
            #return laspy.file.File(self.input_file.path, mode="r").points #laspy <2.00
            return laspy.read(self.input_file.path).points.array
        elif self.input_file_type == FileType.PLY:
            return PlyData.read(self.input_file.path)
        else:
            raise ValueError("Unsupported file type")

    def to_lasfile_object(self):
        if self.input_file_type == FileType.LAS:
            #return laspy.file.File(self.input_file.path, mode="r") laspy<2.0.0
            return laspy.read(self.input_file.path)


