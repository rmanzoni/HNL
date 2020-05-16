import FWCore.ParameterSet.Config as cms

process = cms.Process('NEWDF')

process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)	 # needed for ak10 computation (JMEAnalysis/JetToolbox)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
) 

process.source = cms.Source('PoolSource', 
    fileNames = cms.untracked.vstring(
        ## HNL signal 2018
        'file:/afs/cern.ch/work/m/manzoni/HNL/cmg/CMSSW_10_4_0_patch1/src/CMGTools/HNL/cfg/2018/heavyNeutrino_1.root',
        ## TTBar 2016
#         'root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv3/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/40000/E0277B98-6F16-E911-8C5F-B083FED42B3A.root',
        ## Data 2016H
#         'root://cms-xrd-global.cern.ch//store/data/Run2016H/SingleMuon/MINIAOD/17Jul2018-v1/00000/68B4A70D-998C-E811-816E-AC1F6B23C82E.root',
        ## TTBar 2017
#         'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/C6BB52E8-F341-E811-8A2F-001E677927EC.root',
        ## Data 2017F
#         'root://cms-xrd-global.cern.ch//store/data/Run2017F/SingleMuon/MINIAOD/31Mar2018-v1/100000/70F7C6A6-A739-E811-A1B8-0CC47A4D7674.root'
    ),
)

## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# standard and geometry sequences
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
# https://docs.google.com/presentation/d/1YTANRT_ZeL5VubnFq7lNGHKsiD7D3sDiOPNgXUYVI0I/edit#slide=id.g7068f62c63_1_0
# process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20'
# Data: 102X_dataRun2_v12 (2016, 2017, 2018 A-C), 102X_dataRun2_Prompt_v15 (2018 D)
# MC: 102X_mcRun2_asymptotic_v7 (2016), 102X_mc2017_realistic_v7 (2017), 102X_upgrade2018_realistic_v20 (2018)
# Recommended JEC
# https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC#Recommended_for_MC

# W/ JEC
# 2018 MC
if 'RunIIAutumn18MiniAOD' in process.source.fileNames[0] or \
   'Autumn18' in process.source.fileNames[0]:
    process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20'
# 2017 MC
elif 'RunIIFall17MiniAODv2' in process.source.fileNames[0] or \
     'Fall17' in process.source.fileNames[0]:
    process.GlobalTag.globaltag = '102X_mc2017_realistic_v7'
# 2016 MC
elif 'RunIISummer16MiniAODv3' in process.source.fileNames[0] or \
     'Moriond17_aug2018_miniAODv3' in process.source.fileNames[0]:
    process.GlobalTag.globaltag = '102X_mcRun2_asymptotic_v7'
# 2018 data ABC, 2016 and 2017 data
elif '17Sep2018' in process.source.fileNames[0] or \
     '31Mar2018' in process.source.fileNames[0] or \
     '17Jul2018' in process.source.fileNames[0]:
    process.GlobalTag.globaltag = '102X_dataRun2_v12' 
elif 'Run2018D-PromptReco' in process.source.fileNames[0] or \
     '22Jan2019' in process.source.fileNames[0]:
    process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v15'
else:
    process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v15'

## W/O new JEC
# 2018 MC
# process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v15' # <== use the same GT as used in the original samples (edmProvDump), otherwise you'd get different JECs
# 2017 MC
# process.GlobalTag.globaltag = '94X_mc2017_realistic_v17'
# 2016 MC
# process.GlobalTag.globaltag = '94X_mcRun2_asymptotic_v3'
# 2018 data
# process.GlobalTag.globaltag = '102X_dataRun2_v12' if 'ABC' else '102X_dataRun2_Prompt_v15'
# 2017 data
# process.GlobalTag.globaltag = '94X_dataRun2_v11'
# 2016 data
# process.GlobalTag.globaltag = '94X_dataRun2_v10'

##########################################################################################
## do some skimming on the fly first, require 3 leptons
##########################################################################################

process.goodHighPtMuons = cms.EDFilter('PATMuonSelector',
    src = cms.InputTag('slimmedMuons'),
    cut = cms.string('pt>20 & abs(eta)<2.5 & isMediumMuon'),                                
    filter = cms.bool(False)
)

modified_medium_mu_id = '(segmentCompatibility>0.303 &  (isGlobalMuon & combinedQuality.chi2LocalPosition<12 & combinedQuality.trkKink<20))  |' \
                        '(segmentCompatibility>0.451 & !(isGlobalMuon & combinedQuality.chi2LocalPosition<12 & combinedQuality.trkKink<20))   '

process.goodLowPtMuons = cms.EDFilter('PATMuonSelector',
    src = cms.InputTag('slimmedMuons'),
    cut = cms.string('pt>5 & abs(eta)<2.5 & ( (isLooseMuon & (%s)) | isMediumMuon)' %modified_medium_mu_id),
    filter = cms.bool(False)
)

# RM: super weird bug, if I run the cfg alone, EIDs have dashes as separators
# mvaEleID-Fall17-noIso-V2-wp90
# whereas if I dump the cfg with EdmConfigDump EIDs have underscores as separators!!!!!!
# mvaEleID_Fall17_noIso_V2_wp90
# REMEMBER to swap the commented and uncommented lines when you run locally.
# jeez...
process.goodHighPtEles = cms.EDFilter('PATElectronSelector',
    src = cms.InputTag('slimmedElectrons'),
    cut = cms.string('pt>25 & abs(eta)<2.5 & (electronID("mvaEleID_Fall17_noIso_V2_wp90") | electronID("mvaEleID_Fall17_iso_V2_wp90"))'),
#     cut = cms.string('pt>25 & abs(eta)<2.5 & (electronID("mvaEleID-Fall17-noIso-V2-wp90") | electronID("mvaEleID-Fall17-iso-V2-wp90"))'),
    filter = cms.bool(False)
)
             
