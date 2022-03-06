class WaterTank:
    def __init__(self, capacity, kWh=True):
        if not kWh:
            self.capacity_kWh = self.from_liters_to_kWh(capacity)
            self.capacity_liters = capacity
        else:
            self.capacity_kWh = capacity
            self.capacity_liters = self.from_kWh_to_liters(capacity)
        if self.capacity_liters >= 200:
            self.loss_kW = 0.0056*self.capacity_liters - 0.78
        else:
            self.loss_kW = 0.34
        self.current_state_kWh = 0

    def load_tank(self, load_power_kW):
        new_state = self.current_state_kWh + load_power_kW - self.loss_kW
        if new_state < 0:
            self.current_state_kWh = 0
            return 0
        elif new_state > self.capacity_kWh:
            self.current_state_kWh = self.capacity_kWh
            return self.current_state_kWh + load_power_kW - self.capacity_kWh
        else:
            self.current_state_kWh = new_state
            return load_power_kW

    def reload_tank(self, reload_power_kW):
        new_state = self.current_state_kWh - reload_power_kW - self.loss_kW
        if new_state < 0:
            self.current_state_kWh = 0
            return self.current_state_kWh
        else:
            self.current_state_kWh = new_state
            return reload_power_kW

    def standby(self):
        new_state = self.current_state_kWh - self.loss_kW
        if new_state < 0:
            self.current_state_kWh = 0
        else:
            self.current_state_kWh = new_state

    @staticmethod
    def from_liters_to_kWh(liters):
        water_heat = 4.190
        ref_temp = 10
        supply_temp = 45
        sec_in_hour = 3600
        return liters * water_heat * (supply_temp - ref_temp) / sec_in_hour

    @staticmethod
    def from_kWh_to_liters(kwh):
        water_heat = 4.190
        ref_temp = 10
        supply_temp = 45
        sec_in_hour = 3600
        return kwh / (water_heat * (supply_temp - ref_temp) / sec_in_hour)
