import laspy
import struct
import numpy as np

class LasFileWriter:
    def __init__(self, output_file, cloud_params, reader):
        self.output_file = output_file
        self.cloud_params = cloud_params
        self.input_reader_obj = reader.to_lasfile_object()
        self.input_file_header = reader.to_lasfile_object().header

    def write_point_las(self, point, irradiation, normal_vector):
        extra_bytes = [
            irradiation.global_irradiance,
            irradiation.beam_component,
            irradiation.diffuse_component,
            irradiation.sun_hours,
        ]

        normal_as_rgb = (
            int((0.5 * normal_vector.x + 0.5) * 255.0),
            int((0.5 * normal_vector.y + 0.5) * 255.0),
            int((0.5 * normal_vector.z + 0.5) * 255.0),
        )


        extra_bytes = struct.pack('<' + 'd' * len(extra_bytes), *extra_bytes)
        normal_as_rgb = struct.pack('<HHH', *normal_as_rgb)

        return (point.x,point.y,point.z),normal_as_rgb,extra_bytes

    def fields_to_vlr(self, fields):
        vlr = struct.pack('<H', 0) + struct.pack('<H', 10)
        for idx, field in enumerate(fields):
            num_of_nulls = 192 - (len(field) + 1)
            is_last_row = idx + 1 == len(fields)
            if is_last_row:
                num_of_nulls -= 3
            else:
                num_of_nulls -= 1
            vlr += field.encode() + b'\x00' * num_of_nulls
            if not is_last_row:
                vlr += struct.pack('<H', 10)
        return vlr

    def calculate_offset(self,reader,offsets,scales):
        initial_offsets = offsets
        initial_scales = scales
        #print(offsets,"init offsets")
        #print(scales,"init scales")

        min_x_scaled = min(reader.x)
        min_X_unscaled = min(reader.X)
        #print(min_x_scaled,"x scaled")
        #print(min_X_unscaled,"x unscaled")
        initial_x_offset = offsets[0]
        initial_x_scale = scales[0]
        offset_x = min_x_scaled - (min_X_unscaled * initial_x_scale)

        min_y_scaled = min(reader.y)
        min_Y_unscaled = min(reader.Y)
        initial_y_offset = offsets[1]
        initial_y_scale = scales[1]
        offset_y = min_y_scaled - (min_Y_unscaled * initial_y_scale)

        min_z_scaled = min(reader.z)
        min_Z_unscaled = min(reader.Z)
        initial_z_offset = offsets[2]
        initial_z_scale = scales[2]
        offset_z = min_z_scaled - (min_Z_unscaled * initial_z_scale)

        #print([offset_x,offset_y,offset_z],"ne offsets")

        return np.array([offset_x,offset_y,offset_z])





    def write_output_lasfile(self,point_array, normal_vector_array, extrabytes_array):
        point_array  = np.array(point_array)
        normal_vector_array = np.array(normal_vector_array)
        extrabytes_array = np.array(extrabytes_array)

        min_x = np.floor(np.min(point_array[:,0]))
        min_y = np.floor(np.min(point_array[:,1]))
        min_z = np.floor(np.min(point_array[:,2]))

        extra_bytes_fields = [
            laspy.header.ExtraBytesParams(name="irradiance", type=np.float64),
            laspy.header.ExtraBytesParams(name="beam_component", type=np.float64),
            laspy.header.ExtraBytesParams(name="diffuse_component", type=np.float64),
            laspy.header.ExtraBytesParams(name="insolation_time", type=np.float64)
        ]

        # 1. Create a new header
        header = laspy.LasHeader(point_format=2, version="1.2")
        header.add_extra_dims(extra_bytes_fields)
        #header.offsets = np.array([min_x,min_y,min_z])
        #header.offsets = np.array([8.5525625,-1.238805e+06,6.62075])
        header.offsets = self.calculate_offset(self.input_reader_obj,self.input_file_header.offsets,self.input_file_header.scale)
        #header.scales = np.array([1, 1, 1])
        header.scales = self.input_file_header.scale
        #header.scales = np.array([0.00025,0.00025,0.00025])

        try:
            with laspy.open(self.output_file.path, mode="w", header=header) as writer:
                point_record = laspy.ScaleAwarePointRecord.zeros(point_array.shape[0], header=header)
                point_record.x = point_array[:, 0]
                point_record.y = point_array[:, 1]
                point_record.z = point_array[:, 2]
                point_record.red = normal_vector_array[:, 0]
                point_record.green = normal_vector_array[:, 1]
                point_record.blue = normal_vector_array[:, 2]
                point_record.irradiance = extrabytes_array[:,0]
                point_record.beam_component = extrabytes_array[:,1]
                point_record.diffuse_component = extrabytes_array[:,2]
                point_record.insolation_time = extrabytes_array[:,3]

                writer.write_points(point_record)
        except Exception as e:
            print("Error occurred during file initialization:", e)
