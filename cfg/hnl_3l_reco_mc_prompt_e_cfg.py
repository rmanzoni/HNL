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
from CMGTools.HNL.analyzers.HNLAnalyzer        import HNLAnalyzer
from CMGTools.HNL.analyzers.HNLTreeProducer    import HNLTreeProducer
from CMGTools.HNL.analyzers.HNLGenTreeAnalyzer import HNLGenTreeAnalyzer
from CMGTools.HNL.analyzers.TriggerAnalyzer    import TriggerAnalyzer
from CMGTools.HNL.analyzers.JetAnalyzer        import JetAnalyzer

# import samples, signal
from CMGTools.HNL.samples.localsignal import HN3L_M_2p5_V_0p0173205080757_e_onshell, HN3L_M_2p5_V_0p00707106781187_e_onshell
from CMGTools.HNL.samples.samples_data_2017 import Single_ele_2017
from CMGTools.HNL.samples.localsignal import TTJets_amcat as ttbar

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally

# production         = getHeppyOption('production' , False)
production         = getHeppyOption('production' , False)
pick_events        = getHeppyOption('pick_events', False)

###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [HN3L_M_2p5_V_0p00707106781187_e_onshell, HN3L_M_2p5_V_0p0173205080757_e_onshell]
samples += [ttbar]

for sample in samples:
    sample.triggers  = ['HLT_Ele27_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele32_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele35_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele135_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger

    sample.splitFactor = splitFactor(sample, 1e5)

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
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
    usePrescaled=False,
    unpackLabels=True,
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=False,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

genAna = GeneratorAnalyzer.defaultConfig
genAna.allGenTaus = True # save in event.gentaus *ALL* taus, regardless whether hadronic / leptonic decay

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_Ele27_WPTight_Gsf']         = 'hltEle27WPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele32_WPTight_Gsf']         = 'hltEle32WPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele35_WPTight_Gsf']         = 'hltEle35noerWPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele115_CaloIdVT_GsfTrkIdT'] = 'hltEle115CaloIdVTGsfTrkIdTGsfDphiFilter'
triggers_and_filters['HLT_Ele135_CaloIdVT_GsfTrkIdT'] = 'hltEle135CaloIdVTGsfTrkIdTGsfDphiFilter'

HNLAnalyzer = cfg.Analyzer(
    HNLAnalyzer,
    name='HNLAnalyzer',
    promptLepton='ele',
    triggersAndFilters=triggers_and_filters,
    candidate_selection='maxpt',
)

HNLTreeProducer = cfg.Analyzer(
    HNLTreeProducer,
    name='HNLTreeProducer',
    promptLepType='ele',
)

HNLGenTreeAnalyzer = cfg.Analyzer(
    HNLGenTreeAnalyzer,
    name='HNLGenTreeAnalyzer',
)

# see SM HTT TWiki
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
jetAna = cfg.Analyzer(
    JetAnalyzer,
    name              = 'JetAnalyzer',
    jetCol            = 'slimmedJets',
    jetPt             = 20.,
    jetEta            = 5.,
    relaxJetId        = False, # relax = do not apply jet ID
    relaxPuJetId      = True, # relax = do not apply pileup jet ID
    jerCorr           = False,
    puJetIDDisc       = 'pileupJetId:fullDiscriminant',
    recalibrateJets   = False,
    applyL2L3Residual = 'MC',
    # RM: FIXME! check the GTs
#    mcGT              = '94X_mc2017_realistic_v14',
#    dataGT            = '94X_dataRun2_v6',
    #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
)
###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
#     eventSelector,
    lheWeightAna, # les houches
    jsonAna,
    skimAna,
    triggerAna,
    vertexAna,
    pileUpAna,
    genAna,
    HNLGenTreeAnalyzer,
    HNLAnalyzer,
    jetAna,
    HNLTreeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
#     comp                 = HN3L_M_2p5_V_0p0173205080757_e_onshell
#     comp                 = HN3L_M_2p5_V_0p00707106781187_e_onshell
    comp                 = ttbar
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:50]

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

