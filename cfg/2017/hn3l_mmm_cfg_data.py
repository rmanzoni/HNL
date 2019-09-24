from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.samples_data_2017 import Single_mu_2017, Single_mu_2017E, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017F

samples = [Single_mu_2017E, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017F]
samples = [Single_mu_2017B]#, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D]

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = True 
if testing:
    # run on a single component
    comp = samples[0]
    comp.files = comp.files[:1]
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

isData             = True
isSignal           = False
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False
)
