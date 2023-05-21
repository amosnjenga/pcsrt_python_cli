from .input_params import parse_block_params
from .input_params import parse_centroid
from .input_params import parse_file
from .input_params import parse_horizon
from .input_params import parse_linke
from .input_params import parse_time_range


class InputParams:
    def __init__(self,centroid,time_range, step_mins, linke_turbidity_factor, horizon, voxel_size,
                 average_points_in_voxel, block_process_params, output_ply_ascii,
                 input_file, output_file):
        self.centroid = centroid
        self.time_range = time_range
        self.step_mins = step_mins
        self.linke_turbidity_factor = linke_turbidity_factor
        self.horizon = horizon
        self.voxel_size = voxel_size
        self.average_points_in_voxel = average_points_in_voxel
        self.block_process_params = block_process_params
        self.output_ply_ascii = output_ply_ascii
        self.input_file = input_file
        self.output_file = output_file


    @classmethod
    def parse_obj(cls,kwargs):
        cls.input_file = parse_file(kwargs["input_file"])
        cls.output_file = parse_file(kwargs["output_file"])
        cls.centroid = parse_centroid(kwargs["centroid"])
        cls.output_ply_ascii = kwargs["output_ply_ascii"]
        cls.time_range = parse_time_range(kwargs["time_range"])
        cls.step_mins = kwargs["step_mins"]
        cls.linke_turbidity_factor = parse_linke(kwargs["linke_turbidity_factor"])
        cls.horizon = parse_horizon(kwargs["horizon"])
        cls.block_process_params = parse_block_params(kwargs["block_process_params"])[0]
        cls.voxel_size = kwargs.get('voxel_size',None)
        cls.average_points_in_voxel = kwargs.get('average_points_in_voxel',None)
        cls.desired_average_points_in_voxel = 4

        return cls




