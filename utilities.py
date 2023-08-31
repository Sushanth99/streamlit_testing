#!/usr/bin/env python

## Author: Sushanth Reddy Kamaram
## Email: ksushanthreddy0605@gmail.com

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table

import pickle
import math
import os

## Source class

class Source:
    def __init__(self, filepath, filter=False):        
        # Original data
        self.filepath = filepath
        self.df_ = self.lc_fits_to_df(self.filepath)
        self.shape_ = self.df_.shape
        
        # Latest data
        self.df = self.df_.copy()
        self.is_filtered = False
        self.shape = self.df.shape
        
        if filter == True:
            self.filter_data()
    
    def __len__(self): return len(self.df)

    @staticmethod
    def lc_fits_to_df(lc_file, save_file=False) -> 'DataFrame':
        """ 
        Returns a Pandas data frame from input fits file path. The FITS file
        is the output light curve data from FermiPy analysis.

        Libaries: astropy.table.Table, pandas, numpy libraries 
        Input: path to the FITS file
        Output: pandas.DataFrame with the light curve data with MJD as index
        """
        dat = Table.read(lc_file, format='fits')
        tmin = np.array(dat['tmin'])
        tmax = np.array(dat['tmax'])
        mjd = (np.array(dat['tmin_mjd']) + np.array(dat['tmax_mjd'])) / 2
        flux = np.array(dat['flux'])
        flux_error = np.array(dat['flux_err'])
        eflux = np.array(dat['eflux'])
        eflux_error = np.array(dat['eflux_err'])
        ts = np.array(dat['ts'])

        alpha = np.array([arr[1] for arr in dat['param_values']])
        alpha_error = np.array([arr[1] for arr in dat['param_errors']])
        data = {'flux': flux,
                'flux_error': flux_error,
                'eflux': eflux,
                'eflux_error': eflux_error,
                'tmin': tmin,
                'tmax': tmax,
                'MJD': mjd,
                'TS': ts,
                'alpha': alpha,
                'alpha_error': alpha_error,
               }
        df = pd.DataFrame(data)

        if save_file == True: # Assumes the file name has .fits at the end
            df.to_csv(lc_file.replace('.fits', '.csv'))

        df.set_index('MJD', inplace=True)
        return df
    
    def filter_data(self, flux_ratio=2, index_ratio=2, min_ts=9) -> None:
        self.df = (self.df[(self.df['flux']/self.df['flux_error'] > flux_ratio) & 
                           (np.abs(self.df['alpha']/self.df['alpha_error']) > index_ratio) & 
                           (self.df['TS'] > min_ts)])
        
        self.is_filtered = True
        self.shape = self.df.shape
        return None
    
    def save_to_csv(self, filename=None):
        if filename is None:
            self.df_.to_csv(self.filepath.replace('.fits', '.csv'))
        print(f'Data saved to {self.filepath.replace(".fits", ".csv")}')

