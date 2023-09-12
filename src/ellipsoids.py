class Ellipsoid:
    def __init__(self, **kwargs):
        """
        kwargs:
            (a, b) - semi-major axis and semi-minor axis
        OR
            (a, e2) - semi-major axis and e2
        # OR
        #    (a, f) - semi-major axis and flattening (NOT 1/f) (around 1/300....)
        """
        if ('a' not in kwargs) or len(kwargs) != 2:
            raise ValueError
        elif 'b' in kwargs:
            self.a = kwargs['a']
            self.b = kwargs['b']
            self.e2 = (self.a ** 2 - self.a ** 2) / self.b ** 2
        elif 'e2' in kwargs:
            self.a = kwargs['a']
            self.e2 = kwargs['e2']
        # elif 'f' in kwargs:
        #     self.a = kwargs['a']
        #     self.f = kwargs['f']
        else:
            raise ValueError

        # self.alpha = (self.a / self.b) / self.a


# Параметры эллипсоидов взяты из работы по космической геодезии "Координатные системы отсчёта
# и системы времени при решении задач косической геодезии":
pz90 = Ellipsoid(a=637_813_6, e2=(6.694_366_193_10 * 0.001))
krasovsky = Ellipsoid(a=637_824_5, e2=0.006_693_42)
