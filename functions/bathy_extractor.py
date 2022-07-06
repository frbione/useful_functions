#library imports
import tkinter as tk
from tkinter import filedialog as fd
import os
import pandas as pd
import rasterio

def z_from_tifs():
    '''
    This function samples Z-values from rasters, based on time-varying point coordinates.
    Point coordinates are input from .csv files.

    Important instructions
    Raster files:

    Can be in .tif or .grd (text) formats
    Must be named according to the corresponding time/age. e.g., for 100 Ma: 100.tif

    Point coordinates:

    Must be in .csv format
    Each .csv file must correspond to a unique well/point with a time-varying location
    Each .csv file must be named according to the well/point name. e.g., well_X.csv | X.csv | etc.
    Each .csv file must contain at least 3 columns: 'Time (Ma)' | 'Lat' | 'Lon'
    The column 'Time (Ma)' will be used to associate the correspondent coordinates to the raster of the same age.

    PS: It is extremely recommended that both rasters and sampling points had been created using the same plate rotation model.
    PS2: It is not necessary to have all the rasters-equivalent ages in each point or vice-versa.
     '''

    # opens dialog window for file selection
    root = tk.Tk()
    root.withdraw()

    # path were the files will be saved.
    outPath = os.path.dirname(os.getcwd()) + r'\out'


    # listing raster files paths and names
    rasterPaths = list(fd.askopenfilenames(title='Select raster files', filetypes=[("raster", "*.tif")]))
    rasterNames = []

    for t in range(len(rasterPaths)):
        rasterFiles = os.path.basename(rasterPaths[t])
        rasterNames.append(rasterFiles)

    # listing sampling point files paths and names
    wellPaths = list(fd.askopenfilenames(title='Select sampling point files', filetypes=[("csv", "*.csv")]))
    wellNames = []
    for i in range(len(wellPaths)):
        wellFiles = os.path.basename(wellPaths[i])
        wellNames.append(wellFiles)

    # iterating to create a dataframe for each sampling point file
    for w in range(len(wellPaths)):
        df = pd.DataFrame()

        # NOTE: change the character encoding if needed
        pts = pd.read_csv(wellPaths[w], encoding="ISO-8859-1")
        pts = pts[['Time (Ma)','Lat','Lon']]

        # Creating a list of tuples containing each lat-lon pair of a csv file
        coords = [(x,y) for x, y in zip(pts.Lon, pts.Lat)]

        # Sampling the point coordinates in the raster files
        for t in range(len(rasterPaths)):
            map = rasterio.open(rasterPaths[t])
            age = os.path.basename(rasterPaths[t])
            age = int(age.replace(".tif",""))

            pts['Paleobathimetry_from_Scotese (m)'] = [x[0] for x in map.sample(coords)]

            # Matching the lines containing the corresponding ages from the points and raster files and appending to the final df
            pts2 = pts.loc[pts['Time (Ma)'] == age]
            df = df.append(pts2)
            df.to_csv(outPath + rf'\{wellNames[w]}', index=False)

    return print(f'Process Finished. Files were saved to {outPath} ')

z_from_tifs()



