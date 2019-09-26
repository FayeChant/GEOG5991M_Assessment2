Graphics module
===============
Description
---------------
:*Author*: Faye Chant <gy16fc@leeds.ac.uk>
:*Date*: 2019-09-25
:*Revision*: 1
:*Summary*: The Graphics module uses the geopandas and matplotlib modules to generate an overview plot of a polygon shapefile, and a points shapefile.

Use
---
 
Run Graphics.py after SHPrep.py has successfully run. The user will be prompted to input the working directory.

Process
-------

+ This module plots the final fishnet polygons, and the final obstructions points files, annotated with the cell number for cross reference to the files in OUT\\Cells.

Inputs from User
----------------

+ Working directory in format 'C:\\GEOG5991M\\Stereoheighting' (note no "\\" on the end of the filepath)

Inputs from SHPrep (automatic)
------------------------------

+ OUT\\OBSTRUCTIONS_final.shp
+ OUT\\OBSTRUCTIONS_Fishnet_ptcount.shp

Outputs 
-------

+ OUT\\OBSTRUCTIONS_Fishnet_overview.jpg - an overview diagram of all of the points and the fianl fishnet.

Classes and Modules
-------------------

.. automodule:: Graphics
    :members:
    :undoc-members:
    :show-inheritance:
