def convert_lap_to_normal(lap , type):
    #timedelta64[ns] => timp normal
    
    time = lap.asm8.astype(str)
    timpFinal = ""
    minuteFinal = ''
    secundeFinal = ''
    miliFinal = ''

    if(time[0] == 'N' and time[1] == 'a' and time[2] == 'T'):
        timpFinal = ""
        minuteFinal = ''
        secundeFinal = ''
        miliFinal = ''
    else:
        if(time[0] == '1' or time[0] == '2'):#timp slab/de incalzire
            secunde = time[0]+time[1]+time[2]
            mili = time[3]+time[4]+time[5]
            
        else:   #timp de luat in considerare
            secunde = time[0]+time[1]
            mili = time[2]+time[3]+time[4]
            
        rezultat_secunde = int(secunde)
        minuteF = int(rezultat_secunde/60)
        secundeFinal = ''
        rezultat_secunde = rezultat_secunde%60

        if(rezultat_secunde < 10):
            tuple2 = ('0',str(rezultat_secunde))
            secundeFinal = ''.join(tuple2)
        else:
            secundeFinal = str(rezultat_secunde)
            minuteFinal = str(minuteF)
            miliFinal = mili  #daca il facem int nu mai afiseaza toate 0-urile de la inceput
            tuple = (minuteFinal,':',secundeFinal,'.',miliFinal)
            timpFinal = ''.join(tuple)
    if(type == 'lap'):
        return timpFinal
    elif(type == 'minute'):
        return minuteFinal
    elif(type == 'secunde'):
        return secundeFinal
    elif(type == 'mili'):
        return miliFinal
    return 0


def array_convert_lap_to_normal(x , type):
    #timedelta64[ns] => timp normal
    for lap in x.iterlaps():
        convert_lap_to_normal(lap.LapTime,type)