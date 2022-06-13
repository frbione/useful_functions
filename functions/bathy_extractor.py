import tkinter as tk
from tkinter import filedialog as fd
from os import listdir
from os.path import isfile, join
import os
import pandas as pd
import geopandas as gpd
import rasterio

def extract_from_tif():

    root = tk.Tk()
    root.withdraw()

    #lista contendo o diretório de cada arquivo raster selecionado
    rasterPaths = list(fd.askopenfilenames(title="Selecione os mapas (.tif)"))
    rasterNames = []
    for t in range(len(rasterPaths)):
        rasterFiles = os.path.basename(rasterPaths[t])
        rasterNames.append(rasterFiles)


    wellPaths = list(fd.askopenfilenames(title="Selecione arquivos de pontos/poços (.csv)"))
    wellNames = []
    for i in range(len(wellPaths)):
        wellFiles = os.path.basename(wellPaths[i])
        wellNames.append(wellFiles)


    outPath = fd.askdirectory(title="Selecione a pasta onde deseja salvar os resultados")
    for w in range(len(wellPaths)):
        df = pd.DataFrame()
        pts = pd.read_csv(wellPaths[w], encoding="ISO-8859-1")
        pts = pts[['Time (Ma)','Lat','Lon']]
        coords = [(x,y) for x, y in zip(pts.Lon, pts.Lat)]

        for t in range(len(rasterPaths)):
            map = rasterio.open(rasterPaths[t])
            age = os.path.basename(rasterPaths[t])
            age = int(age.replace(".tif",""))

            pts['Paleobatimetria_Scotese [m]'] = [x[0] for x in map.sample(coords)]
            pts2 = pts.loc[pts['Time (Ma)'] == age]  # Seleciona só a linha que contem a idade desejada, com base no nome do arquivo
            df = df.append(pts2)  # adiciona as idades correspondentes a cada mapa a cada iteração
            df.to_csv(outPath + rf'\{wellNames[w]}', sep='\t', index=False)





extract_from_tif()