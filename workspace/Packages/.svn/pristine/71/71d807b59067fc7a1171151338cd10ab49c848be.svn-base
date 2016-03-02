'''
Created on Oct 30, 2014

@author: Rishi.Patel
'''

import seaborn as sns
import collections
import pandas as pd
#import numpy as np

YLIMITS_TABLE = {
#                'correctedmxaAclr1Max': [-47],
                'Delta PmuRffbA':  [0.5, -0.5],
                'Delta PmuRffbB':  [0.5, -0.5],
                'Delta PmuRfinA':  [0.6, -0.6],
                'Delta PmuRfinB':  [0.6, -0.6],
                'Delta PmuRfauxA': [0.6, -0.6],
                'Delta PmuRfauxB': [0.6, -0.6],
                }

PK_POWER_LUT = {
                'Delta PmuRffbA':  [ -2, -32],
                'Delta PmuRffbB':  [ -2, -32],
                'Delta PmuRfinA':  [ +2, -28],   # ~3dB attn from SMA to Pin
                'Delta PmuRfinB':  [ +2, -28],   # ~3dB attn from SMA to Pin 
                'Delta PmuRfauxA': [-10, -40],
                'Delta PmuRfauxB': [-10, -40],
                }

FREQ_LUT = {
            'Delta PmuRffbA':  [700, 2700],
            'Delta PmuRffbB':  [700, 2700],
            'Delta PmuRfinA':  [700, 2700],
            'Delta PmuRfinB':  [700, 2700],
            'Delta PmuRfauxA': [700, 2700],
            'Delta PmuRfauxB': [700, 2700],
            }

XLIMITS_TABLE = {
                 's_MxgPower_dBm': PK_POWER_LUT,
                 's_Freq_MHz': FREQ_LUT,
                 }

MXG_TO_PORT_LOSS = pd.DataFrame(
                                {
                                 'Delta PmuRffbA':  [14.2, 16.0, 16.0, 16.8],
                                 'Delta PmuRffbB':  [14.2, 15.5, 15.5, 16.3],
                                 'Delta PmuRfinA':  [ 7.5,  9.5,  9.5, 11.9],
                                 'Delta PmuRfinB':  [ 7.3,  8.9,  8.9, 11.5],
                                 'Delta PmuRfauxA': [24.0, 26.0, 26.0, 26.3],
                                 'Delta PmuRfauxB': [24.0, 26.0, 26.0, 26.5],
                                 },
                                index=              [ 700, 1000, 2140, 2700],
                                )


