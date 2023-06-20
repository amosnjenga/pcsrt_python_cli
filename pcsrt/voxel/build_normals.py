from itertools import product
from functools import partial
from multiprocessing import Pool

from .structs import NormalVector,Key,Point
from .normal_from_points import normal_from_points


def process_item(item, voxel_grid, average_points_in_voxel):
    key = Key(item[0][0], item[0][1], item[0][2])
    min_points = 4 if average_points_in_voxel < 4 else int(average_points_in_voxel)
    adjacent_points = search_for_adjacent_points(voxel_grid, key, 5, min_points)
    normal = normal_from_points(adjacent_points)

    failed_used_default = normal is None

    if normal is None or len(normal) == 0:
        normal = NormalVector.upright()

    return key, normal, failed_used_default

def build_normals(voxel_grid, average_points_in_voxel):
    failed_counter = 0

    process_item_partial = partial(process_item, voxel_grid=voxel_grid,
                                   average_points_in_voxel=average_points_in_voxel)

    with Pool() as pool:
        normals = pool.map(process_item_partial, voxel_grid.items())

    for key, normal_vector, failed_used_default in normals:
        if failed_used_default:
            failed_counter += 1

        if isinstance(normal_vector, NormalVector):
            voxel_grid[key.as_tuple()].normal_vector = normal_vector
        else:
            voxel_grid[key.as_tuple()].normal_vector = NormalVector(normal_vector[0], normal_vector[1], normal_vector[2])


    return failed_counter, voxel_grid


def search_for_adjacent_points(voxel_grid, key, max_depth, min_points):
    point_set = set()

    for depth in range(1, max_depth + 1):
        for x, y, z in product(range(-depth, depth + 1), repeat=3):
            if (x, y, z) != (0, 0, 0):
                adjacent_voxel = voxel_grid.get((key.x + x, key.y + y, key.z + z))
                if adjacent_voxel:
                    for point in adjacent_voxel.points:
                        point_set.add((int(point.x * 1000), int(point.y * 1000), int(point.z * 1000)))

        if len(point_set) >= min_points:
            break

    return [Point(x / 1000, y / 1000, z / 1000,0) for x, y, z in point_set]

