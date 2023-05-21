from math import pi

class Horizon:
    def __init__(self, angle_step = 360,horizon_height=[0.], is_flat: bool = True):
        self.angle_step = angle_step
        self.horizon_height = horizon_height
        self.is_flat = is_flat

    def is_visible(self, azimuth,altitude):
        azimuth = azimuth * 180 / pi
        altitude = altitude * 180 / pi
        angle_step = self.angle_step
        if self.is_flat:
            return True
        else:
            angle_idx = int(azimuth // angle_step)
            last_idx = len(self.horizon_height) - 1
            if angle_idx > last_idx:
                angle_idx = last_idx
            left_height = self.horizon_height[angle_idx]
            if angle_idx == last_idx:
                right_height = self.horizon_height[0]
            else:
                right_height = self.horizon_height[angle_idx + 1]
            azimuth_residual = azimuth % angle_step
            horizon_height = left_height + (((right_height - left_height) / angle_step) * azimuth_residual)
            return altitude > horizon_height
