from rinex_processor import GpsNavigationMessageFile
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

path = 'rinex_files/nsk12010.20n' #week 21751
nsk1 = GpsNavigationMessageFile(path)

f = open('emr21146.sp3')
data = f.readlines()


def find_final_xyz(epoch: str, prn: int) -> [float, float, float]:
    header_end_line = 0
    for text_line in data:
        if epoch in text_line.replace("  ", " "):
            break
        else:
            header_end_line += 1
    if header_end_line >= len(data):
        return None

    line = data[header_end_line + prn].split()

    x = float(line[1])
    y = float(line[2])
    z = float(line[3])
    return [x, y, z]


# make data:
differences = []
for i in range(len(nsk1.observations)):
    satellite = nsk1.observations[i]
    # color = COLORS[int(satellite.Epoch.hour / 24 * 9)]
    xyz = satellite.calculate_coordinates()
    prn = nsk1.observations[i].Satellite_PRN_number
    x_o = xyz[0]
    y_o = xyz[1]
    z_o = xyz[2]
    epoch = nsk1.observations[i].Epoch  # 2022  1 16  0  0  0.00000000
    epoch_string = "* " + str(epoch.real_year_m) + " " + str(epoch.month_m) + " " + str(epoch.day_m) + " " + str(epoch.hour) + " " + str(epoch.minute) + " " + str(epoch.second)
    final_xyz = find_final_xyz(epoch_string, prn)
    if not final_xyz:
        continue

    x_f = final_xyz[0] * 1000
    y_f = final_xyz[1] * 1000
    z_f = final_xyz[2] * 1000

    obs = [prn, x_o - x_f, y_o - y_f, z_o - z_f]
    differences.append(obs)

dx = []
for i in range(len(differences)):
    dx.append(differences[i][1])

dy = []
for i in range(len(differences)):
    dy.append(differences[i][2])

dz = []
for i in range(len(differences)):
    dz.append(differences[i][3])


x = range(0, len(dx))
kvdr = []
for i in range(len(differences)):
    kvdr.append(sqrt(differences[i][1]**2 + differences[i][2]**2 + differences[i][3]**2))

plt.bar(x, kvdr)


plt.show()


