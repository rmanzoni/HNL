import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification//Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'

creator = ComponentCreator()

# check if this is the right method
TTJets_amct = creator.makeMyPrivateMCComponent("TTJets_amcat", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER", "PRIVATE", "*.root","phys03", useAAA=True)

TTJets_mdgrph = creator.makeMyPrivateMCComponent("TTJets_madgraph", "/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER", "PRIVATE", "*.root", "phys03", useAAA=True)

SingleEle_2017 = creator.MakeMyPrivateDataComponent("SingleEle_2017", "/SingleElectron/vstampf-HNLSKIM2017-a3ebfef9ab75dc703a0292f5032c1af2/USER", "CMS", "*.root", json, useAAA=True)

hnl_bkg = [
    TTJets_amcat,
    TTJets_mdgrph,
]

data_2017 = [
    SingleEle_2017,
]

##########################################################################################
#BPHParking1_2018A = creator.makeDataComponent("BPHParking1_2018A", "/ParkingBPH1/Run2018A-14May2018-v1/MINIAOD", "CMS", ".*root", json, useAAA=True)
#
#bph_parking_2018A = [
#    BPHParking6_2018A,
#]
#
#BPHParking1_AOD_2018A = creator.makeDataComponent("BPHParking1_AOD_2018A", "/ParkingBPH1/Run2018A-14May2018-v1/AOD", "CMS", ".*root", json, useAAA=True)
#
#bph_parking_AOD_2018A = [
#    BPHParking1_AOD_2018A,
#]
##########################################################################################


##########################################################################################
#BPHParking1_2018A_skimmed = BPHParking1_2018A
#BPHParking6_2018A_skimmed = BPHParking6_2018A
#
#
#BPHParking1_2018A_skimmed.files = glob('/eos/cms/store/group/phys_tau/BKstLL/skimParkingBPHToEEV2/ParkingBPH1/skimParkingBPHToEE/180601_111629/0000/*.root')
#BPHParking6_2018A_skimmed.files = glob('/eos/cms/store/group/phys_tau/BKstLL/skimParkingBPHToEEV1/ParkingBPH6/skimParkingBPHToEE/180529_203228/0000/*.root')
#
#bph_parking_2018A_skimmed = [
#    BPHParking1_2018A_skimmed,
#    BPHParking6_2018A_skimmed,
#]
##########################################################################################
#from glob import glob
#
#SingleEle_2017_files_1 = glob('/eos/cms/store/user/vstampf/SingleElectron/HNLSKIM2017/180709_175142/0000/*.root')
#SingleEle_2017_files_2 = glob('/eos/cms/store/user/vstampf/SingleElectron/HNLSKIM2017/180709_175219/0001/*.root')
#
#SingleEle_2017.files = SingleEle_2017_files_1 + SingleEle_2017_files_2 
#
#TTJets_amct.files = glob('/eos/cms/store/user/vstampf/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/HNLSKIM2017_TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/180711_143059/0000/*.root')
#
#TTJets_mdgrph.files = glob('/eos/cms/store/user/vstampf/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/HNLSKIM2017_TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/180711_151636/0000/*.root')


