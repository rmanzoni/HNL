from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
from CMGTools.HNL.samples.samples_data_2017 import Single_mu_2017, Single_mu_2017E, Single_mu_2017F, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D
from CMGTools.HNL.samples.samples_mc_2017   import TTJets, WJetsToLNu, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 

samples = [DYJetsToLL_M50, DYJetsToLL_M50_ext, DYJetsToLL_M5to50,]
samples = [DYBB]
samples = [Single_mu_2017C]
samples = [TTJets, WJetsToLNu, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ]
samples = [Single_mu_2017E, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017F]


# edit the lines here to specify your ntuple production mode production         = False # state whether you're running production mode or not
production         = False  # state whether you're running production mode or not
isData             = True
isSignal           = False
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm"  # choose from 'ee', 'mm', 'em'
year               = 17

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal, year)