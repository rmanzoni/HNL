# heppy_batch.py -r /store/group/phys_tau/WTau3Mu/DoubleMuLowMass23Feb2019 -o DoubleMuLowMass23Feb2019 wtau3mu_2016_data_doublemu_lowmass_cfg.py -B -b 'run_condor_simple.sh -t 1200 ./batchScript.sh'
# heppy_batch.py -o mmm_bkg_mc_2018 hn3l_mmm_cfg_mc.py -B -b 'run_condor_simple.sh -t 1200 ./batchScript.sh'

from CMGTools.HNL.hn3l_cfg import generateKeyConfigs
from CMGTools.HNL.samples.samples_mc_2018 import all_samples, TTJets, TTJets_ext, WJetsToLNu, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 

# specify the samples considered
# samples = [TTJets, DYJetsToLL_M50_ext]
samples = all_samples

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = False 
if testing:
    # run on a single component
    comp = TTJets_ext
    comp.files = comp.files[:1]
    comp.files = ['/tmp/manzoni/001784E5-D649-734B-A5FF-E151DA54CC02.root'] # one file from TTJets_ext on lxplus700
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

toSelect = []

isData             = False
isSignal           = False
promptLeptonType   = "m"  # choose from 'e', 'm'
L1L2LeptonType     = "mm" # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=True,
    year=2018,
#     toSelect=toSelect,
    saveBigTree=False,
)
