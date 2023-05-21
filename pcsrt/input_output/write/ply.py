import  numpy as np
from plyfile import PlyData, PlyElement

class PlyFileWriter:
    def __init__(self, path,ascii,cloud_params):
        self.output_path = path
        self.ascii = ascii
        self.cloud_params = cloud_params

    def write_point_ply(self,point,irradiation,normal_vector):
        ply_point = (point.x,point.y,point.z,irradiation.global_irradiance,irradiation.beam_component,
                     irradiation.diffuse_component,irradiation.sun_hours)
        return ply_point

    def write_output_plyfile(self, point_array):
        points = np.array(point_array,dtype=[
                    ('x', 'f8'),
                    ('y', 'f8'),
                    ('z', 'f8'),
                    ('irradiance', 'f8'),
                    ('beam_component', 'f8'),
                    ('diffuse_component', 'f8'),
                    ('insolation_time', 'u4')
                ])
        point_element = PlyElement.describe(points,'point')

        with open(self.output_path, mode='w' if ascii else 'wb') as f:
            PlyData([point_element], text=True).write(f)
