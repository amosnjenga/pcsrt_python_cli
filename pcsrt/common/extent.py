
class Extent:
    def __init__(self, min,max): #min and max are tuples (x,y,z)
        self.min = min
        self.max = max

    def update(self,point):
        x, y, z = point
        self.min[0] = min(self.min[0], x)
        self.min[1] = min(self.min[1], y)
        self.min[2] = min(self.min[2], z)
        self.max[0] = max(self.max[0], x)
        self.max[1] = max(self.max[1], y)
        self.max[2] = max(self.max[2], z)

    def get_dimensions(self):
        return (
            self.max[0] - self.min[0] + 1,
            self.max[1] - self.min[1] + 1,
            self.max[2] - self.min[2] + 1,
        )
