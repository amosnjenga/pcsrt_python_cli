from pvlib.solarposition import get_solarposition
from datetime import datetime, timedelta
from math import radians, pi,cos,sin
from scipy.spatial.transform import Rotation
from numpy import identity
import numpy as np

from .sunrise_sunset import calc_sunrise_and_set

class SunPosition:
    def __init__(self, rotation_x, rotation_z, azimuth, altitude, step_coef, time):
        self.rotation_x = rotation_x
        self.rotation_z = rotation_z
        self.azimuth = azimuth
        self.altitude = altitude
        self.step_coef = step_coef
        self.time = time

def get_sun_positions(input_params):
    step_mins = input_params.step_mins
    centroid = input_params.centroid
    horizon = input_params.horizon

    time_range = input_params.time_range
    time_range_from = time_range.from_date
    time_range_to = time_range.to_date
    iter = SunPositionTimeRangeIterator(time_range_from, time_range_to, centroid, step_mins)
    sun_positions = []

    for sun_pos in iter:
        if horizon.is_visible(sun_pos.azimuth, sun_pos.altitude):
            sun_positions.append(sun_pos)

    return sun_positions

class SunPositionTimeRangeIterator:
    def __init__(self, time_range_from, time_range_to, centroid, step_mins):
        self.to = time_range_to
        self.centroid = centroid
        self.step_mins = step_mins
        self.previous_time = None
        self.current_time = time_range_from
        self.sunrise_sunset = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_time < self.to:
            if self.previous_time is None or self.current_time.date().toordinal() != self.previous_time.date().toordinal():
                self.sunrise_sunset = calc_sunrise_and_set(
                    datetime.combine(self.current_time.date(), datetime.min.time()) + timedelta(hours=13),
                    self.centroid.lat,
                    self.centroid.lon
                )

            while self.sunrise_sunset.polar_night and self.current_time <= self.to:
                self.current_time = (self.current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0)
                self.sunrise_sunset = calc_sunrise_and_set(
                    datetime.combine(self.current_time.date(), datetime.min.time()) + timedelta(hours=13),
                    self.centroid.lat,
                    self.centroid.lon
                )

            sunrise = self.sunrise_sunset.sunrise
            sunset = self.sunrise_sunset.sunset

            if not self.sunrise_sunset.polar_day and self.current_time < sunrise:
                self.current_time = sunrise

            next_time = self.current_time + timedelta(minutes=int(self.step_mins))

            if next_time > sunset:
                step_coef = (sunset - self.current_time).total_seconds() / 3600.0
                sun_position = self.get_sun_position(step_coef)

                self.previous_time = self.current_time

                next_day = self.current_time.replace(hour=13, minute=0, second=0) + timedelta(days=1)
                next_day_sunrise = calc_sunrise_and_set(next_day, self.centroid.lat, self.centroid.lon)

                if next_day_sunrise.polar_day or next_day_sunrise.polar_night:
                    self.current_time = self.current_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                else:
                    self.current_time = next_day_sunrise.sunrise

                return sun_position

            elif next_time > self.to:
                step_coef = (self.to - self.current_time).total_seconds() / 3600.0
                sun_position = self.get_sun_position(step_coef)

                self.previous_time = self.current_time
                self.current_time = next_time
                return sun_position

            else:
                step_coef = (next_time - self.current_time).total_seconds() / 3600.0
                sun_position = self.get_sun_position(step_coef)

                self.previous_time = self.current_time
                self.current_time = next_time
                return sun_position

        else:
            raise StopIteration

    def get_sun_position(self, step_coef):
        time = self.current_time
        sol_pos = get_solarposition(time, self.centroid.lat, self.centroid.lon)
        altitude = radians(90.0 - float(sol_pos['apparent_zenith'].iloc[0]))
        azimuth = radians(float(sol_pos['azimuth'].iloc[0]))
        roll = (pi / 2.0) + altitude
        yaw = azimuth - pi

        rotation_x = identity(3)
        rotation_x[1, 1] = cos(roll)
        rotation_x[1, 2] = -sin(roll)
        rotation_x[2, 1] = sin(roll)
        rotation_x[2, 2] = cos(roll)

        rotation_z = identity(3)
        rotation_z[0, 0] = cos(yaw)
        rotation_z[0, 1] = -sin(yaw)
        rotation_z[1, 0] = sin(yaw)
        rotation_z[1, 1] = cos(yaw)

        #rotation_x = Rotation.from_euler('xyz', [roll, 0.0, 0.0], degrees=False).as_matrix()
        #rotation_z = Rotation.from_euler('xyz', [0.0, 0.0, yaw], degrees=False).as_matrix()

        return SunPosition(rotation_x, rotation_z, azimuth, altitude, step_coef, time)

