from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
# from CMGTools.HNL.samples.signal import all_signals_m as samples
# from CMGTools.HNL.samples.localsignal import HN3L_M_2_V_0p00244948974278_e_massiveAndCKM_LO as sample
# from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p0141421356237_mu_massiveAndCKM_LO
# from CMGTools.HNL.samples.signal_new import signals_mu as samples
# from CMGTools.HNL.samples.signal_13sept18 import all_signals_m as samples

# from CMGTools.HNL.samples.samples_data_2017 import Single_mu_2017 as sample
# samples = [sample] 

from CMGTools.HNL.samples.samples_data_2017_noskim import Single_mu_2017, Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017E, Single_mu_2017F
# from CMGTools.HNL.samples.localsignal import  Single_mu_2017B
# samples = [Single_mu_2017B]
# from CMGTools.HNL.samples.samples_mc_2017_noskim import WJetsToLNu_ext 
# samples = [WJetsToLNu_ext]
from CMGTools.HNL.samples.samples_mc_2017_noskim import TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, QCD_pt_15to20_mu, QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu
from CMGTools.HNL.samples.samples_mc_2017 import WW_DoubleScattering, WZTo3LNu, ZZTo4L

# samples = [TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ, WZTo3LNu, ZZTo4L, WW_DoubleScattering]
# samples = [WW, WZ, ZZ, WZTo3LNu, ZZTo4L, WW_DoubleScattering]
# samples = [Single_mu_2017B, Single_mu_2017C, Single_mu_2017D, Single_mu_2017E, Single_mu_2017F]
samples = [TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, QCD_pt_15to20_mu, QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu]


# edit the lines here to specify your ntuple production mode production         = False # state whether you're running production mode or not
production         = True # state whether you're running production mode or not
isData             = False
isSignal           = False
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
