import reload_indexes as ri
import instalation_matcher as im
import pandas as pd
import matplotlib.pyplot as plt

for f_set in im.get_installation_sets():
    building, heat_pump, water_tank = f_set
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
    # plt.plot(hp_heat_power_list_kW, 'bo--', label='moc pompy', markersize=1, linewidth=0.5)
    # plt.plot(building_demand_list_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=3.5, linewidth=0.5)
    # plt.plot(wt_load_level_list_kWh, 'co--', label='poziom naładowania kWh', markersize=1, linewidth=0.5)
    # plt.plot(wt_load_power_list_kW, 'go--', label='moc ładowania magazynu', markersize=1, linewidth=0.5)
    # plt.plot(wt_reload_power_list_kW, 'ro--', label='moc rozładowania magazynu', markersize=1, linewidth=0.5)
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
        electricity_price.append(e_sum* energy_prices_list[i]/1000)

    print('Cena w sumie: '+str(sum(electricity_price)))
    print(sum(electricity_usage_kW))
    print(sum(electric_heater_list_kW))
    print('Zapotrzebowanie budynku w sumie: ' + str(sum(building_demand_list_kW)))


    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_axes([0.1, 0.45, 0.8, 0.5], xticklabels=[])
    plt.title(
        'Dzień w zimie WE dla budynku - typ: {}, pole: {}, mieszkańcy: {}'.format(
            building.type_of_building, building.area, building.people), fontsize=18)
    plt.ylabel('Moc [kW]', fontsize=12)

    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.3])
    plt.title('Stan napełnienia zbiornika [kWh]', fontsize=18)
    plt.xlabel('godziny w roku', fontsize=12, )
    plt.ylabel('Poziom napełnienia [kWh]', fontsize=12)

    ax1.plot(hp_heat_power_list_kW[420:468], 'bo--', label='moc pompy', markersize=4, linewidth=1)
    ax1.plot(building_demand_list_kW[420:468], '.-.', color='grey', label='zapotrzebowanie budynku', markersize=4, linewidth=1)
    ax1.plot(electric_heater_list_kW[420:468], 'ro--', label='moc grzałki', markersize=4, linewidth=1)
    ax1.legend(loc='upper left')

    ax2.plot(wt_load_level_list_kWh[420:468], 'co--', markersize=4, linewidth=1)
    plt.xticks(range(48), range(420, 468),  rotation=60)
    # plt.show()

    plt.savefig('zdj/zima_1d_WE_bud_{}.png'.format(building.area), dpi=300, inches='tight')

    # plt.figure(figsize=(20, 10))
    # plt.xlabel('godziny w roku', fontsize=12)
    # plt.ylabel('Moc cieplna [kW]', fontsize=12)
    # plt.title('Wykorzystanie energii elektrycznej w roku\ntyp budynku: {}, pole powierzchni: {}, ilość mieszkańców: {}'.format(
    #     building.type_of_building, building.area, building.people), fontsize=18)
    # plt.plot(hp_compressor_power_list_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=3.5, linewidth=0.5)
    # # plt.savefig('zdj/elec_usage_WE_{}.png'.format(building.area), dpi=300, inches='tight')
    # plt.show()