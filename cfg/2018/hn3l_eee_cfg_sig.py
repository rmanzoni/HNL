from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.signals_2018 import all_signals_e

samples = all_signals_e

###################################################
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
L1L2LeptonType     = "ee"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=True,
    year=2017
)
