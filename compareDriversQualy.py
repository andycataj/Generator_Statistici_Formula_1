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
#multe importuri, stiu ...

def compareDriversQualy(data_year, data_round, data_session): #functia care va fi apelata in main.py
    fastf1.plotting.setup_mpl()

    if(data_round == 'Testing'):
        session = fastf1.get_testing_session(data_year, 1 ,data_session) #daca e sesiune de teste, se pune 1 (sau 2, doar pentru anul 2022) ca runda
    else:
        session = fastf1.get_session(data_year,data_round,data_session)

    fastf1.Cache.enable_cache('__pycache__')  #cache directory

    session.load() #colectam datele de la API

    tim = teamsDrivers.teams #luam toate echipele

    nrTeams = range(0, 9)
    nrDrivers = range(1, 3)
    #pentru toti pilotii rulam codul de mai jos (for)

    for i in tim:
        nr=-1
        for j in tim[i]:
            nr+=1
            if(nr==0):
                teamName = j
            elif(nr==1):
                driver1 = j #driver 1
            else :
                driver2 = j #driver 2

        driver1_lap = session.laps.pick_driver(driver1).pick_fastest() #luam cel mai rapid tur al pilotului
        driver2_lap = session.laps.pick_driver(driver2).pick_fastest() 

        driver1_telemetry = driver1_lap.get_car_data().add_distance() #luam distanta parcursa pe tur al pilotului
        driver2_telemetry = driver2_lap.get_car_data().add_distance()

        driver1_color = fastf1.plotting.team_color('RBR') #setam culoarea albastra pentru pilotul 1
        driver2_color = fastf1.plotting.team_color('FER') #setam culoarea rosie pentru pilotul 2

        fig, ax = plt.subplots(2, sharex=True, sharey=False) #creem graficul

        #Speed, Distance, Time - comenzile posibile
        ax[0].plot(driver1_telemetry['Time'], driver1_telemetry['Speed'], color=driver1_color, label=driver1, linewidth=1) #creem grafic in functie de Timp si Viteza
        ax[0].plot(driver2_telemetry['Time'], driver2_telemetry['Speed'], color=driver2_color, label=driver2, linewidth=1)

        ax[0].set_xlabel('Time [s]')
        ax[0].set_ylabel('Speed [km/h]')
        ax[0].legend()

        #Speed, Distance, Time
        ax[1].plot(driver1_telemetry['Time'], driver1_telemetry['Distance'], color=driver1_color, label=driver1, linewidth=1) #creem grafic in functie de Timp si Distanta parcursa
        ax[1].plot(driver2_telemetry['Time'], driver2_telemetry['Distance'], color=driver2_color, label=driver2, linewidth=1)

        ax[1].set_xlabel('Time [s]')
        ax[1].set_ylabel('Distance [km]')

        ax[1].legend()

        #-------------------
        #scriem o descriere a graficului
        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                    f"{driver1} {convert.convert_lap_to_normal(driver1_lap.LapTime,'lap')} vs {driver2} {convert.convert_lap_to_normal(driver2_lap.LapTime,'lap')}\n")
        #-------------------
        
        #plt.show()

        #folderul unde se va salva graficul
        directory = 'Rezultate\\'+'Grafice_Comparare_Timpi_de_Calificare'
            
        #creem folderul daca nu exista
        if not os.path.exists(directory):
            os.makedirs(directory)

        #salvam graficul
        plt.savefig(directory+'\\'+str(data_year)+'_'+data_round+'_'+data_session+ ' - '+driver1+' vs '+driver2+'.png', dpi=1000)
    
    #printam un mesaj de finalizare in consola
    print('\n\n--------------------------------------------------------------------------\n')
    print('S-a generat comparatia timpilor intre coechipieri in ritm de calificare')
    print('--------------------------------------------------------------------------\n\n\n')