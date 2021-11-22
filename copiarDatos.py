
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM suite2_sult_all.plant where manual_values is not null")

myresult = mycursor.fetchall()
sql= "INSERT INTO suite2_all.plant (contorno, contorno_image_separated, area, volumen, ndvi_avg, cod_lote, centro, manual_values, data_statistic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
list=[]
for x in myresult:
  list.append((x[1],x[2],x[3],x[4],x[5],x[7],x[8],x[9],x[11]))

mycursor.executemany(sql, list)

mydb.commit()

print(mycursor.rowcount, "was inserted.")