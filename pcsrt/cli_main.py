import argparse
import logging

from .pcsrt import pcsrt

logging.basicConfig(level=logging.INFO)

def cmd_args():
    parser = argparse.ArgumentParser(description='A tool for modeling solar radiation & insolation on point cloud data built in Python.')
    parser.add_argument('-c','--centroid', required=True, help='[<LAT(decimal)>,<LON(decimal)>,<ELEVATION(decimal)>] Point cloud centroid geographical coordinates & elevation')
    parser.add_argument('-t','--time_range', required=True, help='[<FROM(2020-01-01T12:00:00.000Z)>,<TO(2020-03-23T18:00:00.000Z)>] Time range in RFC3339 format')
    parser.add_argument('-s','--step_mins', type=float, required=True, help='[<int>] Step in minutes used in time range')
    parser.add_argument('-l','--linke_turbidity_factor', required=True, help='[<SINGLE_LINKE(decimal)>] or [<MONTHLY_LINKE(12 comma separated decimals)>] Linke turbidity factor - single value or 12 (monthly) values')
    parser.add_argument('input_file',help='[<INPUT_FILE>]')
    parser.add_argument('output_file',help='[<OUTPUT_FILE>]')
    parser.add_argument('-hr','--horizon',help='[<ANGLE_STEP(int)>,<ELEVATION(float,float,...)>] Horizon height used to take in account surrounding horizon (hills) when modeling solar radiation in smaller areas')
    parser.add_argument('-v','--voxel-size',type=float,help='[<float>] Size of the voxel in meters')
    parser.add_argument('-p','--average-points-in-voxel',type=float,default=4,help='[default=4] Used instead of specifying voxel size')
    parser.add_argument('-b','--block-process-params',help='[<SIZE(int)>,<OVERLAP(int)>] Used to divide clod in square blocks and process them sequentially')
    parser.add_argument('--output-ply-ascii',default=False,help="For ply output, specify if using binary (default) or text format")

    args = parser.parse_args()
    config = vars(args)
    return config

def main():
    pcrst_inputs = cmd_args()

    logging.info("========= Point Cloud Solar Radiation Tool =========")

    pcsrt(pcrst_inputs)

    logging.info("====================== Done ========================");

if __name__ == '__main__':
    main()
