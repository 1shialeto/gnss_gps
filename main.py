from rinex_processor import GpsNavigationMessageFile

path = 'rinex_files/nsk10160.22n'

nsk1 = GpsNavigationMessageFile(path)

nsk1.create_csv_sheet()

#for i in range((len(nsk1.observations))):
#    print(nsk1.observations[i].SV_health)
