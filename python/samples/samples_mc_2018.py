import PhysicsTools.HeppyCore.framework.config as cfg
import os

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable
# https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018_AN1

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

TTJets = creator.makeMCComponent(
    name    = 'TTJets', 
    dataset = '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)
TTJets .nGenEvents = TTJets.dataset_entries 

TTJets_ext = creator.makeMCComponent(
    name    = 'TTJets_ext', 
    dataset = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)
TTJets_ext .nGenEvents = TTJets_ext.dataset_entries 


WJetsToLNu = creator.makeMCComponent(
    name    = 'WJetsToLNu', 
    dataset = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 59850.,
    useAAA  = True
)
WJetsToLNu .nGenEvents = WJetsToLNu.dataset_entries 


DYBB = creator.makeMCComponent(
    name    = 'DYBB',
    dataset = '/DYBBJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = 1.459e+01,# +- 5.139e-02 pb
    useAAA  = True
)
DYBB .nGenEvents = DYBB.dataset_entries 


DYJetsToLL_M5to50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M5to50',
    dataset = '/DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root',
    xSec    = -99,
    useAAA  = True
)
DYJetsToLL_M5to50.nGenEvents = DYJetsToLL_M5to50.dataset_entries 


DYJetsToLL_M50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M50',
    dataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 2075.14*3, 
    useAAA  = True
)
DYJetsToLL_M50.nGenEvents = DYJetsToLL_M50.dataset_entries


DYJetsToLL_M50_ext = creator.makeMCComponent(
    name    = 'DYJetsToLL_M50_ext',
    dataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    # xSec    = 1921.8*3, #oldValue 
    xSec    = 2075.14*3, 
    useAAA  = True
)
DYJetsToLL_M50_ext.nGenEvents = DYJetsToLL_M50_ext.dataset_entries


#from fall17 samples of https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDMeasurementsHelp#2017_measurements_MC2017_v2_samp
WW = creator.makeMCComponent(
    name    = 'WW',
    dataset = '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 75.88, 
    useAAA  = True
)
WW.nGenEvents = WW.dataset_entries


#from fall17 samples of https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDMeasurementsHelp#2017_measurements_MC2017_v2_samp
WZ = creator.makeMCComponent(
    name    = 'WZ',
    dataset = '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 27.6, 
    useAAA  = True
)
WZ.nGenEvents = WZ.dataset_entries


#from fall17 samples of https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDMeasurementsHelp#2017_measurements_MC2017_v2_samp
ZZ = creator.makeMCComponent(
    name    = 'ZZ',
    dataset = '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root', 
    xSec    = 12.14, 
    useAAA  = True
)
ZZ.nGenEvents = ZZ.dataset_entries

# VS :: 10/21/19: adding single top & Z/WGamma / are x-sec ok?
ST_sch_lep = creator.makeMCComponent(
    name    = 'ST_sch_lep', 
    # dataset = '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', # MC_2017
    dataset = '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v4/MINIAODSIM', 
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 3.68, 
    useAAA  = True
)

ST_sch_lep .nGenEvents = ST_sch_lep.dataset_entries 


STbar_tch_inc = creator.makeMCComponent(
    name    = 'STbar_tch_inc', 
    # dataset = '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', # MC_2017
    dataset = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 26.23, 
    useAAA  = True
)

STbar_tch_inc .nGenEvents = STbar_tch_inc .dataset_entries 


ST_tch_inc = creator.makeMCComponent(
    name    = 'ST_tch_inc', 
    # dataset = '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', # MC_2017
    dataset = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 44.07, 
    useAAA  = True
)

ST_tch_inc .nGenEvents = ST_tch_inc.dataset_entries 


STbar_tW_inc = creator.makeMCComponent(
    name    = 'STbar_tW_inc', 
    # dataset = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', # MC_2017
    dataset = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM', 
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 35.6, 
    useAAA  = True
)

STbar_tW_inc .nGenEvents = STbar_tW_inc.dataset_entries 


ST_tW_inc = creator.makeMCComponent(
    name    = 'ST_tW_inc', 
    # dataset = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', # MC_2017
    dataset = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 35.6, 
    useAAA  = True
)

ST_tW_inc .nGenEvents = ST_tW_inc.dataset_entries 

WGToLNuG = creator.makeMCComponent(
    name    = 'WGamma', 
    # /WGToLNuG TuneCUETP8M1 13TeV-amcatnloFXFX-pythia8 # MC_2017
    dataset = '/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 405.271,
    useAAA  = True
)

WGToLNuG .nGenEvents = WGToLNuG.dataset_entries 

ZGTo2LG = creator.makeMCComponent(
    name    = 'ZGamma', 
    # /ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 # MC_2017
    dataset = '/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM', 
    dataset = '',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 123.9,
    useAAA  = True
)

WGToLNuG .nGenEvents = WGToLNuG.dataset_entries 
 

# LINK for crosssections: 
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDMeasurementsHelp#2017_measurements_MC2017_v2_samp

##########################################################################################
# assign to each sample its own PU profile file. For 2017 it is important to do it per-sample
##########################################################################################
# TODO temporary workaround for pu of new samples
# DYBB                                      .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYBB.root' 
# DYJetsToLL_M10to50                        .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJets_M10to50.root' 
# DYJetsToLL_M50                            .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50.root' 
# DYJetsToLL_M50_ext                        .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_DYJetsToLL_M50_ext.root' 
# WJetsToLNu                                .puFileMC = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_WJetsToLNu.root'  
##########################################################################################

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
# for ibkg in hnl_bkg_noskim:
    # ibkg.puFileData = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/pileup/pileup_data_golden_json_2017.root'

