from . import horizon

def parse_horizon(input_str,horizonclass=horizon.Horizon):
    if input_str is not None:
        horizon_height = [float(x) for x in input_str.split(',') if x.isnumeric()]

        if len(horizon_height) < 2 or horizon_height is None:
            return horizonclass(angle_step=360, horizon_height=[0.], is_flat=True)

        angle_step = int(horizon_height[0])
        horizon_height.pop(0)
        is_flat = horizon_height[0] == 0.

        return horizonclass(angle_step=angle_step, horizon_height=horizon_height, is_flat=is_flat)

    else:
        return horizonclass(angle_step=360, horizon_height=[0.], is_flat=True)


