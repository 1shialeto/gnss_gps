import vpython
from math import pi

from rinex_processor import GpsNavigationMessageFile
from math import sqrt
from vpython import *

path = 'rinex_files/nsk10160.22n'

nsk1 = GpsNavigationMessageFile(path)

scene = canvas(title='Местоположение спутников ECEF', width=1500, height=900, center=vector(5, 0, 0),
               background=color.gray(0.07))


a = 6378137
b = 6356752.3142
# the first ellipsoid
earth = ellipsoid(pos=vector(0, 0, 0),
                  axis=vector(0, 0, -pi),
                  length=a,
                  height=b,
                  width=a,
                  color=color.white,
                  texture={'file': 'img/t_earth.jpg'})
satellites = []
for i in range(len(nsk1.observations)):
    xyz = nsk1.observations[i].calculate()
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    satellites.append(sphere(pos=vector(x, y, z), radius=100000, color=color.white))

light = distant_light(direction=vector(0.22,  0.44,  2 + pi),       color=color.gray(1))
scene.ambient = color.gray(0.7)

x = arrow(pos=vector(0, 0, 0),
          axis=vector(0, 0, 0),
          length=10000000,
          shaftwidth=100000,
          color=color.red)
y = arrow(pos=vector(0, 0, 0),
          axis=vector(0, 0, -pi),
          length=10000000,
          shaftwidth=100000,
          color=color.blue)
z = arrow(pos=vector(0, 0, 0),
          axis=vector(0, pi, 0),
          length=10000000,
          shaftwidth=100000,
          color=color.green)

oxy = box(pos=vector(0, 0, 0),
          length=55000000,
          height=100000,
          width=55000000,
          opacity=0.2,
          color=color.green,
          texture='img/t_planes.jpg')
oyz = box(pos=vector(0, 0, 0),
          axis=vector(0, pi, 0),
          length=55000000,
          height=100000,
          width=55000000,
          color=color.red,
          opacity=0.2,
          texture='img/t_planes.jpg')
oxz = box(pos=vector(0, 0, 0),
          length=55000000,
          height=55000000,
          width=100000,
          color=color.blue,
          opacity=0.2,
          texture='img/t_planes.jpg')

# ang = 0
# rotate_rate = 0.00005
# while True:
#    rate(10)
#    scene.camera.rotate(ang)
#    ang += rotate_rate
