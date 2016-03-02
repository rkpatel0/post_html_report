'''
Created on Oct 30, 2014

@author: Rishi.Patel
'''

import seaborn as sns
import collections
import pandas as pd
#import numpy as np

class Process(object):
    '''
    Use to post process and analyze data
    Idea is that this should be flexible enough to use with any data set
    '''


    def __init__(self, config={}):
        '''
        Constructor
        '''
        
        self.param = config
        self._load_default(config)
        self.oVarPlt = Variance()
        self.oTimePlt = Time()
        self.oParamPlt = Parameter()
         
    def _load_default(self, config):
        
        self.CONST = {
                      'to_keep': .70,
                      'correctedmxaAclr1Max': -47,      # Spec for ACLR
                      }

        self.y_LUT = {
                      'correctedmxaAclr1Max': 'ACLR1 Max dBc',
                      'pmPaOutDBm': 'PA Output Power dBm',
                      }

    def process_data(self, df, sweep, repeat, result, derate, x_axis='time'):
        '''
        Return a dict of figures based on df and filtering conditions
        
        Parameters
        ------------------------------------------------------------------------
        sweep - list of cols that are input settings
              - ex. backoff, waveform, fw
        
        repeat - list of cols used as pseudo 'x-axis'
               - ex. time, repeat_without_reset
               - note: repeat_with_reset is a special case parameter
               
        result - list of all cols to use as 'y-axis'
               - ex. ACLR1/2 or Output Power
        '''
        
        title = {
                 'correctedmxaAclr1MaxVar': 'ACLR Variance after Convergence',
                 'correctedmxaAclr1MaxTime': 'ACLR Convergence Rate over Time',
                 'pmPaOutDBmVar': 'PA Output Power Variance after Convergence',
                 'pmPaOutDBmTime': 'PA Output Power over Time',
                 }
        
        # Filter Data for Violin plots
        keep_limit = self.CONST['to_keep'] * df['r_RepeatNumWithoutReset'].max()
        vstack_df = df[df['r_RepeatNumWithoutReset'] > keep_limit]
        vstack_df = vstack_df.set_index(sweep + repeat)
        vstack_df = vstack_df.unstack(repeat).transpose()
        
        # Filter Data for Time-Domain Plots
        if x_axis == 'time':
            self._convert_to_time(df)
        tstack_df = df.set_index(sweep + repeat)
        tstack_df = tstack_df.unstack('r_RepeatNumWithReset')
        
        # Generate all plots
        figs = collections.OrderedDict()
        for item in result:
            if item == 'TestTimeRepeatNoReset_s': continue # this a hack for now
            figs[item + 'Var'] = self.oVarPlt.plot(vstack_df, item)
        
        for item in derate:
            figs[item + 'DR'] = self.oParamPlt.plot(tstack_df,item, x_axis)
            
        return figs
    
    def _convert_to_time(self, df):
            
        tmp = df['TestTimeRepeatNoReset_s'].copy()
        tmp.index += 1
        tmp =  df['TestTimeRepeatNoReset_s'] - tmp
        step_size = tmp[(tmp > 0) & (tmp < 3)].mean().round(1)

        df['r_RepeatNumWithoutReset'] = (step_size *  
                                         df['r_RepeatNumWithoutReset']).round(1)
        
    def variance_plot(self, df, item):
        
        # Pass in entire df since need col name either eay
        df = df.xs(item)

        # Set up plot
        fig = sns.plt.figure()
        #fig.set_size_inches(10,10)
        
        # Plot Data
        sns.violinplot(df, bw=.15, cut=0)  # TODO: fix
        sns.boxplot(df, linewidth=2) 
        #sns.plt.plot(base_line * np.ones(len(df)+2), 'red', lw=2)
        
        # Plot Settings
        sns.plt.yticks(fontsize=12)
        sns.plt.ylabel(self.y_LUT[item], fontsize=16)
        #sns.plt.tight_layout()
        
        x_labels = range(len(df.columns))
        ax = sns.plt.subplot()
        ax.set_xticklabels(x_labels)
        
        # Plot info webpage
        title = item + ' Variance after Convergence'
        text = pd.DataFrame(
                            df.columns.tolist(), 
                            columns=df.columns.names, index=x_labels
                            ).transpose()
        
        info = {'data': fig, 'title': title, 'text': text}

        return info
    
    def time_plot(self, s, item, x_axis):
        
        # Pass in entire df since need col name either eay

        # Set up plot
        #fig = sns.plt.figure()
        #fig.set_size_inches(10,10)
        
        tmp = s[item].mean(axis=1).unstack('r_RepeatNumWithoutReset').transpose()
        tmp.plot(lw=2)
        
        # Plot Dressing
        if x_axis == 'time':
            sns.plt.xlabel('Time in Seconds', fontsize=16)
        sns.plt.yticks(fontsize=12)
        sns.plt.ylabel(self.y_LUT[item], fontsize=16)
        
        title = item + ' Variation during adaptation'
        info = {'data': sns.plt.gcf(), 'title': title, 'text': 'HELLO'}

        return info
        
