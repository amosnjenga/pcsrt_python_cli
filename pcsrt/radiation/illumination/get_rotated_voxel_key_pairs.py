import numpy as np

from .structs import RotatedVoxelKeyPair
from itertools import starmap
from pcsrt.voxel import Key

def get_rotated_voxel_key_pair_iterator(voxel_grid, sun_position):
    rot_voxel_key_pair_iter = starmap(
        lambda reference_key, voxel: _rotate_voxel(reference_key, voxel, sun_position),
        voxel_grid.items()
    )
    return rot_voxel_key_pair_iter

def _rotate_voxel(reference_key,voxel,sun_position):
    reference_key = Key(reference_key[0],reference_key[1],reference_key[2])
    voxel_key_as_coords = np.array(reference_key.as_tuple(), dtype=np.float64)

    rotated_voxel_coords = sun_position.rotation_x @ sun_position.rotation_z @ voxel_key_as_coords
    #rotated_voxel_coords = np.dot(sun_position.rotation_x, np.dot(sun_position.rotation_z, voxel_key_as_coords))
    #rotated_voxel_coords = sun_position.rotation_x * sun_position.rotation_z * voxel_key_as_coords
    #print(rotated_voxel_coords)
    rotated_key = (

        int(np.round(rotated_voxel_coords[0] * 2.)),
        int(np.round(rotated_voxel_coords[1] * 2.)),
        int(np.round(rotated_voxel_coords[2] * 2.)),
    )
    #print(rotated_key)

    return RotatedVoxelKeyPair(reference=voxel, rotated_key=rotated_key)
