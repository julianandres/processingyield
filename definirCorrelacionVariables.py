import mysql.connector
import json
import math
import numpy as np

from numpy import mat, sin
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
  datosVolumenImagen=[]
  datosVolumenCalculado=[]
  datosNdvi=[]
  datosAlturaMedida=[]
  datosAlturaCalculada=[]
  datosIafNdvi=[]
  datosNdviMax=[]
  datosNdviMin=[]

def obtenerValoresNormalizadosLista(lista):
   maxVal = max(lista)
   listaR = [element / maxVal for element in lista]
   return listaR

def obtenerRendimientoPlanta(planta):
    jsonMeasurement = json.loads(planta[9])
    ########################################## HEADER
    ##print("#################################HEADER")
    #print("id:"+str(planta[0]))
    ##print(planta[3])
    numeroRamasMuestra=5
    ##print(planta[13])
    if planta[13]==1 : numeroRamasMuestra= obtenerMuestra(jsonMeasurement["numRamasHeader"])
    
    ##print(jsonMeasurement["numNodesHeader"])
    nodosTotalPorRama= int(jsonMeasurement["numNodesHeader"])/numeroRamasMuestra
    
    jsonMeasurement["nodosPorRamaHeader"]=nodosTotalPorRama
    ##print(nodosPorRama)
    numeroNodosMuestra = 10
    if planta[13]==1: numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesHeader"])
    

    ##print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansHeader"])/numeroNodosMuestra
    #print("Muestras Ramas %f" % (numeroRamasMuestra))
    #print("Muestras Nodos %f" % (numeroNodosMuestra))
    #print("nodosPorRama %f"% (nodosTotalPorRama))
    #print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    jsonMeasurement["cafesPorNodoHeader"]=cafesTotalesPorNodo
    ##print(cafesTotalesPorNodo)
    cafesTotalesHeader= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasHeader"])
    ##print(cafesTotalesHeader)
    #print("#################################footer")
    ########################################## FOOOOOTER
    numeroRamasMuestraFooter=5
    if planta[13]==1 : numeroRamasMuestraFooter= obtenerMuestra(jsonMeasurement["numRamasFooter"])
    #print("Muestras Ramas %f" % (numeroRamasMuestraFooter))
    ##print(numeroRamasMuestraFooter)
    nodosTotalPorRama= int(jsonMeasurement["numNodesFooter"])/numeroRamasMuestraFooter
    jsonMeasurement["nodosPorRamaFooter"]=nodosTotalPorRama
    ##print(nodosPorRama)
    numeroNodosMuestra=10
    if planta[13]==1 : numeroNodosMuestra= obtenerMuestra(jsonMeasurement["numNodesFooter"])
    #print("Muestras Nodos %f" % (numeroNodosMuestra))
    ##print(numeroNodosMuestra)
    cafesTotalesPorNodo= int(jsonMeasurement["numBeansFooter"])/numeroNodosMuestra
    jsonMeasurement["cafesPorNodoFooter"]=cafesTotalesPorNodo
    ##print(cafesTotalesPorNodo)
    cafesTotalesFooter= cafesTotalesPorNodo*nodosTotalPorRama*float(jsonMeasurement["numRamasFooter"])
    #print("nodosPorRama %f"% (nodosTotalPorRama))
    #print("cafesPorNodo %f"% (cafesTotalesPorNodo))
    ##print(cafesTotalesFooter)
    total=cafesTotalesFooter+cafesTotalesHeader
    #print("Total %f"%total)
    
    return total
   
    ##print(cafesTotalesFooter)
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
   ##print("AreaCalc : %.3f " %area)
   ##print("AreaDrone : %s " %planta[3])
   return area
def obtenerVolumenDesdeAltura(planta):
   altura = float(json.loads(planta[9])["altura"])
   volumen = float(planta[3])*(altura/200)*(4/3)
   #print("VolumenCalc : %.3f " %volumen)
   return volumen
def obtenerVolumenDesdeImagen(planta):
   altura = float(planta[12])
   volumen = float(planta[3])*(altura/200)*(4/3)
   #print("VolumenImage : %.3f " %volumen)
   #print("altura : %.3f " %altura)
   return volumen
def obtenerVolumenDesdeAlturaAndDiametro(planta):
   altura = float(json.loads(planta[9])["altura"])
   diametro = float(json.loads(planta[9])["diametro"])
   volumen = (math.pi/1000000)*((diametro/2)*(diametro/2))*(altura/2)*(4/3)
   ##print(volumen)
   return volumen
