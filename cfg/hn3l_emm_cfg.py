from CMGTools.HNL.hn3l_cfg import *

# specify the samples considerea
# from CMGTools.HNL.samples.signal import all_signals_e as samples
from CMGTools.HNL.samples.localsignal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO
samples = [HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO]

# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00836660026534_e_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal_new import HN3L_M_2_V_0p00836660026534_e_onshell
# from CMGTools.HNL.samples.signal_new import signals_e as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_e as samples
# from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg as samples
# from CMGTools.HNL.samples.samples_mc_2017_noskim import hnl_bkg_noskim as samples
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.signal import HN3L_M_5_V_0p01_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017, Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
# from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017, Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F

# samples = [Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F]
# samples = [sample]

# from CMGTools.HNL.samples.samples_mc_2017_noskim import WJetsToLNu_ext 
# samples = [WJetsToLNu_ext]

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
isData             = False
isSignal           = True
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm" # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
