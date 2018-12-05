from CMGTools.HNL.hn3l_cfg import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

# production         = getHeppyOption('production' , True)
production         = getHeppyOption('production' , False)
promptLeptonType = "mu" #choose from 'ele', 'mu'
L1L2LeptonType = "em" #choose from 'ee', 'mm', 'em'

config = generateKeyConfigs(production, promptLeptonType, L1L2LeptonType)