def obtenerIafFromNDVI(planta):
   ndviMax = 2*float(json.loads(planta[5])["ndviMax"])
   ndviMin = float(json.loads(planta[5])["ndviMin"])
   ndviMean = float(json.loads(planta[5])["ndviMean"])
   fc = 1-((ndviMax-ndviMean)/((ndviMax-ndviMin)))**(0.6)
   iaf = -2*math.log(1-fc)
   ##print(volumen)
   #return (0.515-((math.e)**(-0.515*iaf-0.644)))
   return iaf

def objective(x, a, b):
	  return a * np.array(x) + b
def getDataFromDataBase():
   mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root"
   )
   mycursor = mydb.cursor()

   mycursor.execute("SELECT * FROM suite2_all_antiguo.plant order by volumen desc")

   myresult = mycursor.fetchall()
   return myresult
def getDataFromDataBaseTest():
   mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root"
   )
   mycursor = mydb.cursor()

   mycursor.execute("SELECT * FROM suite2.plant p WHERE p.altura>0 AND p.altura is not null AND p.cod_lote=5 AND p.id<17090 AND p.id>291")

   myresult = mycursor.fetchall()
   return myresult


def generarMatrizDatos(myresult,includeYield):
   datos = Datos()
   datos.datosArea=[]
   datos.datosAreaCalculada=[]
   datos.datosVolumenImagen=[]
   datos.datosNdvi=[]
   datos.datosAlturaCalculada=[]
   if includeYield:
      datos.datosAlturaMedida=[]
      datos.datosVolumenCalculado=[]
      datos.datosYeld=[]
   datos.datosIafNdvi=[]
   datos.datosNdviMax=[]
   datos.datosNdviMin=[]
   dataInit={}
   for x in myresult:
      spectralVars=json.loads(x[5])
      statisticVars=json.loads(x[11])         
      datos.datosAlturaCalculada.append(x[12])      
      datos.datosArea.append(float(x[3]))
      datos.datosVolumenImagen.append(obtenerVolumenDesdeImagen(x))
      if includeYield :
         datos.datosAreaCalculada.append(obtenerAreaDesdeDiametro(x))
         datos.datosVolumenCalculado.append(obtenerVolumenDesdeAltura(x))
         datos.datosAlturaMedida.append(float(json.loads(x[9])["altura"]))
         yieldPlanta= obtenerRendimientoPlanta(x)
         datos.datosYeld.append(yieldPlanta)      
      datos.datosNdvi.append(float(spectralVars["ndviMean"]))
      datos.datosIafNdvi.append(obtenerIafFromNDVI(x))
      for key in statisticVars.keys():
         if key != "maxHistRedIndexValue":   
            if key in dataInit:
               dataInit[key].append(statisticVars[key])
            else:
               dataInit[key]=[statisticVars[key]]
      for key in spectralVars.keys():
         if key in dataInit:
             dataInit[key].append(spectralVars[key])
         else:
             dataInit[key]=[spectralVars[key]]

      
   if includeYield :
      d = {'yields': datos.datosYeld,  "volImage":datos.datosVolumenImagen,"areaCalc":datos.datosAreaCalculada,'areaImage': datos.datosArea,"hMeasured":datos.datosAlturaMedida,"hImage":datos.datosAlturaCalculada,"dataIafNdvi":datos.datosIafNdvi}
   else:
      d = {"ndvi":datos.datosNdvi, "volImage":datos.datosVolumenImagen,'areaImage': datos.datosArea,"hImage":datos.datosAlturaCalculada,"dataIafNdvi":datos.datosIafNdvi}
   
   d.update(dataInit)
   print(len(d["hImage"]))
   if not includeYield:
      for key in d.keys():
         print ("key ",key,"len ",len(d[key]))
   df = pd.DataFrame(data=d)
   #print("*****************************************")
   return df,datos,d
   

#data= getDataFromDataBase()
#dataframe,datos,dframe = generarMatrizDatos(data)

#pyplot.scatter(dataframe["volImage"],datos.datosYeld,c="black",s=1)
#pyplot.xlabel("volImage")
#pyplot.ylabel("datosYield")

#pyplot.show()
data= getDataFromDataBaseTest()
dataframeTest,datosTest,dictGeneralTest = generarMatrizDatos(data,False)
