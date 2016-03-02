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
        
        
    def fetch_datalogs(self, files, EVK='1900', TEST='', path=''):
        '''
        files: List of the .csv files that are to be processed
        TEST:  Name of test type - CHAR / SOAK / PMU
        EVK:   Name of EVK type
        '''

        if not path:
            path = r'\\lightspeed1\labwork\regression\result/'
            path += TEST + '/'
            path += EVK + '/'
            
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
        
        self._add_time_in_sec(df)
        if 's_Freq_Hz' in df.columns:
            df['s_Freq_MHz'] = df['s_Freq_Hz'] / 1e6

        # Reindex dataframe due to duplicate index
        df = df.reset_index()

    def _add_time_in_sec(self, df):
        # Just add a time column - why not?
        tmp = df['TestTimeRepeatNoReset_s'].copy()
        tmp.index += 1
        tmp =  df['TestTimeRepeatNoReset_s'] - tmp
        try:
            step_size = tmp[(tmp > 0) & (tmp < 3)].mean().round(1)
        except AttributeError:
            warn('Cannot generate timing data - setting to 1')
            step_size = 1
        df['time'] = (step_size * df['r_RepeatNumWithoutReset']).round(1)
        
    def _read_all_files(self, path, files):
        'Append all file_names to read into a dataframe'
        
        raw = pd.DataFrame()
        for name in files:
            full_path = path + name
            data = pd.read_csv(full_path)
            raw = raw.append(data)
            
        return raw