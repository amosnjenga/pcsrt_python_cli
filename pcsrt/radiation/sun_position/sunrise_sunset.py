from math import sin, cos, tan, asin, atan, tanh, radians, degrees,acos,pi
from datetime import datetime, timezone,timedelta
import pytz

#RAD = pi / 180.0
RAD = 0.017453292519943295769236907684886
JD2000 = 2451545.0
#PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286
PI = pi
PI2 = PI * 2.0

class SunriseSunset:
    def __init__(self, sunrise, sunset, polar_day, polar_night):
        self.sunrise = sunrise
        self.sunset = sunset
        self.polar_day = polar_day
        self.polar_night = polar_night

def calc_sunrise_and_set(utc, lat, lon):
    jd = to_julian(utc)
    t = (jd - JD2000) / 36525.0
    h = -50.0 / 60.0 * RAD
    b = lat * RAD  # geographische Breite
    geographische_laenge = lon

    ra_d, dk = berechne_zeitgleichung(t)

    aux = (sin(h) - sin(b) * sin(dk)) / (cos(b) * cos(dk))
    if aux >= 1.0:
        return SunriseSunset(None, None, False, True)
    elif aux <= -1.0:
        return SunriseSunset(None, None, True, False)
    else:
        zeitdifferenz = 12.0 * acos(aux) / PI

        aufgang_lokal = 12.0 - zeitdifferenz - ra_d
        untergang_lokal = 12.0 + zeitdifferenz - ra_d
        aufgang_welt = aufgang_lokal - geographische_laenge / 15.0
        untergang_welt = untergang_lokal - geographische_laenge / 15.0
        jd_start = int(jd)  # discard fraction of day

        aufgang_jd = jd_start - 0.5 + (aufgang_welt / 24.0)
        untergang_jd = jd_start - 0.5 + (untergang_welt / 24.0)

        sunrise = to_utc(aufgang_jd)
        sunset = to_utc(untergang_jd)
        return SunriseSunset(sunrise, sunset, False, False)

def to_utc(jd):
    secs_since_epoch = (jd - 2440587.5) * 86400.0
    secs = int(secs_since_epoch)
    nanos = int((secs_since_epoch - secs) * (1000.0 * 1000.0 * 1000.0))
    microseconds = nanos // 1000  # Convert nanoseconds to microseconds
    return datetime.fromtimestamp(secs, tz=timezone.utc).replace(microsecond=microseconds)

def to_julian(utc):
    utc_with_tz = utc.replace(tzinfo=timezone.utc)  # Make utc offset-aware
    seconds_since_epoch = (utc_with_tz - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
    return (seconds_since_epoch / 86400.0) + 2440587.5

#def in_PI(angle):
 #   while angle > PI:
  #      angle -= PI2
  #  while angle < -PI:
   #     angle += PI2
   # return angle

def in_PI(x):
    n = int(x / PI2)
    result = x - (n * PI2)
    if result < 0.0:
        result += PI2
    return result

def eps(t):
    return RAD * (23.43929111 + ((-46.8150) * t - 0.00059 * t**2 + 0.001813 * t**3) / 3600.0)

def berechne_zeitgleichung(t):
    ra_mittel = 18.71506921 + 2400.0513369 * t + (2.5862e-5 - 1.72e-9 * t) * t * t

    m = in_PI(PI2 * (0.993133 + 99.997361 * t))
    l = in_PI(
        PI2 * (0.7859453
            + m / PI2
            + (6893.0 * sin(m) + 72.0 * sin(2.0 * m) + 6191.2 * t) / 1296.0e3),
    )
    e = eps(t)
    ra = atan(tan(l) * cos(e))

    if ra < 0.0:
        ra += PI
    if l > PI:
        ra += PI

    ra = 24.0 * ra / PI2

    dk = asin(sin(e) * sin(l))

    ra_mittel = 24.0 * in_PI(PI2 * ra_mittel / 24.0) / PI2

    d_ra = ra_mittel - ra
    if d_ra < -12.0:
        d_ra += 24.0
    if d_ra > 12.0:
        d_ra -= 24.0

    d_ra *= 1.0027379

    return (d_ra, dk)
