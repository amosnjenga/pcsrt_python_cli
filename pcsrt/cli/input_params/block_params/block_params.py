from math import inf

class BlockParams:
    def __init__(self, size: int, overlap: int):
        self.size = size
        self.overlap = overlap

    @staticmethod
    def default():
        return BlockParams(size=inf, overlap=0)