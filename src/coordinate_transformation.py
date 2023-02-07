from math import atan2, sqrt, cos, sin, degrees


# TODO: реализация работы с разными эллипсоидами
def XYZtoBLH(args: list[float]) -> list[float]:
    """
    Вычисление геодезических пространственных координат по пространственным прямоугольным координатам
    Source: К. Ф. Афонин - Высшая геодезия. Системы координат и преобразования между ними (2020)
    * BLH - degrees
    * XYZ - meters
    """
    B, L, H = 0, 0, 0  # initial
    X, Y, Z = args[0], args[1], args[2]

    # Параметры эллипсоида WGS-84
    a = 6_378_137.0  # малая полуось
    b = 6_356_752.314_245  # большая полуось
    e2 = (a ** 2 - b ** 2) / a ** 2  # квадрат эксцентриситета

    # Longitude
    L_temp = atan2(Y, X)
    if X == 0:
        if Y == 0:
            raise ValueError
        elif Y > 0:
            L = 90
        elif Y < 0:
            L = 270
    elif X > 0:
        if Y >= 0:
            L = L_temp
        elif Y < 0:
            L = 360 - abs(L_temp)
    elif X < 0:
        if Y >= 0:
            L = 180 - abs(L_temp)
        elif Y < 0:
            L = 180 + L_temp

    # Auxiliary values
    Q = sqrt(X ** 2 + Y ** 2)
    u = atan2(Z, Q * sqrt(1 - e2))

    # Latitude
    arg1 = Z + e2 * ((a * sin(u) ** 3) / (sqrt(1 - e2)))
    arg2 = Q - e2 * a * cos(u) ** 3
    B = atan2(arg1, arg2)

    # Height
    W = sqrt(1 - e2 * sin(B) ** 2)
    N = a / W
    H = Q * cos(B) + Z * sin(B) - N * (1 - e2 * sin(B) ** 2)

    return [degrees(B), degrees(L), round(H, 3)]


if __name__ == "__main__":
    calc = XYZtoBLH([284_946.867, 3_914_611.222, 5_011_671.248])
    ref = [degrees(0.909662408736263), degrees(1.49813388756017), 850.119]
    print(XYZtoBLH([284_946.867, 3_914_611.222, 5_011_671.248]))
    print(ref)
