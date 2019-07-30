from CMGTools.HNL.hn3l_cfg import *

# specify the samples considerea
from CMGTools.HNL.samples.signal import all_signals_e
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017, Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
from CMGTools.HNL.samples.samples_mc_2017_noskim import TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc 

# samples = [TTJets, WJetsToLNu, WJetsToLNu_ext, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc]
samples = [Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F]
# samples = all_signals_e

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
isData             = True
isSignal           = False
promptLeptonType   = "ele" # choose from 'ele', 'mu'
L1L2LeptonType     = "em"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType, isData = isData, isSignal = isSignal)
