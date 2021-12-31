import mysql.connector
import json
import math
import numpy as np

from numpy import sin
from numpy import sqrt
from numpy import arange
from matplotlib import pyplot
import pandas as pd
from sklearn import linear_model
from scipy.stats import pearsonr

class Datos:
  datosYeld=[]
  datosArea=[]
  datosAreaCalculada=[]
  datosVolumen=[]
  datosVolumenCalculado=[]
  datosNdvi=[]
  datosAltura=[]
  datosAlturaCalculada=[]

def obtenerValoresNormalizadosLista(lista):
   maxVal = max(lista)
   listaR = [element / maxVal for element in lista]
   return listaR

def obtenerRendimientoPlanta(planta):
    jsonMeasurement = json.loads(planta[9])
    ########################################## HEADER
    #print("#################################HEADER")
    print(planta[0])
    #print(planta[3])
    numeroRamasMuestra= obtenerMuestra(jsonMeasurement["numRamasHeader"])
    
    #print(numeroRamasMuestra)
    nodosTotalPorRama= int(jsonMeasurement["numNodesHeader"])/numeroRamasMuestra
    
    jsonMeasurement["nodosPorRamaHeader"]=nodosTotalPorRama
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesHeader"])
    

    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansHeader"])/numeroNodosMuestra
    print("Muestras Ramas %f" % (numeroRamasMuestra))
    print("Muestras Nodos %f" % (numeroNodosMuestra))
    print("nodosPorRama %f"% (nodosTotalPorRama))
    print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    jsonMeasurement["cafesPorNodoHeader"]=cafesTotalesPorNodo
    #print(cafesTotalesPorNodo)
    cafesTotalesHeader= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasHeader"])
    #print(cafesTotalesHeader)
    print("#################################footer")
    ########################################## FOOOOOTER
    numeroRamasMuestraFooter= obtenerMuestra(jsonMeasurement["numRamasFooter"])
    print("Muestras Ramas %f" % (numeroRamasMuestraFooter))
    #print(numeroRamasMuestraFooter)
    nodosTotalPorRama= int(jsonMeasurement["numNodesFooter"])/numeroRamasMuestraFooter
    jsonMeasurement["nodosPorRamaFooter"]=nodosTotalPorRama
    #print(nodosPorRama)
    numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesFooter"])
    print("Muestras Nodos %f" % (numeroNodosMuestra))
    #print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansFooter"])/numeroNodosMuestra
    jsonMeasurement["cafesPorNodoFooter"]=cafesTotalesPorNodo
    #print(cafesTotalesPorNodo)
    cafesTotalesFooter= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasFooter"])
    print("nodosPorRama %f"% (nodosTotalPorRama))
    print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    #print(cafesTotalesFooter)
    total=cafesTotalesFooter+cafesTotalesHeader
    print("Total %f"%total)
    
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
def obtenerAreaDesdeDiametro(planta):
   diametro = float(json.loads(planta[9])["diametro"])
   area = (math.pi/10000)*((diametro/2)*(diametro/2))
   #print("AreaCalc : %.3f " %area)
   #print("AreaDrone : %s " %planta[3])
   return area
def obtenerVolumenDesdeAltura(planta):
   altura = float(json.loads(planta[9])["altura"])
   volumen = float(planta[3])*(altura/200)*(4/3)
   print("VolumenCalc : %.3f " %volumen)
   return volumen
def obtenerVolumenDesdeImagen(planta):
   altura = float(planta[12])
   volumen = float(planta[3])*(altura/200)*(4/3)
   print("VolumenImage : %.3f " %volumen)
   return volumen
def obtenerVolumenDesdeAlturaAndDiametro(planta):
   altura = float(json.loads(planta[9])["altura"])
   diametro = float(json.loads(planta[9])["diametro"])
   volumen = (math.pi/1000000)*((diametro/2)*(diametro/2))*(altura/2)*(4/3)
   #print(volumen)
   return volumen

def objective(x, a, b):
	  return a * np.array(x) + b
def getDataFromDataBase():
   mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root"
   )
   mycursor = mydb.cursor()

   mycursor.execute("SELECT * FROM suite2_all_antiguo.plant where id between 0 and 130 order by id desc")

   myresult = mycursor.fetchall()
   return myresult


def generarMatrizDatos(myresult):
   datos = Datos()
   datos.datosYeld=[]
   datos.datosArea=[]
   datos.datosAreaCalculada=[]
   datos.datosVolumen=[]
   datos.datosVolumenCalculado=[]
   datos.datosNdvi=[]
   datos.datosAltura=[]
   datos.datosAlturaCalculada=[]
   print(len(datos.datosYeld))
   for x in myresult:
      print(x[12])
      yieldPlanta= obtenerRendimientoPlanta(x)
      datos.datosAlturaCalculada.append(x[12])
      datos.datosYeld.append(yieldPlanta)
      datos.datosArea.append(float(x[3]))
      datos.datosVolumen.append(obtenerVolumenDesdeImagen(x))
      datos.datosAreaCalculada.append(obtenerAreaDesdeDiametro(x))
      datos.datosVolumenCalculado.append(obtenerVolumenDesdeAltura(x))
      datos.datosNdvi.append(float(json.loads(x[5])["ndviMean"]))
      datos.datosAltura.append(float(json.loads(x[9])["altura"]))
   d = {'yields': datos.datosYeld, "ndvi":datos.datosNdvi, "volumenImagen":datos.datosVolumen,"volumenCalculado":datos.datosVolumenCalculado,"areaCalculada":datos.datosAreaCalculada,'areaImagen': datos.datosArea,"alturaCalculada":datos.datosAlturaCalculada,"alturaImagen":datos.datosAltura}
   df = pd.DataFrame(data=d)
   print("*****************************************")
   return df,datos
   

data= getDataFromDataBase()
dataframe,datos = generarMatrizDatos(data)
pyplot.scatter(datos.datosVolumenCalculado,datos.datosYeld,c="black")
pyplot.xlabel("datosVolumenCalculado")
pyplot.ylabel("datosYield")

pyplot.show()
