from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.samples_data_2018 import Single_mu_2018, Single_mu_2018A, Single_mu_2018B, Single_mu_2018C, Single_mu_2018D

samples = [Single_mu_2018A, Single_mu_2018B, Single_mu_2018C, Single_mu_2018D]
samples = [Single_mu_2018A, Single_mu_2018B, Single_mu_2018C, Single_mu_2018D]
samples = [Single_mu_2018D]

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = True 
if testing:
    # run on a single component
    comp = samples[0]
    comp.files = comp.files[:1]
    comp.files = ['/tmp/manzoni/DD93A253-6D38-C145-A54B-EBDA1D9941C9.root']
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

toSelect = [
    1907001815,
    1906900170,
    1907804418,
    1907294530,
    1906669138,
    1907945433,
]

isData             = True
isSignal           = False
promptLeptonType   = "m" # choose from 'e', 'm'
L1L2LeptonType     = "mm"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False,
    year=2018,
#     toSelect=toSelect,
)
