import numpy as np
from math import pi,sin

from pcsrt.common.constants import SOLAR_CONSTANT

def get_diffuse_irradiance(solar_altitude,incline_angle,normal_vector,solar_distance_variation_correction,
    linke_turbidity_factor,beam_component):
    if len(linke_turbidity_factor) == 1:
        linke_turbidity_factor = linke_turbidity_factor[0]

    diffuse_transmission_function = -0.015843 + 0.030543 * linke_turbidity_factor \
                                    + 0.0003797 * linke_turbidity_factor ** 2

    def diffuse_angular_function(linke_turbidity_factor):
        a_0 = 0.2646 - 0.061581 * linke_turbidity_factor + 0.0031408 * linke_turbidity_factor ** 2.
        if a_0 < 0.002:
            a_0 = 0.002 / diffuse_transmission_function

        a_1 = 2.0402 + 0.018945 * linke_turbidity_factor - 0.011161 * linke_turbidity_factor ** 2.
        a_2 = -1.3025 + 0.039231 * linke_turbidity_factor + 0.0085079 * linke_turbidity_factor ** 2.

        return a_0 + a_1 * sin(solar_altitude) + a_2 * sin(solar_altitude) ** 2.

    _diffuse_angular_function = diffuse_angular_function(linke_turbidity_factor)

    diffuse_irradiance = SOLAR_CONSTANT * solar_distance_variation_correction \
                         * diffuse_transmission_function * _diffuse_angular_function


    slope = normal_vector.angle([normal_vector.x, normal_vector.y, 1.])

    if beam_component is not None:
        modulating_function_kb = beam_component / SOLAR_CONSTANT \
            * solar_distance_variation_correction \
            * np.sin(solar_altitude)

        n = 0.00263 - 0.712 * modulating_function_kb - 0.6883 * modulating_function_kb ** 2.

        if np.degrees(solar_altitude) > 5.7:
            return diffuse_irradiance \
                * (diffuse_function(slope, n) * (1. - modulating_function_kb)
                   + modulating_function_kb * np.sin(incline_angle) / np.sin(solar_altitude))
        else:
            return diffuse_irradiance \
                * (np.cos(slope / 2.)) ** 2. \
                * (1. + modulating_function_kb * (np.sin(slope / 2.)) ** 3.) \
                * (1.
                   + modulating_function_kb
                   * np.sin(incline_angle) ** 2.
                   * (sin((pi / 2.) - solar_altitude)) ** 3.)
    else:
        return diffuse_irradiance * diffuse_function(slope, 0.25227)

def diffuse_function(slope,n):
    return ((1. + np.cos(slope)) / 2.) \
        + (np.sin(slope) - slope * np.cos(slope) - pi * (slope / 2.) * np.sin(slope / 2.) ** 2.) * n
