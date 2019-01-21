from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
# from CMGTools.HNL.samples.signal import all_signals_m as samples
# from CMGTools.HNL.samples.signal_new import signals_mu as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_m as samples

# from CMGTools.HNL.samples.samples_data_2017 import Single_mu_2017 as sample
# samples = [sample] 

# from CMGTools.HNL.samples.samples_data_2017_noskim import Single_mu_2017, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017E, Single_mu_2017F
# samples = [Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017E, Single_mu_2017F]
from CMGTools.HNL.samples.samples_mc_2017_noskim import WJetsToLNu_ext 
samples = [WJetsToLNu_ext]

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
isData             = False
isSignal           = False
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
