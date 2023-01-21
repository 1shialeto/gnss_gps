import numpy
from numpy import sqrt, dot, cross
from numpy.linalg import norm

# Find the intersection of three spheres
# P1,P2,P3 are the centers, r1,r2,r3 are the radii
# Implementaton based on Wikipedia Trilateration article.

P1 = numpy.array([21031628.291, 1897945.217, 16297595.916])
P2 = numpy.array([15387850.260, -6481481.674, 21205641.589])
P3 = numpy.array([-21118938.493, 932872.038, 15865643.064])

r1 = 23612516.130
r2 = 24220471.101
r3 = 24386001.455


def trilaterate(P1, P2, P3, r1, r2, r3):
    temp1 = P2 - P1
    e_x = temp1 / norm(temp1)
    temp2 = P3 - P1
    i = dot(e_x, temp2)
    temp3 = temp2 - i * e_x
    e_y = temp3 / norm(temp3)
    e_z = cross(e_x, e_y)
    d = norm(P2 - P1)
    j = dot(e_y, temp2)
    x = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    y = (r1 * r1 - r3 * r3 - 2 * i * x + i * i + j * j) / (2 * j)
    temp4 = r1 * r1 - x * x - y * y
    if temp4 < 0:
        raise Exception("The three spheres do not intersect!");
    z = sqrt(temp4)
    p_12_a = P1 + x * e_x + y * e_y + z * e_z
    p_12_b = P1 + x * e_x + y * e_y - z * e_z
    return p_12_a, p_12_b


print(trilaterate(P1, P2, P3, r1, r2, r3))
