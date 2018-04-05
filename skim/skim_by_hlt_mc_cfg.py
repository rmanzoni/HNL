from triggers import mu_hlts, ele_hlts
from event_content import miniaod_event_content_mc, aod_event_content

import FWCore.ParameterSet.Config as cms

process = cms.Process('HNLSKIM')

# this inputs the input files
process.source = cms.Source (
    'PoolSource',
    fileNames=cms.untracked.vstring(
        '/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110000/005ED0EB-79F1-E611-B6DA-02163E011C2B.root',
    ),
    secondaryFileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/062AB3F9-48F1-E611-B7BC-02163E0137A0.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/124AC56C-42F1-E611-91DB-02163E019D4A.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/2029FDDB-44F1-E611-91E2-02163E01436E.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/22AAE483-46F1-E611-901C-02163E019BD7.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/30D98C18-40F1-E611-A97C-02163E019B82.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/8475F869-42F1-E611-9CBC-02163E01A495.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/8A2C77FF-48F1-E611-859A-02163E014447.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/A413BD73-42F1-E611-8D69-02163E014294.root',
        '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110002/B0DA89D6-44F1-E611-A240-02163E019DDC.root',
  )
)

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 100 )
)

# load the GT, corresponding to your samples
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'

# skim by HLT trigger
process.triggerSelection = cms.EDFilter( 
    'TriggerResultsFilter',
    triggerConditions     = cms.vstring(mu_hlts + mu_hlts),
    hltResults            = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults            = cms.InputTag( 'gtStage2Digis' ),
)

# path & schedule
process.hltSkim = cms.Path( process.triggerSelection )

# talk to output module
process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('miniAOD_skim.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('hltSkim',)
    ),
    outputCommands = cms.untracked.vstring(
        ['drop *'] + miniaod_event_content_mc + aod_event_content
    ),
)

# A list of analyzers or output modules to be run after all paths have been run.
process.outpath = cms.EndPath(process.out)

# you want a logger, don't you?
process.MessageLogger = cms.Service("MessageLogger")
