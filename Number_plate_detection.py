import cv2
import easyocr
import pyodbc   # for database connection 
import datetime

frameWidth = 640    #Frame Width
franeHeight = 480   # Frame Height

plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500

cap =cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,franeHeight)
cap.set(10,150)


while True:
    success , img  = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade .detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgRoi)
    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF ==ord('s'):
        cv2.imwrite("IMAGE.jpg",imgRoi)
        break

# use easy ocr to read the text from the numberplate
numberplate = cv2.imread('IMAGE.jpg')
reader = easyocr.Reader(['en'])
result = reader.readtext(numberplate)

# Render result
text = result[0][-2]
print(text)



# connecting to database 
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-CUOH6MA\MSSQLSERVER01;"
                      "Database=nivaas;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()


now = datetime.datetime.now()


# checking is the vehicle has already arrived in the premises 
cursor.execute("SELECT number_plate FROM panel_vehicle WHERE number_plate = '"+ text +"'")
counter = 0  # if there is a result, then counter will increase 
for row in cursor:
    counter += 1
    print(row.number_plate)

# if vehicle is already in the premises, update the departure time 
if counter:
    # update operation 
    cursor.execute('UPDATE panel_vehicle SET departure_time = ? WHERE number_plate = ?',(now,text))
    #cnxn.commit()
    
else:
    # if vehicle is not in the premises, insert a new row for this vehicle 
    cursor.execute("INSERT INTO panel_vehicle(number_plate, arrival_time) values(?,?)", (text, now))

cnxn.commit()