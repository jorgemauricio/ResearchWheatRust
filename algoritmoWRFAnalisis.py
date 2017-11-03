#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:46:52 2017

@author: jorgemauricio
"""

#%% librerias
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


def main():
    #%% read data stations
    dataWRF = pd.read_csv('data/db_sonora_wrf.csv')

    #%% read data indicencia
    dataInc = pd.read_csv('data/incidencia_sonora.csv')

    #%% generate new data base
    textToDataIncidencia = 'lat,long,problem,incidencia,anio,mes,dia,ciclo,tipo\n' 

    #%% loop for
    for row in dataInc.itertuples():
        latProcesamiento = getattr(row,'lat')
        longProcesamiento = getattr(row, 'long')
        problemProcesamiento = getattr(row,'problem')
        incidenciaProcesamiento = getattr(row,'incidencia')
        cicloProcesamiento = getattr(row,'ciclo') 
        anio = getattr(row,'anio')
        mes = getattr(row,'mes')
        dia = getattr(row,'dia')
        arrayFechasProcesamiento = generacionDeFechas(anio, mes, dia)
        textToDataIncidencia += "{},{},{},{},{},{},{},{},N\n".format(latProcesamiento, longProcesamiento, problemProcesamiento, incidenciaProcesamiento, anio, mes, dia, cicloProcesamiento)
        for i in arrayFechasProcesamiento:
            tanio, tmes, tdia = i.split("-")
            textToDataIncidencia += "{},{},{},0.0,{},{},{},{},G\n".format(latProcesamiento, longProcesamiento, problemProcesamiento, tanio, tmes, tdia, cicloProcesamiento)
        
       
    #%% from text to data
    tempTitle = 'resultados/db_incidencia_wrf.csv'
    textFile = open(tempTitle, 'w')
    textFile.write(textToDataIncidencia)
    textFile.close()

    #%% read new data incidencia
    dataIncidencia = pd.read_csv('resultados/db_incidencia_wrf.csv')

    #%% generate punto de rocio
    dataWRF['dpoint'] = dataWRF.apply(lambda x: puntoDeRocio(x['humr'], x['tpro']), axis=1)

    #%% generate tmidnight
    dataWRF['tmidnight'] = dataWRF['tmax'] - dataWRF['tmin']

    #%% dataWRF to np arrays
    latInc = np.array(dataIncidencia['lat'])
    longInc = np.array(dataIncidencia['long'])
    problemInc = np.array(dataIncidencia['problem'])
    incidenciaInc = np.array(dataIncidencia['incidencia'])
    cicloInc = np.array(dataIncidencia['ciclo'])
    anioInc = np.array(dataIncidencia['anio'])
    mesInc = np.array(dataIncidencia['mes'])
    diaInc = np.array(dataIncidencia['dia'])
    tipoInc = np.array(dataIncidencia['tipo'])
    indexInc = np.array(dataIncidencia.index)

    #%% create text for data
    textToData = "lat,long,problem,incidencia,anio,mes,dia,ciclo,prec,tmax,tmin,tpro,velv,dirv,humr,dpoint,tmidnight,condiciones,tipo\n"

    #%% loop
    for i in range(len(latInc)):
        anio = anioInc[i]
        mes = mesInc[i]
        dia = diaInc[i]
        latitud = latInc[i]
        longitud = longInc[i]
        incidencia = incidenciaInc[i]
        ciclo = cicloInc[i]
        problema = problemInc[i]
        tipo = tipoInc[i]
        dataTemp = dataWRF.loc[(dataWRF['anio'] == anio) & (dataWRF['mes'] == mes) & (dataWRF['dia'] == dia)]
        dataTemp['distancia'] = dataTemp.apply(lambda x: distanciaPuntoAPunto(x['latitud'], latitud, x['longitud'], longitud), axis=1)
        distanciaMinima = dataTemp['distancia'].min()
        dataTemp = dataTemp.loc[dataTemp['distancia'] == distanciaMinima]
        prec = np.array(dataTemp['prec'])
        tmax = np.array(dataTemp['tmax'])
        tmin = np.array(dataTemp['tmin'])
        tmed = np.array(dataTemp['tpro'])
        velv = np.array(dataTemp['velv'])
        dirv = np.array(dataTemp['dirv'])
        humr = np.array(dataTemp['humr'])
        dpoint = np.array(dataTemp['dpoint'])
        tmidnight = np.array(dataTemp['tmidnight'])
        condicion = validarCondicion(tmed, tmidnight, dpoint)  
        textToData += "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(latitud, longitud, problema, incidencia, anio, mes, dia, ciclo, prec[0], tmax[0], tmin[0], tmed[0], velv[0], dirv[0],humr[0], dpoint[0], tmidnight[0], condicion, tipo)

    #%% from text to data
    tempTitle = 'resultados/db_join_wrf_10_25.csv'
    textFile = open(tempTitle, 'w')
    textFile.write(textToData)
    textFile.close()

    #%% read data
    data = pd.read_csv('resultados/db_join_wrf_10_25.csv')

    #%% generar indice Presencia
    data['indicePresencia'] = data['condiciones'].shift(-1) + data['condiciones'].shift(-2) + data['condiciones'].shift(-3) + data['condiciones'].shift(-4)
    
    #%% eliminar tados generados
    data = data.loc[data['tipo']== 'N']

    #%% generar porcentaje de presencia
    data['porcentajePresencia'] = data['indicePresencia'] * 0.25

    #%% guardar info
    data.to_csv('resultados/db_join_wrf_10_25_pp.csv', index=False)

#%% Longitud del punto 
def distanciaPuntoAPunto(lat1, lat2, long1, long2):
    """
    Calcula la distancia entre el punto de incidencia y el punto de la estacion
    param: lat1: latitud del punto de incidencia
    param: lat2: latitud de la estacion
    param: long1: longitud del punto de incidencia
    param: long2: longitud de la estacion
    """
    dX = (lat2 - lat1) ** 2
    dY = (long2 - long1) ** 2
    return math.sqrt(dX + dY)

#%% generate punto de rocio
def puntoDeRocio(hr, t):
    """
    Calcula el punto de rocio
    param: hr: humedad relativa
    param: t: temperatura ambiente 
    """
    pr = (hr / 100.0)**(1/8.0) * (112 + 0.9 * t) + (0.1 * t) - 112
    return pr

def generacionDeFechas(anio, mes, dia):
    """
    Genera el arreglo de 4 días previos a la fecha de incidencia
    param: anio : año de la incidencia
    param: mes : mes de la incidencia
    param: dia: dia de la incidencia
    """
    arrayFechas = []

    for i in range(0,4,1):
        dia -= 1
        
        if dia < 1:
            mes = mes - 1
            if mes == 2 and anio % 4 == 0:
                diasEnMes = 29
            elif mes == 2 and anio % 4 != 0:
                diasEnMes = 28
            elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                diasEnMes = 31
            elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                diasEnMes = 30
            dia = diasEnMes
        
        if mes < 1:
            mes = 12
        
        fecha = '{}-{}-{}'.format(anio, mes, dia)
        arrayFechas.append(fecha)
    return arrayFechas

def validarCondicion(tempPro, tempMid, dwpoint):
    """
    Calcular si existen condiciones para la presencia de roya
    param: tempPro: temperatura promedio
    param: tempMid: temperatura nocturna
    param: dwpoint: punto de rocio
    """
    if (tempPro >= 10 and tempPro <= 25 ) and (tempMid >= 15 and tempMid <= 20) and dwpoint >= 5:
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()
