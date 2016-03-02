'''
Created on Oct 7, 2014

@author: Rishi.Patel
'''

import seaborn as sns
import numpy as np

class vcoTests(object):
    


    def plotVcoVsLoFreq(self):
        
        start = 3600
        stop = 4600
        center = 2*2140
        
        loFreqRange = np.arange(500, 8400).tolist()
        idxStart = loFreqRange.index(start)
        idxStop = loFreqRange.index(stop)
        idxCenter = loFreqRange.index(center)
        
        vcoFreq = []
        for loFreq in loFreqRange:
            vcoFreq.append(self.getVcoFreq( loFreq))
            
        sns.plt.plot(loFreqRange, vcoFreq)
        sns.plt.plot(loFreqRange[idxStart:idxStop], vcoFreq[idxStart:idxStop], linewidth=2)
        sns.plt.plot(loFreqRange[idxCenter], vcoFreq[idxCenter], 'o', linewidth=20)
        sns.plt.xlabel('LO Frequency MHz')
        sns.plt.ylabel('VCO Frequency MHz')
        sns.plt.title('LO to VCO Frequency Mapping')
        sns.plt.show()
        
    def getVcoFreq(self, loFreq):
        self.BAND = {
                     'ULOWBANDMAX'  : 520,
                     'LOWBANDMAX'  : 1040,
                     'MIDBAND1MAX' : 2048,
                     'MIDBAND2MAX' : 3600,
                     'HIGHBANDMAX' : 5400,
                     'VHIGHBANDMAX': 7000,
                     'UHIGHBANDMAX': 8400,
                     }

        vcoFreq = 0;
        
        if loFreq <= self.BAND['ULOWBANDMAX']:
            vcoFreq = loFreq * 16
        elif loFreq <= self.BAND['LOWBANDMAX']:
            vcoFreq = loFreq * 8
        elif loFreq <= self.BAND['MIDBAND1MAX']:
            vcoFreq = loFreq * 4
        elif loFreq <= self.BAND['MIDBAND2MAX']:
            vcoFreq = loFreq * 2
        elif loFreq <= self.BAND['HIGHBANDMAX']:
            vcoFreq = (loFreq * 4) / 3
        elif loFreq <= self.BAND['VHIGHBANDMAX']:
            vcoFreq = (loFreq * 4) / 5
        elif loFreq <= self.BAND['UHIGHBANDMAX']:
            vcoFreq = (loFreq * 2) / 3
            
        return vcoFreq

if __name__ == '__main__':
    vcoTests().plotVcoVsLoFreq()