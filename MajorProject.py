import processing

#create file paths (edit these to the location of your data)
inputfilepath = 'C:\\Users\\petfr\\OneDrive\\Desktop\\RMIT\\Graduate Certificate of Geospatial Science\\Geospatial Programming\\Major Project\\WorkingData\\'
outputfilepath = 'C:\\Users\\petfr\\OneDrive\\Desktop\\RMIT\\Graduate Certificate of Geospatial Science\\Geospatial Programming\\Major Project\\WorkingData\\'
lvlXFileName = 'LevelCrossings.shp'
trackFileName= 'TrackCentreLine.shp'
stnFileName= 'StationWithPatronage.shp'
sa1FileName= 'MetroSA1s3.shp'
trafFileName= 'Traffic_Volume.shp'
radius_output= 'radius.shp'

lvlXLayer = iface.addVectorLayer(inputfilepath + lvlXFileName, lvlXFileName[:-4], "ogr")
trackLayer = iface.addVectorLayer(inputfilepath + trackFileName, trackFileName[:-4], "ogr")
stnLayer = iface.addVectorLayer(inputfilepath + stnFileName, stnFileName[:-4], "ogr")
sa1Layer = iface.addVectorLayer(inputfilepath + sa1FileName, sa1FileName[:-4], "ogr")
trafLayer = iface.addVectorLayer(inputfilepath + trafFileName, trafFileName[:-4], "ogr")

#creating a 1km buffer to calculate peds and road users affected by level crossings
buffParams = {"INPUT" : lvlXLayer, "DISTANCE" : 1000, "SEGMENTS" : 5, \
"END_CAP_STYPE" : 0, "JOIN_STYLE" : 0, "MITER_LIMIT": 2, \
"DISSOLVE": False, "OUTPUT" : outputfilepath + radius_output}
processing.run("native:buffer", buffParams)
#creating a new layer with the buffer
radiusLayer = iface.addVectorLayer(outputfilepath + radius_output, "", "ogr")

#add new fields in the lvlXLayer to place priority scores
lvlXLayer.startEditing()

lvlXLayer.dataProvider().addAttributes([QgsField("peds",  QVariant.Double, "double", 3, 3)])
lvlXLayer.dataProvider().addAttributes([QgsField("train",  QVariant.Double, "double", 3, 3)])
lvlXLayer.dataProvider().addAttributes([QgsField("road",  QVariant.Double, "double", 3, 3)])

lvlXLayer.updateFields()

lvlXLayer.commitChanges()