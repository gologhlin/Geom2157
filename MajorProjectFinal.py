import processing

#set refernce system so all layers are projected correctly
my_crs=QgsCoordinateReferenceSystem(7855)
QgsProject.instance().setCrs(my_crs)

#create file paths (edit these to the location of your data)
inputfilepath = 'C:\\Users\\petfr\\OneDrive\\Desktop\\RMIT\\Graduate Certificate of Geospatial Science\\Geospatial Programming\\Major Project\\WorkingData\\'
outputfilepath = 'C:\\Users\\petfr\\OneDrive\\Desktop\\RMIT\\Graduate Certificate of Geospatial Science\\Geospatial Programming\\Major Project\\WorkingData\\'
lvlXFileName = 'LevelCrossings7855.shp'
trackFileName= 'PTV_TRAIN_CORRIDOR_CENTRELINE.shp'
stnFileName= 'StationWithPatronage.shp'
sa1FileName= 'MetroSA1s7855.shp'
trafFileName= 'TrafficVolume7855.shp'
radius_output= 'radius.shp'

#create layers to use data
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

#converting data type so it can be manipulated
ttfParams = {"INPUT": sa1Layer, "FIELD" : 'Tot_P_P', "OUTPUT": outputfilepath + sa1Float}
processing.run("qgis:texttofloat", ttfParams)

#creating new layer to use converted data
sa1FloatLayer = iface.addVectorLayer(outputfilepath + sa1Float, "", "ogr")
join_output='join.shp'

#joining the radius layer and SA1 layer together so their useful data is in onelayer
joinParams = {"INPUT" : radiusLayer, "JOIN" : sa1FloatLayer , "PREDICATE" : 0, \
"JOIN_FIELDS" : 'Tot_P_P', "SUMMARIES" : 5, "DISCARD_NONMATCHING": False, \
"OUTPUT" : outputfilepath + join_output}

processing.run("qgis:joinbylocationsummary", joinParams)

#creating new layer of joined data
joinLayer = iface.addVectorLayer(outputfilepath + join_output, "", "ogr")

final_output='final.shp'

#peforming second join to combine traffic data with the radius layer and SA1 layer, 
#so all data is in one attribute table for manipulation
finalParams = {"INPUT" : joinLayer, "JOIN" : trafLayer , "PREDICATE" : 0, \
"JOIN_FIELDS" : 'ALLVEHS_MM', "SUMMARIES" : 5, "DISCARD_NONMATCHING": False, \
"OUTPUT" : outputfilepath + final_output}

processing.run("qgis:joinbylocationsummary", finalParams)

#creating a new layer of joined data
finalLayer = iface.addVectorLayer(outputfilepath + final_output, "", "ogr")

#create new attribute field to store calculation in
finalLayer.startEditing()

finalLayer.dataProvider().addAttributes([QgsField("score",  QVariant.Double)])

finalLayer.updateFields()

finalLayer.commitChanges()

#calculating score based on both variables equally weighted
with edit(finalLayer):
    for f in finalLayer.getFeatures():
        f['score'] = f['Tot_P_P_su']/21035 + f['ALLVEHS_MM']/1592600
        finalLayer.updateFeature(f)

#ordering attribute table so highest scoring level crossing is first (highest ranking)
config = finalLayer.attributeTableConfig()

config.setSortExpression("score") # name of the field
config.setSortOrder(1) # 0:ascending 1:descending

finalLayer.setAttributeTableConfig(config)

#open attribute table
iface.showAttributeTable(iface.activeLayer())