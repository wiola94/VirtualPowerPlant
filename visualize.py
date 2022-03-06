import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ________WYKRES_TEMPERATUR_W_ROKU________________________________
# temperatures = pd.read_csv('temperatury_2017.csv')
# plt.figure(figsize=(20, 10))
# plt.plot(temperatures['temp'], '.-.', markersize=3.5, linewidth=0.5)
# plt.xlabel('godziny w roku', fontsize=12)
# plt.ylabel('temperatura [oC]', fontsize=12)
# plt.title('Dane temperaturowe dla 2017 roku', fontsize=18)
# plt.show()
# plt.savefig('zdj/temperatury.png', dpi=300, inches='tight')

# ________HISTOGRAM_TEMPERATUR_W_ROKU________________________________
# plt.figure(figsize=(20, 10))
# plt.hist(temperatures['temp'], bins=50)
# plt.ylabel('ilość godzin', fontsize=12)
# plt.xlabel('temperatura [oC]', fontsize=12)
# plt.title('Rozkład częstości występowanie temperatur dla 2017 roku', fontsize=18)
# plt.savefig('zdj/temperatury_hist.png', dpi=300, inches='tight')
# temperatures = pd.read_csv('temperatury_2017.csv')


#________WYKRES_CEN_W_ROKU________________________________
energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
energy_prices_list = energy_prices['0'].values.tolist()
plt.figure(figsize=(20, 10))
plt.plot(energy_prices_list[5112:5137], 'r.-.', markersize=3.5, linewidth=0.5)
plt.xlabel('godziny w roku', fontsize=12)
plt.ylabel('Cena energii elektrycznej [PLN]', fontsize=12)
plt.title('Ceny energii elektrycznej w 2017 roku', fontsize=18)
# plt.show()
plt.savefig('zdj/ceny_1_sierpnia_dzien.png', dpi=300, inches='tight')


# ___________CWU_WYKRES_NA_OSOBĘ_______________________
# plt.figure(figsize=(20, 10))
# hot_water = pd.read_excel('hot_water.xlsx')['liters_of_water']
# # plt.bar(x=range(0, 24), height=hot_water[0: 25], color='red')
# plt.plot(hot_water[0: 25], 'rD-.', markersize=8, linewidth=1)
# plt.xlabel('godziny w ciągu dnia', fontsize=12)
# plt.ylabel('Zapotrzebowanie [l/h]', fontsize=12)
# plt.title('Zapotrzebowanie na c.w.u na jedną osobę', fontsize=18)
# plt.savefig('zdj/cwu_plot.png', dpi=300, inches='tight')


# ________WYKRES_ZAPOTRZEBOWANIA_NA_MOC_CIEPLNĄ_W_ROKU_________________________
# plt.figure(figsize=(20, 10))
# plt.xlabel('godziny w roku', fontsize=12)
# plt.ylabel('Moc cieplna [kW]', fontsize=12)
# plt.title('Zapotrzebowanie budynku na ciepło w roku\ntyp budynku: {}, pole powierzchni: {}, ilość mieszkańców: {}'.format(
#     building.type_of_building, building.area, building.people), fontsize=18)
# plt.plot(building_demand_list_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=3.5, linewidth=0.5)
# plt.savefig('zdj/zapotrzebowanie_{}.png'.format(building.area), dpi=300, inches='tight')


# __________________SYMULACJA_WE_DLA_CAŁEGO_ROKU__________________________________________
# fig = plt.figure(figsize=(20, 10))
# ax1 = fig.add_axes([0.1, 0.45, 0.8, 0.5], xticklabels=[])
# plt.title(
#     'Symulacja WE dla budynku - typ: {}, pole: {}, mieszkańcy: {}'.format(
#         building.type_of_building, building.area, building.people), fontsize=18)
# plt.ylabel('Moc [kW]', fontsize=12)
#
# ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.3])
# plt.title('Stan napełnienia zbiornika [kWh]', fontsize=18)
# plt.xlabel('godziny w roku', fontsize=12)
# plt.ylabel('Poziom napełnienia [kWh]', fontsize=12)
#
# ax1.plot(hp_heat_power_list_kW, 'bo--', label='moc pompy', markersize=1, linewidth=0.5)
# ax1.plot(building_demand_list_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=1, linewidth=0.5)
# ax1.plot(electric_heater_list_kW, 'ro--', label='moc grzałki', markersize=1, linewidth=1)
# ax1.legend(loc='upper left')
#
# ax2.plot(wt_load_level_list_kWh, 'co--', markersize=1, linewidth=0.5)
# plt.savefig('zdj/sym_WE_bud_{}.png'.format(building.area), dpi=300, inches='tight')

# __________________ZUŻYCIE_ENERGII_ELEKTRYCZNEJ_W_ROKU__________________________________________
# plt.figure(figsize=(20, 10))
# plt.xlabel('godziny w roku', fontsize=12)
# plt.ylabel('Moc cieplna [kW]', fontsize=12)
# plt.title(
#     'Wykorzystanie energii elektrycznej w roku\ntyp budynku: {}, pole powierzchni: {}, ilość mieszkańców: {}'.format(
#         building.type_of_building, building.area, building.people), fontsize=18)
# plt.plot(hp_compressor_power_list_kW, '.-.', color='grey', label='zapotrzebowanie budynku', markersize=3.5,
#          linewidth=0.5)
# # plt.savefig('zdj/elec_usage_WE_{}.png'.format(building.area), dpi=300, inches='tight')
# plt.show()


# __________________SYMULACJA_WE_DLA_CAŁEGO_ROKU__________________________________________
# fig = plt.figure(figsize=(20, 10))
# ax1 = fig.add_axes([0.1, 0.45, 0.8, 0.5], xticklabels=[])
# plt.title(
#     'Symulacja dzienna dla budynku - typ: {}, pole: {}, mieszkańcy: {}'.format(
#         building.type_of_building, building.area, building.people), fontsize=18)
# plt.ylabel('Moc [kW]', fontsize=12)
#
# ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.3])
# plt.title('Stan napełnienia zbiornika [kWh]', fontsize=18)
# plt.xlabel('godziny w roku', fontsize=12, )
# plt.ylabel('Poziom napełnienia [kWh]', fontsize=12)
#
# ax1.plot(hp_heat_power_list_kW[4320:4368], 'bo--', label='moc pompy', markersize=1, linewidth=0.5)
# ax1.plot(building_demand_list_kW[4320:4368], '.-.', color='grey', label='zapotrzebowanie budynku', markersize=1, linewidth=0.5)
# ax1.plot(electric_heater_list_kW[4320:4368], 'ro--', label='moc grzałki', markersize=1, linewidth=1)
# ax1.legend(loc='upper left' )
#
# ax2.plot(wt_load_level_list_kWh[4320:4368], 'co--', markersize=1, linewidth=0.5)
# plt.xticks(range(48), range(4320, 4368),  rotation=60)
#
# # plt.show()
# plt.savefig('zdj/sym_1d_WE_bud_{}.png'.format(building.area), dpi=300, inches='tight')