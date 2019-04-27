from CMGTools.HNL.plot_cfg_hn3l import *

promptLeptonType = "ele" # do "ele" or "mu"
L1L2LeptonType   = "mm" # do "mm", "me", "ee"
server           = "t3" # do "t3" or "lxplus"

# producePlots(promptLeptonType = promptLeptonType, L1L2LeptonType = L1L2LeptonType)
producePlots(promptLeptonType, L1L2LeptonType, server)
