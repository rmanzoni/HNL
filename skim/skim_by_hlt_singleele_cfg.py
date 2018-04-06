from triggers import ele_hlts
from event_content import miniaod_event_content_data, aod_event_content

import FWCore.ParameterSet.Config as cms

process = cms.Process('HNLSKIM')

# this inputs the input files
process.source = cms.Source (
    'PoolSource',
    fileNames=cms.untracked.vstring(
#         '/store/data/Run2016B/SingleElectron/MINIAOD/18Apr2017_ver2-v1/90000/42D145EB-9C44-E711-B321-B083FED406AD.root',
        '/store/data/Run2016D/SingleElectron/MINIAOD/18Apr2017-v1/60000/9A1581C2-9439-E711-9053-FA163E76CFFE.root',
    ),
#     secondaryFileNames = cms.untracked.vstring(
#     )
)

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 1000 )
)

# skim by HLT trigger
process.triggerSelection = cms.EDFilter( 
    'TriggerResultsFilter',
    triggerConditions = cms.vstring(ele_hlts),
    hltResults        = cms.InputTag( 'TriggerResults', '', 'HLT' ),
    l1tResults        = cms.InputTag( '' ),
)

# path & schedule
process.hltSkim = cms.Path( process.triggerSelection )

# talk to output module
process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('miniAOD_singleele_skim.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('hltSkim',)
    ),
    outputCommands = cms.untracked.vstring(
        ['drop *'] + miniaod_event_content_data + aod_event_content
    ),
)

# A list of analyzers or output modules to be run after all paths have been run.
process.outpath = cms.EndPath(process.out)

# you want a logger, don't you?
process.MessageLogger = cms.Service("MessageLogger")
