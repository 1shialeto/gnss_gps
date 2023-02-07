class Epoch:
    # contains time data
    def __init__(self, *args):

        """
        self.year_m = year  # 2 digits, padded with 0 if necessary
        if self.year_m > 80:
            self.real_year_m = 1900 + year
        else:
            self.real_year_m = 2000 + year
        """

        self.__unix_seconds = 0
        self.__gps_seconds = 0

    def calc_gps_time(self, unix_time) -> float:
        ...

    @property
    def unix(self):
        return self.__unix_seconds

    def gps(self) -> float:
        return self.__gps_seconds

    def gps_week(self) -> int:
        return self.__gps_seconds // 604_800

    def gps_day(self) -> int:
        ...

    def time(self):
        ...

    def date(self):
        ...

    def epoch(self):
        ...

    def seconds_of_gps_week(self):
        ...

    def seconds_of_day(self):
        ...