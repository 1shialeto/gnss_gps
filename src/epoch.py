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
                'gps_sec'
        """
        if args and kwargs:
            raise ValueError
        elif len(args) == 1:
            arg = args[0]
            if type(arg) == 'str':
                epoch_list = arg.split()
            else:
                raise ValueError
        elif len(args) == 6:
            self.__year = self.__correct_year(args[0])
            self.__month = args[1]
            self.__day = args[2]
            self.__hours = args[3]
            self.__minutes = args[4]
            self.__seconds = args[5]
        else:
            raise ValueError


        self.__unix_seconds = 0
        self.__gps_seconds = 0

    def __calc_gps_time(self, unix_time) -> float:
        ...

    def __correct_year(self, year) -> int:
        """
        Исправляет значение года с двухзначного (98) на обычное (1998), если всё ок то просто возвращает значение
        """
        if year // 100 > 0:
            return year
        elif year > 80:
            self.real_year_m = 1900 + year
        else:
            self.real_year_m = 2000 + year

    @property
    def unix(self):
        return self.__unix_seconds

    def gps_seconds(self) -> float:
        return self.__gps_seconds

    def gps_week(self) -> int:
        return self.__gps_seconds // 604_800

    def gps_weekday(self) -> int:
        """
        Возвращает номер GPS дня
        0 Sunday
        1 Monday
        2 Tuesday
        3 Wednesday
        4 Thursday
        5 Friday
        6 Saturday
        """
        ...

    def weekday(self) -> int:
        """
        Возвращает номер дня
        0 Monday
        1 Tuesday
        2 Wednesday
        3 Thursday
        4 Friday
        5 Saturday
        6 Sunday
        """
        ...

    def time(self):
        """
        Возвращает время эпохи в виде строки формата:
        'hours minutes seconds'
        """
        ...

    def date(self):
        """
        Возвращает дату эпохи в виде строки формата:
        'year month day'
        """
        ...

    def epoch(self):
        """
        Возвращает значения эпохи в виде строки формата:
        'year month day hours minutes seconds'
        """
        ...

    def seconds_of_gps_week(self):
        """
        Возвращает количество секунд, прошедшее с начала GPS недели (GPS неделя начинается с воскресенья)
        """
        ...

    def seconds_of_day(self):
        """
        Возвращает количество секунд, прошедшее с начала дня
        """
        ...

if __name__ == "__main__":
    time1 = Epoch(0, unix=0)