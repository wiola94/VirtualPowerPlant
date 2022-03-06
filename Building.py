import pandas as pd
import matplotlib.pyplot as plt


class Building:
    def __init__(self, type, area, people):
        """
        \nTworzenie instancji budynku
        \n:param type: Numer typu budynku zgodnie z poniższą legendą:
        \n1 : Budynek pasywny
        \n2 : Budynek niskoenergetyczny
        \n3 : Nowe budownictwo
        \n4 : Budynek po modernizacji
        \n5 : Budynek niemodernizowany
        \n:param area: pole powierzchni podłogowej budynku [m2]
        """
        self.ref_temperature = -20
        self.internal_temperature = 20
        self.people = people
        self.type_of_building = type
        self.types_of_buildings = {1: 10, 2: 40, 3: 50, 4: 80, 5: 120}
        self.area_coefficient = self.types_of_buildings[type]   # [W/ m2]
        self.ref_power_kW = self.area_coefficient * area
        self.area = area

    def get_heat_power_list_kW(self):
        """
        \nFunkcja liczy zapotrzebowanie na ciepło budynku na podstawie temperatury otoczenia, która jest zczytywana z bazy danych
        \n:return: Zapotrzebowanie na ciepło budynku w kW przez cały rok
        """
        df = pd.read_csv('temperatury_2017.csv')
        df = df['temp']
        heat_power = []
        for i in range(len(df)):
            result = self.ref_power_kW*(self.internal_temperature - df[i])\
                 / (self.internal_temperature-self.ref_temperature)

            if result < 0 or (6500 > i > 3000):
                result = 0
            heat_power.append(result/1000)
        return heat_power

    def get_heat_water_power_list_kW(self):
        """
        Funnkcja która robi fajowe rzeczy
        \n:param hour_in_day: która godzina w ciągu doby
        \n:return: funkcja zwraca wartość mocy w CWU
        """
        hot_water = pd.read_excel('hot_water.xlsx')
        hot_water_list = hot_water['liters_of_water']

        hot_water_merged_list = hot_water_list

        for i in range(364):
            hot_water_merged_list = pd.concat([hot_water_merged_list, hot_water_list], ignore_index=True)

        hot_water_power_list_kW = [self.people*4.19*(60 - 10)*liters / 3600 for liters in hot_water_merged_list]
        return hot_water_power_list_kW

    def get_all_heat_power_list_kW(self):
        cwu = self.get_heat_water_power_list_kW()
        co = self.get_heat_power_list_kW()

        co_cwu = []
        for i in range(len(co)):
            co_cwu.append(co[i] + cwu[i])
        return co_cwu
