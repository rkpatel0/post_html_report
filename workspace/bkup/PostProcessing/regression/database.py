'''
Created on Oct 30, 2014

@author: Rishi.Patel
'''

import pandas as pd
import numpy as np
from warnings import warn

class Reader(object):
    '''
    Use to read log file_names from database and filter based on custom settings
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.info = {}
        
        
    def fetch_datalogs(self, files, TEST='CHAR', EVK='1900', path=''):
        '''
        files: List of the .csv files that are to be processed
        TEST:  Name of test type - CHAR / SOAK / PMU
        EVK:   Name of EVK type
        '''

        TEST = ''
        
        if not path:
            path = r'\\lightspeed1\labwork\regression\result\char/' + TEST + '/' + EVK + '/'
            
        # Save info for other objects
        self.info['path'] = path
        self.info['files'] = files
        
        # Grab data and clean up
        data = self._read_all_files(path, files)
        self._clean_datalogs(data)
        self._remove(data)
        
        return data
    
    def _remove(self, data):
        'remove unused columns from dataframe'
        
        # Use to drop Nan or something...
        pass
        
    def _clean_datalogs(self, df):
        'try to not touch data here'
        
        #df.dropna(inplace=True)

        # Reindex dataframe due to duplicate index
        df.index = range(df.index.size)
        
    def _read_all_files(self, path, files):
        'Append all file_names to read into a dataframe'
        
        raw = pd.DataFrame()
        for name in files:
            full_path = path + name
            data = pd.read_csv(full_path)
            raw = raw.append(data)
            
        return raw