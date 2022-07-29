# BIN_Location
Shows the location of a BIN in a Warehouse and prints out a html image of that location

Populate_mySql_table.py populates the SQL  BIN_LOCATION table already created in MySQL. 
The BIN information (text and location of the text) located in the WarehouseLayout.png is extracted via cv2 and pytesseract.
This information is then passed to the MySQL table BIN_LOCATION.

Get_BIN_location.py takes the BIN ID provided from the url and locates the BIN information in the BIN_LOCATION table. 
The location of that BIN is highlighted in the image and outputted in the browser. A png file is also generated.




