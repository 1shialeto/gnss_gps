import math
from math import radians, degrees


def rad2dms(val_rad):
    """
   :param val_rad: Decimal degree
   :return:
   """
    val_rad = math.degrees(val_rad)
    is_positive = val_rad >= 0
    val_rad = abs(val_rad)
    minutes, seconds = divmod(val_rad * 3600, 60)
    val_degrees, minutes = divmod(minutes, 60)
    val_degrees = val_degrees if is_positive else -val_degrees
    represented = str(round(val_degrees)) + '°' + str(round(minutes)) + "'" + str(round(seconds, 5, )) + '"'
    return represented


def dms2rad(d, m, s):
    return radians(d + m / 60 + s / 3600)
