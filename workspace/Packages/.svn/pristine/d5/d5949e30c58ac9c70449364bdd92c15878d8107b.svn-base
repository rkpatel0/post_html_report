'''
Created on Oct 31, 2014

@author: Rishi.Patel
'''

import regression.analysis as pp
import webgen.report as web
import collections
import pandas as pd


WAVEFORM_PAR_LUT = {
                    'LTE05M1-1#7.51.mat': 7.51,
                    'LTE10M1-1#7.54.mat': 7.54,
                    'LTE20M1-1#7.43.mat': 7.43,
                    'LTE20M1-1D68#7.62': 7.62,
                    }


class Test(object):
    '''
    Top level object to handle slides for webpages and does data filtering
    '''

    def __init__(self, config={}, chan='A'):
        '''
        Constructor
        '''

        self.CHAN = chan
        self._load_defaults()
        self._set_test_defaults()
        self._load_custom(config)

        self.oPlot = pp.Process(
                                self.param['sweep'], 
                                self.param['repeat'],
                                self.param['xaxis'],
                                )

    def _load_defaults(self):

        self.param = {}

        self.param['filter'] = [
                                's_Waveform',
                                's_Backoff_dB'
                                ]

        self.param['variance'] = [
                                'correctedmxaAclr1Max',
#                                'TestTimeRepeatNoReset_s'
                                ]

        self.param['repeat'] = [
                                'r_RepeatNumWithReset',
#                                'r_RepeatNumWithoutReset'
                                ]

        self.param['sweep'] = [
                               's_Vdd_port_1_Vs',
                               's_RfinTarget_dBmPeak',
                               's_RffbTarget_dBmPeak',
                                's_Backoff_dB'
                               ]

        self.param['derate'] = [
                                'correctedmxaAclr1Max',
                                'pmPaOutDBm',
                                'PmuRfin{CH}',
                                'pmRffinInDBm',
                                'PmuRffb{CH}',
                                'pmRffbInDBm',
                                'PmuRfGain{CH}',
                                'pmLoopGainInDBm',
                                'PdetDcDac{CH}',
                                'EdetDcDac{CH}',
                                'PdetIndex{CH}',
                                'PdetIndex{CH}Fine',
                                'EdetIndex{CH}Fine',
                                'CorrIDac{CH}',
                                'CorrQDac{CH}',
                                'Temp',
                                'currentTemp_degrees',
                                'mxgPower',
                                'rfOutAttn',
                                'rfAttnFb',
                                'Error0',
                                'Warning0',
                                ]
        self.param['delta'] = []
        self.param['xaxis'] = 'time'

    def _modify_parameters_by_test(self):
        pass

    def _load_custom(self, config):

        # overwrite default values in param if items are passed in
        for key in self.param.keys():
            if key in config:
                self.param[key] = config[key]

        # Set parameters inside string based on channel
        for i in range(len(self.param['derate'])):
            self.param['derate'][i] = self.param['derate'][i].format(CH=self.CHAN)

        self.param['repeat'] += [self.param['xaxis']]
        self._modify_parameters_by_test()

        # Combine all the parameters to be used
        self.param['all'] = self.param['variance'] + self.param['sweep'] + \
                            self.param['repeat'] + self.param['filter'] + \
                            self.param['derate'] + self.param['delta']

        # Remove duplicates from list by casting as a set
        self.param['all'] = list(set(self.param['all']))

    def data_to_report(self, data, database=False):
        '''
        data: dataframe containing all regression data for report
              columns much match TEST (CHAR/SOAK/PMU) or CUSTOM

        output: will be the report saved to the desired path
        '''

        if data.empty: raise KeyError('Dataframe Empty!')

        # Test Permutations
        permutations = data[self.param['filter']].drop_duplicates()
        permutations.sort(self.param['filter'], inplace=True)
        print 'Total Permutations:\n', permutations

        # Test Pages and Process Data
        pages = []
        self._overview_to_page(pages, data, permutations, database)
        self._summary_to_page(pages, data)
        self._process_data_to_page(pages, data, permutations)

        if self.TESTTYPE == 'PMUTEST':
            summary_report = self.oPlot.summary_df[self.oPlot.summary_df['Status'] != 'PASS'].dropna()
            summary_report = summary_report[summary_report['Port'] != 'PmuRfauxA']
            summary_report = summary_report[summary_report['Port'] != 'PmuRfauxB']
            pages[2].content[0]['data'] = summary_report

        return pages

    def _overview_to_page(self, pages, data, permutations, database):

        test_time_mins = data[data['r_RepeatNumWithoutReset'] == \
                              data['r_RepeatNumWithoutReset'].max()]['TestTimeRepeatNoReset_s'].sum()
        test_time_mins /= 60 * 60 * .8  # 0.80 is scale for SMOOTH MODE and TEMP

        info = data.iloc[0]
        INTRO  = 'Time to run test: <b>{TIME} in hours</b>.<br>'.format(TIME=round(test_time_mins, 2))
        INTRO += 'Data was taken in <b>{MODE} Mode</b>.<br>'.format(MODE=info['Mode'+self.CHAN])
        INTRO += 'EVB Type: <b>{EVB}</b>.<br>'.format(EVB=str(info['EVBTYPE']))
        INTRO += 'EVB Number: <b>{NUM}</b>.<br>'.format(NUM=str(info['EVBNUM']))
        INTRO += 'Process Type: <b>{PROC}</b>.<br>'.format(PROC=str(info['PROCESS']))
        INTRO += 'Firmware Revision Num: <b>{FW}</b>.<br>'.format(FW=str(info['FwVersion']))
        INTRO += 'Firmware Name: <b>{FW}</b>.<br>'.format(FW=str(info['s_Fw']))
        INTRO += 'PA Name: <b>{PA}</b>.<br>'.format(PA=str(info['paName']))
        INTRO += 'PA kSat Peak: <b>{SAT} dBm</b>.<br>'.format(SAT=str(info['paKsat_dBmPeak']))

        PERM_BODY = (
        'List of settings that have been sweeped inside data file(s)'
                     )
        FILE_BODY = (
        'Files were taken from the following database {DB}. <br> List of files '
        'used to generate data are below.'
                     ).format(DB=database['path'])
        files_df = pd.DataFrame(database['files'], columns=['File Name'])

        d = {
             0: {'title': 'Overview', 'text': INTRO},
             1: {'data': files_df, 'title': 'Firmware Files', 'text': FILE_BODY},
             2: {'data': permutations, 'title': 'Permutations', 'text': PERM_BODY},
             }

        pages.append(web.Page('General', TYPE='TOC'))
        pages.append(web.Page('_Overview', d))

    def _summary_to_page(self, pages, data):

        LUT = collections.OrderedDict()
        LUT['Min I CORR DAC'] = 'CorrIDac{CH}'.format(CH=self.CHAN)
        LUT['Min Q CORR DAC'] = 'CorrQDac{CH}'.format(CH=self.CHAN)
        LUT['Error'] = 'Error0'
        LUT['Warning'] = 'Warning0'

        columns = data['s_Waveform'].unique().tolist()
        df = pd.DataFrame(columns=columns, index=LUT.keys())

        for wf in columns:
            d = data[data['s_Waveform'] == wf]
            for key, value in LUT.items():
                if key == 'Warning' or key == 'Error':
                    df.loc[key, wf] = d[value].max()
                else:
                    df.loc[key, wf] = d[value].min()

        info = {'title': 'Test Plan Result', 'data': df}
        pages.append(web.Page('_Summary', {1: info})) 

    def _process_data_to_page(self, pages, data, permutations):   

        # Setup parameters for post processing data       
        wf_list = permutations['s_Waveform'].unique().tolist()

        # Filter and collect data by permutation
        for idx in permutations.index:

            print 'Permutation ', len(pages) - 2, ' of ', permutations.index.size
            print permutations.ix[idx]

            # Copy and Filter Data for Permutation
            df = data[self.param['all']].dropna()
            if df.empty: print 'CURRENT ITERATION IS EMPTY'; continue
            for col in permutations.columns:
                df = df[df[col] == permutations.loc[idx, col]]

            # Create TOC by Waveform
            if data.loc[idx, 's_Waveform'] in wf_list:
                wf_list.remove(data.loc[idx, 's_Waveform'])
                pages.append(web.Page('WF_' + data.loc[idx, 's_Waveform'], TYPE='TOC'))

            # Process Data and Format for WebReport
            name = self._get_page_name(len(pages), permutations.ix[idx])
            fig_info = self._convert_data_to_figs(df, str(len(pages)))
            pages.append(web.Page(name, fig_info))

            # uncomment for quick debug
            #if len(pages) == 6: break

    def _convert_data_to_figs(self, df, ext=''):

        waveforms = df.s_Waveform.unique()

        if len(waveforms) == 1 and waveforms[0] in WAVEFORM_PAR_LUT:
            offset = WAVEFORM_PAR_LUT[df['s_Waveform'].unique()[0]]    
        else:
            offset = 0

        # Process and Plot data by type
        figs_var = self.oPlot.process_variance(df, self.param['variance'])
        figs_time = self.oPlot.process_in_time(df, self.param['derate'])
        figs_delta = self.oPlot.process_delta(df, self.param['delta'], xaxis_os=offset)

        # Combine all fig data
        figs_raw = collections.OrderedDict(
                                           figs_var.items() + 
                                           figs_time.items() + 
                                           figs_delta.items()
                                           )

        # Add a Title and Extension
        figs = collections.OrderedDict()
        for key, value in figs_raw.items():
            value['title'] = ext + '. ' + value['title']
            figs[key + ext] = value

        return figs

    def _get_page_name(self, i, condtion):

        page_name = '_' + str(i) + '.'

        LUT = {
               's_Backoff_dB': 'BO_{X}',
               's_Vdd_port_1_Vs': 'VDD_{X}',
               's_RfinTarget_dBmPeak': 'IN_{X}',
               's_RffbTarget_dBmPeak': 'FB_{X}',
               's_Fw': 'FW_{X}',
               's_Temperature_degC': 'T_{X}',
               's_Freq_MHz': 'F_{X}MHz',
               's_MxgPower_dBm': 'P_{X}dBm',
               }

        for item in self.param['filter']:
            if item == 's_Waveform':
                pass
            else:
                page_name += '_' + LUT[item].format(X=str(condtion[item]))

        return page_name


