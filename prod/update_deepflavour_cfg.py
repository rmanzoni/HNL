import FWCore.ParameterSet.Config as cms

process = cms.Process('NEWDF')

process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)	 # needed for ak10 computation (JMEAnalysis/JetToolbox)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
) 

## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# standard and geometry sequences
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
# https://docs.google.com/presentation/d/1YTANRT_ZeL5VubnFq7lNGHKsiD7D3sDiOPNgXUYVI0I/edit#slide=id.g7068f62c63_1_0
# process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20'
process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v15' # <== use the same GT as used in the original samples (edmProvDump), otherwise you'd get different JECs

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
    process.patJetCorrFactorsNewDFTraining                        +
    process.updatedPatJetsNewDFTraining                           +
    process.pfImpactParameterTagInfosNewDFTraining                +
    process.pfInclusiveSecondaryVertexFinderTagInfosNewDFTraining +
    process.pfDeepCSVTagInfosNewDFTraining                        +
    process.pfDeepFlavourTagInfosNewDFTraining                    +
    process.pfDeepFlavourJetTagsNewDFTraining                     +
    process.patJetCorrFactorsTransientCorrectedNewDFTraining      +
    process.updatedPatJetsTransientCorrectedNewDFTraining         +
#     process.slimmedJets
    process.selectedUpdatedPatJetsNewDFTraining
)


# Configure the object that writes an output file
process.output = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        'keep *_*_*_*',
        'drop *_*_*_NEWDF',
        'keep patJets_selectedUpdatedPatJetsNewDFTraining_*_NEWDF'
    ),
)

process.out = cms.EndPath(process.output)

