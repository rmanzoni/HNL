from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
# from CMGTools.HNL.samples.signal import all_signals_e as samples
# from CMGTools.HNL.samples.signal_new import signals_e as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_e as samples
# from CMGTools.HNL.samples.signal import HN3L_M_5_V_0p01_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017, Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
from CMGTools.HNL.samples.samples_mc_2017_noskim import WJetsToLNu_ext 
samples = [WJetsToLNu_ext]
# samples =[sample]

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
isData             = False
isSignal           = False
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
