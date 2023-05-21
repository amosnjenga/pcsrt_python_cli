
class VoxelIrradiance:
    def __init__(self,voxel,global_irradiance,beam_component,diffuse_component):
        self.voxel = voxel
        self.global_irradiance = global_irradiance
        self.beam_component = beam_component
        self.diffuse_component = diffuse_component
