from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.signals_2017 import HN3L_M_4_V_0p00290516780927_e_massiveAndCKM_LO

samples = [HN3L_M_4_V_0p00290516780927_e_massiveAndCKM_LO]

###################################################
comp = samples[0]
comp.fineSplitFactor = 10 # fine splitting, multicore

# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = False 
if testing:
    # run on a single component
    comp = samples[0]
    comp.files = comp.files[:1]
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

isData             = False
isSignal           = True
promptLeptonType   = "e" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False,
    year=2017
)
