import dateutil.parser as date_parser
from . import time_range

def parse_time_range(input_str,timerangeclass=time_range.TimeRange):
    input_list = input_str.split(",")
    if len(input_list) != 2:
        return None, "Invalid time range format"
    try:
        from_date = date_parser.parse(input_list[0].strip())
        to_date = date_parser.parse(input_list[1].strip())
        time_range = timerangeclass(from_date, to_date)
        return time_range
    except ValueError as e:
        return None, str(e)

