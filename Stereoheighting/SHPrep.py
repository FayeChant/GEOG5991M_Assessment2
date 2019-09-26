# ---------------------------------------------------------------------------
#: Import modules required
# noinspection PyUnresolvedReferences
import arcpy
#from arcpy import env
import os
import Stereoframework


# Input workspace
#set workspace for ArcMap env.workspace = "C:\..."
#env.workspace = "C:\\GEOG5991M\\Stereoheighting"

# Set to overwrite existing files
#arcpy.env.overwriteOutput = True

# Set filenames to work on using Stereoframework.Files class
files = Stereoframework.Files()
files.printing()  #: Prints the names of the files set to check class is instantiated properly.

# Model
try:
    # Defines new fields to add to original shapefile
    Newfields = [["INT2DBL", "DOUBLE", "2", "", "[FieldINT1]"], ["STRING2DBL", "DOUBLE", "2", "", "[Field7]"],
                 ["INCSTRLEN", "STRING", "", "10", "[Field1]"], ["INDEX", "SHORT", "", "", "0"]]
    # loop through each new field and assigns the framework from the field class of the Stereoframework.py module,
    # and the attributes set in "Newfields"
    fields = []
    for i in range(len(Newfields)):
        attr = (Newfields[i])
        fields.append(Stereoframework.FIELD(attr[0], attr[1], attr[2], attr[3], attr[4]))
    # Make a copy of features in orig file to work on
    arcpy.CopyFeatures_management(files.orig, files.copy, "", "0", "0", "0")
    # Add new fields to obstructions file
    for field in fields:
        arcpy.AddField_management(files.copy, field.fieldname, field.fieldtype, "", field.decplaces, field.fieldlen, "",
                                  "NULLABLE", "NON_REQUIRED", "")
    # Copy original fields to newly formatted fields
    field.calcfield(files.copy)
    # Get a list of all fields in the obstruction file
    fieldlist = arcpy.ListFields(files.copy)
    # set up empty list
    fieldlist2 = []
    # extract only field name
    for field in fieldlist:
        fieldlist2.append(field.name)
    print("all fields = ", fieldlist2)
    # Define fields to retain in final obstructions file
    keepfield = [u"FID", u"OBJECTID", u"Shape", u"INCSTRLEN", u"STRING2DBL", u"Field2", u"Field5", u"INT2DBL", u"INDEX"]
    print("Keeping ", keepfield)
    # empty list
    Drop_Field = []
    # Compile list of fields to delete
    for field in fieldlist2:
        if field not in keepfield:
            Drop_Field.append(field)
    print("dropping ", Drop_Field)
    # Delete unwanted fields
    arcpy.DeleteField_management(files.copy, Drop_Field)
    print("fields deleted")
    # Sort records by geographic location
    arcpy.Sort_management(files.copy, files.final, "Shape ASCENDING", "UL")
    print("points sorted")
    # Assign new ID number to points
    Code_Block = "rec=0 \\ndef autoIncrement(): \\n    global rec \\n    pStart = 1 \\n    pInterval = 1 \\n    if (rec == 0): \\n        rec = pStart \\n    else: \\n        rec += pInterval \\n    return rec"
    arcpy.CalculateField_management(files.final, "INDEX", "autoIncrement()", "PYTHON_9.3", Code_Block)
    print("new id assigned")

    # If more than 10 points in obstruction file, extract smaller cells as individual shapefiles
    # count points in sorted (final) file.
    featureclass = files.final
    variable = "INDEX"
    features = Stereoframework.Features(featureclass)
    # set coordinates system of fishnet
    #    env.outputCoordinateSystem = features.coord_sys()
    # Count all points in file
    count = features.maxfromshp(featureclass, variable)
    print("initial point count set")

    # Process: find correct fishnet
    # Start at 2 * 2 cells and loop through finer fishnets, counting points in each polygon until below threshold.
    # threshold of 10 per cell max.
    fishnet = Stereoframework.Fishnet(featureclass)
    numrows = 1
    print("framework copied")
    while count > 10:
        numrows += 1
        fishnet.grid(Code_Block, numrows, files.tempfishnet)
        # join points file to fishnet
        fishnet.joinpts2grid(files.tempfishnet, files.final, files.Fishnet_count)
        # count points in each polygon of the fishnet
        featureclass = files.Fishnet_count
        field1 = "JOIN_COUNT"
        MaxValue = features.maxfromshp(featureclass, field1)
        count = MaxValue
        print("Max = " + str(count))
    print("found fishnet - " + str(numrows) + "by" + str(numrows) + "cells")

    # Output points in each cell of fishnet as individual shapefiles.
    fishnet.intersect(files.fishnet2obstr)
    counter = 1
    max_count = ((numrows * numrows)+1)
    print("max cells = ", str(max_count))
    while counter < max_count:
        fishnet.divpts2cells(files.fishnet2obstr, counter)
        counter += 1

    # Delete temp files
    files.deletefiles()
    print("Program complete")
    
except Exception as err:
    print(err.args[0])
