SHPrep module
=============
Description
---------------
:*Author*: Faye Chant <gy16fc@leeds.ac.uk>
:*Date*: 2019-09-25
:*Revision*: 1
:*Summary*: This is a module to prepare contractor supplied obstructions files for stereoheighting.Typically these files contain hundreds of points and many fields that are not required for stereoheighting, or are incorrectly formatted. The module expects an input points shapefile with a standard set of fields, so for the purposes of this excercise a dummy file has been created and is supplied under "Testdata". In addition, an arbitrary threshold of no more than 10 points per shapefile is set. In reality this would be higher and can be altered at line 114 of SHPrep.py.

Process
-------

This script uses the Stereoframework module to modify the contractor obstructions points shapefile into the required format.

+ Step 1. It reformats the required fields, and deletes unwanted fields. 
+ Step 2. It sorts the points based on geographic location and adds a new id number.  
+ Step 3. If the shapefile contains more than 10 points, it optimises a grid of cells over the points extent, and outputs the points contained within each cell as separate shapefiles.

Inputs from User
----------------

+ Working directory in format 'C:\\GEOG5991M\\Stereoheighting' (note no "\" on the end of the filepath)
+ Obstructions shapefile.

Output
------

* OUT\OBSTRUCTIONS_final.shp* - Modified Obstructions file reformatted with unwanted fields removed, sorted by geographic location
* OUT\OBSTRUCTIONS_Fishnet_ptcount.shp* - Polygon shapefile of the final fishnet with a count of the points in each cell
* Cells\Obstructions_cellxx.shp - - Shapefile of the points contained within each indivdual cell of the fishnet.


.. automodule:: SHPrep
    :members:
    :undoc-members:
    :show-inheritance:

