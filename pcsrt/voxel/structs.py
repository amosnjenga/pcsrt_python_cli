from math import pow, floor
import numpy as np


class GetCoords:
    def x(self):
        pass

    def y(self):
        pass

    def z(self):
        pass

class IntoVoxelKey:
    def to_key(self, voxel_size):
        pass

class Translation:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class TranslatePoint:
    def translate(self, translation):
        self.x -= translation.x
        self.y -= translation.y
        self.z -= translation.z

    def translate_rev(self, translation):
        self.x += translation.x
        self.y += translation.y
        self.z += translation.z

class TrimDecimals:
    def trim_decimals(self,n):
        coef = pow(10, n)
        #self.x = floor(self.x * coef + 0.5) / coef
        #self.y = floor(self.y * coef + 0.5) / coef
        #self.z = floor(self.z * coef + 0.5) / coef
        self.x = floor(self.x * coef) / coef
        self.y = floor(self.y * coef) / coef
        self.z = floor(self.z * coef) / coef

class PushPoint:
    def push_point(self, point):
        pass

class IntoVoxel:
    def to_voxel(self, voxel_size):
        pass

class Point(GetCoords, IntoVoxelKey, TranslatePoint, TrimDecimals, IntoVoxel):
    def __init__(self, x,y,z,overlap):
        self.x = x
        self.y = y
        self.z = z
        self.overlap = overlap
        super()

    def as_numpy_vec(self):
        return np.array([self.x, self.y, self.z])

    def to_voxel(self, voxel_size):
        key = self.to_key(voxel_size)
        irradiation = Irradiation(global_irradiance=0.,beam_component=0.,diffuse_component=0.,sun_hours=0.)
        normal_vector = NormalVector(x=0.0, y=0.0, z=0.0)
        return Voxel(key[0],key[1],key[2],irradiation,normal_vector,[self])

    def to_key(self,voxel_size):
        key = tuple(map(lambda x: int(floor(x / voxel_size)), (self.x, self.y, self.z)))
        return key

    def x(self):
        return self.x

    def y(self):
        return self.y

    def z(self):
        return self.z

class NormalVector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def as_numpy_vec(self):
        return np.array([self.x, self.y, self.z])

    def from_na_vec(self,na_vec):
        if na_vec[2] < 0.:
            return NormalVector(-na_vec[0], -na_vec[1], -na_vec[2])
        else:
            return NormalVector(na_vec[0], na_vec[1], na_vec[2])

    #def angle(self, vec):
        #return np.arccos(self.as_numpy_vec().dot(vec) / (np.linalg.norm(self.as_numpy_vec()) * np.linalg.norm(vec)))
        #return np.angle(vec)

    def angle(self,vec):
        vector = np.array(vec)
        norm = np.linalg.norm(vector)
        _angle = np.arccos(vec[2] / norm)  # Calculate the angle of inclination
        return _angle
    @staticmethod
    def upright():
        return NormalVector(0., 0., 1.)


class Irradiation:
    def __init__(self,global_irradiance,beam_component,diffuse_component,sun_hours):
        self.global_irradiance = global_irradiance
        self.beam_component = beam_component
        self.diffuse_component = diffuse_component
        self.sun_hours = sun_hours

class Voxel(PushPoint):
    def __init__(self,x,y,z,irradiation,normal_vector,points):
        self.x = x
        self.y = y
        self.z = z
        self.irradiation = irradiation
        self.normal_vector = normal_vector
        self.points = points

    def push_point(self, point):
        self.points.append(point)

    def to_key(self):
        return (self.x,self.y,self.z)

class Key:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def as_tuple(self):
        return (self.x,self.y,self.z)

