from CMGTools.HNL.hn3l_cfg import generateKeyConfigs
from CMGTools.HNL.samples.samples_mc_2017 import TTJets, WJetsToLNu, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 

# specify the samples considered
samples = [TTJets, DYJetsToLL_M50_ext]#, WJetsToLNu, TTJets_ext, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, WW, WZ, ZZ]
samples = [TTJets, DYJetsToLL_M50_ext, WJetsToLNu, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, WW, WZ, ZZ]
samples = [DYBB]

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
isSignal           = False
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm" # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False
)
