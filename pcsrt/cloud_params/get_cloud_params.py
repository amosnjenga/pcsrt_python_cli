from ..common import Extent
from .average_points import get_average_points_in_voxel
from .voxel_size import get_voxel_size_and_average_points

class CloudParams:
    def __init__(self, voxel_size,average_points_in_voxel,point_count, extent):
        self.voxel_size = voxel_size
        self.average_points_in_voxel = average_points_in_voxel
        self.point_count = point_count
        self.extent = extent


def get_cloud_params(input_params,reader):
    extent = Extent(
        min=[float('inf'), float('inf'), float('inf')],
        max=[float('-inf'), float('-inf'), float('-inf')]
    )

    point_count = 0
    for point in reader.to_point_reader():
        point_count += 1
        extent.update((point[0],point[1],point[2]))

    block_params = input_params.block_process_params

    if input_params.voxel_size is None and input_params.average_points_in_voxel is None:
        voxel_size, average_points_in_voxel = get_voxel_size_and_average_points(
            reader,extent, block_params, input_params.desired_average_points_in_voxel,0.5)
    else:
        voxel_size = input_params.voxel_size
        average_points_in_voxel = get_average_points_in_voxel(reader,extent, block_params, voxel_size)

    cloud_params = CloudParams(
        voxel_size=voxel_size,
        average_points_in_voxel=average_points_in_voxel,
        point_count=point_count,
        extent=extent,
    )

    return cloud_params
