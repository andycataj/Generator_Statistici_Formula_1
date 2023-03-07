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

#functia care va fi apelata in main.py
def TimingTableGenerator(info_data_year, info_data_round,info_data_session, info_data_minute_referinta, info_data_TimpDeReferinta):
    if(info_data_round == 'Testing'):#daca e sesiune de teste, se pune 1 (sau 2, doar pentru anul 2022) ca runda
        session = fastf1.get_testing_session(info_data_year, 1 ,info_data_session)
    else:
        session = fastf1.get_session(info_data_year,info_data_round,info_data_session)

    fastf1.Cache.enable_cache('__pycache__')  #cache directory

    laps = session.load() #colectam datele de la API

    drivers = pd.unique(session.laps['Driver']) #luam toti pilotii din sesiunea curenta

    for driver in drivers:

        #----------------------------------------------
        #Timpii tuturor pilotilor in excel#
        status = session.laps.pick_driver(driver).TrackStatus #daca se intampla ceva pe circuit, aceasta variabila va avea o valoare diferita de 1
        
        all = session.laps.pick_driver(driver)
        lapStartDate = session.laps.pick_driver(driver).LapStartDate #timpul de start al turului cronometrat
        driverNumber = session.laps.pick_driver(driver).DriverNumber #numarul de legitimare a pilotului
        lapTime = session.laps.pick_driver(driver).LapTime #timpul de tur

        sector1Time = session.laps.pick_driver(driver).Sector1Time #timpul pe sectorul 1
        sector2Time = session.laps.pick_driver(driver).Sector2Time
        sector3Time = session.laps.pick_driver(driver).Sector3Time


        compound = session.laps.pick_driver(driver).Compound #tipul de pneuri folosite
        trackStatus = session.laps.pick_driver(driver).TrackStatus #la fel ca si status, de backup, pentru ca API-ul mai da gresi uneori la acest status si putem compara cele doua valori
        lapNumber = session.laps.pick_driver(driver).LapNumber #numarul de tururi pe acel pneu

        freshTyre = session.laps.pick_driver(driver).FreshTyre #1 daca e primul tur pe pneu, 0 daca nu
        tyreLife = session.laps.pick_driver(driver).TyreLife #numarul de tururi pe acel pneu
        stint = session.laps.pick_driver(driver).Stint  #numarul de stinturi (iesiri pe circuit)



        timpiiArray = [] #array cu timpii de tur
        timpCompetitiv = [] 
        bun = False
        for lap in all.iterlaps():
            #print(lap[1].LapTime)

            #----------------Laptime----------------    
            #de aici pana la urmatorul comentariu de acelasi tip,
            #se face conversia din laptime (timp salvat in format special pentru memorarea miimilor de secunda) in timp normal, cum numaram noi normal secundele
            td = lap[1].LapTime
            time = td.asm8.astype(str)
            if(time[0] == 'N' and time[1] == 'a' and time[2] == 'T'):
                #daca pilotul iese pe circuit primim NaT, deoarece timpul va fi slab, 
                # datorita faptului ca pilotul va incalzi cauciucurile 
                # si timpul nu este de luat in calcul
                timpii_pe_tur = ""
                timpiiArray.append(timpii_pe_tur)
                timpCompetitiv.append("0")
                #print("Timp slab")
            else:
                if(time[0] == '1'):#timp slab/de incalzire
                    #ce este peste 100 de secunde, este un timp mai slabut in ritm de calificare
                    secunde = time[0]+time[1]+time[2]
                    mili = time[3]+time[4]+time[5]
                    
                else:   #timp cronometrat
                    secunde = time[0]+time[1]
                    mili = time[2]+time[3]+time[4]
                    
                rezultat_secunde = int(secunde)
                minute = int(rezultat_secunde/60)
                rez_secunde = ''
                rezultat_secunde = rezultat_secunde%60

                if(rezultat_secunde < info_data_TimpDeReferinta and minute <= info_data_minute_referinta):
                    timpCompetitiv.append("1")
                    #print("Timp bun")
                else:
                    timpCompetitiv.append("0")
                    #print("Timp slab")

                #print(timpCompetitiv)

                if(rezultat_secunde < 10): 
                    #daca o sa avem timpul 1:07.123, fara acest tuple2 nu vom avea acel 0 in fata lui 7
                    tuple2 = ('0',str(rezultat_secunde))
                    rez_secunde = "".join(tuple2)
                else:
                    rez_secunde = str(rezultat_secunde)
                rezultat_mili = mili  #daca il facem int nu mai afiseaza toate 0-urile de la inceput
                
                tuple = (str(minute),':',rez_secunde,'.',rezultat_mili)
                timpii_pe_tur = "".join(tuple)
                timpiiArray.append(timpii_pe_tur)
                
            #----------------Laptime----------------
            #ceea ce am facut aici inlocuieste fucntia strftimedelta cu care vine acest API, 
            #pentru ca nu as fi reusit sa fac toate functiile pe care mi le doream eu cu 
            #functia lor predefinita

        
        factor = 86400.00000001009 #factorul de conversie din laptime in secunde

        #data = pd.DataFrame({'LapStartDate':lapStartDate,'DriverNumber':driverNumber,'LapTime':timpiiArray,'Compound':compound,'TrackStatus':trackStatus,'LapNumber':lapNumber})
        data = pd.DataFrame({'Lap':lapNumber,'Driver':driverNumber,'LapTime':timpiiArray,'Sector 1':sector1Time*factor,'Sector 2':sector2Time*factor,'Sector 3':sector3Time*factor,'Compound':compound,'Stint':stint,'TyreLife':tyreLife,'FreshTyre':freshTyre,'Flags':trackStatus,'LapStartDate':lapStartDate})

        #folderul unde se va salva excelul
        directory = 'Rezultate\\'+'Timpi_Excell'+'_' + str(info_data_year) + '_'+info_data_round+'_'+ info_data_session
        
        if not os.path.exists(directory):#creem folderul daca nu exista
            os.makedirs(directory)

        def align_center(x): #aliniem la centru
            return ['text-align: center' for x in x]

        #scriem in excel
        for column in data:
            column_width = max(data[column].astype(str).map(len).max(), len(column)+4)
            col_idx = data.columns.get_loc(column)

        data.style.apply(align_center, axis=0).to_excel(os.path.join(directory,driver+'.xlsx'), sheet_name=info_data_session, index=False)
        
        #Timpii tuturor pilotilor in excel#
        #----------------------------------------------'''
    print('\n\n-------------------------------------------------\n')
    print('S-au generat toate tabelele cu timpii pilotilor')
    print('-------------------------------------------------\n\n\n')


#un mic bug, timpul pe sectoare nu se afiseaza corect in excel,
#daca utilizatorul vrea timpul exact in excel, dupa virgula,
#trebuie sa atribuie celulei sau coloanei de celule proprietatea
#de formatare a textului "General" sau "Text"

#nu pot face nimic in acest sens, deoarece API-ul nu ofera compatibilitatea cu excelul de a procesa aceste date