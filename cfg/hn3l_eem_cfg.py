from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
# from CMGTools.HNL.samples.signal import all_signals_e as samples
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal import HN3L_M_8_V_0p00244948974278_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p00282842712475_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.signal_new import signals_e as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_e as samples
from CMGTools.HNL.samples.samples_mc_2017_noskim import TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext 
from CMGTools.HNL.samples.samples_mc_2017 import WW_DoubleScattering, WZTo3LNu, ZZTo4L, WJetsToLNu
samples = [TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW_DoubleScattering, WZTo3LNu, ZZTo4L, WJetsToLNu]

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
isData             = False
isSignal           = False
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