class Process(object):
    '''
    Use to post process and analyze data
    Idea is that this should be flexible enough to use with any data set
    '''


    def __init__(self, sweep, repeat, xaxis):
        '''
        Parameters
        ------------------------------------------------------------------------
        sweep - list of cols that are input settings
              - ex. backoff, waveform, fw
        
        repeat - list of cols used as pseudo 'x-axis'
               - ex. time, repeat_without_reset
               - note: repeat_with_reset is a special case parameter
               
        xaxis  - For plots vs a parameter such as time or MXG power
        ------------------------------------------------------------------------
        '''
        
        self.sweep = sweep
        self.repeat = repeat
        self.xaxis = xaxis
        
        self._load_default()
        self.oVarPlt = Variance()
        self.oParamPlt = Parameter(xaxis)

        self.RECORD_SUMMARY = True

    def _load_default(self):
        
        self.CONST = {
                      'to_keep': .70,
                      }

        self.y_LUT = {
                      'correctedmxaAclr1Max': 'ACLR1 Max dBc',
                      'pmPaOutDBm': 'PA Output Power dBm',
                      }

        self.SUM_COL = ['Waveform', 'Freq (MHz)', 'Port',
                        'Max Spec (dBm)', 'Max Delta (dBm)', 'Power of Max Delta pKdBm',
                        'Min Spec (dBm)', 'Min Delta (dBm)', 'Power of Min Delta pKdBm',
                        'Status']
        
        self.summary_df = pd.DataFrame(index=range(100),
                                       columns=self.SUM_COL
                                       )

    def process_delta(self, df, delta, xaxis_os=0, baseline='s_Temperature_degC', CAL=30):
        '''
        df - pandas dataframe containing data to plot
        delta - is a list of parameters in df columns that are to be plotted
              - against xaxis which is passed in as an input parameter
        xaxis_os - constant offset for all parameters
                 - i.e. waveform PAR
        baseline - name of parameter to use to base;ine other parameters
        CAL - value to use for baseline > value must exist inside baseline col 
        
        NOTE:
        this function (and class) really needs to be cleaned up a bit
        '''
        
        if not delta: return {}

        # Get a list of the temp sweeps
        temps = df[baseline].unique().tolist()
        df[self.xaxis] += xaxis_os
        
        # Make df accessable by temp
        df_temp = df.set_index(baseline)

        new_series = pd.DataFrame()
        new_df = pd.DataFrame()
        for temp in temps:
            # Subtract CAL datapoint over each condition from all other temp points
            tmp_df = df_temp.loc[temp, delta].reset_index() - \
                     df_temp.loc[CAL,  delta].reset_index()
            new_series = new_series.append(tmp_df)
            new_df = new_df.append(df_temp.ix[temp].reset_index())
 
        # Add New Parameters        
        for item in delta:
            new_df['Delta ' + item] = new_series[item]
        
        # Get info for summary
        if self.RECORD_SUMMARY:
            self._update_summary(new_df[new_df[baseline] != CAL], delta)
            
        # Stack all but the delta (PMU) columns - for plotting convience
        stack_df = new_df.set_index(self.sweep + self.repeat)
        stack_df = stack_df.unstack('r_RepeatNumWithoutReset')

        figs = collections.OrderedDict()
        for item in delta:
            figs[item + 'DL'] = self.oParamPlt.plot(stack_df,'Delta ' + item)
            #figs[item + 'RW'] = self.oParamPlt.plot(stack_df, item)
        
        return figs

    def _update_xaxis(self, data, item):
        
        for freq, loss in MXG_TO_PORT_LOSS[item].iteritems():
            data[self.xaxis][data['s_Freq_MHz'] == freq] -= loss

    def _update_summary(self, df, delta):
        
        # Statics
        wf = df['s_Waveform'].unique()[0]
        freq = df['s_Freq_MHz'].unique()[0]
        
        html_str = '<font color="{COL}"><b>{VAL}</b></font>'.format
        for item_short in delta:
            item = 'Delta ' + item_short
            
            valid = df.copy()
            self._update_xaxis(valid, item)
            
            # keep on the valid range by power level
            pmu = valid[valid[self.xaxis] < max(XLIMITS_TABLE[self.xaxis][item])]
            pmu = pmu[item][pmu[self.xaxis] > min(XLIMITS_TABLE[self.xaxis][item]) + 10]
        
            if pmu.max() >  max(YLIMITS_TABLE[item]) and pmu.min() <  min(YLIMITS_TABLE[item]):
                STATUS = 'FAIL BOTH'
                max_col = 'firebrick'
                min_col = 'firebrick'
            elif pmu.max() >  max(YLIMITS_TABLE[item]):
                STATUS = 'FAIL HIGH'
                max_col = 'darkorchid'
                min_col = 'green'
            elif pmu.min() <  min(YLIMITS_TABLE[item]):
                STATUS = 'FAIL LOW'
                max_col = 'green'
                min_col = 'darkorchid'
            else:
                STATUS = 'PASS'
                max_col = 'green'
                min_col = 'green'
            index = len(self.summary_df.dropna())
            self.summary_df.ix[index] = [
                 wf, freq, item_short, 
                 max(YLIMITS_TABLE[item]), html_str(COL=max_col, VAL=pmu.max()), 
                 valid['s_MxgPower_dBm'][pmu.idxmax()].iloc[0],
                 min(YLIMITS_TABLE[item]), html_str(COL=min_col, VAL=pmu.min()),
                 valid['s_MxgPower_dBm'][pmu.idxmin()].iloc[0],
                 STATUS]
            
    def process_variance(self, df, variance):
        '''
        Return a dict of figures based on df and filtering conditions
        '''
        
        if not variance: return {}

        # Filter Data for Violin plots
        keep_limit = self.CONST['to_keep'] * df[self.xaxis].max()
        vstack_df = df[df[self.xaxis] > keep_limit]
        vstack_df = vstack_df.set_index(self.sweep + self.repeat)
        vstack_df = vstack_df.unstack(self.repeat).transpose()
        
        # Generate all plots
        figs = collections.OrderedDict()
        for item in variance:
            if item == 'TestTimeRepeatNoReset_s': continue # this a hack for now
            figs[item + 'Var'] = self.oVarPlt.plot(vstack_df, item)
        
        return figs
        
    def process_in_time(self, df, derate):

        '''
        Return a dict of figures based on df and filtering conditions
        '''
   
        if not derate: return {}

        tstack_df = df.set_index(self.sweep + self.repeat)
        tstack_df = tstack_df.unstack('r_RepeatNumWithReset')
        
        figs = collections.OrderedDict()
        for item in derate:
            figs[item + 'DR'] = self.oParamPlt.plot(tstack_df,item)
            
        return figs
                
