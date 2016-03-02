'''
Created on Oct 31, 2014

@author: Rishi.Patel
'''

import regression.analysis as pp
import webgen.report as web
import collections
import pandas as pd

class Generate(object):
    '''
    Top level object to handle slides for webpages and does data filtering
    '''

    def __init__(self, config={}, chan='A', test='CHAR'):
        '''
        Constructor
        '''
        
        self.CHAN = chan
        self._load_default(config, test)
        self.oPlot = pp.Process()

    def _load_default(self, config, test):
        
        self.param = {}
        
        self.param['filter'] = [
                                's_Waveform',
                                's_Backoff_dB'
                                ]

        self.param['result'] = [
                                'correctedmxaAclr1Max',
                                'TestTimeRepeatNoReset_s'
                                ]
        
        self.param['repeat'] = [
                                'r_RepeatNumWithReset',
                                'r_RepeatNumWithoutReset'
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
                                'Error0',
                                'Warning0',
                                ]

        # Modify defaults based on test
        if test == 'CHAR':
            self.param['sweep'] += ['s_Temperature_degC']
        elif test == 'SOAK':
            self.param['filter'] += ['s_RfinTarget_dBmPeak', 's_RffbTarget_dBmPeak']
        else:
            print 'INVALID TEST TYPE'

        # overwrite default values in param if items are passed in
        for key in self.param.keys():
            if key in config:
                self.param[key] = config[key]

        # Set parameters inside string based on channel
        for i in range(len(self.param['derate'])):
            self.param['derate'][i] = self.param['derate'][i].format(CH=self.CHAN)
        
        # Combine all the parameters to be used
        self.param['all'] = self.param['result'] + self.param['sweep']   + \
                            self.param['repeat'] + self.param['filter'] + \
                            self.param['derate']
                            
        # Remove duplicates from list by casting as a set
        self.param['all'] = list(set(self.param['all']))

    def create_pages(self, data, database=False):
 
        pages = []
        
        permutations = data[self.param['filter']].drop_duplicates()
        permutations.sort(self.param['filter'], inplace=True)
        
        self._overview_to_page(pages, data, permutations, database)
        self._summary_to_page(pages, data)
        self.process_data_to_page(pages, data, permutations)
    
        return pages
    
    def _overview_to_page(self, pages, data, permutations, database):
        
        test_time_mins = data[data['r_RepeatNumWithoutReset'] == data['r_RepeatNumWithoutReset'].max()]['TestTimeRepeatNoReset_s'].sum()
        test_time_mins /= 60*60*.8  # 0.80 is scale for SMOOTH MODE and TEMP
        
        info = data.loc[0]
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
    
    def process_data_to_page(self, pages, data, permutations):   

        # Setup parameters for post processing data       
        wf_list = permutations['s_Waveform'].unique().tolist()

        # Filter and collect data by permutation
        print 'Total Permutations:\n', permutations
        for idx in permutations.index:
            
            print 'Permutation ', len(pages)-2, ' of ', permutations.index.size
            print permutations.ix[idx]
            
            # Copy and Filter Data for Permutation
            df = data[self.param['all']].dropna()
            for col in permutations.columns:
                df = df[df[col] == permutations.loc[idx, col]]
            
            # Create TOC by Waveform
            if data.loc[idx, 's_Waveform'] in wf_list:
                wf_list.remove( data.loc[idx, 's_Waveform'] )
                pages.append(web.Page('WF_' + data.loc[idx, 's_Waveform'], TYPE='TOC'))
                
            page_name = self._get_page_name(len(pages), permutations.ix[idx])
            oData = Slides(self.param, self.oPlot)
            pages.append(oData.process(df, page_name, len(pages))) 

            # use this for debug - to make processing shorter
            #if len(pages) == 4: break
            
    def _get_page_name(self, i, condtion):
            
        page_name = '_' + str(i) + '.'
            
        LUT = {
               's_Backoff_dB': 'BO_{X}',
               's_Vdd_port_1_Vs': 'VDD_{X}',
               's_RfinTarget_dBmPeak': 'IN_{X}',
               's_RffbTarget_dBmPeak': 'FB_{X}',
               's_Fw': 'FW_{X}',
               's_Temperature_degC': 'T_{X}',
               }
            
        for item in self.param['filter']:
            if item == 's_Waveform':
                pass
            else:
                page_name += '_' + LUT[item].format(X=str(condtion[item]))
        
        return page_name

               
class Slides(object):
    '''
    General Template transferring data into a webpage
    '''
    
    def __init__(self, config, oPlot):
        
        self.param = config
        self.oPlot = oPlot
        
    def process(self, df, page_name, ext=''):

        figs_info = self.oPlot.process_data(df,
                                            self.param['sweep'], 
                                            self.param['repeat'],
                                            self.param['result'],
                                            self.param['derate'],
                                            )
        page = collections.OrderedDict()
        if type(ext) != str():
            ext = str(ext)
        for key, value in figs_info.items():
            value['title'] += ' ' + ext
            page[key + ext] = value
            
        return web.Page(page_name, page)
    