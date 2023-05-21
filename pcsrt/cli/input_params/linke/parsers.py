import re
from . import linke

def parse_linke(input_str,linkeclass=linke.Linke):
    single_re = re.compile(r"^\d+\.{0,1}\d*$")
    monthly_re = re.compile(r"^(\d+\.{0,1}\d*,){11}\d+\.{0,1}\d*$")
    if single_re.match(input_str):
        single_linke = float(input_str)
        return linkeclass([int(single_linke)])
    elif monthly_re.match(input_str):
        linke_list = list(map(float, input_str.split(',')))
        linke_array = [int(linke_list[i]) for i in range(12)]
        return linkeclass.from_array(linke_array)
    else:
        return ValueError("Invalid Linke turbidity factor value [Use single float value or 12 (monthly) float values separated by comma]")
