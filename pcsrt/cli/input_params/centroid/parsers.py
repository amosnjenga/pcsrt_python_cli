from . centroid import Centroid

def parse_centroid(input,centroidclass=Centroid):
    input_vec = [float(i) for i in input.split(",")]

    if len(input_vec) != 3:
        return None, "Centroid coordinates invalid"
    else:
        lat = input_vec[0]
        lon = input_vec[1]
        elevation = input_vec[2]

        #if not (-90.0 <= lat <= 90.0):
         #   return None, "Centroid lat not in -90°;90° range"
        #elif not (-180.0 <= lon <= 180.0):
          #  return None, "Centroid lon not in -180°;180° range"
        #else:
         #   return centroidclass(lat, lon, elevation)
        return centroidclass(lat, lon, elevation)
