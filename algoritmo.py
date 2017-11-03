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

#%% longitud 
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
