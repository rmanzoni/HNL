import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

TTJets = creator.makeMCComponent(
    name    = 'TTJets', 
    dataset = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)

WJetsToLNu = creator.makeMCComponent(
    name    = 'WJetsToLNu', 
    dataset = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 59850.,
    useAAA  = True
)

WJetsToLNu_ext = creator.makeMCComponent(
    name    = 'WJetsToLNu_ext', 
    dataset = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 59850.,
    useAAA  = True
)

ZZZ = creator.makeMCComponent(
    name    = 'ZZZ', 
    dataset = '/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)

ggZZTo2e2mu_ext = creator.makeMCComponent(
    name    = 'ggZZTo2e2mu_ext', 
    dataset = '/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)
ggZZTo2e2mu_ext.nGenEvents = ggZZTo2e2mu_ext.dataset_entries

ggZZTo2e2nu = creator.makeMCComponent(
    name    = 'ggZZTo2e2nu', 
    dataset = '/GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00172,
    useAAA  = True
)
ggZZTo2e2nu.nGenEvents = ggZZTo2e2nu.dataset_entries

ggZZTo2e2nu_ext = creator.makeMCComponent(
    name    = 'ggZZTo2e2nu_ext', 
    dataset = '/GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00172,
    useAAA  = True
)
ggZZTo2e2nu_ext.nGenEvents = ggZZTo2e2nu_ext.dataset_entries

ggZZTo2e2tau = creator.makeMCComponent(
    name    = 'ggZZTo2e2tau', 
    dataset = '/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)
ggZZTo2e2tau.nGenEvents = ggZZTo2e2tau.dataset_entries

ggZZTo2e2tau_ext = creator.makeMCComponent(
    name    = 'ggZZTo2e2tau_ext', 
    dataset = '/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)
ggZZTo2e2tau_ext.nGenEvents = ggZZTo2e2tau_ext.dataset_entries

ggZZTo2mu2nu = creator.makeMCComponent(
    name    = 'ggZZTo2mu2nu', 
    dataset = '/GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00172,
    useAAA  = True
)
ggZZTo2mu2nu.nGenEvents = ggZZTo2mu2nu.dataset_entries

ggZZTo2mu2nu_ext = creator.makeMCComponent(
    name    = 'ggZZTo2mu2nu_ext', 
    dataset = '/GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00172,
    useAAA  = True
)
ggZZTo2mu2nu_ext.nGenEvents = ggZZTo2mu2nu_ext.dataset_entries

ggZZTo2mu2tau = creator.makeMCComponent(
    name    = 'ggZZTo2mu2tau', 
    dataset = '/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)
ggZZTo2mu2tau.nGenEvents = ggZZTo2mu2tau.dataset_entries

ggZZTo2mu2tau_ext = creator.makeMCComponent(
    name    = 'ggZZTo2mu2tau_ext', 
    dataset = '/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.00319,
    useAAA  = True
)
ggZZTo2mu2tau_ext.nGenEvents = ggZZTo2mu2tau_ext.dataset_entries

ggZZTo4e = creator.makeMCComponent(
    name    = 'ggZZTo4e', 
    dataset = '/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.001586,
    useAAA  = True
)
ggZZTo4e.nGenEvents = ggZZTo4e.dataset_entries

ggZZTo4mu = creator.makeMCComponent(
    name    = 'ggZZTo4mu', 
    dataset = '/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.001586,
    useAAA  = True
)
ggZZTo4mu.nGenEvents = ggZZTo4mu.dataset_entries

ggZZTo4tau = creator.makeMCComponent(
    name    = 'ggZZTo4tau', 
    dataset = '/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.001586,
    useAAA  = True
)
ggZZTo4tau.nGenEvents = ggZZTo4tau.dataset_entries

W1JetsToLNu = creator.makeMCComponent(
    name    = 'W1JetsToLNu', 
    dataset = '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 9493,
    useAAA  = True
)
W1JetsToLNu.nGenEvents = W1JetsToLNu.dataset_entries

W2JetsToLNu = creator.makeMCComponent(
    name    = 'W2JetsToLNu', 
    dataset = '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v4/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 3120,
    useAAA  = True
)
W2JetsToLNu.nGenEvents = W2JetsToLNu.dataset_entries

W3JetsToLNu = creator.makeMCComponent(
    name    = 'W3JetsToLNu', 
    dataset = '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 942.3,
    useAAA  = True
)
W3JetsToLNu.nGenEvents = W3JetsToLNu.dataset_entries

W4JetsToLNu = creator.makeMCComponent(
    name    = 'W4JetsToLNu', 
    dataset = '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 524.2,
    useAAA  = True
)
W4JetsToLNu.nGenEvents = W4JetsToLNu.dataset_entries

DYBB = creator.makeMCComponent(
    name    = 'DYBB',
    dataset = '/DYBBJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = 1.459e+01,# +- 5.139e-02 pb
    useAAA  = True
)

DYJetsToLL_M10to50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M10to50',
    dataset = '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = (1.581e+04)*1.23,# +- 2.890e+01 pb
    useAAA  = True
)

DYJetsToLL_M10to50_ext = creator.makeMCComponent(
    name    = 'DYJetsToLL_M10to50_ext',
    dataset = '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = (1.581e+04)*1.23,# +- 2.890e+01 pb
    useAAA  = True
)

DYJetsToLL_M50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M50',
    dataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 1921.8*3, 
    useAAA  = True
)
DYJetsToLL_M50.nGenEvents = DYJetsToLL_M50.dataset_entries

DYJetsToLL_M50_ext = creator.makeMCComponent(
    name    = 'DYJetsToLL_M50_ext',
    dataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 1921.8*3, 
    useAAA  = True
)


DY1JetsToLL_M50 = creator.makeMCComponent(
    name    = 'DY1JetsToLL_M50', 
    dataset = '/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 1016, 
    useAAA  = True
)

DY2JetsToLL_M50 = creator.makeMCComponent(
    name    = 'DY2JetsToLL_M50', 
    dataset = '/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 331.4,
    useAAA  = True
)

DY2JetsToLL_M50_ext = creator.makeMCComponent(
    name    = 'DY2JetsToLL_M50_ext', 
    dataset = '/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 331.4,
    useAAA  = True
)

DY3JetsToLL_M50 = creator.makeMCComponent(
    name    = 'DY3JetsToLL_M50', 
    dataset = '/DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 96.36,
    useAAA  = True
)

DY3JetsToLL_M50_ext = creator.makeMCComponent(
    name    = 'DY3JetsToLL_M50_ext', 
    dataset = '/DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 96.36,
    useAAA  = True
)

 
QCD_pt_15to20_mu = creator.makeMCComponent(
    name    = 'QCD_pt_15to20_mu', 
    dataset = '/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 2.798e+06,# +- 9.154e+03 pb
    useAAA  = True
)

QCD_pt_20to30_mu = creator.makeMCComponent(
    name    = 'QCD_pt_20to30_mu', 
    dataset = '/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 2.533e+06,# +- 8.257e+03 pb
    useAAA  = True
) 

QCD_pt_30to50_mu = creator.makeMCComponent(
    name    = 'QCD_pt_30to50_mu', 
    dataset = '/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 1.375e+06,# +- 4.484e+03 pb
    useAAA  = True
) 

QCD_pt_50to80_mu = creator.makeMCComponent(
    name    = 'QCD_pt_50to80_mu', 
    dataset = '/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 3.770e+05,# +- 1.214e+03 pb
    useAAA  = True
) 

QCD_pt_80to120_mu = creator.makeMCComponent(
    name    = 'QCD_pt_80to120_mu',
    dataset = '/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 8.880e+04,# +- 2.854e+02 pb
    useAAA  = True
) 

# fake electrons
QCD_pt_20to30_bcToE = creator.makeMCComponent(
    name    = 'QCD_pt_20to30_bcToE', 
    dataset = '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 3.053e+05,# +- 1.049e+03 pb
    useAAA  = True
) 

QCD_pt_30to80_bcToE = creator.makeMCComponent(
    name    = 'QCD_pt_30to80_bcToE', 
    dataset = '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 3.616e+05,# +- 1.361e+03 pb
    useAAA  = True
) 

QCD_pt_80to170_bcToE = creator.makeMCComponent(
    name    = 'QCD_pt_80to170_bcToE', 
    dataset = '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 3.377e+04,# +- 1.088e+02 pb
    useAAA  = True
) 

QCD_pt_170to250_bcToE = creator.makeMCComponent(
    name    = 'QCD_pt_170to250_bcToE', 
    dataset = '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 2.136e+03,# +- 1.359e+01 pb
    useAAA  = True
) 

QCD_pt_250toInf_bcToE = creator.makeMCComponent(
    name    = 'QCD_pt_250toInf_bcToE', 
    dataset = '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 5.596e+02,# +- 2.029e+00 pb
    useAAA  = True
) 

QCD_pt_15to20_em = creator.makeMCComponent(
    name    = 'QCD_pt_15to20_em', 
    dataset = '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 1.309e+06,# +- 8.450e+03 pb
    useAAA  = True
) 

QCD_pt_20to30_em = creator.makeMCComponent(
    name    = 'QCD_pt_20to30_em',
    dataset = '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 4.920e+06,# +- 3.187e+04 pb
    useAAA  = True
) 

QCD_pt_30to50_em = creator.makeMCComponent(
    name    = 'QCD_pt_30to50_em',
    dataset = '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 6.397e+06,# +- 2.039e+04 pb
    useAAA  = True
) 

QCD_pt_50to80_em = creator.makeMCComponent(
    name    = 'QCD_pt_50to80_em', 
    dataset = '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 1.989e+06,# +- 6.197e+03 pb
    useAAA  = True
) 

# NOT ON DAS!
#QCD_pt_80to120_em = creator.makeMCComponent(
#    name    = 'QCD_pt_80to120_em', 
#    dataset = '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
#    user    = 'CMS',
#    pattern = '.*root',
#    useAAA  = True
#) 

QCD_pt_120to170_em = creator.makeMCComponent(
    name    = 'QCD_pt_120to170_em', 
    dataset = '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 6.633e+04,# +- 2.318e+02 pb
    useAAA  = True
) 

# NOT ON DAS!
#QCD_pt_170to300_em = creator.makeMCComponent(
#    name    = 'QCD_pt_170to300_em', 
#    dataset = '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
#    user    = 'CMS',
#    pattern = '.*root',
#    useAAA  = True
#) 

QCD_pt_300toInf_em = creator.makeMCComponent(
    name    = 'QCD_pt_300toInf_em', 
    dataset = '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    xSec    = 1.108e+03,# +- 4.856e+00 pb
    useAAA  = True
) 

qcd = [QCD_pt_15to20_em, QCD_pt_20to30_em, QCD_pt_30to50_em, QCD_pt_50to80_em, QCD_pt_120to170_em, QCD_pt_300toInf_em, QCD_pt_20to30_bcToE, QCD_pt_30to80_bcToE, QCD_pt_80to170_bcToE, QCD_pt_170to250_bcToE, QCD_pt_250toInf_bcToE, QCD_pt_15to20_mu, QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu]

qcd_e = [QCD_pt_15to20_em, QCD_pt_20to30_em, QCD_pt_30to50_em, QCD_pt_50to80_em, QCD_pt_120to170_em, QCD_pt_300toInf_em, QCD_pt_20to30_bcToE, QCD_pt_30to80_bcToE, QCD_pt_80to170_bcToE, QCD_pt_170to250_bcToE, QCD_pt_250toInf_bcToE]

qcd_mu = [QCD_pt_15to20_mu, QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu]

# W1JetsToLNu = creator.makeMCComponent(
    # name    = 'W1JetsToLNu', 
    # dataset = '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',
    # user    = 'CMS',
    # pattern = '.*root',
    # xSec    = 8.139e+03,# +- 3.379e+01 pb
    # useAAA  = True
# ) 
# W1JetsToLNu.nGenEvents = W1JetsToLNu.dataset_entries

# W2JetsToLNu = creator.makeMCComponent(
    # name    = 'W2JetsToLNu', 
    # dataset = '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v4/MINIAODSIM',
    # user    = 'CMS',
    # pattern = '.*root',
    # xSec    = 2.781e+03,# +- 1.672e+01 pb
    # useAAA  = True
# ) 
# W2JetsToLNu.nGenEvents = W2JetsToLNu.dataset_entries

# W3JetsToLNu = creator.makeMCComponent(
    # name    = 'W3JetsToLNu',
    # dataset = '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    # user    = 'CMS',
    # pattern = '.*root', 
    # xSec    = 993.4*1.17, 
    # useAAA  = True
# )
# W3JetsToLNu.nGenEvents = W3JetsToLNu.dataset_entries
# #.sigma = 993.4*1.17 pb; .nevents = 6265138; .L = 5390.395413145565 pb^-1 
 
# W4JetsToLNu = creator.makeMCComponent(
    # name    = 'W4JetsToLNu',
    # dataset = '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    # user    = 'CMS',
    # pattern = '.*root', 
    # xSec    = 542.4*1.17, 
    # useAAA  = True
# )
# W4JetsToLNu.nGenEvents = W4JetsToLNu.dataset_entries
#.sigma = 542.4*1.17 pb; .nevents = 3356894; .L = 5289.712704535714 pb^-1  

wjets = [W1JetsToLNu, W2JetsToLNu, W3JetsToLNu, W4JetsToLNu]

# LINK for crosssections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns

##########################################################################################
# assign to each sample its own PU profile file. For 2017 it is important to do it per-sample
##########################################################################################
# TODO temporary workaround for pu of new samples
DYBB                                      .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50.root' 
DYJetsToLL_M10to50                        .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50.root' 
DYJetsToLL_M10to50_ext                    .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50.root' 
WJetsToLNu_ext                            .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WJetsToLNu.root'
for i in qcd+wjets:                      i.puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_TTJets_amcat.root' # derived manually 
### the ones below are fine
TTJets                                    .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_TTJets_amcat.root' # derived manually 
ZZZ                                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_ZZZ.root' # derived manually 
WZZ                                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WZZ.root' # derived manually 
WWZ                                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WWZ.root' # derived manually 
WWW                                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WWW.root' # derived manually 
WWTo2L2Nu                                 .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WWTo2L2Nu.root' # derived manually 
WGGJets                                   .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WGGJets.root' # derived manually 
TTWJetsToLNu                              .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_TTWJetsToLNu.root' # derived manually 
TTZToLL_M10                               .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_TTZToLL_M10.root' # derived manually 
TTZToLL_M1to10                            .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_TTZToLL_M1to10.root' # derived manually 
ST_sch_lep                                .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_ST_s-channel_4f_leptonDecays.root' # derived manually 
STbar_tch_inc                             .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_ST_t-channel_antitop_4f_inclusiveDecays.root' # derived manually 
ST_tch_inc                                .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_ST_t-channel_top_4f_inclusiveDecays.root' # derived manually 
STbar_tW_inc                              .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_STbar_tW_inc.root' # derived manually 
ST_tW_inc                                 .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_ST_tW_inc.root' # derived manually 
WJetsToLNu                                .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WJetsToLNu.root'   # in Albert W3JetsToLNu-LO  /W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
W3JetsToLNu                               .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_W3JetsToLNu.root'  # in Albert W3JetsToLNu-LO  /W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
W4JetsToLNu                               .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_W4JetsToLNu.root'  # in Albert W4JetsToLNu-LO  /W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
DYJetsToLL_M50                            .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50.root' 
DYJetsToLL_M50_ext                        .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50_ext.root' 
DY1JetsToLL_M50                           .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DY1JetsToLL_M50.root' # derived manually   
DY2JetsToLL_M50                           .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DY2JetsToLL_M50.root' # derived manually     
DY2JetsToLL_M50_ext                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DY2JetsToLL_M50_ext.root' # derived manually 
DY3JetsToLL_M50                           .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DY3JetsToLL_M50.root' # derived manually     
DY3JetsToLL_M50_ext                       .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DY3JetsToLL_M50_ext.root' # derived manually 


##########################################################################################
hnl_bkg_noskim = [
    TTJets,
    WJetsToLNu,
    WJetsToLNu_ext,
    ZZZ, 
    WZZ, 
    WWZ, 
    WWW, 
    WWTo2L2Nu, 
    WGGJets, 
    TTWJetsToLNu, 
    TTZToLL_M10, 
    TTZToLL_M1to10, 
    ST_sch_lep, 
    STbar_tch_inc, 
    ST_tch_inc, 
    STbar_tW_inc, 
    ST_tW_inc, 
    DYJetsToLL_M10to50,
    DYJetsToLL_M10to50_ext,
    DYJetsToLL_M50,
    DYJetsToLL_M50_ext,
    DY1JetsToLL_M50,     
    DY2JetsToLL_M50,     
    DY2JetsToLL_M50_ext, 
    DY3JetsToLL_M50,     
    DY3JetsToLL_M50_ext, 
] 

hnl_bkg_noskim += qcd + wjets + [DYBB]
for sample in hnl_bkg_noskim: sample.nGenEvents = sample.dataset_entries




##########################################################################################
#  data PileUp profile
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Pileup_JSON_Files_For_Run_II
# have a loo at this too, the mb cross section might be off https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/755.html
'''
pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt\
              --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt\
              --calcMode true --minBiasXsec 69200 --maxPileupBin 200 --numPileupBins 200  pileup_data_golden_json_2017.root
'''
for ibkg in hnl_bkg_noskim:
    ibkg.puFileData = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_data_golden_json_2017.root'
