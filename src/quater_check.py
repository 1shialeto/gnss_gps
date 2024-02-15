from math import pi, sin, cos


def quarter_check(val):
    """
    По своей сути, исключает ситуацию, когда значение \nu приводит к тому, что значение E_i оказывается отрицательным.
    """
    _x = sin(val / 2)
    _y = cos(val / 2)
    if _x < 0:
        return val + pi
    elif _x > 0 and _y <= 0:
        return val + 2 * pi
    else:
        return val


def quarter_check_xy(val, y, x):
    """
    По своей сути, исключает ситуацию, когда значение \nu приводит к тому, что значение E_i оказывается отрицательным.
    """
    _x = x
    _y = y
    if _x < 0:
        return val + pi
    elif _x > 0 and _y <= 0:
        return val + 2 * pi
    else:
        return val
