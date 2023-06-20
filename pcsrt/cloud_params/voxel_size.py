from .average_points import get_average_points_in_voxel
from math import pow

def get_voxel_size_and_average_points(reader, extent, block_params, desired_average_points_in_voxel, precision):
    average_points_in_voxel = get_average_points_in_voxel(reader, extent, block_params, 1.0)
    voxel_size = pow((desired_average_points_in_voxel / average_points_in_voxel),1.0 / 3.0)

    while abs(average_points_in_voxel - desired_average_points_in_voxel) > precision:
        average_points_in_voxel = get_average_points_in_voxel(reader, extent, block_params, voxel_size)
        voxel_size = pow(((pow(voxel_size,3.0) * desired_average_points_in_voxel) / average_points_in_voxel),1.0 / 3.0)

    voxel_size = (voxel_size * 100.0) / 100
    return voxel_size, round(average_points_in_voxel,2)
