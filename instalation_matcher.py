import pandas as pd

from WaterTankCreator import WaterTankCreator
from HeatPumpCreator import HeatPumpCreator
from Building import Building
from WaterTank import WaterTank


def get_installation_sets():

    installation_list = []

    hp_creator = HeatPumpCreator()
    wt_creator = WaterTankCreator()

    build1 = Building(3, 130, people=2)
    build2 = Building(1, 200, people=4)
    build3 = Building(2, 165, people=2)
    buildings = [build1, build2, build3]
    heat_pumps = hp_creator.heat_pumps
    temperatures = pd.read_csv('temperatury_2017.csv').values.tolist()

    for building in buildings:
        demands = building.get_all_heat_power_list_kW()
        dem_with_minus_5_C = []
        for i in range(len(temperatures)):
            if -5.5 < temperatures[i][1] <= -4.5:
                dem_with_minus_5_C.append(demands[i])

        max_demand = max(dem_with_minus_5_C)
        print('Maksymalne zapotrzebowanie na CO i CWU dla -5 C: {}'.format(max_demand))

        big_heat_pumps = []
        for heat_pump in heat_pumps:
            if heat_pump.get_heat_power_kW(-5) > max_demand:
                big_heat_pumps.append(heat_pump)

        if big_heat_pumps:
            best_heat_pump = big_heat_pumps[0]
            for big_heat_pump in big_heat_pumps:
                if big_heat_pump.get_heat_power_kW(-5) < best_heat_pump.get_heat_power_kW(-5):
                    best_heat_pump = big_heat_pump
            print('dopasowana pompa ma moc w -5 C: {}'.format(best_heat_pump.get_heat_power_kW(-5)))
        else:
            print('nie udało się dobrać pompy')
            continue

        hp_demand_15_C = best_heat_pump.get_heat_power_kW(15)

        water_tank_rule = {12: WaterTank.from_liters_to_kWh(12*30),
                        16: WaterTank.from_liters_to_kWh(16*30),
                        25: WaterTank.from_liters_to_kWh(25*30),
                        35: WaterTank.from_liters_to_kWh(35*30),
                        60: WaterTank.from_liters_to_kWh(60*30)}

        if hp_demand_15_C <= 12:
            ideal_water_tank_capacity_kWh = water_tank_rule[12]
        elif 12< hp_demand_15_C <= 16:
            ideal_water_tank_capacity_kWh = water_tank_rule[16]
        elif 16< hp_demand_15_C <= 25:
            ideal_water_tank_capacity_kWh = water_tank_rule[25]
        elif 25< hp_demand_15_C <= 35:
            ideal_water_tank_capacity_kWh = water_tank_rule[35]
        elif 35< hp_demand_15_C <= 60:
            ideal_water_tank_capacity_kWh = water_tank_rule[60]

        water_tanks = wt_creator.water_tanks
        big_water_tanks = []

        for water_tank in water_tanks:
            if water_tank.capacity_kWh > ideal_water_tank_capacity_kWh:
                big_water_tanks.append(water_tank)

        best_water_tank = big_water_tanks[0]
        for big_water_tank in big_water_tanks:
            if big_water_tank.capacity_kWh < best_water_tank.capacity_kWh:
                best_water_tank = big_water_tank

        installation_list.append((building, best_heat_pump, best_water_tank))
        print('dobrany magazyn o pojemności w kWh: {}\n'.format(best_water_tank.capacity_kWh))

    return installation_list


