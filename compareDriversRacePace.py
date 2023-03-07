import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
import os
from fastf1.core import Laps
import extra_data.teams as teamsDrivers
import extra_data.convert_lap_to_normal as convert
from pandas import DataFrame


def compareDriversRacePace(data_year, data_round, data_session, driver1, driver2): #functia care va fi apelata in main.py
    fastf1.plotting.setup_mpl()

    if(data_round == 'Testing'):
        session = fastf1.get_testing_session(data_year, 1 ,data_session) #daca e sesiune de teste, se pune 1 (sau 2, doar pentru anul 2022) ca runda
    else:
        session = fastf1.get_session(data_year,data_round,data_session)

    fastf1.Cache.enable_cache('__pycache__')  #cache directory

    session.load() #colectam datele de la API

    driver1Name = driver1 #pilotul 1 ales in main.py
    driver2Name = driver2 #pilotul 2 ales in main.py

    laps = session.load_laps(with_telemetry=True) #colectam datele de la API, dar in special telemetria
    driver1 = laps.pick_driver(driver1Name) #luam timpul pe tur al pilotului
    driver2 = laps.pick_driver(driver2Name)

    fig, ax = plt.subplots(figsize=(10,6)) #creem graficul
    ax.plot(driver1['LapNumber'], driver1['LapTime'], color='red')
    ax.plot(driver2['LapNumber'], driver2['LapTime'], color='cyan')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} {data_session}\n") #scriem o descriere a graficului

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    plt.legend([driver1Name,driver2Name])

     #folderul unde se va salva graficul
    directory = 'Rezultate\\'+'Grafice_Comparare_Timpi_de_Cursa'
            
    if not os.path.exists(directory):#creem folderul daca nu exista
        os.makedirs(directory)

    #salvam graficul
    plt.savefig(directory+'\\'+str(data_year)+'_'+data_round+'_'+data_session+"_"+driver1Name+' vs '+driver2Name+'.png', dpi=1000)

    #printam un mesaj de finalizare in consola
    print('\n\n--------------------------------------------------------------------------------------------------------\n')
    print('S-a generat comparatia timpilor intre cei doi piloti setati in programul principal (driver1 si driver2)')
    print('--------------------------------------------------------------------------------------------------------\n\n\n')
    