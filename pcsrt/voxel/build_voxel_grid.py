from math import floor

def build_voxel_grid(points,voxel_size):
    voxel_grid={}

    for point in points:
        key = tuple(map(lambda x: int(floor(x / voxel_size)), (point.x, point.y, point.z)))

        if key in voxel_grid:
            voxel = voxel_grid[key]
            voxel.push_point(point)
        else:
            voxel = point.to_voxel(voxel_size)
            voxel_grid[key] = voxel

    return voxel_grid
