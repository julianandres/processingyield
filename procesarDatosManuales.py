import mysql.connector
import json
import math
import numpy as np

from numpy import sin
from numpy import sqrt
from numpy import arange
from scipy.optimize import curve_fit
from matplotlib import pyplot
import pandas as pd
from sklearn import linear_model
from scipy.stats import pearsonr

class Datos:
  datosYeld=[]
  datosArea=[]
  datosVolumen=[]
  datosVolumenCalculado=[]
  datosNdvi=[]
  datosAltura=[]

def obtenerValoresNormalizadosLista(lista):
   maxVal = max(lista)
   listaR = [element / maxVal for element in lista]
   return listaR

def obtenerVolumenDesdeAltura(planta):
   altura = float(json.loads(planta[9])["altura"])
   diametro = float(json.loads(planta[9])["diametro"])
   volumen = (math.pi/1000000)*((diametro/2)*(diametro/2))*(altura/2)*(4/3)
   print(volumen)
   return volumen

def obtenerRendimientoPlanta(planta):
    jsonMeasurement = json.loads(planta[9])
    ########################################## HEADER
    print(planta[0])
    #print(planta[3])
    numeroRamasMuestra= obtenerMuestra(jsonMeasurement["numRamasHeader"])
    print("Muestras Ramas %f" % (numeroRamasMuestra))
    
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesHeader"])
    print("Muestras Nodos %f" % (numeroNodosMuestra))

    nodosTotalPorRama= int(jsonMeasurement["numNodesHeader"])/numeroRamasMuestra
    print("nodosPorRama %f"% (nodosTotalPorRama))
    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansHeader"])/numeroNodosMuestra
    print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    #print(cafesTotalesPorNodo)
    #print(cafesTotalesHeader)
    print("#################################footer")
    ########################################## FOOOOOTER
    numeroRamasMuestraFooter= obtenerMuestra(jsonMeasurement["numRamasFooter"])
    print("Muestras Ramas %f" % (numeroRamasMuestraFooter))
    #print(numeroRamasMuestraFooter)
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesFooter"])
    print("Muestras Nodos %f" % (numeroNodosMuestra))
    nodosTotalPorRama= int(jsonMeasurement["numNodesFooter"])/numeroRamasMuestra
    print("nodosPorRama %f"% (nodosTotalPorRama))
    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansFooter"])/numeroNodosMuestra
    print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    #print(cafesTotalesPorNodo)
    print("*****************************************")
   
    #print(cafesTotalesFooter)
def obtenerMuestra(population):
     population = float(population)
     valueZ=1.28
     error=0.08
     numerator = (valueZ*valueZ)*(0.5*0.5)*population
     denominator= ((error*error)*(population-1))+(valueZ*valueZ)*(0.5*0.5)
     rta = math.trunc(numerator/denominator)
     return rta
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM suite2_all_antiguo.plant where id<20")

myresult = mycursor.fetchall()
for x in myresult:
  obtenerRendimientoPlanta(x)
  