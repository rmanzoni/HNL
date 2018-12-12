from CMGTools.HNL.hn3l_cfg import *

# specify the samples considerea
# from CMGTools.HNL.samples.signal import all_signals_e as samples
# from CMGTools.HNL.samples.localsignal import HN3L_M_2_V_0p00836660026534_e_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00836660026534_e_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal_new import HN3L_M_2_V_0p00836660026534_e_onshell
# from CMGTools.HNL.samples.signal_new import signals_e as samples
from CMGTools.HNL.samples.signal_13sept18 import all_signals_e as samples


# samples =[HN3L_M_2_V_0p00836660026534_e_onshell]


# edit the lines here to specify your ntuple production mode 
production         = False # state whether you're running production mode or not
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm" # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType)
