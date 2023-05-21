class Centroid:
    def __init__(self, lat,lon,elevation):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation

    def __repr__(self) -> str:
        return f"Centroid(lat={self.lat}, lon={self.lon}, elevation={self.elevation})"
