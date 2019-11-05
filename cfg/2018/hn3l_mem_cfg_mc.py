from CMGTools.HNL.hn3l_cfg import generateKeyConfigs

# specify the samples considered
from CMGTools.HNL.samples.samples_mc_2018   import TTJets, TTJets_ext, WJetsToLNu, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 

samples = [TTJets_ext, DYJetsToLL_M50, DYJetsToLL_M50_ext, DYJetsToLL_M5to50,]
samples = [TTJets, WJetsToLNu, TTJets_ext, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ]
samples = [DYBB]

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = True 
if testing:
    # run on a single component
    comp = samples[0]
    comp = TTJets_ext
    # comp.files = comp.files[:1]
    comp.files = ['/work/vstampf/check_4ch_ntuplizer.input.root']
    comp.files = ['/afs/cern.ch/work/m/manzoni/public/001784E5-D649-734B-A5FF-E151DA54CC02.root']
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]
###################################################

isData             = False
isSignal           = False
promptLeptonType   = "m" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(
    samples, 
    promptLeptonType, 
    L1L2LeptonType, 
    isData=isData, 
    isSignal=isSignal,
    prefetch=False,
    year=2018
)
