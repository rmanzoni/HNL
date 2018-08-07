import os
from collections import OrderedDict
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
from CMGTools.RootTools.utils.splitFactor import splitFactor

# import Heppy analyzers:
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer      import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector     import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer    import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer  import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer  import LHEWeightAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer   import TriggerAnalyzer


# import HNL analyzers:
from CMGTools.HNL.analyzers.HNLAnalyzer           import HNLAnalyzer
from CMGTools.HNL.analyzers.HNLTreeProducerSignal import HNLTreeProducerSignal
from CMGTools.HNL.analyzers.HNLTreeProducerData   import HNLTreeProducerData
from CMGTools.HNL.analyzers.HNLGenTreeAnalyzer    import HNLGenTreeAnalyzer
from CMGTools.HNL.analyzers.RecoGenAnalyzer       import RecoGenAnalyzer
from CMGTools.HNL.analyzers.CheckHNLAnalyzer      import CheckHNLAnalyzer

# import samples, signal
# from CMGTools.HNL.samples.signal import all_signals as samples
# from CMGTools.HNL.samples.signal import all_signals_e as samples
# from CMGTools.HNL.samples.signal import signals_mass_3 as samples
# from CMGTools.HNL.samples.signal import signals_test as samples
# from CMGTools.HNL.samples.signal import signals_mass_1
# from CMGTools.HNL.samples.signal import signals_mass_2p1

# from CMGTools.HNL.samples.signal import HN3L_M_2p5_V_0p0173205080757_e_onshell
# from CMGTools.HNL.samples.signal import HN3L_M_2p5_V_0p0173205080757_e_onshell
from CMGTools.HNL.samples.localsignal import TTJets_amcat as ttbar
# from CMGTools.HNL.samples.signal import disp1plus as samples
# from CMGTools.HNL.samples.localsignal import HN3L_M_2p5_V_0p0173205080757_e_onshell
# from CMGTools.HNL.samples.localsignal import HN3L_M_2p5_V_0p0173205080757_e_onshell, HN3L_M_2p5_V_0p00707106781187_e_onshell

cfg.PromptLeptonMode = 'ele' # 'ele', 'muon'
cfg.DataSignalMode = 'data' # 'signal', 'data'

puFileMC   = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Moriond17_PU25ns_V1.root'
puFileData = '/afs/cern.ch/user/a/anehrkor/public/Data_Pileup_2016_271036-284044_80bins.root'

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production         = getHeppyOption('production' , False)
pick_events        = getHeppyOption('pick_events', False)

###################################################
###               HANDLE SAMPLES                ###
###################################################

# samples = [HN3L_M_2p5_V_0p00707106781187_e_onshell, HN3L_M_2p5_V_0p0173205080757_e_onshell] #comment if you want to use all samples
samples = [ttbar]

for sample in samples:
    sample.triggers  = ['HLT_Ele27_WPTight_Gsf_v%d'          %i for i in range(1, 15)]
    sample.triggers += ['HLT_Ele32_WPTight_Gsf_v%d'          %i for i in range(4, 5)]
    sample.triggers += ['HLT_Ele35_WPTight_Gsf_v%d'          %i for i in range(4, 5)]
    sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(4, 5)]
    sample.triggers += ['HLT_Ele135_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(4, 5)]
    # sample.triggers  = ['HLT_IsoMu24_v%d'                    %i for i in range(4, 5)] #muon trigger
    # sample.triggers += ['HLT_IsoMu27_v%d'                    %i for i in range(4, 5)] #muon trigger
    # sample.triggers += ['HLT_Mu50_v%d'                       %i for i in range(4, 5)] #muon trigger
    # sample.triggers += ['HLT_IsoMu24_v%d'                    %i for i in range(4, 5)] #muon trigger

    # sample.splitFactor = splitFactor(sample, 1e5)
    # sample.puFileData = puFileData
    # sample.puFileMC   = puFileMC

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    # toSelect=[]
    toSelect=[326]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_IsoMu24'] = ['hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09'                                                                                                                ]

HNLAnalyzer = cfg.Analyzer(
    HNLAnalyzer,
    name='HNLAnalyzer',
)

if cfg.DataSignalMode == 'signal': # 'signal', 'data'
    HNLTreeProducer = cfg.Analyzer(
        HNLTreeProducerSignal,
        name='HNLTreeProducerSignal',
        # fillL1=False,
    )
if cfg.DataSignalMode == 'data': # 'signal', 'data'
    HNLTreeProducer = cfg.Analyzer(
        HNLTreeProducerData,
        name='HNLTreeProducerData',
        # fillL1=False,
    )

HNLGenTreeAnalyzer = cfg.Analyzer(
    HNLGenTreeAnalyzer,
    name='HNLGenTreeAnalyzer',
)

RecoGenAnalyzer = cfg.Analyzer(
    RecoGenAnalyzer,
    name='RecoGenAnalyzer',
)

CheckHNLAnalyzer = cfg.Analyzer(
    CheckHNLAnalyzer,
    name='CheckHNLAnalyzer',
)

###################################################
###                  SEQUENCE                   ###
###################################################
if cfg.DataSignalMode == 'data':
    sequence = cfg.Sequence([
    #     eventSelector,
        lheWeightAna, # les houche
        jsonAna,
        skimAna,
        # triggerAna,
        vertexAna,
        pileUpAna,
        HNLAnalyzer,
        HNLTreeProducer,
    ])

if cfg.DataSignalMode == 'signal':
    sequence = cfg.Sequence([
    #     eventSelector,
        lheWeightAna, # les houche
        jsonAna,
        skimAna,
        # triggerAna,
        vertexAna,
        pileUpAna,
        HNLGenTreeAnalyzer,
        RecoGenAnalyzer,
        HNLAnalyzer,
        CheckHNLAnalyzer,
        HNLTreeProducer,
    ])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    # comp                 = HN3L_M_2p5_V_0p0173205080757_e_onshell
    # comp                 = HN3L_M_2p5_V_0p00707106781187_e_onshell
    # comp                 = samples
    comp                 = ttbar
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:]

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = None,
    events_class = Events
)

printComps(config.components, True)




















