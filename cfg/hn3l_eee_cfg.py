from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
# from CMGTools.HNL.samples.signal import all_signals_e as samples
# from CMGTools.HNL.samples.signal_new import signals_e as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_e as samples
# from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017, Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
# from CMGTools.HNL.samples.samples_data_2017_noskim import  Single_ele_2017B
# from CMGTools.HNL.samples.localsignal import  WJetsToLNu_ext
from CMGTools.HNL.samples.samples_mc_2017 import TTJets_amcat
# from CMGTools.HNL.samples.samples_mc_2017 import DYBB,DYJetsToLL_M10to50
# samples = [Single_ele_2017B,Single_ele_2017C,Single_ele_2017D,Single_ele_2017E,Single_ele_2017F]
#samples = [DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M10to50_ext, DYJetsToLL_M50_ext]
#samples = [DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext]
# from CMGTools.HNL.samples.samples_mc_2017_noskim import WJetsToLNu 
# samples = [WJetsToLNu]
samples = [TTJets_amcat]
# from CMGTools.HNL.samples.localsignal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO
# samples = [HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO]
# samples = [DYJetsToLL_M10to50]


# edit the lines here to specify your ntuple production mode 
production         = False # state whether you're running production mode or not
isData             = False
isSignal           = True
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "ee"  # choose from 'ee', 'mm', 'em'


# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
