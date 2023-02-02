from rinex_processor import GpsNavMessageFile
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from datetime import datetime

# =========================================================================
navigation_file_path = '../data/raw/nsk12010.20n'
# =========================================================================

# Calculating list of XYZ-coordinates with navigation messages:
nsk1 = GpsNavMessageFile(navigation_file_path)
XYZ_orbital = []
for index, observation in enumerate(nsk1.observations):
    try:
        xyz = observation.calculate_coordinates()
        XYZ_orbital.append(xyz)
    except EnvironmentError:
        print(f'Error with calculating XYZ in obsN{index}.')
        XYZ_orbital.append([0, 0, 0])
        continue


# Creating list of XYZ-coordinates from final-ephemeris:
XYZ_final = []


def find_xyz_in_final(observation, epoch) -> [float, float, float]:
    # Check existence of final ephemeris file and get if it needed

    number_of_day_of_week = datetime.isoweekday(datetime(year, month, day))
    if number_of_day_of_week == 7:
        number_of_day_of_week = 0

    final_ephemeris_number = str(int(observation.GPS_Week)) + str(number_of_day_of_week)
    try:
        # NOTE: файлы final могут начинаться с букв 'emr' или 'igs', надо бы как то это отлавливать, но мне лень
        # Поэтому файлы просто хранятся с приставкой gps*****.sp3.
        ephemeris_file_path = open(f'../data/external/gps{final_ephemeris_number}.sp3')
    except FileNotFoundError:
        # TODO: Реализация автоматического получения файла с серверов https://nasa.gov
        print(f'ФАЙЛ ФИНАЛЬНЫХ ЭФЕМЕРИД gps{final_ephemeris_number}.sp3 НЕ НАЙДЕН. СКАЧАЙТЕ ФАЙЛ И ПОМЕСТИТЕ ЕГО')
        print('В ПАПКУ: "data/external/')
        return [0, 0, 0]

    final_ephemeris_data = ephemeris_file_path.readlines()

    for line_index, text_line in enumerate(final_ephemeris_data):
        if text_line[0] == '*' and int(text_line.split()[4]) == epoch.hour and int(text_line.split()[5]) == epoch.minute:
            # мы нашли строку с правильной эпохой
            for i in range(32):
                current_string = final_ephemeris_data[line_index + i + 1]
                if current_string[0] == '*':
                    break
                elif observation.Satellite_PRN_number == int(current_string[2:4]):
                    xyz_iter = current_string.split()
                    x = float(xyz_iter[1])
                    y = float(xyz_iter[2])
                    z = float(xyz_iter[3])
                    return [x, y, z]
                else:
                    continue
        else:
            continue


for num, observation in enumerate(nsk1.observations):
    # Check existence of final ephemeris file and get if it needed
    epoch = observation.Epoch
    year = epoch.real_year_m
    month = epoch.month_m
    day = epoch.day_m
    hour = epoch.hour
    minute = epoch.minute
    second = epoch.second

    if minute % 15 == 0 and second == 0:  # Если время наблюдения кратно 15 минутам:
        # Find final XYZ in ephemeris file
        xyz_final = find_xyz_in_final(observation, epoch)
        XYZ_final.append(xyz_final)
    else:
        # Do interpolation
        XYZ_final.append([0, 0, 0])
        """
        epoch_before = Epoch()
        epoch_after = Epoch()
        """
        ...


# make data:
deviation = []
x_labels = []
for i in range(211):
    dx = XYZ_final[i][0]*1000 - XYZ_orbital[i][0]
    dy = XYZ_final[i][1]*1000 - XYZ_orbital[i][1]
    dz = XYZ_final[i][2]*1000 - XYZ_orbital[i][2]
    obs = sqrt(dx**2 + dy**2 + dz**2)
    deviation.append(obs)
    print(obs)


x = range(211)


plt.bar(x, deviation)


plt.show()

