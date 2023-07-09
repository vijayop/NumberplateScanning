import cv2
import easyocr
import pyodbc   # for database connection 
import datetime
import pandas as pd 

text = 'P 688 CC'

# connecting to database 
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-CUOH6MA\MSSQLSERVER01;"
                      "Database=nivaas;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()


now = datetime.datetime.now()


cursor.execute("SELECT number_plate FROM panel_vehicle WHERE number_plate = '"+ text +"'")
counter = 0 
for row in cursor:
    counter += 1
    print(row.number_plate)
if counter:
    # update operation 
    print('There is something')
    cursor.execute('UPDATE panel_vehicle SET departure_time = ? WHERE number_plate = ?',(now,text))
    cnxn.commit()
    
else:
    print('there is nothing')

# records = cursor.fetchall()
# count = cursor.rowcount
# print(count)

# if count > 0:
#     cursor.execute('UPDATE vehicle SET departure_time= %s WHERE number_plate = %s',(formatted_date,text))
#     records = cursor.fetchall()
# else:
#cursor.execute("INSERT INTO panel_vehicle(number_plate, arrival_time) values(?,?)", (text, now))
#records = cursor.fetchall()
#cnxn.commit()
#print("No. of  records : ",cursor.rowcount)
