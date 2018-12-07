from CMGTools.HNL.hn3l_cfg import *

# specify the samples considered
from CMGTools.HNL.samples.signal import all_signals_m as samples

# edit the lines here to specify your ntuple production mode 
production         = True # state whether you're running production mode or not
promptLeptonType   = "mu" # choose from 'ele', 'mu'
L1L2LeptonType     = "mm"  # choose from 'ee', 'mm', 'em'

# this calls the master cfg file with the proper settings
config = generateKeyConfigs(samples,production, promptLeptonType, L1L2LeptonType)
