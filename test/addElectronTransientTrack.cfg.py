# Import CMS python class definitions such as Process, Source, and EDProducer
import FWCore.ParameterSet.Config as cms

# Set up a process named MakeElectronTracks
processName = "MakeElectronTracks"
process = cms.Process(processName)

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'


#configure the source that read the input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # 'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-8_V-0.00547722557505_tau_massiveAndCKM_LO/heavyNeutrino_1.root',
        # 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/243801C3-F441-E811-89FA-0025905C54DA.root',
        'file:/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/testfile.root',
        # 'file:/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/testfile_ttw.root',
    )    
)


# # add the VolumeBasedMagneticFieldESProducer
# process.VolumeBasedMagneticFieldESProducerNew = cms.ESProducer(
    # "VolumeBasedMagneticFieldESProducer",
    # timerOn                     = cms.untracked.bool(False),
    # useParametrizedTrackerField = cms.bool(False),
    # label                       = cms.untracked.string('MFConfig_RI_RII_160812_3_8T'),
    # version                     = cms.string('MFConfig_RI_RII_160812_3_8T'),
    # debugBuilder                = cms.untracked.bool(True),
    # cacheLastVolume             = cms.untracked.bool(True),
    # scalingVolumes              = cms.vint32(),
    # scalingFactors              = cms.vdouble()
# )

# load producer AddElectronTransientTrack
process.ttk = cms.EDProducer(
    'AddElectronTransientTrack',
    patEleSrc = cms.InputTag('slimmedElectrons'),
)

# talk to output module
process.out = cms.OutputModule("PoolOutputModule",
    # fileName = cms.untracked.string("/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/outputElectronTracks.root")
    fileName = cms.untracked.string("/eos/user/d/dezhu/HNL/projects/20181119_ElectronTracks/outputElectronTracks.root")
)

#Define which modules and sequences to run
process.mypath = cms.Path(process.ttk)

# A list of analyzers or output modules to be run after all paths have been run. 
process.outpath = cms.EndPath(process.out)

## logger
# process.MessageLogger.cerr.FwkReport.reportEvery = 1


