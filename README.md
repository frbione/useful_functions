# Useful functions 
This is a set of useful functions developed by [frbione](https://github.com/frbione) in order to automate some tasks during his PhD thesis development.<br>

    
### **bathy_extractor** 
#### extract_from_tif

This function can sample Z-values from paleobathymetric maps (rasters), based on time-varying point coordinates,
which are input from .csv points files. The rasters + points set derives from plate tectonics kinematic models, such as [GPlates](https://www.gplates.org/) or [pyGplates](https://www.gplates.org/docs/pygplates/).
<br>

**Important instructions** <br>
Raster files:
- Can be in .tif or .grd formats
- Must be named according to the corresponding age. e.g., for 100 Ma: 100.tif <br>

Point files:

- Must be in .csv format
- Each .csv file must correspond to a unique well/point with a time-varying location
- Each .csv file must be named according to the well/point name. e.g., well_X.csv | X.csv | etc.
- Each .csv file must contain at least 3 columns: 'Time (Ma)' | 'Lat' | 'Lon' 
- The column 'Time (Ma)' must contain age values correspondent to the raster paleomaps' ages. 

PS: It is important that both the rasters + points set had been created using the same plate rotation model.<br>
PS2: It is **not necessary** to have **all** the rasters-equivalent ages in each point or vice-versa

<br></br>
### **grd_maker** 
#### xyz_to_grd


This function can convert tabular XYZ data from .txt or .csv files to grid text file format (.grd). Example [here](http://surferhelp.goldensoftware.com/topics/ascii_grid_file_format.htm).
<br>

** Important instructions** <br>
XYZ files:
- Can be in .txt or .csv formats
- Must be tab '\t' separated, but this can be changed in the original function for comma-separated files<br>
- This function only converts the file, it does not resize or reshape the original grid. 
