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

def compareAllDriversQualy(info_data_year, info_data_round,info_data_session): #functia care va fi apelata in main.py
    if(info_data_round == 'Testing'):
        session = fastf1.get_testing_session(info_data_year, 1 ,info_data_session) #daca e sesiune de teste, se pune 1 (sau 2, doar pentru anul 2022) ca runda
    else:
        session = fastf1.get_session(info_data_year,info_data_round,info_data_session)

    fastf1.Cache.enable_cache('__pycache__')  #cache directory

    laps = session.load()  #colectam datele de la API

    drivers = pd.unique(session.laps['Driver']) 
    #luam fiecare pilot in parte dupa timpul pe tur

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True) #sortam de la timpul cel mai lent la cel mai rapid

    pole_lap = fastest_laps.pick_fastest() #selectam cel mai rapid timp
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime'] #calculam diferenta dintre cel mai rapid timp al fiecarui pilot si cel mai rapid timp al sesiunii

    #coloram fiecare pilot dupa culoarea echipei
    team_colors = list() 
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)

    fig, ax = plt.subplots() #creem graficul


    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='black') #creem bara de diferenta de timpi

    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # intoarcem valorile astfel incat sa fie de la cel mai rapid la cel mai lent
    ax.invert_yaxis()

    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    ax.set_xlabel('Lap Time Delta to Pole Position [s]')

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms') #convertim timpul in formatul MM:SS.MS

    plt.suptitle(f"{session.event['EventName']} {session.event.year} {info_data_session}\n"
                f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    #folderul unde se va salva graficul
    directory = 'Rezultate\\'+'Grafice_Comparare_Diferenta_Timp_Calificare'
        
    if not os.path.exists(directory):#creem folderul daca nu exista
        os.makedirs(directory)
    
    #salvam graficul
    plt.savefig(directory+'\\'+'Gaps_'+ str(info_data_year)+'_'+info_data_round+'_'+info_data_session+'.png', dpi=300)
    
    #printam un mesaj de finalizare in consola
    print('\n\n----------------------------------------------------------------\n')
    print('S-a generat graficul cu comparatia timpilor intre toti pilotii')
    print('----------------------------------------------------------------\n\n\n')
