import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

TTJets = creator.makeMCComponent(
    name    = 'TTJets', 
    dataset = '/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)
TTJets .nGenEvents = TTJets.dataset_entries 

WJetsToLNu = creator.makeMCComponent(
    name    = 'WJetsToLNu', 
    dataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 61334.9, # AN_v3
    useAAA  = True
)
WJetsToLNu .nGenEvents = WJetsToLNu.dataset_entries 

WJetsToLNu_ext = creator.makeMCComponent(
    name    = 'WJetsToLNu_ext', 
    dataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 61334.9, # AN_v3
    useAAA  = True
)
WJetsToLNu_ext .nGenEvents = WJetsToLNu_ext.dataset_entries 

ZZZ = creator.makeMCComponent(
    name    = 'ZZZ', 
    dataset = '/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.01398, 
    useAAA  = True
)

ZZZ .nGenEvents = ZZZ.dataset_entries 


WZZ = creator.makeMCComponent(
    name    = 'WZZ', 
    dataset = '/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.05565, 
    useAAA  = True
)

WZZ .nGenEvents = WZZ.dataset_entries 


WWZ = creator.makeMCComponent(
    name    = 'WWZ', 
    dataset = '/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.1651, 
    useAAA  = True
)

WWZ .nGenEvents = WWZ.dataset_entries 


WWW = creator.makeMCComponent(
    name    = 'WWW', 
    dataset = '/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.2086, 
    useAAA  = True
)

WWW .nGenEvents = WWW.dataset_entries 


WWTo2L2Nu = creator.makeMCComponent(
    name    = 'WWTo2L2Nu', 
    dataset = '/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    # /WWTo2L2Nu_13TeV-powheg-herwigpp/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' #THERE'S ALSO THIS!
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 0.1729, 
    useAAA  = True
)

WWTo2L2Nu .nGenEvents = WWTo2L2Nu.dataset_entries 


ST_sch_lep = creator.makeMCComponent(
    name    = 'ST_sch_lep', 
    dataset = '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 3.68, 
    useAAA  = True
)

ST_sch_lep .nGenEvents = ST_sch_lep.dataset_entries 


STbar_tch_inc = creator.makeMCComponent(
    name    = 'STbar_tch_inc', 
    dataset = '/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 26.23, 
    useAAA  = True
)

STbar_tch_inc .nGenEvents = STbar_tch_inc .dataset_entries 


ST_tch_inc = creator.makeMCComponent(
    name    = 'ST_tch_inc', 
    dataset = '/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 44.07, 
    useAAA  = True
)

ST_tch_inc .nGenEvents = ST_tch_inc.dataset_entries 


STbar_tW_inc = creator.makeMCComponent(
    name    = 'STbar_tW_inc', 
    dataset = '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 35.6, 
    useAAA  = True
)

STbar_tW_inc .nGenEvents = STbar_tW_inc.dataset_entries 


ST_tW_inc = creator.makeMCComponent(
    name    = 'ST_tW_inc', 
    dataset = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 35.6, 
    useAAA  = True
)

ST_tW_inc .nGenEvents = ST_tW_inc.dataset_entries 

DYBB = creator.makeMCComponent(
    name    = 'DYBB',
    dataset = '/DYBBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = 1.459e+01,# +- 5.139e-02 pb
    useAAA  = True
)
DYBB .nGenEvents = DYBB.dataset_entries 

DYJetsToLL_M10to50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M10to50',
    dataset = '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v3/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = 18610.0, # AN_v3
    useAAA  = True
)
DYJetsToLL_M10to50.nGenEvents = DYJetsToLL_M10to50.dataset_entries 

DYJetsToLL_M10to50_ext = creator.makeMCComponent(
    name    = 'DYJetsToLL_M10to50_ext',
    dataset = '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = 18610.0, # AN_v3
    useAAA  = True
)

DYJetsToLL_M50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M50',
    dataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 6020.85, # from AN_v3
    useAAA  = True
)
DYJetsToLL_M50.nGenEvents = DYJetsToLL_M50.dataset_entries


WW = creator.makeMCComponent(
    name    = 'WW',
    dataset = '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 75.88, 
    useAAA  = True
)
WW.nGenEvents = WW.dataset_entries

WZ = creator.makeMCComponent(
    name    = 'WZ',
    dataset = '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 27.6, 
    useAAA  = True
)
WZ.nGenEvents = WZ.dataset_entries

ZZ = creator.makeMCComponent(
    name    = 'ZZ',
    dataset = '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 12.14, 
    useAAA  = True
)
ZZ.nGenEvents = ZZ.dataset_entries

WZTo3LNu = creator.makeMCComponent(
    name    = 'WZTo3LNu',
    dataset = '/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 4.4297, 
    useAAA  = True
)
WZTo3LNu.nGenEvents = WZTo3LNu.dataset_entries

ZZTo4L = creator.makeMCComponent(
    name    = 'ZZTo4L',
    dataset = '/ZZTo4L_13TeV_powheg_pythia8_ext1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 1.256, 
    useAAA  = True
)
ZZTo4L.nGenEvents = ZZTo4L.dataset_entries


# LINK for crosssections: 
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDMeasurementsHelp#2017_measurements_MC2017_v2_samp


##########################################################################################
#  data PileUp profile
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Pileup_JSON_Files_For_Run_II
# have a loo at this too, the mb cross section might be off https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/755.html
'''
pileupCalc.py -i $CMSSW_BASE/src/CMGTools/HNL/data/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt\
              --inputLumiJSON pileup_latest_16.txt\
              --calcMode true --minBiasXsec 69200 #TODO CHECK THE MB XSEC --maxPileupBin 200 --numPileupBins 200  pileup_data_golden_json_2016.root
'''

all_samples = [TTJets, WJetsToLNu, WJetsToLNu_ext, ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, DYBB, DYJetsToLL_M10to50, DYJetsToLL_M10to50_ext, DYJetsToLL_M50, WW, WW, WZ, WZ, ZZ, WZTo3LNu, ZZTo4L]