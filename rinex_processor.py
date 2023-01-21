from math import sqrt, cos, sin, pi, atan2
import csv

GPS_NAV_MESSAGE_FILE_START_BYTE = 3
GPS_NAV_MESSAGE_FILE_INFO_DURATION = 19


class Epoch:
    # Class, that contains time data. The main purpose is transition from "UTC-time" to "GPS-week-time"
    def __init__(self, outer_instance, year: int, month: int, day: int, hour: int, minute: int, second: float):
        self.year_m = year  # 2 digits, padded with 0 if necessary
        if self.year_m > 80:
            self.real_year_m = 1900 + year
        else:
            self.real_year_m = 2000 + year

        self.month_m = month
        self.day_m = day
        self.hour = hour
        self.minute = minute
        self.second = second

        self.t_sec = self.second + self.minute * 60 + self.hour * 3600  # время, переведённое в секунды

        Day_month = [[0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],  # Leap year
                     [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]]  # Standard year
        # TODO: переписать проверку високосного года
        isLeapYear = 0 if self.real_year_m % 4 == 0 else 1

        # Вот тут ничего не понимаю, формула, которая дана в РГР, всегда даёт значение GPSDay больше на 1 день, чем надо.
        self.GPSDay = Day_month[isLeapYear][self.month_m - 1] + self.day_m - 5
        # self.GPSDay = Day_month[isLeapYear][self.month_m - 1] + self.day_m - 1 - 5

        N_year = self.real_year_m - 1980
        Day_year = N_year * 365 + N_year // 4
        self.tGPSsec = (Day_year + self.GPSDay) * 86400 + self.t_sec

        # TODO: сделать учёт Leap Seconds (високосных секунд) ???

        # outer_instance нужен, чтобы получить WN (Week Number) из GpsObservation
        self.outer_instance = outer_instance
        WN = outer_instance.GPS_Week
        self.GPSsec = self.tGPSsec - WN * 7 * 86400


class GpsNavMessageHeader:
    def __init__(self, Format_version, File_type, PGM, Run_by, Date, Comment, ION_ALPHA, ION_BETA,
                 A0, A1, T, W, Leap_seconds):
        self.Format_version = Format_version
        self.File__type = File_type
        self.PGM = PGM
        self.Run_by = Run_by
        self.Date = Date
        self.Comment = Comment
        self.ION_ALPHA = ION_ALPHA
        self.ION_BETA = ION_BETA
        # DELTA-UTC
        self.A0 = A0
        self.A1 = A1
        self.T = T
        self.W = W
        self.Leap_seconds = Leap_seconds


