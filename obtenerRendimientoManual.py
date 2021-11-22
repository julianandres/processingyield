import mysql.connector
import json
import math
import numpy as np


def obtenerRendimientoPlanta(planta):
    jsonMeasurement = json.loads(planta[9])
    ########################################## HEADER
    print("#################################HEADER")
    #print(planta[0])
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
    #print(cafesTotalesHeader)
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
    #print(cafesTotalesFooter)
    
    total=cafesTotalesFooter+cafesTotalesHeader
    return total
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

mycursor.execute("SELECT * FROM suite2_all.plant where cod_lote = 3")

myresult = mycursor.fetchall()
datosYeld=[]
datosArea=[]
for x in myresult:
  yieldPlanta= obtenerRendimientoPlanta(x)
  print(yieldPlanta)
  datosYeld.append(yieldPlanta)
  print(float(x[4]))
  datosArea.append(float(json.loads(x[9])["altura"]))

r = np.corrcoef(datosYeld, datosArea)
print(r)