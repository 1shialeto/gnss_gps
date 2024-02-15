def linear_interpolation(x0, y0, x1, y1):
    interpolated_y = []
    m = (y1 - y0) / (x1 - x0)  # Вычисляем коэффициент наклона
    c = y0 - m * x0  # Вычисляем свободный член
    x = x0 + 1  # Начинаем со следующего целого значения X после x0
    while x < x1:
        y = m * x + c  # Используем уравнение прямой для интерполяции Y
        interpolated_y.append(y)
        x += 1
    return interpolated_y


x0, y0 = 187, 19
x1, y1 = 203, 17

interpolated_y = linear_interpolation(x0, y0, x1, y1)
print(interpolated_y)

