import threading
import logging


from .illumination import get_rotated_voxel_key_pair_iterator, IlluminationMap
from .radiation_components import get_irradiance
from .radiation_components import VoxelIrradiance
from .sun_position import get_sun_positions

def calc_solar_radiation(voxel_grid,input_params):
    sun_positions = get_sun_positions(input_params)
    logging.info("Visible sun epochs: %d", len(sun_positions))

    def process_sun_position(sun_position):
        rot_voxel_key_pairs = get_rotated_voxel_key_pair_iterator(voxel_grid, sun_position)

        voxel_illumination_map = IlluminationMap.create()

        for rot_voxel_key_pair in rot_voxel_key_pairs:
            voxel_in_shadow = voxel_illumination_map.get_voxel_in_shadow(rot_voxel_key_pair)
            if voxel_in_shadow is not None:
                irradiance = get_irradiance(input_params, voxel_in_shadow, sun_position, True)
                update_global_irradiance(voxel_in_shadow, irradiance, True, sun_position.step_coef)

        for _, illuminated_voxel in voxel_illumination_map.map.values():
            irradiance = get_irradiance(input_params, illuminated_voxel, sun_position, False)
            update_global_irradiance(illuminated_voxel, irradiance, False, sun_position.step_coef)

    threads = []
    for sun_position in sun_positions:
        t = threading.Thread(target=process_sun_position, args=(sun_position,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def update_global_irradiance(voxel,irradiance,in_shadow,step_coef):
        irradiation = voxel.irradiation
        irradiation.global_irradiance += irradiance.global_irradiance * step_coef
        irradiation.beam_component += irradiance.beam_component * step_coef
        irradiation.diffuse_component += irradiance.diffuse_component * step_coef
        irradiation.sun_hours += 0 if in_shadow else 1 * step_coef
