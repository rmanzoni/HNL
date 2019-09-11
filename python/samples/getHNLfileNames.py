'''
wget http://tomc.web.cern.ch/tomc/availableDisplacedTrileptonSamples.txt
wget http://tomc.web.cern.ch/tomc/privateHeavyNeutrinoSamples.txt

13/9/2018
wget http://tomc.web.cern.ch/tomc/availableHeavyNeutrinoSamples.txt
wget http://tomc.web.cern.ch/tomc/heavyNeutrinoFileList.txt

29/8/2019
wget http://tomc.web.cern.ch/tomc/heavyNeutrino/availableHeavyNeutrinoSamples.txt
wget http://tomc.web.cern.ch/tomc/heavyNeutrino/heavyNeutrinoFileList.txt
'''

import re
from collections import OrderedDict, Counter

class HNLSample():
    def __init__(self, 
                 recommended, 
                 type,
                 requested, 
                 mass, 
                 v2, 
                 ctau, 
                 ctau_ratio_to_theory, 
                 nevents, 
                 xs, 
                 xse, 
                 year,
                 path, 
                 files=[]):
        self.recommended       = recommended      
        self.type              = type             
        self.requested         = requested
        if ctau_ratio_to_theory=='-':    
            self.ctau_ratio = 1.
        else:
            self.ctau_ratio = float(ctau_ratio_to_theory)        
        self.path              = path   
        self.mass              = mass   
        self.v2                = v2     
        self.ctau              = ctau  # [mm]
        self.nevents           = nevents
        self.xs                = xs
        self.xse               = xse
        self.year              = int(year.replace('v3',''))
        self.files             = files
        self.name              = path.split('/')[-1]
        self.title             = path.split('/')[-1].replace('.', 'p').replace('HeavyNeutrino_trilepton', 'HN3L').replace('HN3L_M-','HN3L_M_').replace('V-0p', 'V_0p')#.replace('e-', 'eminus')
    
        if 'e-' in self.title:
            coupling = re.search('V-\d.\d*e-\d*', self.title)
            if len(coupling.group()):
                new_coupling = float(coupling.group()[2:].replace('p', '.'))
                self.title = self.title.replace(coupling.group(), 'V_%.14f' %new_coupling).replace('.', 'p')
                    
    def __str__(self):
        blabla  = self.title
        blabla += '\n\tyear                 %d  ' %self.year
        blabla += '\n\ttype                 %s  ' %self.type
        blabla += '\n\tmass [GeV]           %.1f' %self.mass
        blabla += '\n\tv2                   %f'   %self.v2
        blabla += '\n\tctau [mm]            %.2f' %self.ctau
        blabla += '\n\tctau ratio to theory %.2f' %self.ctau_ratio
        blabla += '\n\tnevents              %d'   %self.nevents
        blabla += '\n\txs                   %.5f' %self.xs
        blabla += '\n\txse                  %.5f' %self.xse
        blabla += '\n\t'+str(self.files)
        return blabla
    
    def _prependPath(self):
        self.files = ['/'.join(['root://cms-xrd-global.cern.ch/', self.path, ifile]) for ifile in self.files]

