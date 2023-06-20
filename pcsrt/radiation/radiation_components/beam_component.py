from math import exp, pow, sin
from pcsrt.common.constants import SOLAR_CONSTANT


def get_beam_irradiance(elevation,solar_altitude,incline_angle,solar_distance_variation_correction,linke_turbidity_factor):
    if len(linke_turbidity_factor) == 1:
        linke_turbidity_factor = linke_turbidity_factor[0]

    elevation_correction = exp(-elevation / 8434.5)
    temp_1 = 0.1594 + solar_altitude * (1.123 + 0.065656 * solar_altitude)
    temp_2 = 1. + solar_altitude * (28.9344 + 277.3971 * solar_altitude)
    solar_altitude_refraction_correction = 0.061_359 * temp_1 / temp_2
    solar_altitude_angle = solar_altitude + solar_altitude_refraction_correction
    relative_optical_air_mass = elevation_correction / (
            sin(solar_altitude_angle) +
            0.50572 * pow((degrees(solar_altitude_angle) + 6.07995),-1.6364))

    if relative_optical_air_mass <= 20.0:
        rayleigh_optical_thickness = 1. / (6.6296 + relative_optical_air_mass
                                           * (1.7513 + relative_optical_air_mass
                                              * (-0.1202 + relative_optical_air_mass
                                                 * (0.0065 - relative_optical_air_mass * 0.00013))))
    else:
        rayleigh_optical_thickness = 1.0 / (10.4 + 0.718 * relative_optical_air_mass)

    beam_transmittance = exp(
        -0.8662 * linke_turbidity_factor * relative_optical_air_mass * rayleigh_optical_thickness
    )

    beam_irradiance = (
        SOLAR_CONSTANT
        * solar_distance_variation_correction
        * sin(incline_angle)
        * beam_transmittance
    )

    return beam_irradiance