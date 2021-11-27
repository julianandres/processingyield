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
    print("#################################HEADER")
    print(planta[0])
    #print(planta[3])
    numeroRamasMuestra= obtenerMuestra(jsonMeasurement["numRamasHeader"])
    #print(numeroRamasMuestra)
    nodosTotalPorRama= int(jsonMeasurement["numNodesHeader"])/numeroRamasMuestra
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesHeader"])
    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansHeader"])/numeroNodosMuestra
    #print(cafesTotalesPorNodo)
    cafesTotalesHeader= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasHeader"])
    print(cafesTotalesHeader)
    #print("#################################footer")
    ########################################## FOOOOOTER
    numeroRamasMuestraFooter= obtenerMuestra(jsonMeasurement["numRamasFooter"])
    #print(numeroRamasMuestraFooter)
    nodosTotalPorRama= int(jsonMeasurement["numNodesFooter"])/numeroRamasMuestraFooter
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesFooter"])
    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansFooter"])/numeroNodosMuestra
    #print(cafesTotalesPorNodo)
    cafesTotalesFooter= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasFooter"])
    print(cafesTotalesFooter)
    total=cafesTotalesFooter+cafesTotalesHeader
    return total
   
    #print(cafesTotalesFooter)
def obtenerMuestra(population):
     population = float(population)
     valueZ=1.28
     error=0.08
     numerator = (valueZ*valueZ)*(0.5*0.5)*population
     denominator= ((error*error)*(population-1))+(valueZ*valueZ)*(0.5*0.5)
     rta = math.trunc(numerator/denominator)
     return rta
def obtenerVolumenDesdeAltura(planta):
   altura = float(json.loads(planta[9])["altura"])
   diametro = float(json.loads(planta[9])["diametro"])
   volumen = (math.pi/1000000)*((diametro/2)*(diametro/2))*(altura/2)*(4/3)
   print(volumen)
   return volumen
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM suite2_all_antiguo.plant where id>20")

myresult = mycursor.fetchall()

datos = Datos()
for x in myresult:
  yieldPlanta= obtenerRendimientoPlanta(x)
  datos.datosYeld.append(yieldPlanta)
  datos.datosArea.append(float(x[3]))
  datos.datosVolumen.append(float(x[4]))
  datos.datosVolumenCalculado.append(obtenerVolumenDesdeAltura(x))
  datos.datosNdvi.append(float(json.loads(x[5])["ndviMean"]))
  datos.datosAltura.append(float(json.loads(x[9])["altura"]))
  

#pyplot.scatter(datos.datosVolumen, datos.datosVolumenCalculado,c="red")
#pyplot.scatter(datos.datosArea, datos.datosAltura,c="red")
#pyplot.scatter(datos.datosNdvi, datos.datosVolumenCalculado,c="blue")
#pyplot.scatter(datos.datosAltura, datos.datosNdvi,c="green")
pyplot.scatter(datos.datosYeld, datos.datosVolumenCalculado,c="black")
pyplot.show()