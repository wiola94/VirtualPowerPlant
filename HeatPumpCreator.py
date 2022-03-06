import pandas as pd

from HeatPump import HeatPump


class HeatPumpCreator:
    def __init__(self):
        self.parameters = pd.read_excel('heat_pump.xlsx')
        self.temperatures = self.parameters['temp'].values
        self.heat_powers = self.parameters['hp'].values
        self.compressor_powers = self.parameters['cp'].values
        self.heat_pumps = []
        for i in range(len(self.temperatures)):
            if i % 4 == 0:
                self.heat_pumps.append(HeatPump(self.temperatures[i:i+4], self.heat_powers[i:i+4],
                                                self.compressor_powers[i:i+4]))