class GpsObservation:
    def __init__(self, Satellite_PRN_number: int, year: int, month: int, day: int, hour: int, minute: int,
                 second: float, SV_clock_bias: float, SV_clock_drift: float, SV_clock_drift_rate: float, IODE: float,
                 C_rs: float, Delta_n: float, M0: float, C_uc: float, e_Eccentricity: float, C_us: float, sqrt_A: float,
                 T_oe: float, C_ic: float, OMEGA0: float, C_is: float, i0: float, C_rc: float, omega, OMEGA_DOT, IDOT,
                 Codes_on_L2_channel, GPS_Week, L2_P, SV_accuracy, SV_health, TGD, IODS, t_tm,
                 Fit_interval
                 ):
        # === OBS. RECORD: PRN / EPOCH / SV CLK ===
        self.Satellite_PRN_number = Satellite_PRN_number
        self.SV_clock_bias = SV_clock_bias
        self.SV_clock_drift = SV_clock_drift
        self.SV_clock_drift_rate = SV_clock_drift_rate
        # === OBS. RECORD: BROADCAST ORBIT - 1 ===
        self.IODE = IODE  # Issue of Data, Ephemeris
        self.C_rs = C_rs
        self.Delta_n = Delta_n
        self.M0 = M0
        # === OBS. RECORD: BROADCAST ORBIT - 2 ===
        self.C_uc = C_uc
        self.e_Eccentricity = e_Eccentricity
        self.C_us = C_us
        self.sqrt_A = sqrt_A
        # === OBS. RECORD: BROADCAST ORBIT - 3 ===
        self.T_oe = T_oe
        self.C_ic = C_ic
        self.OMEGA0 = OMEGA0
        self.C_is = C_is
        # === OBS. RECORD: BROADCAST ORBIT - 4 ===
        self.i0 = i0
        self.C_rc = C_rc
        self.omega = omega
        self.OMEGA_DOT = OMEGA_DOT
        # === OBS. RECORD: BROADCAST ORBIT - 5 ===
        self.IDOT = IDOT
        self.Codes_on_L2_channel = Codes_on_L2_channel
        self.GPS_Week = GPS_Week
        self.L2_P = L2_P
        # === OBS. RECORD: BROADCAST ORBIT - 6 ===
        self.SV_accuracy = SV_accuracy
        self.SV_health = SV_health
        self.TGD = TGD
        self.IODS = IODS
        # === OBS. RECORD: BROADCAST ORBIT - 7 ===
        self.t_tm = t_tm
        self.Fit_interval = Fit_interval
        # === Epoch init ===
        self.Epoch = Epoch(self, year=year, month=month, day=day, hour=hour, minute=minute, second=second)

        self.t_k = self.Epoch.t_sec - self.T_oe

        # Учёт момента перехода "начало/конец недели"
        if self.t_k > 302_400:
            self.t_k -= 604_800
        elif self.t_k < -302_400:
            self.t_k += 604_800

    def get_list(self) -> list:
        out_list = [self.Satellite_PRN_number, self.Epoch.year_m, self.Epoch.month_m, self.Epoch.day_m, self.Epoch.hour,
                    self.Epoch.minute, self.Epoch.second, self.SV_clock_bias, self.SV_clock_drift,
                    self.SV_clock_drift_rate,
                    self.IODE, self.C_rs, self.Delta_n, self.M0, self.C_uc, self.e_Eccentricity, self.C_us, self.sqrt_A,
                    self.T_oe, self.C_ic, self.OMEGA0, self.C_is, self.i0, self.C_rc, self.omega, self.OMEGA_DOT,
                    self.IDOT,
                    self.Codes_on_L2_channel, self.GPS_Week, self.L2_P, self.SV_accuracy, self.SV_health,
                    self.TGD, self.IODS, self.t_tm, self.Fit_interval]
        return out_list

    def calculate_coordinates(self):
        # Calculates XYZ coordinates from observation in WGS-84
        OMEGA_e = 7.292_115_146_7e-5
        mu = 3.986_005e+14
        A = self.sqrt_A ** 2
        n0 = sqrt(mu / (A ** 3))
        n = n0 + self.Delta_n

        M = (self.M0 + n * self.t_k + 2 * pi) % (2 * pi)

        # TODO: Переделать под нормальный вид
        E = M
        for i in range(10):
            E = M + (self.e_Eccentricity * sin(E))

        E_final = (E + 2 * pi) % (2 * pi)

        nu = atan2((sqrt(1 - self.e_Eccentricity ** 2)) * sin(E_final) / (1 - self.e_Eccentricity * cos(E_final)), (cos(E_final) - self.e_Eccentricity) / (1 - self.e_Eccentricity * cos(E_final)))

        PHI = nu + self.omega

        du = self.C_us * sin(2 * PHI) + self.C_uc * cos(2 * PHI)
        dr = self.C_rs * sin(2 * PHI) + self.C_rc * cos(2 * PHI)
        di = self.C_is * sin(2 * PHI) + self.C_ic * cos(2 * PHI)

        u = PHI + du
        r = A * (1 - self.e_Eccentricity * cos(E_final)) + dr
        i = self.i0 + di + self.IDOT * self.t_k

        # Orbital coordinates of satellite
        x = r * cos(u)
        y = r * sin(u)

        OMEGA_k = self.OMEGA0 + (self.OMEGA_DOT - OMEGA_e) * self.t_k - OMEGA_e * self.T_oe

        # Satellite coordinates in ECEF CS (WGS-84)
        X = x * cos(OMEGA_k) - y * cos(i) * sin(OMEGA_k)
        Y = x * sin(OMEGA_k) + y * cos(i) * cos(OMEGA_k)
        Z = y * sin(i)
        return [X, Y, Z]


