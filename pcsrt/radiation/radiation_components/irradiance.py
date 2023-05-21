import numpy as np
from datetime import datetime


from .structs import VoxelIrradiance
from .beam_component import get_beam_irradiance
from .diffuse_component import get_diffuse_irradiance

def solar_distance_variation_correction(no_of_day):
    j = 2. * np.pi * no_of_day / 365.25
    return 1. + 0.034221 * np.cos(j - 0.048869)

def get_irradiance(input_params,voxel,sun_position,in_shadow):
    no_of_day = sun_position.time.toordinal() - datetime(sun_position.time.year, 1, 1).toordinal() + 1
    month = sun_position.time.month
    linke_turbidity_factor = input_params.linke_turbidity_factor.get_val(month)

    solar_altitude = sun_position.altitude
    solar_azimuth = sun_position.azimuth
    elevation = input_params.centroid.elevation
    solar_distance_variation_correction_var = solar_distance_variation_correction(no_of_day)

    zenith_angle = (np.pi / 2.) - solar_altitude
    sun_direction = np.array([
        np.sin(solar_azimuth) * np.cos(zenith_angle),
        np.cos(solar_azimuth) * np.cos(zenith_angle),
        np.sin(solar_altitude)
    ])

    incline_angle = (np.pi / 2.) - np.arccos(np.dot(voxel.normal_vector.as_numpy_vec(), sun_direction))
    #incline_angle[incline_angle < 0] += np.pi / 2.
    incline_angle = np.where(incline_angle < 0, incline_angle + np.pi / 2, incline_angle)

    beam_component = get_beam_irradiance(
        elevation,
        solar_altitude,
        incline_angle,
        solar_distance_variation_correction_var,
        linke_turbidity_factor,
    ) if not in_shadow else None

    diffuse_component = get_diffuse_irradiance(
        solar_altitude,
        incline_angle,
        voxel.normal_vector,
        solar_distance_variation_correction_var,
        linke_turbidity_factor,
        beam_component,
    )

    beam_component = beam_component if beam_component is not None else 0.
    diffuse_component = diffuse_component

    global_irradiance = beam_component + diffuse_component

    return VoxelIrradiance(voxel,global_irradiance,beam_component,diffuse_component)


