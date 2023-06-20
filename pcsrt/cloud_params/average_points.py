import concurrent.futures
import itertools
import math
from collections import defaultdict

from .. import voxel
from ..voxel import get_voxel_block_iterator


def get_average_points_in_voxel(reader, extent, block_params, voxel_size):

    block_iterator = get_voxel_block_iterator(reader, extent, block_params)

    # Create a concurrent.futures.ThreadPoolExecutor to execute the tasks in parallel.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list of tasks to be executed in parallel.
        tasks = []
        for block in block_iterator:
            tasks.append(executor.submit(_get_average_points_in_block, block, voxel_size))

        # Get the results of the tasks.
        results = [task.result() for task in tasks]

    # Calculate the average number of points per voxel.
    total_points = sum(result.points for result in results)
    total_voxels = sum(result.voxels for result in results)
    return total_points / total_voxels


def _get_average_points_in_block(block, voxel_size):
    voxel_map = defaultdict(int)
    points = 0
    for point in block.points:
        points += 1
        key = point.to_key(voxel_size)
        voxel_map[key] += 1

    voxels = len(voxel_map)
    return Counter(points, voxels)


class Counter:
    def __init__(self, points, voxels):
        self.points = points
        self.voxels = voxels

    def __repr__(self):
        return f"Counter(points={self.points}, voxels={self.voxels})"







