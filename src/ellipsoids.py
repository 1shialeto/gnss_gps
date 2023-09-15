from math import sqrt, sin


class Ellipsoid:
    def __init__(self, **kwargs):
        """
            (a: float, b: float) - semi-major axis and semi-minor axis
        OR
            (a: float, e2: float) - semi-major axis and e2
        """
        if ('a' not in kwargs) or len(kwargs) != 2:
            raise ValueError
        elif 'b' in kwargs:
            self.a = float(kwargs['a'])
            self.b = float(kwargs['b'])
            self.e2 = (self.a ** 2 - self.a ** 2) / self.b ** 2
        elif 'e2' in kwargs:
            self.a = float(kwargs['a'])
            self.e2 = float(kwargs['e2'])
        # elif 'f' in kwargs:
        #     self.a = kwargs['a']
        #     self.f = kwargs['f']
        else:
            raise ValueError

    # self.alpha = (self.a / self.b) / self.a

    def N(self, B: float):
        """
        :param B: latitude (rads)
        :return: radius of curvature of the ellipsoid in the first vertical (meters)
        """
        N = self.a / sqrt(1 - self.e2 * sin(B) ** 2)
        return N


pz9011 = Ellipsoid(a=6_378_136, e2=0.006_694_3662)
krasovsky = Ellipsoid(a=6_378_245, e2=0.006_693_42)
wgs84 = Ellipsoid(a=6_378_137, e2=0.006_694_38)
