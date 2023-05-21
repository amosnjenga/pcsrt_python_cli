from abc import ABC,abstractmethod

class WriteOutput(ABC):
    @abstractmethod
    def write_point_las(self, point, irradiation, normal_vector):
        pass

    @abstractmethod
    def write_point_ply(self, point, irradiation, normal_vector):
        pass

