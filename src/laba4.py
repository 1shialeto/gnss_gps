# Лабораторные работы по космической геодезии
# Работа 1. Координатные системы отсчёта и системы времени при решении задач космической геодезии
# Усольцев Артём, ПГ-31, 2023 год
# Вариант 3
########################################################################################################################
import numpy as np
from math import sqrt, pi, acos, atan, tan, sin, cos, radians, degrees
from quater_check import quarter_check, quarter_check_xy
from rad_dms_hms import rad2dms

# Исходные данные
# Вариант 3
mu = 398_600.5
T0 = 20 + 36 / 60 + 14.56 / 3600  # hms
r_vector = np.array([
    [2882.29],
    [6174.61],
    [-651.55],
])
r_hatch_vector = np.array([
    [-1.0706415],
    [-0.9199195],
    [-8.1917582],
])

# Вариант 12 - Ярик
# mu = 398_600.5
# T0 = 20 + 17 / 60 + 6.31 / 3600  # hms
# r_vector = np.array([
#     [-1495.85],
#    [-7131.49],
#    [11760.37],
# ])
#r_hatch_vector = np.array([
#    [4.9522686],
#    [2.9237356],
#    [0.8745270],
#])


# Кривое удобство
x = r_vector.item(0)
y = r_vector.item(1)
z = r_vector.item(2)
x_hatch = r_hatch_vector.item(0)
y_hatch = r_hatch_vector.item(1)
z_hatch = r_hatch_vector.item(2)

########################################################################################################################
##############################################                 #########################################################
##############################################     РЕШЕНИЕ     #########################################################
##############################################                 #########################################################
########################################################################################################################

##### 1. Формулы для вычисления параметров орбиты.
## a) интеграл Лапласа, интеграл площадей и константа энергии движения:
r = sqrt(x ** 2 +
         y ** 2 +
         z ** 2)

r_hatch = sqrt(x_hatch ** 2 +
               y_hatch ** 2 +
               z_hatch ** 2)

h = r_hatch ** 2 - 2 * mu / r

c_x = y * z_hatch - z * y_hatch
c_y = z * x_hatch - x * z_hatch
c_z = x * y_hatch - y * x_hatch

c_vector = np.array([
    [c_x],
    [c_y],
    [c_z],
])

c = sqrt(c_x ** 2 +
         c_y ** 2 +
         c_z ** 2)

lambda_x = - (mu / r) * x + c_z * y_hatch - c_y * z_hatch
lambda_y = - (mu / r) * y + c_x * z_hatch - c_z * x_hatch
lambda_z = - (mu / r) * z + c_y * x_hatch - c_x * y_hatch

lambda_vector = np.array([
    [lambda_x],
    [lambda_y],
    [lambda_z],
])

_lambda = sqrt(lambda_x ** 2 +
               lambda_y ** 2 +
               lambda_z ** 2)

## б) элементы, задающие размеры, форму орбиты и движение по орбите:
e = _lambda / mu
p = c ** 2 / mu
a = p / (1 - e ** 2)
b = a * sqrt(1 - e ** 2)
r_pi = a * (1 - e)
r_a = a * (1 + e)
n = sqrt(mu / a ** 3)
P = 360 / n

## в) элементы, задающие ориентировку орбиты:
i = acos(c_z / c)  # TODO: не проверяю acos?
Omega = quarter_check_xy(atan(c_x / -c_y),
                         c_x, -c_y)
omega = quarter_check_xy(atan((c * lambda_z) / (c_x * lambda_y - c_y * lambda_x)),
                         c * lambda_z, (c_x * lambda_y - c_y * lambda_x))  # 133

## г) элементы, задающие положение спутника на орбите:
u = quarter_check_xy(atan(z * c / (y * c_x - x * c_y)),
                     z * c, (y * c_x - x * c_y))

v = quarter_check_xy(atan(c * np.dot(np.squeeze(r_vector), np.squeeze(r_hatch_vector)) / (x * lambda_x + y * lambda_y + z * lambda_z)),
                     c * np.dot(np.squeeze(r_vector), np.squeeze(r_hatch_vector)), (x * lambda_x + y * lambda_y + z * lambda_z)
                     )

E = quarter_check_xy(atan((sqrt((1 - e) / (1 + e)) * tan(v / 2))) * 2,
                     sin((sqrt((1 - e) / (1 + e)) * tan(v / 2))) * 2, cos((sqrt((1 - e) / (1 + e)) * tan(v / 2))) * 2)

M = E - (e * sin(E))

delta_t = (M / n) / 3600  # in seconds (rads/rads)
t_pi = T0 - delta_t

##### 2. Контроль вычислений
# if c_vector * r_vector == 0:
#     print("кайфуха брат")
# else:
#    print("ээ брат че то не так")
print(t_pi)
