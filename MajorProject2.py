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

sa1Float='sa1Float.shp'

ttfParams = {"INPUT": sa1Layer, "FIELD" : 'Tot_P_P', "OUTPUT": outputfilepath + sa1Float}
processing.run("qgis:texttofloat", ttfParams)

sa1FloatLayer = iface.addVectorLayer(outputfilepath + sa1Float, "", "ogr")

join_output='join.shp'

joinParams = {"INPUT" : radiusLayer, "JOIN" : sa1FloatLayer , "PREDICATE" : 0, \
"JOIN_FIELDS" : 'Tot_P_P', "SUMMARIES" : 5, "DISCARD_NONMATCHING": False, \
"OUTPUT" : outputfilepath + join_output}

processing.run("qgis:joinbylocationsummary", joinParams)

joinLayer = iface.addVectorLayer(outputfilepath + join_output, "", "ogr")

join2_output='join2.shp'

join2Params = {"INPUT" : joinLayer, "JOIN" : trafLayer , "PREDICATE" : 0, \
"JOIN_FIELDS" : 'ALLVEHS_MM', "SUMMARIES" : 5, "DISCARD_NONMATCHING": False, \
"OUTPUT" : outputfilepath + join2_output}

processing.run("qgis:joinbylocationsummary", join2Params)

join2Layer = iface.addVectorLayer(outputfilepath + join2_output, "", "ogr")