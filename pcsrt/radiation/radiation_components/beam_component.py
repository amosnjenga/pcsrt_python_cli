from math import exp, pow, sin
from pcsrt.common.constants import SOLAR_CONSTANT

def get_beam_irradiance(elevation,solar_altitude,incline_angle,solar_distance_variation_correction,linke_turbidity_factor):
    if len(linke_turbidity_factor) == 1:
        linke_turbidity_factor = linke_turbidity_factor[0]

    relative_optical_air_mass = ((-elevation / 8434.5) * exp(1)) / (
        sin(solar_altitude)
        + 0.50572 * pow(solar_altitude + 6.07995, -1.6364)
    )

    rayleigh_optical_thickness = (
        1.0
        / (
            6.6296
            + relative_optical_air_mass
            * (
                1.7513
                + relative_optical_air_mass
                * (
                    -0.1202
                    + relative_optical_air_mass
                    * (0.0065 - relative_optical_air_mass * 0.00013)
                )
            )
            )
            if relative_optical_air_mass <= 20.0
            else 1.0 / (10.4 + 0.718 * relative_optical_air_mass)
    )

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
