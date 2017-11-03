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
    dataStations = pd.read_csv('data/db_sonora.csv')

    #%% read data indicencia
    dataIncidencia = pd.read_csv('data/incidencia_sonora.csv')

    #%% generate punto de rocio
    dataStations['dpoint'] = dataStations.apply(lambda x: puntoDeRocio(x['humr'], x['tmed']), axis=1)

    #%% generate tmidnight
    dataStations['tmidnight'] = dataStations['tmax'] - dataStations['tmin']

    #%% dataStations to np arrays
    latInc = np.array(dataIncidencia['lat'])
    longInc = np.array(dataIncidencia['long'])
    problemInc = np.array(dataIncidencia['problem'])
    incidenciaInc = np.array(dataIncidencia['incidencia'])
    cicloInc = np.array(dataIncidencia['ciclo'])
    anioInc = np.array(dataIncidencia['anio'])
    mesInc = np.array(dataIncidencia['mes'])
    diaInc = np.array(dataIncidencia['dia'])
    indexInc = np.array(dataIncidencia.index)

    #%% create text for data
    textToData = "lat, long, problem, incidencia, anio, mes, dia, ciclo, prec, tmax, tmin,tmed, velvmax,velv, dirvvmax, dirv, radg,humr, et, dpoint, tmidnight\n"

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
        dataTemp = dataStations.loc[(dataStations['anio'] == anio) & (dataStations['mes'] == mes) & (dataStations['dia'] == dia)]
        dataTemp['distancia'] = dataTemp.apply(lambda x: distanciaPuntoAPunto(x['latitud'], latitud, x['longitud'], longitud), axis=1)
        distanciaMinima = dataTemp['distancia'].min()
        dataTemp = dataTemp.loc[dataTemp['distancia'] == distanciaMinima]
        prec = np.array(dataTemp['prec'])
        tmax = np.array(dataTemp['tmax'])
        tmin = np.array(dataTemp['tmin'])
        tmed = np.array(dataTemp['tmed'])
        velvmax = np.array(dataTemp['velvmax'])
        velv = np.array(dataTemp['velv'])
        dirvvmax = np.array(dataTemp['dirvvmax'])
        dirv = np.array(dataTemp['dirv'])
        radg = np.array(dataTemp['radg'])
        humr = np.array(dataTemp['humr'])
        et = np.array(dataTemp['et'])
        dpoint = np.array(dataTemp['dpoint'])
        tmidnight = np.array(dataTemp['tmidnight'])
        textToData += "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(latitud, longitud, problema, incidencia, anio, mes, dia, ciclo, prec[0], tmax[0], tmin[0], tmed[0], velvmax[0], velv[0], dirvvmax[0], dirv[0],radg[0],humr[0],et[0], dpoint[0], tmidnight[0])

    #%% from text to data
    tempTitle = 'resultados/db_join.csv'
    textFile = open(tempTitle, 'w')
    textFile.write(textToData)
    textFile.close()

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

def genracionDeFechas(anio, mes, dia):
    """
    Genera el arreglo de 4 días previos a la fecha de incidencia
    """
    # Generate Days
    arrayFechas = []

    for i in range(0,5,1):
        if i == 0:
            newDiaString = '{}'.format(dia)
            if len(newDiaString) == 1:
                newDiaString = '0' + newDiaString
            newMesString = '{}'.format(mes)
            if len(newMesString) == 1:
                newMesString = '0' + newMesString
            fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
            arrayFechas.append(fecha)
        if i > 0:
            dia = dia + 1
            if mes == 2 and anio % 4 == 0:
                diaEnElMes = 29
            elif mes == 2 and anio % 4 != 0:
                diaEnElMes = 28
            elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                diaEnElMes = 31
            elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                diaEnElMes = 30
            if dia > diaEnElMes:
                mes = mes + 1
                dia = 1
            if mes > 12:
                anio = anio + 1
                mes = 1
            newDiaString = '{}'.format(dia)
            if len(newDiaString) == 1:
                newDiaString = '0' + newDiaString
            newMesString = '{}'.format(mes)
            if len(newMesString) == 1:
                newMesString = '0' + newMesString
            fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
            arrayFechas.append(fecha)



if __name__ == "__main__":
    main()
