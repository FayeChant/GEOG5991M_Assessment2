"""Stereoheighting data preparation tool.
Copyright (C) <2019>  <Faye Chant>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

# 0 SETUP ACTIVITIES
import os
import arcpy
from arcpy import env


arcpy.env.overwriteOutput = True
# CREATE CLASS
class Files():
    """**Set the file paths of the files to use.**
      
      *Original point file* - input by user (Default "OBSTRUCTIONS.shp")
     
      *Final* - reformatted with unwanted fields removed, sorted by geographic location - input by user
      (default = OUT\\OBSTRUCTIONS_final.SHP")
     
      *Fishnet* - polygon file to define cells for splitting up the point file.
     
      *Fishnet_Count* - Spatial join of Final and Fishnet with count of points in each cells
     
      *Copy* - temporary file. A copy of Original
     
      *Tempfishnet* - temporary file. Used for optimising fishnet
     
      *Fishnet2Obstr* - temporary file. Used to intersect points with Polygon and assign cell number for exporting
      shapefiles of points within individual cells."""

    def __init__(self):
        # root directory you're working in
        self.root = arcpy.GetParameterAsText(0)
        if self.root == '#' or not self.root:
            self.root = "C:\GEOG5991M\Stereoheighting"  # provide a default value if unspecified
        self.orig = arcpy.GetParameterAsText(1)
        if self.orig == '#' or not self.orig:
            self.orig = os.path.join(self.root, "Testdata\OBSTRUCTIONS.shp")  # provide a default value if unspecified
        self.final = os.path.join(self.root, "OUT\\OBSTRUCTIONS_final.shp")
        self.copy = os.path.join(self.root, "OUT\\OBSTRUCTIONSCOPY.shp")
        self.Fishnet_count = os.path.join(self.root, "OUT\\OBSTRUCTIONS_Fishnet_ptcount.shp")
        self.tempfishnet = os.path.join(self.root, "OUT\\OBSTRUCTIONS_fishnet_temp.shp")
        self.fishnet2obstr = os.path.join(self.root, "OUT\\Fishnet_OBSTRUCTIONS_ID.shp")

    def printing(self):
        """Print the filenames to check the Class framework is successfully applied."""
        print("orig = ", self.orig, "final = ", self.final, "copy = ", self.copy)

    def deletefiles(self):
        """Delete unwanted/temporary files """
        arcpy.Delete_management(self.tempfishnet)
        arcpy.Delete_management(self.copy)
        arcpy.Delete_management(self.fishnet2obstr)   

#        arcpy.Delete_management(self.Fishnet_count)
class Field():
    """**Set field attributes for new fields**; *fieldname, fieldtype, decplaces,
    fieldlen, expression*.
  
    field name = text string
    
    field type = DOUBLE, FLOAT, SHORT, LONG, STRING
    
    decimal places = the number of decimal places for field types of DOUBLE or FLOAT
    
    field length = number of characters for field types of STRING
    
    "expression" to be used in the field calculator to copy over the original field name (re-format it) or set a
    default value"""

    def __init__(self, fieldname, fieldtype, decplaces, fieldlen, expression):
        self.fieldname = fieldname
        self.fieldtype = fieldtype
        self.decplaces = decplaces
        self.fieldlen = fieldlen
        self.expression = expression

    def printing(self):
        """Print the field attributes to check the Field class framework is successfully applied"""
        print("fieldname = ", self.fieldname, ", fieldtype = ", self.fieldtype, ", number of dec places = ",
              self.decplaces, ", field length = ", self.fieldlen,
              "expression = ", self.expression)

    def calcfield(self, file):
        """Copy the existing fields to the new correctly formatted fields"""
        arcpy.CalculateField_management(file, self.fieldname, self.expression, "VB", "")


class Features():
    """**Set up and manipulates the feature class shapefiles.**"""

    def __init__(self, featureclass):
        self.Featureclass = featureclass
        self.desc = arcpy.Describe(self.Featureclass)

    def maxfromshp(self, featureclass, variable):
        """Calculate the maximum value from a variable within a feature class."""
        cursor = arcpy.da.SearchCursor(featureclass, variable)
        firstrecord = True
        for row in cursor:
            if firstrecord:
                firstrecord = False
                maxvalue = int(row[0])
            else:
                maxvalue = max(int(row[0]), maxvalue)
        return maxvalue

    def origin(self):
        """ USe the describe tool in ArcPy to generate the lower left corner coordinates of a
        feature class."""
        origin = str(self.desc.extent.XMin) + " " + str(self.desc.extent.YMin)
        return origin

    def yaxis(self):
        """ Use the describe tool in ArcPy to generate the YAxis coordinates of a feature class
        (for use in the fishnet tool)."""
        yaxis = str(self.desc.extent.XMin) + " " + str(self.desc.extent.YMin + 10)
        return yaxis

    def opp_corner(self):
        """ Use the describe tool in ArcPy to generate the upper right corner coordinates of a
        feature class."""
        opp_corner = str(self.desc.extent.XMax) + " " + str(self.desc.extent.YMax)
        return opp_corner

    def coord_sys(self):
        """Set the coordinate system as the spatial reference of the shapefile (for the fishnet tool)."""
        coord_sys = self.desc.spatialReference
        return coord_sys


class Fishnet(Features):
    """**Set up the methods to optimise the fishnet over the points file, and exporting shapefiles
    of points within individual cells.**"""

    def grid(self, code_block, numrows, tempfishnet):
        """Set up the fishnet tool from arcpy and calculate an id number for each cell of the fishnet."""
        origin = self.origin()
        yaxis = self.yaxis()
        opp_corner = self.opp_corner()
        numcolumns = numrows
        arcpy.CreateFishnet_management(tempfishnet, origin, yaxis, "0", "0", numrows, numcolumns, opp_corner,
                                       "NO_LABELS", "#", "POLYGON")
        arcpy.CalculateField_management(tempfishnet, "Id", "autoIncrement()", "PYTHON_9.3", code_block)
        print("grid ", numcolumns, "by", numrows, "complete")

    def joinpts2grid(self, tempfishnet, sorted, fishnet_count):
        """Join the points to the fishnet cells to count how many points fall in each cell."""
        # count points in each polygon of the fishnet
        targetfeatures = tempfishnet
        joinfeatures = sorted
        join_operation = "JOIN_ONE_TO_ONE"
        keep = "true"
        match = "CONTAINS"
        arcpy.SpatialJoin_analysis(targetfeatures, joinfeatures, fishnet_count, join_operation, keep, "", match, "", "")
        print("spatial join complete")

    def intersect(self, grid2pts):
        """Intersect the points with the fishnet to assign the id number of the fishnet cell within
        which each point resides."""
        in_features = ["OUT\\OBSTRUCTIONS_final.shp", "OUT\\OBSTRUCTIONS_fishnet_temp.shp"]
        print(in_features)
        join_attributes = "ALL"
        output_type = "POINT"
        arcpy.Intersect_analysis(in_features, grid2pts, join_attributes, "", output_type)
        print("intersect complete")

    def divpts2cells(self, grid2pts, counter):
        """Output the points contained within each cell to an individual shapefile."""
        output = ("OUT\\Cells\\Obstructions_cell" + str(counter) + ".shp")
        print("saving ", output)
        where_clause = '"id" = ' + "%s" % counter
        arcpy.Select_analysis(grid2pts, output, where_clause)
