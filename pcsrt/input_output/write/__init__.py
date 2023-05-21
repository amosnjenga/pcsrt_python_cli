
from pcsrt.cli import FileType
from .writeOutput import WriteOutput
from .las import LasFileWriter
from .ply import PlyFileWriter

class Error(Exception):
    pass

class Writer(WriteOutput):
    def __init__(self, writer):
        self.writer = writer
        self.output_file_type = None
        super()

    @staticmethod
    def new(output_file, output_ply_ascii, cloud_params,reader):
        if output_file.file_type in [FileType.LAS, FileType.LAZ]:
            writer = LasFileWriter(output_file, cloud_params,reader)
            Writer.output_file_type = output_file.path
        elif output_file.file_type == FileType.PLY:
            writer = PlyFileWriter(output_file.path, output_ply_ascii, cloud_params)
            Writer.output_file_type = output_file.path
        else:
            raise Error("Invalid file type")

        return Writer(writer)

    def write(self,output_file_type,voxel_grid,translation):
        if output_file_type in [FileType.LAS, FileType.LAZ]:
            point_array = []
            normal_vector_array = []
            extrabytes_array = []

            for (_, voxel) in voxel_grid.items():
                irradiation = voxel.irradiation

                for point in voxel.points:
                    if not point.overlap:
                        point.translate_rev(translation)
                        _point,_normal_vector,_extra_bytes = self.write_point_las(point, irradiation, voxel.normal_vector)
                        point_array.append([_point[0],_point[1],_point[2]])
                        normal_vector_array.append([_normal_vector[0],_normal_vector[1],_normal_vector[2]])
                        extrabytes_array.append([_extra_bytes[0],_extra_bytes[1],_extra_bytes[2],_extra_bytes[3]])

            return point_array,normal_vector_array,extrabytes_array

        elif  output_file_type == FileType.PLY:
            point_array = []
            for (_, voxel) in voxel_grid.items():
                irradiation = voxel.irradiation

                for point in voxel.points:
                    if not point.overlap:
                        point.translate_rev(translation)
                        ply_point = self.write_point_ply(point, irradiation, voxel.normal_vector)
                        point_array.append(ply_point)
            return point_array



    def write_point_las(self, point, irradiation, normal_vector):
        return self.writer.write_point_las(point, irradiation, normal_vector)

    def write_output_lasfile(self,point_array,normal_vector_array,extrabytes_array):
        self.writer.write_output_lasfile(point_array,normal_vector_array,extrabytes_array)

    def write_point_ply(self, point, irradiation, normal_vector):
        return self.writer.write_point_ply(point, irradiation,normal_vector)

    def write_output_plyfile(self,point_array):
        self.writer.write_output_plyfile(point_array)




