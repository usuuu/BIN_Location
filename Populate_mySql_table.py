#Import modules
import cv2
import requests
import pytesseract
from pytesseract import Output
import re
import mysql.connector
from mysql.connector import Error

#Populate the table
def insert_varibles(binnum,product,locationX, locationY):

    connection = mysql.connector.connect(host='localhost',
                                        database='WAREHOUSE',
                                        user='root',
                                        password='XXXX')

    cursor = connection.cursor()


    
    mySql_insert_query = """    INSERT INTO BINLOCATION (BIN_Number, Product, LocationX, LocationY) 
                                VALUES (%s, %s, ST_ASTEXT(ST_GeomFromText(%s),  ST_GeomFromText(%s)) """

    record = (binnum,product,locationX, locationY)
    cursor.execute(mySql_insert_query, record)
    connection.commit()
    print("Record inserted successfully into bin location table")


lowercase  = "[a-zQO]"

#Input the image
img = cv2.imread("WarehouseLayout.png")

#make the image black and white
grey = cv2.cvtColor(img,  cv2.COLOR_BGR2GRAY)

#Keep the black text and remove everything else 
thresh2 = cv2.threshold(grey,254,255,cv2.THRESH_BINARY)[1]

#Exact the data from the image anf store it in a dictionary 
d = pytesseract.image_to_data(thresh2, output_type=Output.DICT, lang='eng')

#Get the number of enteries  
n_boxes = len(d['text'])

#loop through each value and extract the heigh, width, x and y coordinates. Clean up the BIN numbers
for i in range(n_boxes):
   
    if d['conf'][i] != "-1":
       
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
  
        coordinates = '´%s %s' % (x, y) #(x+w, y+h)
        width_heigth = '%s %s' % (x+w, y+h)
                
        #Check format of BIN Number
        text = d['text'][i]
        if re.findall("O|Q", text[1]):
            text = text[0:1] + str(0) + text[1+1: ]
        text = (re.sub(lowercase, "", text))