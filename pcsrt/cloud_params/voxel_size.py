from .average_points import get_average_points_in_voxel

def get_voxel_size_and_average_points(reader,extent,block_params,desired_average_points_in_voxel,precision,point_count):
    average_points_in_voxel = get_average_points_in_voxel(reader, extent, block_params,voxel_size=None)
    voxel_size = (desired_average_points_in_voxel / average_points_in_voxel) ** (1. / 3.)

    if point_count <= 100000:
        max_iterations = 100  # Set the maximum number of iterations here
    elif point_count > 100000 and point_count <= 1000000:
        max_iterations = 50
    else:
        max_iterations = 10

    while abs(average_points_in_voxel - desired_average_points_in_voxel) > precision:
        average_points_in_voxel = get_average_points_in_voxel(reader, extent, block_params, voxel_size)
        voxel_size = ((voxel_size ** 3 * desired_average_points_in_voxel) / average_points_in_voxel) ** (1. / 3.)

        max_iterations -= 1

        if max_iterations <= 0:
            break

    voxel_size = round(voxel_size * 100.) / 100.

    return voxel_size,average_points_in_voxel