class GpsNavigationMessageFile:

    @staticmethod
    def convert_raw_data_to_normal_float(raw_string: str) -> float:
        char_remov = ["E", "D", "d"]
        funny = raw_string
        for char in char_remov:
            # replace() "returns" an altered string
            funny = funny.replace(char, "e")
        try:
            return float(funny.strip())
        except ValueError:
            return 0

    @staticmethod
    def read_line(string: str) -> list:
        values = [0, 0, 0, 0]  # Because  .append() function, if you try to add (null) does nothing
        for j in range(0, 4):
            start = GPS_NAV_MESSAGE_FILE_START_BYTE + GPS_NAV_MESSAGE_FILE_INFO_DURATION * j
            end = GPS_NAV_MESSAGE_FILE_START_BYTE + GPS_NAV_MESSAGE_FILE_INFO_DURATION * (j + 1)
            values[j] = float(GpsNavigationMessageFile.convert_raw_data_to_normal_float(string[start:end]))
        return values

    @staticmethod
    def read_first_line(string: str) -> list:
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Should be NOT ITERABLE (?)
        values[0] = int(string[0:2].strip())
        values[1] = int(string[2:5].strip())
        values[2] = int(string[5:8].strip())
        values[3] = int(string[8:11].strip())
        values[4] = int(string[11:15].strip())
        values[5] = int(string[15:17].strip())
        values[6] = float(GpsNavigationMessageFile.convert_raw_data_to_normal_float(string[17:22]))
        values[7] = float(GpsNavigationMessageFile.convert_raw_data_to_normal_float(string[22:41]))
        values[8] = float(GpsNavigationMessageFile.convert_raw_data_to_normal_float(string[41:60]))
        values[9] = float(GpsNavigationMessageFile.convert_raw_data_to_normal_float(string[60:79]))
        return values

    def __init__(self, file_gnmf_path: str):
        self.f = open(file_gnmf_path, 'r')
        self.data = self.f.readlines()
        self.file_name = file_gnmf_path.split('/')[-1]
        # Finding line number of "Header End-Line"
        self.header_end_line = 0
        for text_line in self.data:
            if "END OF HEADER" in text_line.strip():
                break
            else:
                self.header_end_line += 1

        # Reading header data
        # TODO: self.header = GpsNavMessageHeader()

        # Reading observations
        self.amount_of_observations = int((len(self.data) - self.header_end_line) / 8)
        self.observations = [] * self.amount_of_observations
        for k in range(self.amount_of_observations):  # every observation

            # === OBS. RECORD: PRN / EPOCH / SV CLK ===
            bo0 = self.read_first_line(self.data[k * 8 + 1 + self.header_end_line])
            Satellite_PRN_number, year, month, day, hour, minute, second, SV_clock_bias, SV_clock_drift, \
            SV_clock_drift_rate = bo0[0], bo0[1], bo0[2], bo0[3], bo0[4], bo0[5], bo0[6], bo0[7], bo0[8], bo0[9]

            # === OBS. RECORD: BROADCAST ORBIT - 1 ===
            bo1 = self.read_line(self.data[k * 8 + 2 + self.header_end_line])
            IODE, C_rs, Delta_n, M0 = bo1[0], bo1[1], bo1[2], bo1[3]

            # === OBS. RECORD: BROADCAST ORBIT - 2 ===
            bo2 = self.read_line(self.data[k * 8 + 3 + self.header_end_line])
            C_uc, e_Eccentricity, C_us, sqrt_A = bo2[0], bo2[1], bo2[2], bo2[3]

            # === OBS. RECORD: BROADCAST ORBIT - 3 ===
            bo3 = self.read_line(self.data[k * 8 + 4 + self.header_end_line])
            T_oe, C_ic, OMEGA0, C_is = bo3[0], bo3[1], bo3[2], bo3[3]

            # === OBS. RECORD: BROADCAST ORBIT - 4 ===
            bo4 = self.read_line(self.data[k * 8 + 5 + self.header_end_line])
            i0, C_rc, omega, OMEGA_DOT = bo4[0], bo4[1], bo4[2], bo4[3]

            # === OBS. RECORD: BROADCAST ORBIT - 5 ===
            bo5 = self.read_line(self.data[k * 8 + 6 + self.header_end_line])
            IDOT, Codes_on_L2_channel, GPS_Week, L2_P = bo5[0], bo5[1], bo5[2], bo5[3]

            # === OBS. RECORD: BROADCAST ORBIT - 6 ===
            bo6 = self.read_line(self.data[k * 8 + 7 + self.header_end_line])
            SV_accuracy, SV_health, TGD, IODS = bo6[0], bo6[1], bo6[2], bo6[3]

            # === OBS. RECORD: BROADCAST ORBIT - 7 ===
            bo7 = self.read_line(self.data[k * 8 + 8 + self.header_end_line])
            t_tm, Fit_interval = bo7[0], bo7[1]

            self.observations.append(GpsObservation(Satellite_PRN_number, year, month, day, hour, minute,
                                                    second, SV_clock_bias, SV_clock_drift, SV_clock_drift_rate, IODE,
                                                    C_rs, Delta_n, M0, C_uc, e_Eccentricity, C_us, sqrt_A,
                                                    T_oe, C_ic, OMEGA0, C_is, i0, C_rc, omega, OMEGA_DOT, IDOT,
                                                    Codes_on_L2_channel, GPS_Week, L2_P, SV_accuracy, SV_health,
                                                    TGD, IODS, t_tm, Fit_interval))

    def create_csv_sheet(self):
        with open(f'{self.file_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            header = 'Satellite_PRN_number, year, month, day, hour, minute, second, SV_clock_bias, SV_clock_drift, ' \
                     'SV_clock_drift_rate, IODE, C_rs, Delta_n, M0, C_uc, e_Eccentricity, C_us, sqrt_A, T_oe, C_ic, ' \
                     'OMEGA0, C_is, i0, C_rc, omega, OMEGA_DOT, IDOT, Codes_on_L2_channel, GPS_Week, L2_P, SV_accuracy, ' \
                     'SV_health, TGD, IODS, t_tm, Fit_interval'.replace(' ', '').split(',')
            writer.writerow(header)
            for i in range(len(self.observations)):
                data = self.observations[i].get_list()
                writer.writerow(data)


if __name__ == "__main__":
    path = 'rinex_files/nsk10160.22n'
    nsk1 = GpsNavigationMessageFile(path)
    print(nsk1.observations[10].calculate_coordinates())
