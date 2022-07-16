#Import all the modules

import cv2
import requests
import pytesseract
from pytesseract import Output
import re
import mysql.connector
from mysql.connector import Error
import os,webbrowser
import urllib.request
from urllib.parse import urlparse

#Fake url to input BINNumber
u= urlparse('//www.cwi.nl:80/%7Eguido/Python.html?binlocation=<A01C11>')

#To take from a url 

#Check the pattern of the Bin inputted
pattern = '\w{1}\d{2}\w{1}\d{2}'

#From the URL take what is after the question mark 
user_input = re.findall(pattern, u[4])[0]


#webbrowser.open(url)

#function to get the image of the bin location and output to browser
def get_image(sql_records):

    for row in sql_records:
            (x,y,w,h) = (int(row[0]),int(row[1]),int(row[2]),int(row[3]))

            img2 = cv2.imread("WarehouseLayout_Base.png")
            img2 = cv2.rectangle(img2, (x,y), (w, h), (0,0,0), -1)
           
            cv2.imwrite(filename, img2)
            html = '<html position:fixed;><img src="%s"></html>' %filename
            path = os.path.abspath(filename+'.html')
            url = 'file://' + path

            with open(path, 'w') as f:
                f.write(html)
            webbrowser.open(url)
            
#Select the x,y coordinates of the bin for mysql table            
def get_bin_location(bin):
    
    connection = mysql.connector.connect(host='localhost',
                                        database='WAREHOUSE',
                                        user='root',
                                        password='xxxx')

    sql_select_Query = "select St_X(LocationX), St_Y (LocationX),  St_X(LocationY), St_Y (LocationY) from BINLOCATION WHERE BIN_Number = '%s'" % bin 
    

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    records = cursor.fetchall()
    #print("Total number of rows in table: ", cursor.rowcount)
   

    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    
    get_image(records)

#Check the BIN number entered is the correct pattern 

def check_bin_pattern(input):
    if re.match(pattern, input):
        #Per checks
        input_upper = input[0:3].upper()
        get_bin_location(input_upper)
    else:
        print("It looks like the input is invalid\nThe BIN must be in the format of letter,two digits a letter and two digits\n")
        print("Here is an example: A02C11\n Please try again.")


filename = user_input+".png"

check_bin_pattern(user_input)

        
    