class Plots( object ):
    
    def __init__(self):
        self._load_constants()
        self._properties()
        
    def _load_constants(self):
        
        self.CONST = {
                      'to_keep': .70,
                      'correctedmxaAclr1Max': -47,      # Spec for ACLR
                      'LINEWIDTH': 2,
                      'BANDWITH': 0,
                      'CUT': 0.25,
                      }

        self.y_LUT = {
                      'correctedmxaAclr1Max': 'ACLR1 Max dBc',
                      'pmPaOutDBm': 'PA Output Power dBm',
                      'currentTemp_degrees': 'Case Temp degC',
                      'Temp': 'IC Temp degC',
                      }
    
    def _dressing(self, item=''):
        
        TICK_SIZE = 12
        FONT_SIZE = 16
        
        if item in self.y_LUT:
            ylabel = self.y_LUT[item]
        else:
            ylabel = item
            
        # TODO: need to make current figure be the focus somehow...
        #sns.plt.title(self.TITLE(item))
        sns.plt.xlabel(self.X_LABEL, fontsize=FONT_SIZE)
        sns.plt.ylabel(ylabel, fontsize=FONT_SIZE)
        sns.plt.yticks(fontsize=TICK_SIZE)
    
        #sns.plt.tight_layout()

    def _info(self, fig=False, item='', text=''):
        
        if not fig:
            fig = sns.plt.gcf()
        
        return {'data': fig, 'title': self.TITLE(PARAM=item), 'text': text}
    
    def _baseline(self, item):
        pass
    
    def plot(self):
        
        print "should not call this function directly..."
        
    def _get_text(self, df, xlabel):
        
        text = pd.DataFrame(
                            df.columns.tolist(), 
                            columns=df.columns.names, 
                            index=xlabel
                            ).transpose()
        return text
    
class Parameter( Plots ):
    
    def _properties(self):
        
        self.TITLE = '{PARAM} convergence over time'.format
        self.X_LABEL = 'Time (seconds)'
        
    def plot(self, df, item, x_type='time'):
        
        s = df[item].mean(axis=1).unstack('r_RepeatNumWithoutReset').transpose()
        s.plot(lw=2, colormap='Paired_r')
 
        xlabel = self._remap_legend(s)
        text = self._get_text(s, xlabel)
        self._dressing(item)

        return self._info(sns.plt.gcf(), item, text)
    
    def _remap_legend(self, s):
        
        #num_of_plots = s.columns.labels[0].size
        #num_of_plots = s.columns.labels[0].size
        
        xlabels = range(len(s.columns))
        sns.plt.legend(xlabels, loc='upper right')
        
        return xlabels
    
    
class Variance( Plots ):
    
    def _properties(self):
        
        self.TITLE = '{PARAM} Variance after Convergence'.format
        self.X_LABEL = 'Index'
        
    def plot(self, df, item):
        
        df = df.xs(item)
        
        fig = sns.plt.figure()
        
        sns.violinplot(df, bw=.25, cut=0)  # TODO: fix
        sns.boxplot(df, linewidth=2) 
        #sns.plt.plot(base_line * np.ones(len(df)+2), 'red', lw=2
        
        xlabel = self._remap_xaxis(df)
        text = self._get_text(df, xlabel)
        self._dressing(item)
        
        return self._info(fig, item, text)
        
    def _remap_xaxis(self, df):
        
        xlabels = range(len(df.columns))
        ax = sns.plt.subplot()
        ax.set_xticklabels(xlabels)
        
        return xlabels
        
class Time( Plots ):
    
    ''' 
    Class no longer needed!!!!
    '''
    def _properties(self):
        pass
    
    def plot(self, s, item, x_type):
        
        s[item].mean(axis=1).unstack('r_RepeatNumWithoutReset').transpose().plot(lw=2)
        
        # Plot Dressing
        if x_type == 'time':
            xlabel = 'Time in Seconds'
        else:
            xlabel = 'Repeat counter between resets'
            
        ylabel = self.y_LUT[item]
        self._dressing(xlabel=xlabel, ylabel=ylabel)
        
        title = item + ' Variation during adaptation'
        return {'data': sns.plt.gcf(), 'title': title, 'text': ''}
        
class BackOff( Plots ):
    
    def plot(self):
        pass