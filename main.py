from src import rinex_processor as rinex
from vpython import *
from random import randint

COLORS = [color.red, color.yellow, color.black, color.green, color.orange, color.white, color.blue,
          color.cyan, color.magenta]

path = 'data/raw/nsk10160.22n'
# nsk1 = rinex.GpsNavMessageFile(path)

scene = canvas(title='Местоположение спутников ECEF', width=1600, height=900, center=vector(5, 0, 0),
               background=color.gray(0.07))


def draw_ellipsoid():
    """
    Отрисовывает Земной эллипсоид
    """
    a = 6_378_137 * 2
    b = 6_356_752.314 * 2
    earth = ellipsoid(pos=vector(0, 0, 0),
                      axis=vector(0, 0, -1),
                      length=a,
                      height=b,
                      width=a,
                      color=color.white,
                      texture={'file': 'img/t_earth.jpg',
                               'bumpmap': 'img/t_earth_normal.jpg'})


def draw_observations(obs):
    """
    Отрисовывает положение всех наблюдений
    """
    satellites = []
    for i in range(len(obs.observations)):
        satellite = obs.observations[i]
        # color = COLORS[int(satellite.Epoch.hour / 24 * 9)]
        xyz = satellite.calculate_coordinates()
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        satellites.append(sphere(pos=vector(x, y, z), radius=100000, color=color.red))


def draw_light():
    scene.ambient = color.gray(0.7)


def draw_coordinate_system():
    x = arrow(pos=vector(0, 0, 0),
              axis=vector(0, 0, 0),
              length=10000000,
              shaftwidth=100000,
              color=color.red)
    y = arrow(pos=vector(0, 0, 0),
              axis=vector(0, 0, -1),
              length=10000000,
              shaftwidth=100000,
              color=color.blue)
    z = arrow(pos=vector(0, 0, 0),
              axis=vector(0, 1, 0),
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
              axis=vector(0, 1, 0),
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


def draw_vectors():
    one = arrow(pos=vector(0, 0, 0),
              axis=vector(0, 0, 10),
              length=10000000,
              shaftwidth=100000,
              color=color.yellow)
    two = arrow(pos=vector(0, 0, 0),
              axis=vector(0, 10, 0),
              length=10000000,
              shaftwidth=100000,
              color=color.yellow)
    three = arrow(pos=vector(0, 0, 0),
              axis=vector(-10, 0, 0),
              length=10000000,
              shaftwidth=100000,
              color=color.yellow)
    four = arrow(pos=vector(0, 0, 0),
              axis=vector(10, 0, 0),
              length=10000000,
              shaftwidth=100000,
              color=color.yellow)

if __name__ == "__main__":
    draw_light()
    draw_ellipsoid()
    draw_coordinate_system()
    draw_vectors()
    # Цикл, чтобы в консоль не лезли ошибки
    while True:
        pass


