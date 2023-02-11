import datetime


class Epoch:
    # contains time data
    def __init__(self, *args, **kwargs):
        """
        Способы инициализации:
            string:
                '*  2020  7 18  0  0  0.00000000'
                '2020  7 18  0  0  0.00000000'
                '[int, int, int, int, int, float]'
                '22  1 16  0  0  0.0000000  '
                'unix=int'
                'gps_sec=int'
        """
        if args:
            tz = datetime.timezone.utc  # нужно чтобы datetime.datetime не выдавал UNIX время в часовом поясе пользователя
            if len(args) == 1 and type(args[0]) == 'str' or 'tuple':
                epoch_list = args[0].split()

                self._year = self.__correct_year(epoch_list[-6])
                self._month = int(epoch_list[-5])
                self._day = int(epoch_list[-4])
                self._hours = int(epoch_list[-3])
                self._minutes = int(epoch_list[-2])
                self._seconds = float(epoch_list[-1])
                microseconds = int(self._seconds % 1 * 1000000)
                self.__dt = datetime.datetime(self._year, self._month, self._day, self._hours, self._minutes,
                                              int(self._seconds), microseconds, tz)

            elif len(args) == 6:
                self._year = self.__correct_year(args[0])
                self._month = int(args[1])
                self._day = int(args[2])
                self._hours = int(args[3])
                self._minutes = int(args[4])
                self._seconds = float(args[5])
                microseconds = int(self._seconds % 1 * 1000000)
                self.__dt = datetime.datetime(self._year, self._month, self._day, self._hours, self._minutes,
                                              int(self._seconds), microseconds, tz)
            else:
                raise ValueError
        elif kwargs:
            ...
        else:
            raise ValueError

        self.__unix_seconds = self.__dt.timestamp()
        self.__gps_seconds = self.__calc_gps_time(self.__unix_seconds)

    def __calc_gps_time(self, unix_time) -> float:
        diffSec_gps_unix = 315964800  # difference between UNIX start and GPS-T start
        date = self._year + self._month / 12
        gps_time = self.__unix_seconds - diffSec_gps_unix
        return gps_time

    @staticmethod
    def __correct_year(year) -> int:
        """
        Исправляет значение года с двухзначного (98) на обычное (1998), если всё ок то просто возвращает значение
        """
        year = int(year)
        if year // 100 > 0:
            return year
        elif year > 80:
            return 1900 + year
        else:
            return 2000 + year

    @property
    def unix(self) -> float:
        """
        Возвращает UNIX-timestamp эпохи
        """
        return self.__unix_seconds

    @property
    def gps_seconds(self) -> float:
        """
        Возвращает GPS время эпохи в секундах
        """
        return self.__gps_seconds

    @property
    def gps_week(self) -> int:
        """
        Возвращает номер GPS недели эпохи
        """
        # pycharm почему-то ругается, что при целочисленном делении будет float??
        gps_week = int(self.__gps_seconds // 604_800)
        return gps_week

    @property
    def gps_weekday(self) -> int:
        """
        Возвращает номер GPS дня
        0 Sunday
        6 Saturday
        """
        weekdays_gps = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}
        weekday = self.__dt.weekday()
        gps_weekday = weekdays_gps[weekday]
        return gps_weekday

    @property
    def weekday(self) -> int:
        """
        Возвращает номер дня
        0 Monday
        6 Sunday
        """
        return self.__dt.weekday()

    @property
    def time(self) -> str:
        """
        Возвращает время эпохи в виде строки формата:
        'hours minutes seconds'
        """
        h_m_s = [str(self._hours), str(self._minutes), str(self._seconds)]
        time_string = ' '.join(h_m_s)
        return time_string

    @property
    def date(self) -> str:
        """
        Возвращает дату эпохи в виде строки формата:
        'year month day'
        """
        y_m_d = [str(self._year), str(self._month), str(self._day)]
        date_string = ' '.join(y_m_d)
        return date_string

    @property
    def epoch(self) -> str:
        """
        Возвращает значения эпохи в виде строки формата:
        'year month day hours minutes seconds'
        """
        epoch_string = ' '.join([self.date, self.time])
        return epoch_string

    @property
    def seconds_of_gps_week(self) -> float:
        """
        Возвращает количество секунд, прошедшее с начала GPS недели (GPS неделя начинается с воскресенья)
        """
        return self.__gps_seconds - self.gps_week * 604_800

    @property
    def seconds_of_day(self) -> float:
        """
        Возвращает количество секунд, прошедшее с начала дня
        """
        t_sec = self._seconds + self._minutes * 60 + self._hours * 3600
        return t_sec
