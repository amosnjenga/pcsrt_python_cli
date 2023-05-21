class RotatedVoxelKeyPair:
    def __init__(self, reference, rotated_key):
        self.reference = reference
        self.rotated_key = rotated_key

class IlluminationMapUtils:
    @staticmethod
    def create():
        return IlluminationMap()

    @staticmethod
    def get_voxel_in_shadow(illumination_map, rot_voxel_key_pair):
        return illumination_map.get_voxel_in_shadow(rot_voxel_key_pair)

class IlluminationMap(IlluminationMapUtils):
    def __init__(self):
        self.map = {}

    def get_voxel_in_shadow(self, rot_voxel_key_pair):
        key = (rot_voxel_key_pair.rotated_key[0], rot_voxel_key_pair.rotated_key[1])

        if key in self.map:
            last_rot_voxel_key_pair_z, last_rot_voxel_ref = self.map[key]

            if rot_voxel_key_pair.rotated_key[2] < last_rot_voxel_key_pair_z:
                self.map[key] = (rot_voxel_key_pair.rotated_key[2], rot_voxel_key_pair.reference)
                return last_rot_voxel_ref
            else:
                return rot_voxel_key_pair.reference
        else:
            self.map[key] = (rot_voxel_key_pair.rotated_key[2], rot_voxel_key_pair.reference)
            return None

    @staticmethod
    def create():
        return IlluminationMap()


