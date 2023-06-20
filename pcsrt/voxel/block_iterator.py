import math
from .structs import Point,Translation

def get_voxel_block_iterator(reader, extent, block_params):
    x_length, y_length, _ = extent.get_dimensions()
    if math.isinf(block_params.size):
        x_blocks = 1
        y_blocks = 1
    else:
        x_blocks = int((x_length / block_params.size) + 0.5)
        y_blocks = int((y_length / block_params.size) + 0.5)

    reader = reader
    blocks = []

    for i in range(x_blocks):
        for j in range(y_blocks):
            block = Block(block_params.size, block_params.overlap,i,j,x_blocks,y_blocks,extent)
            for p in reader.to_point_reader():
                point = Point(p[0],p[1],p[2],block_params.overlap)
                #print(block.is_in_block(point))
                #print(block.is_in_overlap_block(point))
                block.push_point(Point(p[0],p[1],p[2],block_params.overlap))
            blocks.append(block)

    return blocks

class Block:
    def __init__(self, block_size, block_overlap,i,j,x_blocks,y_blocks,extent):
        self.block_count = x_blocks * y_blocks
        self.block_number = i * y_blocks + j + 1
        self.points = []
        self.right_edge = i == x_blocks - 1
        self.top_edge = j == y_blocks - 1

        if block_size == math.inf:
            self.min_x = extent.min[0]
            self.min_y = extent.min[1]
            self.max_x = extent.max[0]
            self.max_y = extent.max[1]
        else:
            self.min_x = extent.min[0] + (i * block_size)
            self.min_y = extent.min[1] + (j * block_size)
            self.max_x = self.min_x + block_size
            self.max_y = self.min_y + block_size
        self.bbox = (self.min_x, self.min_y, self.max_x, self.max_y)

        self.translation = Translation(
            #x=self.min_x // 1,
            x=int(self.min_x),
            #y=self.min_y // 1,
            y=int(self.min_x),
            #z=extent.min[2] // 1,
            z=int(extent.min[2])
        )

        if block_overlap > 0:
            self.min_x, self.min_y, self.max_x, self.max_y = self.bbox
            self.overlap_bbox = (self.min_x - block_overlap, self.min_y - block_overlap, self.max_x + block_overlap, self.max_y + block_overlap)
        else:
            self.overlap_bbox = None

    def push_point(self, point):
        if self.is_in_overlap_block(point):
            overlap = not self.is_in_block(point)
            point = Point(
                x=point.x,
                y=point.y,
                z=point.z,
                overlap=overlap
            )
            point.translate(self.translation)
            point.trim_decimals(3)
            self.points.append(point)

    def is_in_block(self, point):
        min_x, min_y, max_x, max_y = self.bbox
        left = point.x >= min_x
        bottom = point.y >= min_y

        if self.right_edge:
            right = point.x <= max_x
        else:
            right = point.x < max_x

        if self.top_edge:
            top = point.y <= max_y
        else:
            top = point.y < max_y

        return left and bottom and right and top

    def is_in_overlap_block(self, point):
        if self.overlap_bbox is None:
            min_x, min_y, max_x, max_y = self.bbox
        else:
            min_x, min_y, max_x, max_y = self.overlap_bbox

        return min_x <= point.x <= max_x and min_y <= point.y <= max_y
