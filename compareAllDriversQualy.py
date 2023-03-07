import matplotlib.pyplot as plt
import pandas as pd
from timple import timedelta
import fastf1
import fastf1.plotting
import os
from fastf1.core import Laps
import extra_data.teams as teamsDrivers
import extra_data.convert_lap_to_normal as convert
from pandas import DataFrame
from timple.timedelta import strftimedelta

def compareAllDriversQualy(info_data_year, info_data_round,info_data_session):
    if(info_data_round == 'Testing'):
        session = fastf1.get_testing_session(info_data_year, 1 ,info_data_session)
    else:
        session = fastf1.get_session(info_data_year,info_data_round,info_data_session)

    fastf1.Cache.enable_cache('__pycache__')  #cache directory

    laps = session.load()  # whatever session you want to load

    drivers = pd.unique(session.laps['Driver'])

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)

    fig, ax = plt.subplots()

    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='black')

    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])
    #ax.set_yticklabels(fastest_laps['LapTime'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    ax.set_xlabel('Lap Time Delta to Pole Position [s]')

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} {info_data_session}\n"
                f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    #print(fastest_laps.index)

    directory = 'Rezultate\\'+'Grafice_Comparare_Diferenta_Timp_Calificare'
        
    if not os.path.exists(directory):
        os.makedirs(directory)
    print('\n\n----------------------------------------------------------------\n')
    print('S-a generat graficul cu comparatia timpilor intre toti pilotii')
    print('----------------------------------------------------------------\n\n\n')

    plt.savefig(directory+'\\'+'Gaps_'+ str(info_data_year)+'_'+info_data_round+'_'+info_data_session+'.png', dpi=300)