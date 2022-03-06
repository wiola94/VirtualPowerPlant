
import instalation_matcher as im
import pandas as pd
import matplotlib.pyplot as plt

for f_set in im.get_installation_sets():
    building, heat_pump, water_tank = f_set
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
    # plt.plot(wt_load_power_list_kW, 'ro--', label='ładowanie magazynu', markersize=1, linewidth=0.5)
    # plt.plot(hp_heat_power_list_kW, 'bo--', label='moc pompy', markersize=1, linewidth=0.5)
    # plt.plot(building_demand_list_kW, 'go--', label='zapotrzebowanie budynku', markersize=1, linewidth=0.5)
    # plt.plot(wt_load_level_list_kWh, 'co--', label='poziom naładowania kWh', markersize=1, linewidth=0.5)
    # plt.plot(electric_heater_list_kW, 'ro--', label='moc grzałki', markersize=4, linewidth=1)
    # plt.legend()
    # plt.show()


    energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
    energy_prices_list = energy_prices['0'].values.tolist()

    electricity_price = []
    electricity_usage_kW = []
    for i in range(len(temperatures)):
        e_sum = hp_compressor_power_list_kW[i] + electric_heater_list_kW[i]
        electricity_usage_kW.append(e_sum)
        electricity_price.append(e_sum * energy_prices_list[i] / 1000)

    print('Cena w sumie: '+str(sum(electricity_price)))
    print(sum(electricity_usage_kW))
    print(sum(electric_heater_list_kW))
    print('Zapotrzebowanie budynku w sumie: ' + str(sum(building_demand_list_kW)))

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_axes([0.1, 0.45, 0.8, 0.5], xticklabels=[])
    plt.title(
        'Dzień w zimie dla budynku - typ: {}, pole: {}, mieszkańcy: {}'.format(
            building.type_of_building, building.area, building.people), fontsize=18)
    plt.ylabel('Moc [kW]', fontsize=12)

    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.3])
    plt.title('Stan napełnienia zbiornika [kWh]', fontsize=18)
    plt.xlabel('godziny w roku', fontsize=12)
    plt.ylabel('Poziom napełnienia [kWh]', fontsize=12)

    ax1.plot(hp_heat_power_list_kW[420:468], 'bo--', label='moc pompy', markersize=4, linewidth=1)
    ax1.plot(building_demand_list_kW[420:468], '.-.', color='grey', label='zapotrzebowanie budynku', markersize=4, linewidth=1)
    ax1.plot(electric_heater_list_kW[420:468], 'ro--', label='moc grzałki', markersize=4, linewidth=1)
    ax1.legend(loc='upper left')
    plt.xticks(range(48), range(420, 468), rotation=60)
    ax2.plot(wt_load_level_list_kWh[420:468], 'co--', markersize=4, linewidth=1)
    # plt.show()

    plt.savefig('zdj/zima_1d_bud_{}.png'.format(building.area), dpi=300, inches='tight')
    #
    # plt.figure(figsize=(20, 10))
    # plt.xlabel('godziny w roku', fontsize=12)
    # plt.ylabel('Moc cieplna [kW]', fontsize=12)
    # plt.title(
    #     'Wykorzystanie energii elektrycznej w roku\ntyp budynku: {}, pole powierzchni: {}, ilość mieszkańców: {}'.format(
    #         building.type_of_building, building.area, building.people), fontsize=18)
    # plt.plot(electricity_usage_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=3.5, linewidth=0.5)
    # plt.savefig('zdj/elec_usage_{}.png'.format(building.area), dpi=300, inches='tight')