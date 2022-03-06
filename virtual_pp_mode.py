import reload_indexes as ri
import instalation_matcher as im
import pandas as pd
import matplotlib.pyplot as plt

first_set = im.get_installation_sets()[0]
building, heat_pump, water_tank = first_set
building_demand_list_kW = building.get_all_heat_power_list_kW()
temperatures = pd.read_csv('temperatury_2017.csv')['temp'].values.tolist()

max_indexes, reload_indexes = ri.get_reload_indexes()
day_numer = 0
break_hour = 0
wt_load_on = True

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

    external_temperature = temperatures[i]
    hp_max_heat_power_kW = heat_pump.get_heat_power_kW(external_temperature)
    hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(external_temperature)
    hp_heat_power_kW = 0
    hp_compressor_power_kW = 0
    electric_heater_kW = 0

    building_demand_kW = building_demand_list_kW[i]


    wt_load_level_kWh = water_tank.current_state_kWh
    wt_load_power_kW = 0
    wt_reload_power_kW = 0

    if i == 5:
        print('heh')

    # Czy godzina = 0 ?
    if i % 24 == 0:

        break_hour = reload_indexes[day_numer]
        day_numer += 1

        # Włącz pompę ciepła i włącz możliwość łądowania zbiornika
        heat_pump.is_hp_on = True
        hp_max_heat_power_kW = heat_pump.get_heat_power_kW(external_temperature)
        hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(external_temperature)
        wt_load_on = True

        # Zapotrzebowanie > 0
        if building_demand_kW > 0:

            # Moc pompy > zapotrzebowanie
            if hp_max_heat_power_kW > building_demand_kW:

                # Grzej wodę pompą, zbiornik.load()
                hp_heat_power_kW = building_demand_kW
                wt_load_power_kW = water_tank.load_tank(hp_max_heat_power_kW - building_demand_kW)
                hp_heat_power_kW += wt_load_power_kW
                hp_compressor_power_kW = hp_heat_power_kW*hp_max_compressor_power_kW/hp_max_heat_power_kW
                wt_reload_power_kW = 0
                wt_load_level_kWh = water_tank.current_state_kWh
                electric_heater_kW = 0

            # Grzej wodę pompą, włącz grzałkę
            else:
                hp_heat_power_kW = hp_max_heat_power_kW
                hp_compressor_power_kW = hp_max_compressor_power_kW
                wt_load_power_kW = 0
                wt_reload_power_kW = 0
                wt_load_level_kWh = water_tank.current_state_kWh
                electric_heater_kW = building_demand_kW - hp_max_heat_power_kW

        # Zbiornik.load()
        else:
            wt_load_power_kW = water_tank.load_tank(hp_max_heat_power_kW)
            hp_heat_power_kW = wt_load_power_kW
            hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
            wt_reload_power_kW = 0
            wt_load_level_kWh = water_tank.current_state_kWh
            electric_heater_kW = 0

    else:

        # Godzina startu rozładowywania
        if i in reload_indexes:

            # Włącz możliwość ładowania zbiornika
            wt_load_on = True

            # Energia w zbiorniku > Zapotrzebowania
            if water_tank.current_state_kWh > building_demand_kW:

                # Wyłącz pompę cieła, zbiornik.reload()
                heat_pump.is_hp_on = False
                wt_reload_power_kW = water_tank.reload_tank(building_demand_kW)
                wt_load_power_kW = 0
                wt_load_level_kWh = water_tank.current_state_kWh
                hp_heat_power_kW = 0
                hp_compressor_power_kW = 0
                electric_heater_kW = 0

            # Włącz pompę ciepła
            else:
                heat_pump.is_hp_on = True
                hp_max_heat_power_kW = heat_pump.get_heat_power_kW(external_temperature)
                hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(external_temperature)

                # Zapotrzebowanie > Moc pompy + Zbiornik
                if building_demand_kW > hp_max_heat_power_kW + water_tank.current_state_kWh:

                    # Grzej wodę pompą, Zbiornik.reload(), włącz grzałkę
                    hp_heat_power_kW = hp_max_heat_power_kW
                    hp_compressor_power_kW = hp_max_compressor_power_kW
                    wt_reload_power_kW = water_tank.reload_tank(water_tank.current_state_kWh)
                    wt_load_power_kW = 0
                    wt_load_level_kWh = water_tank.current_state_kWh
                    electric_heater_kW = building_demand_kW - hp_heat_power_kW - wt_reload_power_kW

                # Grzej wodę pompą zbiornik.reload()
                else:
                    wt_reload_power_kW = water_tank.reload_tank( water_tank.current_state_kWh)
                    hp_heat_power_kW = building_demand_kW - wt_reload_power_kW
                    hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                    wt_load_power_kW = 0
                    wt_load_level_kWh = water_tank.current_state_kWh
                    electric_heater_kW = 0

        else:

            # Czy pompa jest właczona
            if heat_pump.is_hp_on:

                # Czy iterator mniejszy od godziny startu rozładowywania
                if i < break_hour:

                    # Moc pompy > Zapotrzebowanie
                    if hp_max_heat_power_kW > building_demand_kW:

                        # czy zbiornik pełen?
                        if water_tank.current_state_kWh >= water_tank.capacity_kWh:

                            # Grzej wodę pompą i wyłącz możliwość łądowania zbiornika
                            hp_heat_power_kW = building_demand_kW
                            hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                            wt_load_power_kW = 0
                            wt_reload_power_kW = 0
                            wt_load_on = False
                            water_tank.standby()
                            wt_load_level_kWh = water_tank.current_state_kWh
                            electric_heater_kW = 0

                        else:

                            # czy wyłączona możliwość ładowania zbiornika
                            if not wt_load_on:

                                # Grzej wodę pompą, Zbiornik.standby()
                                hp_heat_power_kW = building_demand_kW
                                hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                                wt_load_power_kW = 0
                                wt_reload_power_kW = 0
                                water_tank.standby()
                                wt_load_level_kWh = water_tank.current_state_kWh
                                electric_heater_kW = 0

                            else:

                                # Grzej wode pompą ciepła, zbiornik.load()
                                wt_load_power_kW = water_tank.load_tank(hp_max_heat_power_kW - building_demand_kW)
                                hp_heat_power_kW = building_demand_kW + wt_load_power_kW
                                hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                                wt_reload_power_kW = 0
                                wt_load_level_kWh = water_tank.current_state_kWh
                                electric_heater_kW = 0

                    else:

                        # Zapotrzebowanie > Moc pompy ciepła + zbiornik
                        if building_demand_kW > hp_max_heat_power_kW + water_tank.current_state_kWh:

                            # Grzej wodę pompą, Zbiornik.reload(), włącz grzałkę
                            hp_heat_power_kW = hp_max_heat_power_kW
                            hp_compressor_power_kW = hp_max_compressor_power_kW
                            wt_reload_power_kW = water_tank.reload_tank(water_tank.current_state_kWh)
                            wt_load_power_kW = 0
                            wt_load_level_kWh = 0
                            electric_heater_kW = building_demand_kW - hp_heat_power_kW - wt_reload_power_kW

                        else:

                            # Grzej wodę pompą, zbiornik.reload()
                            hp_heat_power_kW = hp_max_heat_power_kW
                            hp_compressor_power_kW = hp_max_compressor_power_kW
                            wt_reload_power_kW = water_tank.reload_tank(building_demand_kW - hp_heat_power_kW)
                            wt_load_power_kW = 0
                            wt_load_level_kWh = water_tank.current_state_kWh
                            electric_heater_kW = 0

                else:

                    # Moc pompy > zapotrzebowania
                    if hp_max_heat_power_kW > building_demand_kW:

                        #Grzej wodę pompą
                        hp_heat_power_kW = building_demand_kW
                        hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                        wt_load_power_kW = 0
                        wt_reload_power_kW = 0
                        wt_load_level_kWh = water_tank.current_state_kWh
                        electric_heater_kW = 0

                    else:

                        # Grzej wodę pompą, włącz grzałkę
                        hp_heat_power_kW = hp_max_heat_power_kW
                        hp_compressor_power_kW = hp_max_compressor_power_kW
                        wt_load_power_kW = 0
                        wt_reload_power_kW = 0
                        wt_load_level_kWh = water_tank.current_state_kWh
                        electric_heater_kW = building_demand_kW - hp_heat_power_kW

            else:

                # Energia w zbiorniku > Zapotrzebowanie
                if water_tank.current_state_kWh > building_demand_kW:

                    # Zbiornik.reload
                    wt_reload_power_kW = water_tank.reload_tank(building_demand_kW)
                    wt_load_power_kW = 0
                    wt_load_level_kWh = water_tank.current_state_kWh
                    hp_heat_power_kW = 0
                    hp_compressor_power_kW = 0
                    electric_heater_kW = 0

                else:

                    # Włącz pompę
                    heat_pump.is_hp_on = True
                    hp_max_heat_power_kW = heat_pump.get_heat_power_kW(external_temperature)
                    hp_max_compressor_power_kW = heat_pump.get_compressor_power_kW(external_temperature)

                    # Zapotrzebowanie > Moc pompy ciepła + zbiornik

                    if building_demand_kW > hp_max_heat_power_kW + water_tank.current_state_kWh:

                        # Grzej wodę pompą, zbiornik.reload(), włącz grzałkę
                        hp_heat_power_kW = hp_max_heat_power_kW
                        hp_compressor_power_kW = hp_max_compressor_power_kW
                        wt_reload_power_kW = water_tank.reload_tank(water_tank.current_state_kWh)
                        wt_load_power_kW = 0
                        wt_load_level_kWh = water_tank.current_state_kWh
                        electric_heater_kW = building_demand_kW - hp_heat_power_kW - wt_reload_power_kW

                    else:

                        # Grzej wodę pompą, zbiornik.reload()
                        wt_reload_power_kW = water_tank.reload_tank(water_tank.current_state_kWh)
                        hp_heat_power_kW = building_demand_kW - wt_reload_power_kW
                        hp_compressor_power_kW = hp_heat_power_kW * hp_max_compressor_power_kW / hp_max_heat_power_kW
                        wt_load_power_kW = 0
                        wt_load_level_kWh = 0
                        electric_heater_kW = 0

    # Zapisz stany budynku, pompy, zbiornika i grzałki
    # new_load_level_state = wt_load_level_kWh - water_tank.loss_kW
    # if new_load_level_state <= 0:
    #     wt_load_level_kWh = 0
    # else:
    #     wt_load_level_kWh = new_load_level_state

    hp_heat_power_list_kW.append(hp_heat_power_kW)
    hp_compressor_power_list_kW.append(hp_compressor_power_kW)
    wt_load_level_list_kWh.append(wt_load_level_kWh)
    wt_load_power_list_kW.append(wt_load_power_kW)
    wt_reload_power_list_kW.append(wt_reload_power_kW)
    electric_heater_list_kW.append(electric_heater_kW)


#plt.plot(wt_load_power_list_kW, 'ro--', label='ładowanie magazynu', markersize=1, linewidth=0.5)
plt.plot(hp_heat_power_list_kW, 'bo-', label='moc pompy', markersize=2, linewidth=0.5)
plt.plot(building_demand_list_kW, 'go-', label='zapotrzebowanie budynku', markersize=2, linewidth=1)
plt.plot(wt_load_level_list_kWh, 'co-', label='poziom naładowania kWh', markersize=2, linewidth=0.5)
# plt.plot(wt_load_power_list_kW, 'co--', label='moc ładowania magazynu', markersize=1, linewidth=0.5)
# plt.plot(wt_reload_power_list_kW, 'ro--', label='moc rozładowania magazynu', markersize=1, linewidth=0.5)
plt.plot(electric_heater_list_kW, 'ro-', label='moc grzałki', markersize=2, linewidth=1)
plt.legend()
plt.show()

energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
energy_prices_list = energy_prices['0'].values.tolist()

electricity_price = []
for i in range(len(temperatures)):
    e_sum = (hp_compressor_power_list_kW[i] + electric_heater_list_kW[i]) * energy_prices_list[i]/1000
    electricity_price.append(e_sum)

print(sum(electricity_price))