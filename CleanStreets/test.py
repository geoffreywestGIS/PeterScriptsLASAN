__author__ = 'GeoffreyWest'

PeterTable = "C:\PeterText.gdb\Table_55_56"
myOutputFile = open("C:\PeterScripts\CleanStreets\Peter.txt", 'w')
rows = arcpy.da.SearchCursor(PeterTable, ["PtrText"])


for row in rows:
        myOutputFile.write(str(row[0]) + '\n')
        del row, rows
   myOutputFile.close()