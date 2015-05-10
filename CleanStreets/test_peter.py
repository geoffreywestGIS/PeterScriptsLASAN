__author__ = 'GeoffreyWest'

import arcpy

fc = "C:\CleanStreets_55_56.gdb\SO_SC_Open_55_56_5_4_15"
myOutputFile = open("C:\PeterScripts\CleanStreets\open_test.txt",'w')
rows =arcpy.da.SearchCursor(fc, ["PeterField"])
for row in rows:
    myOutputFile.write(str(row[0]) + '\n')
del row, rows
myOutputFile.close()