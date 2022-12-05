from rinex_processor import GpsNavigationMessageFile
from math import sqrt
path = 'rinex_files/nsk10160.22n'

nsk1 = GpsNavigationMessageFile(path)


distances = []
for i in range(len(nsk1.observations)):
    xyz = nsk1.observations[i].calculate()
    dist = sqrt(xyz[0]**2 + xyz[1]**2 + xyz[2]**2)
    distances.append(dist)
    print(dist)