if __name__ == '__main__':

    samplesdict = OrderedDict()

    with open('heavyNeutrinoFileList.txt') as ff:
        content = ff.readlines()

    current_key = ''
    for ii, line in enumerate(content):
        line = line.rstrip()
        if line.startswith('/pnfs/iihe/cms/'):
            current_key = line.replace(':','')
        if current_key not in samplesdict.keys():
            samplesdict[current_key] = []
        elif line.startswith('heavyNeutrino'):
            samplesdict[current_key].append(line)
        else:
            pass

    print '\n\n\n\n\n'
    
    with open('availableHeavyNeutrinoSamples.txt') as ff:
        content = ff.readlines()

    toread = OrderedDict()
    toread[2016] = []
    toread[2017] = []
    toread[2018] = []

    start_reading = -99
    
    for ii, line in enumerate(content[:]):
        line = line.rstrip()
        if line.startswith('recommended'):
            start_reading = -2
        if start_reading>=-2:
            start_reading+=1
        if start_reading<=0:
            continue
        pieces = line.split()
        if len(pieces)<14:
            continue
        
        if pieces[0] != '*':
            continue 

        my_hnl_sample = HNLSample(
            recommended          = int(pieces[0]!='*')  ,
            type                 = pieces[1]            ,
            requested            = pieces[2]            ,
            mass                 = float(pieces[3])     ,
            v2                   = float(pieces[4])     ,
            ctau                 = float(pieces[5])     ,
            ctau_ratio_to_theory = pieces[6]            ,
            nevents              = int(float(pieces[7])),
            xs                   = float(pieces[8])     ,
            xse                  = float(pieces[10])    ,
            year                 = pieces[12]           ,
            path                 = pieces[13]           ,
        )

        # don't consider hadronic samples
        if 'lljj' in my_hnl_sample.title: continue
                
        if my_hnl_sample.year==2016: toread[2016].append(my_hnl_sample)
        if my_hnl_sample.year==2017: toread[2017].append(my_hnl_sample)
        if my_hnl_sample.year==2018: toread[2018].append(my_hnl_sample)


    for yy in [2016, 2017, 2018]:
        
        toread[yy].sort(key = lambda x : (x.mass, x.v2))
        
        # check for duplicates
        names = [sample.title for sample in toread[yy]]
        duplicates = [name for name, count in Counter(names).items() if count > 1]
        if len(duplicates)>0:
            print 'WARNING! Found duplicates in year %d' %yy
            for ii in duplicates:
                print '\t', ii
            exit(0)


        with open('signals_%d.py'%yy, 'w') as f: 
            
            print >> f, 'import PhysicsTools.HeppyCore.framework.config as cfg'
            print >> f, 'import os'
            print >> f, ''
            print >> f, '#####COMPONENT CREATOR'
            print >> f, ''
            print >> f, 'from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator'
            print >> f, ''
            print >> f, 'creator = ComponentCreator()'

            for sample in toread[yy]:
                if sample.path not in samplesdict.keys():
            #         print sample.path, 'missing'
                    continue
                sample.files = samplesdict[sample.path]
                sample._prependPath()

            for sample in toread[yy]:
                print >> f, "{0:65} = creator.makeMCComponentFromLocal({1:65}, 'XXX', path=os.environ['CMSSW_BASE']+'/src/CMGTools/HNL/python/samples', pattern='.*dummy')".format(sample.title, "'"+sample.title+"'")

            print >> f,  '\n\n'

            for sample in toread[yy]:
                print >> f, sample.title + '.files = ['
                for ii in sample.files:
                    print >> f, "    {0:200},".format("'"+ii.replace('/pnfs/iihe/cms', '')+"'")
                print >> f, ']'

            print >> f, '\n\n'

            for sample in toread[yy]:
                print >> f, "{0:65}.ctau = {1:10} ; {0:65}.v2 = {2:10} ; {0:65}.mass = {3:10} ; {0:65}.nGenEvents = {4:10} ; {0:65}.xs = {5:10} ; {0:65}.xse = {6:10} ;  {0:65}.ctau_ratio_theory = {7:10} ; {0:65}.year = {8:10}".format(sample.title, sample.ctau, sample.v2, sample.mass, sample.nevents, sample.xs, sample.xse, sample.ctau_ratio, sample.year)

            print >> f, '\n\n' 

            print >> f, 'all_signals = ['
            for sample in toread[yy]:
                print >> f, '    %s,' %sample.title
            print >> f, ']'            

            print >> f, '\n\n' 

            print >> f, "all_signals_e  = [isample for isample in all_signals if '_e_'   in isample.name]"
            print >> f, "all_signals_m  = [isample for isample in all_signals if '_mu_'  in isample.name]"
            print >> f, "all_signals_t  = [isample for isample in all_signals if '_tau_' in isample.name]"
            print >> f, "all_signals_2l = [isample for isample in all_signals if '_2l_'  in isample.name]" # e/mu mixing
            print >> f, "all_signals_3l = [isample for isample in all_signals if '_3l_'  in isample.name]" # e/mu/tau mixing
            
            print >> f, '\n\n' 




