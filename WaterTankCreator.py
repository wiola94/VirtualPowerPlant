import pandas as pd
import numpy as np
from WaterTank import WaterTank


class WaterTankCreator:

    def __init__(self):
        self.parameters = pd.read_excel('water_tank.xlsx')
        self.capacities_kWh = self.parameters['kWh'].values
        self.capacities_liters = self.parameters['liters'].values
        self.water_tanks = []

        for i in range(len(self.parameters)):
            if np.isnan(self.capacities_liters[i]):
                self.new_tank = WaterTank(self.capacities_kWh[i])
            else:
                self.new_tank = WaterTank(self.capacities_liters[i], False)
            self.water_tanks.append(self.new_tank)

        for tank in self.water_tanks:
            print(tank.capacity_kWh)

