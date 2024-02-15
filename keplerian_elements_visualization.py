from vpython import *

COLORS = [color.red, color.yellow, color.black, color.green, color.orange, color.white, color.blue,
          color.cyan, color.magenta]

scene = canvas(title='Визуализация пути ИСЗ по элементам орбиты Кеплера', width=1600, height=900, center=vector(5, 0, 0),
               background=color.gray(0.07))


def draw_earth():
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


orbit = ellipsoid(pos=vector(0, 0, 0),
                  length=10000, height=0, width=10000)


# if __name__ == "__main__":
#     draw_light()
#     draw_earth()
#     draw_coordinate_system()
#     draw_vectors()
#     # Цикл, чтобы в консоль не лезли ошибки
a = 0
e = 0
i = 0
Omega = 0
omega = 0
theta = 0

sl_a = slider(min=0.3, max=3, value=a)

while True:
    pass
