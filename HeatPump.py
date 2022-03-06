class HeatPump:
    def __init__(self, external_temperature, heat_power_kW, compressor_power_kW):
        self.a0 = (heat_power_kW[0]-(heat_power_kW[1]*external_temperature[0]-heat_power_kW[0]*external_temperature[1])
                   / (external_temperature[0]-external_temperature[1]))/external_temperature[0]
        self.b0 = (heat_power_kW[1]*external_temperature[0]-heat_power_kW[0]*external_temperature[1])\
                  / (external_temperature[0]-external_temperature[1])
        self.a1 = (heat_power_kW[1]-(heat_power_kW[2]*external_temperature[1]-heat_power_kW [1]*external_temperature[2])
                   / (external_temperature[1]-external_temperature[2]))/external_temperature[1]
        self.b1 = (heat_power_kW[2]*external_temperature[1]-heat_power_kW[1]*external_temperature[2])\
                  / (external_temperature[1] - external_temperature[2])
        self.a2 = (heat_power_kW[2]-(heat_power_kW[3]*external_temperature[2]-heat_power_kW[2]*external_temperature[3])
                   / (external_temperature[2] - external_temperature[3]))/external_temperature[2]
        self.b2 = (heat_power_kW[3]*external_temperature[2]-heat_power_kW[2]*external_temperature[3])\
                  / (external_temperature[2] - external_temperature[3])

        self.c0 = (compressor_power_kW[0] - (
                    compressor_power_kW[1] * external_temperature[0] - compressor_power_kW[0] * external_temperature[1])
                   / (external_temperature[0] - external_temperature[1])) / external_temperature[0]
        self.d0 = (compressor_power_kW[1] * external_temperature[0] - compressor_power_kW[0] * external_temperature[1])\
                  / (external_temperature[0] - external_temperature[1])
        self.c1 = (compressor_power_kW[1] - (
                    compressor_power_kW[2] * external_temperature[1] - compressor_power_kW[1] * external_temperature[2])
                   / (external_temperature[1] - external_temperature[2])) / external_temperature[1]
        self.d1 = (compressor_power_kW[2] * external_temperature[1] - compressor_power_kW[1] * external_temperature[2])\
                  / (external_temperature[1] - external_temperature[2])
        self.c2 = (compressor_power_kW[2] - (
                    compressor_power_kW[3] * external_temperature[2] - compressor_power_kW[2] * external_temperature[3])
                   / (external_temperature[2] - external_temperature[3])) / external_temperature[2]
        self.d2 = (compressor_power_kW[3] * external_temperature[2] - compressor_power_kW[2] * external_temperature[3]) \
                  / (external_temperature[2] - external_temperature[3])

        self.t0 = external_temperature[0]
        self.t1 = external_temperature[1]
        self.t2 = external_temperature[2]
        self.t3 = external_temperature[3]

        self.is_hp_on = True

    def get_heat_power_kW(self, external_temp):
        if self.is_hp_on == True:
            if external_temp < self.t1:
                heat_power = self.a0*external_temp+self.b0
            elif self.t1 <= external_temp < self.t2:
                heat_power = self.a1 * external_temp + self.b1
            else:
                heat_power = self.a2 * external_temp + self.b2
            return heat_power
        else:
            return 0

    def get_compressor_power_kW(self, external_temp):
        if self.is_hp_on == True:
            if external_temp < self.t1:
                compressor_power = self.c0*external_temp+self.d0
            elif self.t1 <= external_temp < self.t2:
                compressor_power = self.c1 * external_temp + self.d1
            else:
                compressor_power = self.c2 * external_temp + self.d2
            return compressor_power
        else:
            return 0
