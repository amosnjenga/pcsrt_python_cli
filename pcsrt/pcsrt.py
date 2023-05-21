import logging
from math import ceil

from . import cli
from . import cloud_params
from . import input_output
from . import voxel
from . import radiation

from .cli import InputParams,FileType
from .cloud_params import get_cloud_params
from .input_output import Reader,Writer
from .voxel import build_normals,build_voxel_grid,get_voxel_block_iterator
from .radiation import calc_solar_radiation

logging.basicConfig(level=logging.INFO)

# noinspection PyTypeChecker
def pcsrt(pcrst_inputs):
    input_params = InputParams.parse_obj({
        "input_file": pcrst_inputs['input_file'],
        "output_file": pcrst_inputs['output_file'],
        "centroid": pcrst_inputs['centroid'],
        "output_ply_ascii": pcrst_inputs['output_ply_ascii'],
        "time_range": pcrst_inputs['time_range'],
        "step_mins": pcrst_inputs['step_mins'],
        "linke_turbidity_factor": pcrst_inputs['linke_turbidity_factor'],
        "horizon":pcrst_inputs['horizon'],
        "block_process_params": pcrst_inputs['block_process_params']
    })

    logging.info("Reading cloud params...")
    reader = Reader(input_params.input_file)
    cloud_params = get_cloud_params(input_params, reader)

    logging.info(
        "Computing solar radiation for:\nInput file: {}\nPoint count: {}\nAverage points: {}\nVoxel size: {}\nTime range: {} - {}\nTime step: {}min".format(
        input_params.input_file.path,
        cloud_params.point_count,
        ceil(cloud_params.average_points_in_voxel * 10) / 10,
        cloud_params.voxel_size,
        input_params.time_range.from_date.strftime("%Y-%m-%dT%H:%M:%S"),
        input_params.time_range.to_date.strftime("%Y-%m-%dT%H:%M:%S"),
        input_params.step_mins
        )
    )

    logging.info("Computing solar radiation...")
    writer = Writer.new(input_params.output_file, input_params.output_ply_ascii, cloud_params,reader)

    block_iterator = get_voxel_block_iterator(reader,cloud_params.extent,input_params.block_process_params)

    for index,block in enumerate(block_iterator):
        logging.info("Processing cloud block {}/{}...".format(index + 1, len(block_iterator)))
        voxel_grid = build_voxel_grid(block.points, cloud_params.voxel_size)

        logging.info("Building normals for voxels...")
        failed_normals = build_normals(voxel_grid, cloud_params.average_points_in_voxel)

        if failed_normals[0] > 0:
            logging.warning("Failed to construct normals on %d voxels.", failed_normals[0])

        logging.info("Calculating solar radiation..")
        calc_solar_radiation(voxel_grid, input_params)

        logging.info(
            "Writing solar radiation for block to file {}".format(input_params.output_file.path)
        )

        if input_params.output_file.file_type in [FileType.LAS,FileType.LAZ]:
            pa,na,eta = writer.write(input_params.output_file.file_type,voxel_grid, block.translation)
            writer.write_output_lasfile(pa,na,eta)
        elif input_params.output_file.file_type in [FileType.PLY]:
            pa = writer.write(input_params.output_file.file_type,voxel_grid,block.translation)
            writer.write_output_plyfile(pa)
        else:
            raise ValueError("Unsupported file type")


if __name__ == '__main__':
    pcsrt()