class Plots( object ):
    
    def __init__(self, xaxis=''):
        self._load_constants()
        self._properties(xaxis)
        
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
        
        sns.plt.xlabel(self.X_LABEL, fontsize=FONT_SIZE)
        sns.plt.ylabel(ylabel, fontsize=FONT_SIZE)
        sns.plt.yticks(fontsize=TICK_SIZE)

        if item not in YLIMITS_TABLE: return

        if item in YLIMITS_TABLE:
            min_limit = min(YLIMITS_TABLE[item]) * 2
            max_limit = max(YLIMITS_TABLE[item]) * 2
            sns.plt.ylim([min_limit, max_limit])
        
        if item in XLIMITS_TABLE[self.xaxis]:
            min_limit = min(XLIMITS_TABLE[self.xaxis][item]) - 5
            max_limit = max(XLIMITS_TABLE[self.xaxis][item]) + 5
            sns.plt.xlim([min_limit, max_limit])
        
        for spec in YLIMITS_TABLE[item]:
            sns.plt.plot(sns.plt.xlim(), [spec, spec],'r--')

        for spec in XLIMITS_TABLE[self.xaxis][item]:
            sns.plt.plot([spec, spec], sns.plt.ylim(),'b--')
            #pass
            
    
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
    
    def _properties(self, xaxis):
        
        X_LUT = {
                 'time': 'Time in Seconds',
                 's_MxgPower_dBm': 'Peak Power at SMA in dBm',
                 's_Freq_MHz': 'Frequency in MHz',
                 }
        
        self.xaxis = xaxis
        self.TITLE = '{PARAM} performance over ' + xaxis
        self.TITLE = self.TITLE.format
        self.X_LABEL = X_LUT.setdefault(xaxis,xaxis)
    
    def plot(self, df, item):
        
        
        if self.xaxis == 's_MxgPower_dBm' and item in MXG_TO_PORT_LOSS.columns:
            freq = df.index[0][df.index.names.index('s_Freq_MHz')]
            loss = MXG_TO_PORT_LOSS.loc[freq,item]
        elif self.xaxis == 's_Freq_MHz':
            # How to modify this????
            loss = 0
        else:
            loss = 0
            
        k = df[item].unstack(self.xaxis).transpose()
        s = df[item].mean(axis=1).unstack(self.xaxis).transpose()

        k.index = k.index.droplevel(0) + (loss * -1)
        s.index -= loss
        
        # Order matters below
        k.plot(lw=0.5, colormap='Paired_r', style='*' )
        s.plot(ax=sns.plt.gca(), lw=2, colormap='Paired_r')
        sns.plt.plot()
        
        xlabel = self._remap_legend(s)
        text = self._get_text(s, xlabel)
        self._dressing(item)

        return self._info(sns.plt.gcf(), item, text)
    
    def _remap_legend(self, s):
        
        xlabels = range(len(s.columns))
        sns.plt.legend(xlabels, loc='upper right')
        
        return xlabels
    
    
class Variance( Plots ):
    
    def _properties(self, xaxis):
        
        #xaxis does not do anything
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
        
class BackOff( Plots ):
    
    def plot(self):
        pass