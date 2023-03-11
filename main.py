import TimingTableGenerator as ttg
import compareAllDriversQualy as cadq
import compareDriversQualy as cdq
import compareDriversRacePace as cdrp

data_year = 2023    #Putem seta anul intre 2018 si 2023
data_round = 'Bahrain' #Rundele din 2023: Testing, Bahrain
#Pentru rundele din anii anteriori consultati site-ul oficial https://www.formula1.com/en/results.html
data_session = 'Race' #Sesiuni: FP1, FP2, FP3, Qualifying, Race

#timp de referinta pentru luarea in calcul a timpilor competitivi, nu si cei obtinuti in tururile de incalzire a pneurilor
minute_referinta = 1
TimpDeReferinta = 50 #1:51.0 - aprox 120% din timpul de baza

#Va rezulta un grafic de comparare a timpilor de cursa 
#sau simulare de cursa (sau chiar si de calificare) a celor doi piloti de mai jos
driver1 = 'VER'
driver2 = 'HAM'
# Optiuni:  'VER', 'HAM', 'BOT', 'NOR', 'PIA', 'PER',
#   'ALO', 'OCO', 'GAS', 'STR', 'HUL', 'RUS', 'DEV', 
# 'SAI', 'LEC', 'TSU', 'ALB', 'SAR', 'MAG', 'ZHO', 'DRU'

print('=====================')
print('---------------------')
print("An: ", data_year)
print("Cursa: ", data_round)
print("Sesiunea: ", data_session)
print('---------------------')
print('Totul este pregatit!')
print('=====================')

cdrp.compareDriversRacePace(data_year, data_round, data_session, driver1, driver2) # => Rezultate/Grafice_Comparare_Timpi_de_Cursa
ttg.TimingTableGenerator(data_year, data_round, data_session, minute_referinta, TimpDeReferinta) # => Rezultate/Timpi_Excell

#Functiile aceastea sunt valabile MOMENTAN doar pentru cursele din anul 2023
if(data_year == 2023):
    cadq.compareAllDriversQualy(data_year, data_round, data_session) # => Rezultate/Grafice_Comparare_Diferenta_Timp_Calificare
    cdq.compareDriversQualy(data_year, data_round, data_session) # => Rezultate/Grafice_Comparare_Timpi_de_Calificare

print('\n\n\n==============================')
print('  Verifica folderul generat!')
print('==============================')


