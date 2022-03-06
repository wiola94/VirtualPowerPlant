
import instalation_matcher as im
import pandas as pd
import matplotlib.pyplot as plt

first_set = im.get_installation_sets()[0]
building, heat_pump, water_tank = first_set
building_demand_list_kW = building.get_all_heat_power_list_kW()
temperatures = pd.read_csv('temperatury_2017.csv')['temp'].values.tolist()

hp_heat_power_list_kW = []
hp_compressor_power_list_kW = []
wt_load_level_list_kWh = []
wt_reload_power_list_kW = []
wt_load_power_list_kW = []
electric_heater_list_kW = []

for i in range(len(building_demand_list_kW)):

    # Weź aktualne dla godziny:
    # - moc pompy ciepła
    # - zapotrzebowanie budynku
    # - moc kompresora pompy ciepła
    # - temperatura otoczenia
    # - stan zbiornika

    hp_max_heat_power_kW = heat_pump.get_heat_power_kW(temperatures[i])
    hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(temperatures[i])
    hp_heat_power_kW = 0
    hp_compressor_power_kW = 0
    electric_heater_kW = 0

    building_demand_kW = building_demand_list_kW[i]
    external_temperature = temperatures[i]

    wt_load_level_kWh = water_tank.current_state_kWh
    wt_load_power_kW = 0
    wt_reload_power_kW = 0

    if building_demand_kW > 0:

        # Czy zbiornik pełny
        if water_tank.current_state_kWh >= water_tank.capacity_kWh:

            # Wyłącz pompę ciepła i zbiornik.reload()
            heat_pump.is_hp_on = False
            wt_reload_power_kW = water_tank.reload_tank(building_demand_kW)
            wt_load_level_kWh = water_tank.current_state_kWh
            wt_load_power_kW = 0
            hp_heat_power_kW = 0
            hp_compressor_power_kW = 0
            electric_heater_kW = 0
        else:

            # Czy pompa ciepła włączona
            if heat_pump.is_hp_on:

                # Moc cieplna > Zapotrzebowanie
                if hp_max_heat_power_kW > building_demand_kW:

                    # Ogrzewaj dom
                    hp_heat_power_kW = building_demand_kW
                    # Zbiornik.load()
                    wt_load_power_kW = water_tank.load_tank(hp_max_heat_power_kW - hp_heat_power_kW)
                    hp_heat_power_kW += wt_load_power_kW
                    hp_compressor_power_kW = hp_heat_power_kW*hp_max_compressor_power_kW/hp_max_heat_power_kW
                    electric_heater_kW = 0
                    wt_reload_power_kW = 0
                    wt_load_level_kWh = water_tank.current_state_kWh
                else:

                    # Energia w zbiorniku > (Zapotrzebowanie - moc cieplna pompy)
                    if water_tank.current_state_kWh > (building_demand_kW - hp_max_heat_power_kW):

                        # Ogrzewaj dom
                        hp_heat_power_kW = hp_max_heat_power_kW
                        wt_reload_power_kW = water_tank.reload_tank(building_demand_kW - hp_heat_power_kW )
                        hp_compressor_power_kW = hp_max_compressor_power_kW
                        wt_load_power_kW = 0
                        electric_heater_kW = 0
                        wt_load_level_kWh = water_tank.current_state_kWh
                    else:

                        # Ogrzewaj dom, włącz grzałkę, zbiornik.reload()
                        hp_heat_power_kW = hp_max_heat_power_kW
                        wt_reload_power_kW = water_tank.reload_tank(building_demand_kW - hp_heat_power_kW)
                        hp_compressor_power_kW = hp_max_compressor_power_kW
                        wt_load_power_kW = 0
                        electric_heater_kW = building_demand_kW - hp_heat_power_kW - wt_reload_power_kW
                        wt_load_power_kW = 0

            else:

                # Energia w zbiorniku > Zapotrzebowanie
                if water_tank.current_state_kWh > building_demand_kW:

                    # Zbiornik.reload()
                    wt_reload_power_kW = water_tank.reload_tank(building_demand_kW)
                    wt_load_power_kW = 0
                    hp_heat_power_kW = 0
                    hp_compressor_power_kW = 0
                    electric_heater_kW = 0
                    wt_load_level_kWh = water_tank.current_state_kWh

                else:

                    # Włącz pompę ciepła
                    heat_pump.is_hp_on = True
                    hp_max_heat_power_kW = heat_pump.get_heat_power_kW(temperatures[i])
                    hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(temperatures[i])

                    # Moc cieplna > Zapotrzebowanie - pobór ze zbiornika
                    if hp_max_heat_power_kW >= building_demand_kW - water_tank.current_state_kWh:

                        # Ogrzewaj dom, Zbiornik.load()
                        hp_heat_power_kW = building_demand_kW - water_tank.current_state_kWh
                        wt_reload_power_kW = water_tank.reload_tank(building_demand_kW - hp_heat_power_kW)
                        wt_reload_power_kW = 0
                        wt_load_power_kW = water_tank.load_tank(hp_max_heat_power_kW - hp_heat_power_kW)
                        wt_load_level_kWh = water_tank.current_state_kWh
                        hp_heat_power_kW += wt_load_power_kW
                        hp_compressor_power_kW = hp_heat_power_kW*hp_max_compressor_power_kW/hp_max_heat_power_kW
                        electric_heater_kW = 0

                    else:

                        # Ogrzewaj dom, zbiornik.reload(), włacz grzałkę
                        hp_heat_power_kW = hp_max_heat_power_kW
                        hp_compressor_power_kW = hp_max_compressor_power_kW
                        wt_reload_power_kW = water_tank.reload_tank(water_tank.current_state_kWh)
                        wt_load_level_kWh = 0
                        wt_load_power_kW = 0
                        electric_heater_kW = building_demand_kW - hp_heat_power_kW - wt_reload_power_kW

    else:
        # Zbiornik.standby()
        water_tank.standby()
        hp_heat_power_kW = 0
        hp_compressor_power_kW = 0
        wt_load_level_kWh = water_tank.current_state_kWh
        wt_load_power_kW = 0
        wt_reload_power_kW = 0
        electric_heater_kW = 0

    # Zapisz stany budynku, pompy, zbiornika i grzałki
    hp_heat_power_list_kW.append(hp_heat_power_kW)
    hp_compressor_power_list_kW.append(hp_compressor_power_kW)
    wt_load_level_list_kWh.append(wt_load_level_kWh)
    wt_load_power_list_kW.append(wt_load_power_kW)
    wt_reload_power_list_kW.append(wt_reload_power_kW)
    electric_heater_list_kW.append(electric_heater_kW)

# energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
# plt.plot(energy_prices['0'].values)
plt.plot(electric_heater_list_kW, 'ro--', label='grzałka', markersize=1, linewidth=0.5)
# plt.plot(hp_heat_power_list_kW, 'bo--', label='moc pompy', markersize=1, linewidth=0.5)
plt.plot(building_demand_list_kW, 'go--', label='zapotrzebowanie budynku', markersize=1, linewidth=0.5)
# plt.plot(wt_load_level_list_kWh, 'co--', label='poziom naładowania kWh', markersize=1, linewidth=0.5)
plt.legend()
plt.show()


energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
energy_prices_list = energy_prices['0'].values.tolist()

electricity_price = []
for i in range(len(temperatures)):
    e_sum = (hp_compressor_power_list_kW[i] + electric_heater_list_kW[i]) * energy_prices_list[i]/1000
    electricity_price.append(e_sum)

print(sum(electricity_price))
