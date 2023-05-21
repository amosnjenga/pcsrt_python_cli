class LasPoint:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def to_key(self, voxel_size):
        return (
            round(self.x / voxel_size),
            round(self.y / voxel_size),
            round(self.z / voxel_size)
        )

    def x(self):
        return self.x

    def y(self):
        return self.y

    def z(self):
        return self.z