class Pmu(Test):

    def _set_test_defaults(self):

        self.TESTTYPE = 'PMU'

        # Modify defaults based on test
        self.param['variance'] = []
        self.param['derate'] = []
        self.param['delta'] = [
                               'PmuRffbA', 'PmuRffbB',
                               'PmuRfinA', 'PmuRfinB',
                               'PmuRfauxA', 'PmuRfauxB'
                               ]
        self.param['filter'] = ['s_Waveform']
        self.param['sweep'] = ['s_Vdd_port_1_Vs', 's_Temperature_degC']
        self.param['repeat'] = ['r_RepeatNumWithoutReset']
        self.param['xaxis'] = 's_MxgPower_dBm'

    def _modify_parameters_by_test(self):

        # Crappy way of adding additional parameters to DELTA LUT
        DELTA_LUT = {
                     's_Freq_MHz': 's_MxgPower_dBm',
                     's_MxgPower_dBm': 's_Freq_MHz',
                     }

        self.param['filter'] += [DELTA_LUT[self.param['xaxis']]] 
        self.param['sweep'] += [DELTA_LUT[self.param['xaxis']]] 


class Soak(Test):

    def _set_test_defaults(self):

        self.TESTTYPE = 'SOAK'
        self.param['filter'] += ['s_RfinTarget_dBmPeak', 's_RffbTarget_dBmPeak']


class Char(Test):

    def _set_test_defaults(self):

        self.TESTTYPE = 'CHAR'
        self.param['sweep'] += ['s_Temperature_degC']


