from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.samples_data_2018 import Single_ele_2018, Single_ele_2018A, Single_ele_2018B, Single_ele_2018C, Single_ele_2018D,

samples = Single_ele_2018

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = True 
if testing:
    # run on a single component
    comp = samples[0]
    # comp.files = comp.files[:1]
    comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

isData             = True
isSignal           = False
promptLeptonType   = "e" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False
)
