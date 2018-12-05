from CMGTools.HNL.hn3l_cfg import *
from CMGTools.HNL.hn3l_cfg import generateConfigs

# production         = getHeppyOption('production' , True)
# production         = getHeppyOption('production' , False)
production = False
promptLeptonType = "mu" #choose from 'ele', 'mu'
L1L2LeptonType = "em" #choose from 'ee', 'mm', 'em'

generateConfigs(production, promptLeptonType, L1L2LeptonType)
