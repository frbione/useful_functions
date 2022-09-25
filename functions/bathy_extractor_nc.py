# library imports
import os
import xarray as xr
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd

def merge_ncs():
    '''
    This function merges the Scotese & Wright (2018) NetCDF files
    into a single file with a time dimension.

    Important instructions:

    * n = 5 is the time step originally provided by Scotese & Wright (2018)
     '''

    # opens dialog window for file selection
    root = tk.Tk()
    root.withdraw()

    # path where the files will be saved.
    outPath = os.path.dirname(os.getcwd()) + r'\out'

    ncPaths = list(fd.askopenfilenames(title='Select NetCDF files',
                                    filetypes=[("NetCDF", "*.nc")]))

    # Expanding dimension for the first NC file, then, we will do the same iteratively and merge the rest of the files.

    dset_0 = xr.open_dataset(ncPaths[0])

    time_arr = np.empty(1)
    time_arr.fill(0)

    time_dim = xr.DataArray(time_arr, coords={'time': time_arr},
                        dims=["time"])

    dset_0 = dset_0.expand_dims(time=time_dim)

    # Iterating through and merging the other files
    # n = 5 refers to the original time step of 5 Ma provided by Scotese & Wright (2018)
    n = 5
    for nc in range(1,len(ncPaths)):
        dset = xr.open_dataset(ncPaths[nc])
        time_arr = np.empty(1)
        time_arr.fill(n)
        n += 5

        time_dim = xr.DataArray(time_arr, coords={'time': time_arr},
                                dims=["time"])

        dset = dset.expand_dims(time=time_dim)

        dset_0 = xr.merge([dset_0, dset])

    dset_0.to_netcdf(outPath+r'\Merged.nc')

    return(print('NetCDF summary: \n\n', dset_0, f'\n\nFile was saved to {outPath}\Merged.nc'))

merge_ncs()


