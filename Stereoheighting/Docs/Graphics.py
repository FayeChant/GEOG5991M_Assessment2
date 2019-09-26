# Python Scipt to run after SHPrep.py
# Process:Print overview graphic of obstructions point file on to fishnet

# O.Import modules required
import matplotlib.pyplot as plt
import os
import geopandas as gpd


# 1. Create a class to define all the files to use.
class Files():
    """**Class description**.
    
      The "files" class sets the file paths of the files to use
      
      It will use the following files:
      
      *Final*. Input - reformatted 'obstructions' point file with unwanted fields removed, sorted by geographic location
     
      *Fishnet_Count*. Input - Spatial join of Final and Fishnet with count of po   ints in each cell.
     
      *jpg*. - Output - graphic plot saved by running this module."""

    def __init__(self):
        # root directory you're working in
        self.root = input("type root directory: ")
        if self.root == '#' or not self.root:
            self.root = "C:\\GEOG5991M\\Stereoheighting"  # provide a default value if unspecified
        # final point file from SHprep.py
        self.final = os.path.join(self.root, "OUT\\OBSTRUCTIONS_final.shp")  # provide a default value if unspecified
        # final fishnet with point counts from SHprep.py
        self.fishnet_count = input("type output fishnet_ptcount file name from SHPrep: ")
        if self.fishnet_count == '#' or not self.root:
            self.fishnet_count = os.path.join(self.root, "OUT\\OBSTRUCTIONS_Fishnet_ptcount.shp")
        # output graphic file
        self.jpg = os.path.join(self.root, "OUT\\OBSTRUCTIONS_Fishnet_overview.jpg")

    def printing(self):
        """This method prints the filenames to check the Files class framework is successfully applied"""
        print("Files set to: Point file = ", self.final, "Fishnet with point count = ", self.fishnet_count)


# 2. Create graphic
# 2.1 Setup
# Copy framework for files from class Files.
files = Files()
# Run "printing" method to check filepaths set correctly
files.printing()
# 2.2 Print Graphic
# error capture
try:
    # set graphic up
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlabel("Longitude, decimal degrees")
    ax.set_ylabel("Latitude, decimal degrees")
    # read fishnet file
    fishnet = gpd.read_file(files.fishnet_count, driver='shapefile')
    # plot fishnet file
    fishnet.plot(ax=ax, color='white', edgecolor='blue');
    # read points file
    obstr = gpd.read_file(files.final)
    # plot points file
    obstr.plot(ax=ax, marker='o', color='red', markersize=5);
    # plot annotations of each cell number
    fishnet.apply(lambda x: ax.annotate(s=x.Id, xy=x.geometry.centroid.coords[0], ha='center'), axis=1);
    # save file
    filename = files.jpg
    plt.savefig(filename, dpi=600, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=True, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
    print("Program complete")
# COMPLETE
except Exception as err:
    print(err.args[0])
