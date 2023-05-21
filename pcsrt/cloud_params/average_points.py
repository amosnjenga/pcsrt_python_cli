from math import floor
from concurrent.futures import ThreadPoolExecutor,as_completed

from .. import voxel
from ..voxel import get_voxel_block_iterator


class Counter:
    def __init__(self,point_count,voxel_count):
        self.point_count = point_count
        self.voxel_count = voxel_count


def get_average_points_in_voxel(reader, extent, block_params, voxel_size):
    block_iterator = get_voxel_block_iterator(reader, extent, block_params)

    total_point_count = 0
    total_voxel_count = 0
    voxel_keys = set()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_block, block, voxel_size,voxel_keys) for block in block_iterator]

        for future in as_completed(futures):
            result = future.result()
            total_point_count += result["point_count"]
            total_voxel_count += result["voxel_count"]

    if total_voxel_count != 0:
        return total_point_count / total_voxel_count
    else:
        return 0


def process_block(block, voxel_size,voxel_keys):
    point_count = 0

    if voxel_size is None:
        desired_point_count = 4  # Set the desired point count here 10000
        desired_difference = 0.5  # Set the desired difference in points here

        min_voxel_size = 1  # Set the lower bound of voxel size
        max_voxel_size = 4  # Set the upper bound of voxel size
        epsilon = 0.001  # Set the convergence threshold

        while True:
            voxel_size = (min_voxel_size + max_voxel_size) / 2.0
            point_count = 0
            voxel_keys = set()

            for point in block.points:
                point_count += 1
                key = tuple(int(floor(x / voxel_size)) for x in [point.x,point.y,point.z])
                voxel_keys.add(key)

            difference = point_count - desired_point_count

            if abs(difference) <= desired_difference or max_voxel_size - min_voxel_size < epsilon:
                break  # Stop the loop if the desired point count is reached within the desired difference or convergence threshold

            if difference < 0:
                min_voxel_size = voxel_size
            else:
                max_voxel_size = voxel_size

    else:
        for point in block.points:
            point_count += 1
            key = tuple(int(floor(x / voxel_size)) for x in [point.x, point.y, point.z])
            voxel_keys.add(key)

    return {"point_count": point_count, "voxel_count": len(voxel_keys)}