# missing HoE selection because it requires rho and I didn't bother adding a module to do that.. it's just a skim
# https://github.com/rmanzoni/cmssw/blob/heppy_106X_hnl/PhysicsTools/Heppy/python/physicsobjects/Electron.py#L433
# https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/plugins/cuts/GsfEleDEtaInSeedCut.cc#L24-L29
modified_loose_ele_id = '(isEB & superCluster.isNonnull & superCluster.seed.isNonnull & ecalEnergy>0. & full5x5_sigmaIetaIeta<0.11   & abs((deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta))<0.00477 & abs(deltaPhiSuperClusterTrackAtVtx)<0.222 & abs(1.0/ecalEnergy - eSuperClusterOverP/ecalEnergy)<0.241) | ' \
                        '(isEE & superCluster.isNonnull & superCluster.seed.isNonnull & ecalEnergy>0. & full5x5_sigmaIetaIeta<0.0314 & abs((deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta))<0.00868 & abs(deltaPhiSuperClusterTrackAtVtx)<0.213 & abs(1.0/ecalEnergy - eSuperClusterOverP/ecalEnergy)<0.14 )   '

process.goodLowPtEles = cms.EDFilter('PATElectronSelector',
    src = cms.InputTag('slimmedElectrons'),
    cut = cms.string('pt>5 & abs(eta)<2.5 & (%s | electronID("mvaEleID_Fall17_noIso_V2_wp90") | electronID("mvaEleID_Fall17_iso_V2_wp90"))' %modified_loose_ele_id),                                
#     cut = cms.string('pt>5 & abs(eta)<2.5 & (%s | electronID("mvaEleID-Fall17-noIso-V2-wp90") | electronID("mvaEleID-Fall17-iso-V2-wp90"))' %modified_loose_ele_id),                                
    filter = cms.bool(False)
)

process.goodLeptons = cms.EDFilter(
    'PATLeptonCountFilter',
    electronSource = cms.InputTag('goodLowPtEles'),
    muonSource     = cms.InputTag('goodLowPtMuons'),
    tauSource      = cms.InputTag('slimmedTaus'),
    countElectrons = cms.bool(True),
    countMuons     = cms.bool(True),
    countTaus      = cms.bool(False),
    minNumber = cms.uint32(3),
    maxNumber = cms.uint32(999999),
)

process.goodHighPtLeptons = cms.EDFilter(
    "PATLeptonCountFilter",
    electronSource = cms.InputTag('goodHighPtEles'),
    muonSource     = cms.InputTag('goodHighPtMuons'),
    tauSource      = cms.InputTag("slimmedTaus"),
    countElectrons = cms.bool(True),
    countMuons     = cms.bool(True),
    countTaus      = cms.bool(False),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
)

# # Clever idea, clone slimmedJets with a different name and call the new, updated collection slimmedJets
# # https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/slimming/applyDeepBtagging_cff.py
# <=========== DOESN'T WORK

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
# https://twiki.cern.ch/twiki/bin/view/CMS/DeepJet#94X_installation_recipe_X_10
updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJets'),
   pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
   svSource = cms.InputTag('slimmedSecondaryVertices'),
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
   btagDiscriminators = [
      'pfDeepFlavourJetTags:probb',
      'pfDeepFlavourJetTags:probbb',
      'pfDeepFlavourJetTags:problepb',
      'pfDeepFlavourJetTags:probc',
      'pfDeepFlavourJetTags:probuds',
      'pfDeepFlavourJetTags:probg'
      ],
   postfix='NewDFTraining'
)

process.p = cms.Path(
    # SKIM
    # remove the skim for now because I don't have a way to save 
    # the original LHE weight info
    # ... need all events at python level
    # I had a solution, need to find it
#     process.goodLowPtEles       +
#     process.goodLowPtMuons      +
#     process.goodLeptons         +
#     process.goodHighPtEles      +
#     process.goodHighPtMuons     +
#     process.goodHighPtLeptons   +
    # RECOMPUTE BTAG AND JEC
    process.patJetCorrFactorsNewDFTraining                        +
    process.updatedPatJetsNewDFTraining                           +
    process.pfImpactParameterTagInfosNewDFTraining                +
    process.pfInclusiveSecondaryVertexFinderTagInfosNewDFTraining +
    process.pfDeepCSVTagInfosNewDFTraining                        +
    process.pfDeepFlavourTagInfosNewDFTraining                    +
    process.pfDeepFlavourJetTagsNewDFTraining                     +
    process.patJetCorrFactorsTransientCorrectedNewDFTraining      +
    process.updatedPatJetsTransientCorrectedNewDFTraining         +
    process.selectedUpdatedPatJetsNewDFTraining
)


# Configure the object that writes an output file
process.output = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        'keep *_*_*_*',
        'drop *_*_*_%s' %process.name_(),
        'keep patJets_selectedUpdatedPatJetsNewDFTraining_*_%s' %process.name_(),
    ),
    SelectEvents = cms.untracked.PSet( 
        SelectEvents = cms.vstring('p')
    )
)

process.out = cms.EndPath(process.output)

