#Datasets that are necessary:
#Geodatabase with Network dataset and 2 shapefiles (point features) containing unique routeids for the start and end locations.

#Import system modules
import arcpy, arcinfo
from arcpy import env
import os

start_time = time.time()
try:
    #Set environment settings
    output_dir = "C:/Data"
    #The NA layer's data will be saved to the workspace specified here
    env.workspace = os.path.join(output_dir, "Output.gdb")
    env.overwriteOutput = True

    print ("environment settings done")

    #Set local variables
    input_gdb = "<pathtodatabase>
    network = os.path.join(input_gdb, "Network", "Network_ND6")
    stops_home = os.path.join(input_gdb, "start_points")
    stops_work = os.path.join(input_gdb, "end_points")
    layer_name = "Routes"
    out_routes_featureclass = "RoutesA"
    impedance = "Length"

    print ("local variables done")

    #Create a new Route layer.  Optimize on TravelTime, but compute the
    #distance traveled by accumulating the Meters attribute.
    result_object = arcpy.na.MakeRouteLayer(network, layer_name, impedance,
                                         accumulate_attribute_name=["Length"],
                                         hierarchy="NO_HIERARCHY",output_path_shape = "TRUE_LINES_WITH_MEASURES",UTurn_policy = "ALLOW_UTURNS",
                                        restriction_attribute_name =["Oneway"])

    print ("new route layer done")
    #Get the layer object from the result object. The route layer can now be
    #referenced using the layer object.
    layer_object = result_object.getOutput(0)

    #Get the names of all the sublayers within the route layer.
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    #Stores the layer names that we will use later
    stops_layer_name = sublayer_names["Stops"]
    routes_layer_name = sublayer_names["Routes"]

    #Before loading the commuters' home and work locations as route stops, set
    #up field mapping.  Map the "Commuter_Name" field from the input data to
    #the RouteName property in the Stops sublayer, which ensures that each
    #unique Commuter_Name will be placed in a separate route.  Matching
    #Commuter_Names from stops_home and stops_work will end up in the same
    #route.
    field_mappings = arcpy.na.NAClassFieldMappings(layer_object, stops_layer_name)
    field_mappings["RouteName"].mappedFieldName = "RouteID"

    #Add the commuters' home and work locations as Stops. The same field mapping
    #works for both input feature classes because they both have a field called
    #"Commuter_Name"
    arcpy.na.AddLocations(layer_object, stops_layer_name, stops_home,
                        field_mappings, "",
                        exclude_restricted_elements = "EXCLUDE")
    arcpy.na.AddLocations(layer_object, stops_layer_name, stops_work,
                        field_mappings, "", append="APPEND",
                        exclude_restricted_elements = "EXCLUDE")

    print ("Add locations done")

    #Solve the route layer.
    arcpy.CheckOutExtension('Network')
    arcpy.na.Solve(layer_object)

    print ("Solve done")

    # Get the output Routes sublayer and save it to a feature class
    layer_object.saveACopy(out_routes_featureclass)


    print("Script completed successfully")

except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print("An error occurred on line %i" % tb.tb_lineno)
    print(str(e))

arcpy.CheckInExtension('Network')

elapsed_time = time.time() - start_time
print elapsed_time