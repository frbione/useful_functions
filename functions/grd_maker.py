import pandas as pd
import numpy as np
import rasterio
import tkinter as tk
from tkinter import filedialog as fd
import os

def xyz_to_grd():
        root = tk.Tk()
        root.withdraw()

        filetypes = ('text files', '*.txt'), ('csv files', '*.csv')
        xyzFilePath = fd.askopenfilenames(title="Select the XYZ files to be converted (.txt or .csv).",filetypes=[('text files','*.txt'),('csv files', '*.csv')])
        outPath = fd.askdirectory(title="Select output directory for the converted files (.grd)")

        #xyzNames = []
        for t in range(len(xyzFilePath)):
                xyzFile = os.path.basename(xyzFilePath[t])
                xyzFile = xyzFile[:len(xyzFile) - 4]
                data = pd.read_csv(xyzFilePath[t], header=None, sep='\t')
                data = data.rename(columns={0: "X", 1: "Y", 2: "Z"})
                data_size = len(data.index)

                # Getting grid parameters
                nx = len(data.X.unique())
                print("nx = ", nx)
                ny = len(data.Y.unique())
                print("ny = ", ny)
                xmin = min(data.X)
                print("xmin = ", xmin)
                xmax = max(data.X)
                print("xmax = ", xmax)
                ymin = min(data.Y)
                print("ymin = ", ymin)
                ymax = max(data.Y)
                print("ymax = ", ymax)
                zmin = min(data.Z)
                print("zmin = ", zmin)
                zmax = max(data.Z)
                print("zmax = ", zmax)

                # Creating the .grd blank file
                grd = open(outPath+rf"\{xyzFile}.grd", "w+")
                grd.write(f"DSAA\n{nx} {ny}\n{xmin} {xmax}\n{ymin} {ymax}\n{zmin} {zmax}\n")  # Header

                print("Original XYZ file: ", data)

                cols = data.X.unique()  # lista de diferentes Xcoords
                rows = data.Y.unique()  # lista de diferentes Ycoords

                # Creating the empty matrix
                mat = pd.DataFrame(columns=cols, index=rows).sort_index(ascending=True)
                print("Empty matrix: ", mat)

                # Filling the matrix
                for d in range(0, data_size - 1):
                        mat.loc[data.Y.iloc[d], data.X.iloc[d]] = data.Z.iloc[d]

                mat = mat.fillna(99999)  # nan values
                print("Filled matrix: ", mat)

                # Body of the .grd
                mat.to_csv(outPath+rf"\{xyzFile}.grd", header=False, index=False, sep=' ', mode='a', line_terminator='\n\n')

                # Writing final file
                with open(outPath+rf"\{xyzFile}.grd", "r") as scan:
                        grd.write(scan.read())

                print('File saved to: ', outPath+rf"\{xyzFile}.grd")
